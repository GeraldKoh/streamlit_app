import streamlit as st
import pandas as pd
import numpy as np
import requests
from urllib.error import URLError

st.set_page_config(page_title='INVEMP Tasty Bytes Group 5', page_icon='🍖🍕🍜')

st.sidebar.title("INVEMP: Inventory/Warehouse Management & Prediction on Sales per Menu Item")
st.sidebar.markdown("This web app allows you to explore the internal inventory of Tasty Bytes. You can explore these functions in the web app (Description of Page)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Prediction A', 'Prediction B', 'Sales Prediction Australia', 'Prediction D', 'Prediction E'])


with tab3:
    # Define the app title and favicon
    st.title('Shift Sales of Cities in Australia')

    #import pandas
    data_aust = pd.read_csv('shiftsales_menuitem_au.csv')

    # Let's put a city list here so they can the city want to view
    city_selected = streamlit.multiselect("City", list(data_aust['City'].unique))
# fruits_to_show = my_fruit_list.loc[fruits_selected]

# # Display the table on the page.
# streamlit.dataframe(fruits_to_show)
    
    st.subheader('Predict')
    st.markdown("This tab allows predictions on the price of a listing based on the neighbourhood and room type. The model used is a Random Forest Regressor trained on the Airbnb Singapore listings dataset.")
    st.write('Choose a neighborhood group, neighborhood, and room type to get the predicted average price.')
