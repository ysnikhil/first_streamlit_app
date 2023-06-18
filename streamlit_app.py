import streamlit
import pandas

#Building first streamlit app using python on HEALTHY DINER

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Read the S3 file given by snowflake in pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Make the first column as the index so that multipicker can read the data well
my_fruit_list=my_fruit_list.set_index('Fruit')

#Add multipicker on the created index
fruits_selected=streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])

#Read only those fruits which user has selected in the multipicker
fruits_to_show=my_fruit_list.loc[fruits_selected]

#Load the dataframe in streamlit app
streamlit.dataframe(fruits_to_show)


