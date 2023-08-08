import streamlit as st
import pandas as pd
import numpy as np
import requests
import requests
import zipfile
import io
import pickle
import joblib
from joblib import load
from urllib.error import URLError

st.set_page_config(page_title='INVEMP Tasty Bytes Group 5', page_icon='🍖🍕🍜')

st.sidebar.title("INVEMP: Inventory/Warehouse Management & Prediction on Sales per Menu Item")
st.sidebar.markdown("This web app allows you to explore the internal inventory of Tasty Bytes. You can explore these functions in the web app (Description of Page)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Prediction A', 'Prediction B', 'Prediction C', 'Prediction D', 'Sales Prediction Australia'])

with tab5:
    # Load the serialized trained model rf.pkl and scaler object scaler.pkl
    with open('xgb_final.pkl', 'rb') as file:
        xgb_final = pickle.load(file)
    with open('scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    # Define the app title and favicon
    st.title('Shift Sales of Cities in Australia :australia:')

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

    city = maintable["CITY"].unique()
    city_mapping = {cities: c for c, cities in enumerate(city)}
    city_labels = list(city_mapping.keys())

    shiftid = maintable["SHIFT_ID"].unique()
    shiftid_mapping = {shift: s for s, shift in enumerate(shiftid)}
    shiftid_labels = list(shiftid_mapping.keys())

    # menu_items = maintable["MENU_ITEM_NAME"].unique()
    # menu_item_mapping = {item: i for i, item in enumerate(menu_items)}
    # menu_item_labels = list(menu_item_mapping.keys())

    def get_city():
        city = st.selectbox('Select a City', city_labels)
        return city    
        
    def get_shiftid():
        shiftid = st.selectbox('Select a Shift', shiftid_labels)
        return shiftid
        
    # def get_menu_item():
    #     menu_item = st.selectbox('Select a Menu Item', menu_item_labels)
    #     return menu_item
        
    # Define the user input fields
    city_input = get_city()
    shiftid_input = get_shiftid()
    # menu_item_input = get_menu_item()

    shiftid_table = maintable[['SHIFT_ID', 'CITY', 'MENU_ITEM_NAME', 'ITEM_CATEGORY', 'ITEM_SUBCATEGORY', 'TRUCK_BRAND_NAME', 'SHIFT_SALES']]
    shiftid_display = maintable[maintable['SHIFT_ID'] == shiftid_input]

    # Display the table on the page.
    st.dataframe(shiftid_display)

    # st.write(maintable)
    # maintable.head()


    
    st.subheader('Predict')
    st.markdown("This tab allows predictions on the price of a listing based on the neighbourhood and room type. The model used is a Random Forest Regressor trained on the Airbnb Singapore listings dataset.")
    st.write('Choose a neighborhood group, neighborhood, and room type to get the predicted average price.')

    st.subheader('Evaluate')
