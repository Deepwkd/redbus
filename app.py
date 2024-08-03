import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def get_data():
    # Database connection details
    connection_string = 'mysql+pymysql://root:9600578719@localhost/redbus'
    engine = create_engine(connection_string)
    
    # query to retrieve bus route data
    query = "SELECT * FROM bus_routes"
    data = pd.read_sql(query, engine)
    return data


#  title of the Streamlit app
st.title("BUS SELECTOR APP")

# Fetching  data from the CSV/database
data = get_data()

# Ensuring the data is loaded or not
if data.empty:
    st.error("No data available in the database.")
else:
    # User inputs for filtering data
    routes = st.multiselect("Select Routes", data['route'].unique())
    bus_names = st.multiselect("Select Bus Name", data['name'].unique())
    bus_types = st.multiselect("Select Bus Type", data['type'].unique()) 
    price_range = st.slider("Select Price Range", int(data['price'].min()), int(data['price'].max()), (int(data['price'].min()), int(data['price'].max())))
    star_rating = st.slider("Select Minimum Star Rating", 0.0, 5.0, 0.0)
    min_seats_available = st.slider("Minimum Seats Available", 0, int(data['seats_available'].max()), 0)
   


    # Apply filters based on user inputs
    if bus_names:
        data = data[data['name'].isin(bus_names)]

    if bus_types:
        data = data[data['type'].isin(bus_types)]

    if routes:
        data = data[data['route'].isin(routes)]

    data = data[(data['price'] >= price_range[0]) & (data['price'] <= price_range[1])]
    data = data[data['rating'] >= star_rating]

    if min_seats_available > 0:
        data = data[data['seats_available'] >= min_seats_available]

    
    # Displaying the filtered data in a table
    st.dataframe(data)

 


    

