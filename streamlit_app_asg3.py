import streamlit as st
import pandas as pd
import numpy as np
import requests
import requests
import zipfile
import io
from urllib.error import URLError

st.set_page_config(page_title='INVEMP Tasty Bytes Group 5', page_icon='🍖🍕🍜')

st.sidebar.title("INVEMP: Inventory/Warehouse Management & Prediction on Sales per Menu Item")
st.sidebar.markdown("This web app allows you to explore the internal inventory of Tasty Bytes. You can explore these functions in the web app (Description of Page)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Prediction A', 'Prediction B', 'Prediction C', 'Prediction D', 'Sales Prediction Australia'])


with tab5:
    # Define the app title and favicon
    st.title('Shift Sales of Cities in Australia')

    def read_csv_from_zipped_github(url):
    # Send a GET request to the GitHub URL
        response = requests.get(url)

    # Check if the request was successful
        if response.status_code == 200:
            # Create a BytesIO object from the response content
            zip_file = io.BytesIO(response.content)

            # Extract the contents of the zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Assume there is only one CSV file in the zip archive (you can modify this if needed)
                csv_file_name = zip_ref.namelist()[0]
                with zip_ref.open(csv_file_name) as csv_file:
                    # Read the CSV data into a Pandas DataFrame
                    df = pd.read_csv(csv_file)

            return df
        else:
            st.error(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            return None
    github_url = "https://github.com/GeraldKoh/streamlit_app/raw/main/shiftsalesau.zip"
    maintable = read_csv_from_zipped_github(github_url)

    city_mapping = {'Sydney': 0, 'Melbourne': 1}
    city_reverse_mapping = {v: k for k, v in city_mapping.items()}
    city_labels = list(city_mapping.keys())\

    shiftid = maintable["SHIFT_ID"].unique()
    shiftid_mapping = {shift: s for s, shift in enumerate(shiftid)}
    shiftid_labels = list(shiftid_mapping.keys())

    menu_items = maintable["MENU_ITEM_NAME"].unique()
    menu_item_mapping = {item: i for i, item in enumerate(menu_items)}
    menu_item_labels = list(menu_item_mapping.keys())

    def get_city():
        city = st.selectbox('Select a City', city_labels)
        return city    
        
    def get_shiftid():
        shiftid = st.selectbox('Select a Shift', shiftid_labels)
        return shiftid
        
    def get_menu_item():
        menu_item = st.selectbox('Select a Menu Item', menu_item_labels)
        return menu_item
        
    # Define the user input fields
    city_input = get_city()
    shiftid_input = get_shiftid()
    menu_item_input = get_menu_item()

    shiftid_table = maintable[['SHIFT_ID', 'CITY', 'TIME', 'MENU_ITEM_NAME', 'ITEM_CATEGORY', 'ITEM_SUBCATEGORY', 'TRUCK_BRAND_NAME', 'SHIFT_SALES']]
    shiftid_display = shiftid_table[shiftid_table['SHIFT_ID'] == shiftid_input and shiftid_table['CITY'] == city_input]

    # Display the table on the page.
    st.dataframe(shiftid_display)

    # st.write(maintable)
    # maintable.head()
    
# def load_data():
#     # First load the original airbnb listtings dataset
#     data = pd.read_csv("listings.csv") #use this for the original dataset, before transformations and cleaning
#     return data

    # #import pandas
    # data_aust = pd.read_csv('shiftsales_menuitem_au.csv')
    # data_aust.head()

    

    # # Let's put a city list here so they can the city want to view
    # city_selected = streamlit.multiselect("City", list(data_aust['City'].unique))
# fruits_to_show = my_fruit_list.loc[fruits_selected]

# # Display the table on the page.
# streamlit.dataframe(fruits_to_show)
    
    st.subheader('Predict')
    st.markdown("This tab allows predictions on the price of a listing based on the neighbourhood and room type. The model used is a Random Forest Regressor trained on the Airbnb Singapore listings dataset.")
    st.write('Choose a neighborhood group, neighborhood, and room type to get the predicted average price.')
