import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

#For styling the buttons and filters
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        color: Red; 
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
    }
    .filter-box {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .stSidebar {
        background-color: #FFB6C1;
    }
    </style>
    """, unsafe_allow_html=True)

# Database connection 
def get_data_from_db(query):
    connection_string = 'mysql+pymysql://root:9600578719@localhost/redbus'
    engine = create_engine(connection_string)
    return pd.read_sql(query, engine)

# Sidebar for navigation: Home and Main Menu
with st.sidebar:
    st.markdown('<p class="big-font">Options</p>', unsafe_allow_html=True)
    page = st.selectbox("Navigate", ['Home', 'Main Menu'])

# If Home is selected, show welcome page
if page == 'Home':
    st.markdown('<p class="big-font">Welcome to the Bus Filtering App!</p>', unsafe_allow_html=True)
    st.write("Use this app to filter and search for buses ")

# If Main Menu is selected, show  filtering options
elif page == 'Main Menu':
    st.markdown('<p class="big-font">Bus Filtering Options</p>', unsafe_allow_html=True)

    # SQL Query to load unique routes for dropdown selection
    routes_query = "SELECT DISTINCT CONCAT(from_place, ' to ', to_place) as route FROM bus_routes"
    routes_df = get_data_from_db(routes_query)
    routes_list = ['Choose an option'] + routes_df['route'].tolist()

    # Filter boxes with some color and styling
    with st.container():
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        selected_route = st.selectbox("Select the Route", routes_list)
        bus_name_list = ['Choose an option']
        selected_bus_name = 'Choose an option'
        bus_type_list = ['Choose an option']
        selected_bus_type = 'Choose an option'

        if selected_route != 'Choose an option':
            # Extracting from_place and to_place from selected_route
            from_place, to_place = selected_route.split(" to ")

            # SQL Query to load bus names for the selected route
            names_query = f"SELECT DISTINCT name FROM bus_routes WHERE from_place = '{from_place}' AND to_place = '{to_place}'"
            names_df = get_data_from_db(names_query)
            bus_name_list = ['Choose an option'] + names_df['name'].tolist()

            # Bus Name dropdown
            selected_bus_name = st.selectbox("Select the Bus Name", bus_name_list)

            if selected_bus_name != 'Choose an option':
                # SQL Query to load bus types for the selected bus name
                bus_type_query = f"SELECT DISTINCT type FROM bus_routes WHERE name = '{selected_bus_name}'"
                bus_type_df = get_data_from_db(bus_type_query)
                bus_type_list = ['Choose an option'] + bus_type_df['type'].tolist()

                # Dropdown for bus type selection (based on selected bus name)
                selected_bus_type = st.selectbox("Select the Bus Type", bus_type_list)

        # Dropdown for ratings selection 
        selected_rating = st.selectbox("Select the Ratings", ['Choose an option'] + [f'{i}-{i+1}' for i in range(1, 5)])

        # Slider for starting time selection 
        start_time = st.slider("Starting Time", min_value=0, max_value=23, value=(0, 23), step=1)

        # Slider for bus fare range selection
        fare_range = st.slider("Bus Fare Range", min_value=100, max_value=5000, value=(100, 3000), step=100)

        st.markdown('</div>', unsafe_allow_html=True)

        # Fare and rating condition handling
        fare_condition = f"AND price BETWEEN {fare_range[0]} AND {fare_range[1]}"

        # Extracting the lower and upper bound of the selected rating
        rating_condition = ""
        if selected_rating != 'Choose an option':
            rating_min, rating_max = map(float, selected_rating.split('-'))
            rating_condition = f"AND rating >= {rating_min} AND rating < {rating_max}"

        # start and end times
        start_time_min = f"{start_time[0]:02d}:00"
        start_time_max = f"{start_time[1]:02d}:00"

        # Query conditions for filtering buses
        name_condition = f"AND name = '{selected_bus_name}'" if selected_bus_name != 'Choose an option' else ''
        bus_type_condition = f"AND type = '{selected_bus_type}'" if selected_bus_type != 'Choose an option' else ''

        # Only execute the query if a valid route is selected
        if selected_route != 'Choose an option':
            # SQL Query to get filtered bus data
            bus_filter_query = f"""
                SELECT route, name, type, departure_time, arrival_time, duration, price, seats_available, rating, from_place, to_place
                FROM bus_routes
                WHERE from_place = '{from_place}' 
                AND to_place = '{to_place}' 
                {name_condition} 
                {bus_type_condition}
                {fare_condition}
                {rating_condition}
                AND departure_time >= '{start_time_min}' AND departure_time < '{start_time_max}'
            """

            filtered_buses_df = get_data_from_db(bus_filter_query)

            # Displaying results or a message if no buses are found
            if filtered_buses_df.empty:
                st.write("No buses found with the selected criteria.")
            else:
                # Displaying only the relevant columns in the output table
                st.table(filtered_buses_df[['name', 'type', 'departure_time', 'arrival_time', 'duration', 'price', 'seats_available', 'rating']])


 


    

