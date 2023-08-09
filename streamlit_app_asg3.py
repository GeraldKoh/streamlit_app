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
        xgb_final = joblib.load(file)
    with open('scaler.pkl', 'rb') as file:
        scaler = joblib.load(file)
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

    # Load the cleaned and transformed dataset
    data = pd.read_csv('final_shiftsales_au.csv')
    shiftsales = data[['SHIFT_SALES']] # extract price column from listings_new2.csv
    
    city = maintable["CITY"].unique()
    city_mapping = {cities: c for c, cities in enumerate(city)}
    city_labels = list(city_mapping.keys())

    shiftid = maintable["SHIFT_ID"].unique()
    shiftid_mapping = {shift: s for s, shift in enumerate(shiftid)}
    shiftid_labels = list(shiftid_mapping.keys())

    # menu_items = maintable["MENU_ITEM_NAME"].unique()
    # menu_item_mapping = {item: i for i, item in enumerate(menu_items)}
    # menu_item_labels = list(menu_item_mapping.keys())

    # def get_city():
    city_input = st.selectbox('Select a City', maintable['CITY'].unique(), key = 'city')
    # room_type = st.sidebar.selectbox("Room type", data['room_type'].unique(), key='room_type')
        # return city    
    
    # def get_shiftid():
    shiftid_input = st.selectbox('Select a Shift', maintable['SHIFT_ID'].unique(), key='shiftid')
        # return shiftid
        
    # Define the user input fields
    # city_input = get_city()
    # shiftid_input = get_shiftid()

    # shiftid_table = maintable[['SHIFT_ID', 'CITY', 'MENU_ITEM_NAME', 'TRUCK_BRAND_NAME', 'ITEM_CATEGORY', 'ITEM_SUBCATEGORY']]
    # shiftid_display = shiftid_table[shiftid_table['SHIFT_ID'] == shiftid_input]

    # # Display the table on the page.
    # st.dataframe(shiftid_display)

    # Create a function that takes neighbourhood_group as an argument and returns the corresponding integer value.
    def match_city(city):
        return city_mapping[city_input]
    city_int = match_city(city_input)

    def match_shiftid(shiftid):
        return shiftid_mapping[shiftid_input]
    shiftid_int = match_shiftid(shiftid_input)

    # Filter the DataFrame based on the SHIFT_ID
    filtered_df = data[(data['SHIFT_ID'] == shiftid_int) & (data['CITY'] == city_int)]
    st.write(filtered_df)
    
    st.subheader('Predict')
    # Create a price prediction button
    if st.button('Predict Price'):
        city_int = match_city(city_input)
        shiftid_int = match_shiftid(shiftid_input)
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
        
        input_df = pd.DataFrame(final_input_df, columns=['SHIFT_ID','CITY','AVG_TEMPERATURE_AIR_2M_F','AVG_WIND_SPEED_100M_MPH',
                                         'TOT_PRECIPITATION_IN',
                                         'TOT_SNOWFALL_IN', 'SHIFT_NUMBER', 'MENU_ITEM_NAME', 
                                         'ITEM_CATEGORY','ITEM_SUBCATEGORY','TRUCK_BRAND_NAME','YEAR'])
        st.write(input_df)
        # input_data = [[shiftid_input, city_input, AVG_TEMPERATURE_AIR_2M_F, AVG_WIND_SPEED_100M_MPH, TOT_PRECIPITATION_IN, TOT_SNOWFALL_IN, SHIFT_NUMBER, MENU_ITEM_NAME, ITEM_CATEGORY, ITEM_SUBCATEGORY, TRUCK_BRAND_NAME,YEAR]]
        # input_df = pd.DataFrame(input_data, columns=['SHIFT_ID','CITY','AVG_TEMPERATURE_AIR_2M_F','AVG_WIND_SPEED_100M_MPH','TOT_PRECIPITATION_IN','TOT_SNOWFALL_IN','SHIFT_NUMBER', 'MENU_ITEM_NAME', 'ITEM_CATEGORY','ITEM_SUBCATEGORY','TRUCK_BRAND_NAME','YEAR'])
        prediction = xgb_final.predict(input_df)
        total_ss = 0
        # for index, row in input_df.iterrows():
        #     # Get the prediction for the current row
        #     prediction = xgb_final.predict(row.values.reshape(1, -1))[0]
        #     # Display the prediction for the current row
        #     st.write(f"Prediction for Row {index + 1}: {prediction}")
        #     # Add the prediction to the total sum
        #     total_ss += prediction
        # # Display the total sum of predictions
        # st.write(f"Total Sum of Predictions: {total_ss}")
        # predicted_price = '${:,.2f}'.format(prediction)
        st.write(prediction)
        # st.write('The predicted average price is {}.'.format(total_ss))
    # st.markdown("This tab allows predictions on the price of a listing based on the neighbourhood and room type. The model used is a Random Forest Regressor trained on the Airbnb Singapore listings dataset.")
    # st.write('Choose a neighborhood group, neighborhood, and room type to get the predicted average price.')
    # st.subheader('Evaluate')
