import streamlit as st
import pandas as pd
import numpy as np
import requests
import requests
import zipfile
import io
import pickle
import joblib
from PIL import Image
from joblib import load
from urllib.error import URLError

st.set_page_config(page_title='INVEMP Tasty Bytes Group 5', page_icon='🍖🍕🍜')

st.sidebar.title("INVEMP: Inventory/Warehouse Management & Prediction on Sales per Menu Item")
st.sidebar.markdown("This web app allows you to explore the internal inventory of Tasty Bytes. You can explore these functions in the web app: Churn Prediction, Customer Revenue Calculation, Bundled Item Sales Analysis, Truck Implementation and Shift Sales Australia")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Prediction A', 'Prediction B', 'Prediction C', 'Prediction D', 'Sales Prediction Australia'])


with tab5:
    # Load the serialized trained model rf.pkl and scaler object scaler.pkl
    with open('xgb_final.pkl', 'rb') as file:
        xgb_final = joblib.load(file)
    with open('scaler.pkl', 'rb') as file:
        scaler = joblib.load(file)
    # Define the app title and favicon
    st.title('Shift Sales of Cities in Australia 💸')

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

    # Load the cleaned and transformed dataset
    data = pd.read_csv('final_shiftsales_au.csv')
    shift_sales= data[['SHIFT_SALES']] 
    data_projected = pd.read_csv('projected_shiftsales_au.csv')
    projected_shift_sales= data_projected[['SHIFT_SALES']] 
    
    city = maintable["CITY"].unique()
    city_mapping = {cities: c for c, cities in enumerate(city)}
    city_labels = list(city_mapping.keys())

    shiftid = maintable["SHIFT_ID"].unique()
    shiftid_mapping = {shift: s for s, shift in enumerate(shiftid)}
    shiftid_labels = list(shiftid_mapping.keys())

    year = maintable["YEAR"].unique()
    year_mapping = {yr: y for y, yr in enumerate(year)}
    year_labels = list(year_mapping.keys())

    image = Image.open('Sydney_Image.jpg')
    st.image(image, caption='An Iconic View of Australia')

    st.markdown("This tab allows predictions on Shift Sales of a shift based on the City, Year & Shift ID. There are 2 predictions that we can make here: 1 on the current food truck business and 1 after menu optimization has been implemeted. The model used is a XGBoost model trained on the Tasty Bytes dataset.")
    st.write('Select City, Year & Shift to get the predicted Shift Sales!')

    city_input = st.selectbox('Select a City', maintable['CITY'].unique(), key='city')
    year_input = st.selectbox('Select a Year', maintable['YEAR'].unique(), key='year')
    # # Filter the maintable based on the selected city_input
    # filtered_shift_ids = maintable[maintable['CITY'] == city_input]['SHIFT_ID'].unique()
    # shiftid_input = st.selectbox('Select a Shift', filtered_shift_ids, key='shiftid')

    filtered_table = maintable[(maintable['CITY'] == city_input) & (maintable['YEAR'] == year_input)]
    filtered_shift_ids = filtered_table['SHIFT_ID'].unique()
    shiftid_input = st.selectbox('Select a Shift', filtered_shift_ids, key='shiftid')
    
    # Define the user input fields
    # city_input = get_city()
    # shiftid_input = get_shiftid()

    selected_table = maintable[['SHIFT_ID','YEAR', 'CITY', 'MENU_ITEM_NAME', 'TRUCK_BRAND_NAME', 'ITEM_CATEGORY', 'ITEM_SUBCATEGORY']]
    city_shift_display = selected_table[(selected_table['SHIFT_ID'] == shiftid_input) & (selected_table['CITY'] == city_input) & (selected_table['YEAR'] == year_input)]

    # Display the table on the page.
    st.write('Menu Items in Shift!')
    st.dataframe(city_shift_display)

    # Create a function that takes neighbourhood_group as an argument and returns the corresponding integer value.
    def match_city(city):
        return city_mapping[city_input]
    city_int = match_city(city_input)

    def match_shiftid(shiftid):
        return shiftid_mapping[shiftid_input]
    shiftid_int = match_shiftid(shiftid_input)

    def match_year(year):
        return year_mapping[year_input]
    year_int = match_year(year_input)

    # Filter the DataFrame based on the SHIFT_ID
    filtered_df = data[(data['SHIFT_ID'] == shiftid_input) & (data['CITY'] == city_int) & (data['YEAR'] == year_input)]
    new_filtered_df = data_projected[(data_projected['SHIFT_ID'] == shiftid_input) & (data_projected['CITY'] == city_int) & (data_projected['YEAR'] == year_input)]
    
    st.subheader('Predict 🎯')
    # Create a price prediction button
    if st.button('Predict Current Shift Sales'):
        city_int = match_city(city_input)
        shiftid_int = match_shiftid(shiftid_input)
        year_int = match_year(year_input)
        # Create an empty list to store individual input DataFrames
        input_dfs = []
        # Iterate over each row in the filtered DataFrame
        for i in range(len(filtered_df)):
            # Get the values for each column in the current row
            values = filtered_df.iloc[i].values
            # Create an individual input DataFrame for the current row
            input_data = [values]  # Include all columns
            columns = filtered_df.columns
            input_df = pd.DataFrame(input_data, columns=columns)
            # Append the input DataFrame to the list
            input_dfs.append(input_df)
        # Concatenate all input DataFrames into a single DataFrame
        final_input_df = pd.concat(input_dfs, ignore_index=True)
        
        input_df = pd.DataFrame(final_input_df, columns=['SHIFT_ID','MENU_ITEM_ID','CITY','AVG_TEMPERATURE_AIR_2M_F','AVG_WIND_SPEED_100M_MPH','TOT_PRECIPITATION_IN','SHIFT_NUMBER', 'YEAR','ITEM_CATEGORY_Dessert','ITEM_CATEGORY_Main','ITEM_CATEGORY_Beverage',
                                                         'ITEM_CATEGORY_Snack', 'ITEM_SUBCATEGORY_Cold Option','ITEM_SUBCATEGORY_Hot Option','ITEM_SUBCATEGORY_Warm Option','TRUCK_BRAND_NAME_Freezing Point','TRUCK_BRAND_NAME_Better Off Bread',
                                                         'TRUCK_BRAND_NAME_Kitakata Ramen Bar','TRUCK_BRAND_NAME_Peking Truck', 'TRUCK_BRAND_NAME_Smoky BBQ','TRUCK_BRAND_NAME_Le Coin des Crêpes','TRUCK_BRAND_NAME_Plant Palace',
                                                         'TRUCK_BRAND_NAME_Tasty Tibs','TRUCK_BRAND_NAME_Cheeky Greek',"TRUCK_BRAND_NAME_Nani's Kitchen",'TRUCK_BRAND_NAME_The Mega Melt','TRUCK_BRAND_NAME_Revenge of the Curds','TRUCK_BRAND_NAME_The Mac Shack','TRUCK_BRAND_NAME_Not the Wurst Hot Dogs',"TRUCK_BRAND_NAME_Guac n' Roll"])
        prediction = xgb_final.predict(input_df)
        total_sales = prediction.sum()
        st.write("Total Shift Sales Before Revamp: ${:.2f}".format(total_sales))
        
    st.subheader('Predict (After Menu Optimization) 🎯')
    st.write('Click the button below only if the YEAR is set to 2022 to see the increase!')
    if st.button('Predict Shift Sales After Menu Optimization'):
        city_int = match_city(city_input)
        shiftid_int = match_shiftid(shiftid_input)
        year_int = match_year(year_input)
        new_input_dfs = []
        for i in range(len(new_filtered_df)):
            # Get the values for each column in the current row
            values = new_filtered_df.iloc[i].values
            input_data = [values]  # Include all columns
            columns = new_filtered_df.columns
            input_df = pd.DataFrame(input_data, columns=columns)
            
            # Append the input DataFrame to the list
            new_input_dfs.append(input_df)
        
        # Concatenate all input DataFrames into a single DataFrame
        new_final_input_df = pd.concat(new_input_dfs, ignore_index=True)
        
        # new_input_df = pd.DataFrame(new_final_input_df, columns=['CITY','AVG_TEMPERATURE_AIR_2M_F','AVG_WIND_SPEED_100M_MPH',
        #                                  'TOT_PRECIPITATION_IN',
        #                                  'TOT_SNOWFALL_IN', 'SHIFT_NUMBER', 'MENU_ITEM_NAME', 
        #                                  'ITEM_CATEGORY','ITEM_SUBCATEGORY','TRUCK_BRAND_NAME','YEAR'])
        new_input_df = pd.DataFrame(new_final_input_df, columns=['SHIFT_ID','MENU_ITEM_ID','CITY','AVG_TEMPERATURE_AIR_2M_F','AVG_WIND_SPEED_100M_MPH','TOT_PRECIPITATION_IN','SHIFT_NUMBER', 'YEAR','ITEM_CATEGORY_Dessert','ITEM_CATEGORY_Main','ITEM_CATEGORY_Beverage',
                                                         'ITEM_CATEGORY_Snack', 'ITEM_SUBCATEGORY_Cold Option','ITEM_SUBCATEGORY_Hot Option','ITEM_SUBCATEGORY_Warm Option','TRUCK_BRAND_NAME_Freezing Point','TRUCK_BRAND_NAME_Better Off Bread',
                                                         'TRUCK_BRAND_NAME_Kitakata Ramen Bar','TRUCK_BRAND_NAME_Peking Truck', 'TRUCK_BRAND_NAME_Smoky BBQ','TRUCK_BRAND_NAME_Le Coin des Crêpes','TRUCK_BRAND_NAME_Plant Palace',
                                                         'TRUCK_BRAND_NAME_Tasty Tibs','TRUCK_BRAND_NAME_Cheeky Greek',"TRUCK_BRAND_NAME_Nani's Kitchen",'TRUCK_BRAND_NAME_The Mega Melt','TRUCK_BRAND_NAME_Revenge of the Curds','TRUCK_BRAND_NAME_The Mac Shack','TRUCK_BRAND_NAME_Not the Wurst Hot Dogs',"TRUCK_BRAND_NAME_Guac n' Roll"])
        projected_prediction = xgb_final.predict(new_input_df)
        projected_total_sales = projected_prediction.sum()
        st.write("Projected Total Shift Sales After Menu Optimization: ${:.2f}".format(projected_total_sales))



