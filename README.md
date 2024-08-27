Bus Data Collection and Selector Application
This repository contains a Jupyter Notebook for collecting bus route data, an automation script for data collection, and a Streamlit-based web application for selecting and filtering buses based on various criteria.

Overview
Data Collection
The data_collection.ipynb notebook is designed to collect detailed bus route information, including bus types, timings, and durations. It processes the data and prepares it for further use in the application.

Automation
The automation.ipynb notebook automates the process of collecting bus data. This may include scraping data from web sources or interacting with APIs to gather up-to-date information on bus services.

BUS SELECTOR APP
The app.py script is a Streamlit-based web application that allows users to interact with the bus data collected. Users can filter buses by route, name, type, price, rating, and seat availability. The filtered results are displayed directly within the app.

INSTALLATION:
Prerequisites
Python 3.7+
Jupyter Notebook
Streamlit
MySQL Database

USAGE:

Data Collection
*Run data_collection.ipynb to collect and preprocess bus route data.
*Optionally, use automation.ipynb to automate data collection from various sources.

BUS SELECTOR APP
*Use the app.py to start the Streamlit app. Users can filter buses by multiple criteria and view the results interactively.
