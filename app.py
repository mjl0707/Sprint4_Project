#importing necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

#pulling the .csv into a dataframe
vehicles = pd.read_csv("C:\\Users\\13303\\Documents\\Projects\\Sprint_4\\vehicles_us.csv")

vehicles.head()

#checking the counts and types for each field in the dataframe
vehicles.info()

#checking the dataframe for null values
vehicles.isna().sum()

#getting the median model year
median_model_year = vehicles['model_year'].median()

#getting the median odometer value
median_odometer = vehicles['odometer'].median()

#getting the median number of cylinders
median_cylinders = vehicles['cylinders'].median()

#replacing nulls in the model_year field with the median model year
vehicles['model_year'] = vehicles['model_year'].fillna(median_model_year)

#replacing nulls in the odometer field with the median odometer value
vehicles['odometer'] = vehicles['odometer'].fillna(median_odometer)

#replacing nulls in the paint_color field with the value "unknown"
vehicles['paint_color'] = vehicles['paint_color'].fillna('Unknown')

#replacing nulls in the cylinders field with the median number of cylinders 
vehicles['cylinders'] = vehicles['cylinders'].fillna(median_cylinders)

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

st.header('Count of Cars by Make')
#building a histogram that shows the count of cars by make
make_ct = px.histogram(vehicles, x='make')
st.write(make_ct)




