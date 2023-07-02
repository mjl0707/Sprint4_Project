#importing necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

#pulling the .csv into a dataframe
vehicles = pd.read_csv("vehicles_us.csv")

vehicles.head()

#checking the counts and types for each field in the dataframe
vehicles.info()

#checking the dataframe for null values
vehicles.isna().sum()

#filling in NULLs in model_year with median based on car model 
vehicles['model_year'] = vehicles['model_year'].fillna(vehicles.groupby(['model'])['model_year'].transform('median'))

#filing in NULLs in odometer based on model and model_year
vehicles['odometer'] = vehicles['odometer'].fillna(vehicles.groupby(['model','model_year'])['odometer'].transform('median'))

#filling in NULLs in cylinders based on car model 
vehicles['cylinders'] = vehicles['cylinders'].fillna(vehicles.groupby(['model'])['cylinders'].transform('median'))

#replacing nulls in the paint_color field with the value "unknown"
vehicles['paint_color'] = vehicles['paint_color'].fillna('Unknown')

#replacing nulls in the is_4wd field with a 0 for no
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)

#checking for nulls after making replacements above
vehicles.isna().sum()

#getting the year part of the date_posted field
vehicles['posted_year'] = pd.DatetimeIndex(vehicles['date_posted']).year

#calculating the car's age at time of posting by subtracting the model year value by the posted year value
vehicles['car_age'] = vehicles['posted_year'] - vehicles['model_year']

#breaking the model column into two parts, make and model for further analysis of the make field and returning the top 5 rows
vehicles[['make', 'model']] = vehicles['model'].str.split(" ", n = 1, expand = True)
vehicles.head()

#create header
st.header('Used Cars Analysis')
st.write("""
##### The data below shows information on used cars posted from 2018-2019
""")
#use a checkbox to show only domestic makes or all makes
only_domestic = st.checkbox('Show Only Domestic Makes')
domestic = ['ford', 'chrysler', 'chevrolet', 'ram', 'gmc', 'jeep', 'dodge', 'cadillac', 'buick']
if only_domestic:
    vehicles = vehicles[vehicles['make'].isin(domestic)]
#inserting the dataframe
st.dataframe(vehicles)

st.header('Car Price by Age')
#building a scatter plot that shows price of the cars by their age
age_scatter = px.scatter(vehicles, x='car_age', y='price')
st.write(age_scatter)

st.header('Count of Cars by Price')
#building a histogram that shows the count of cars by make
price_ct = px.histogram(vehicles, x='price')
st.write(price_ct)




