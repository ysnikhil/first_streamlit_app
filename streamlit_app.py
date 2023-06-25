import streamlit
import pandas
import requests 
import snowflake.connector

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


#New section to displace the fruityvice fruits advice
streamlit.header('Fruityvice Fruit Advice')

#Take inputs from user
fruit_input=streamlit.text_input('What fruit would you like to get more details about:', 'kiwi')
streamlit.write('You have entered',fruit_input)

#Use the user input to append in the api response
fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + fruit_input)
normalized_api_json_response=pandas.json_normalize(fruityvice_response.json())

streamlit.dataframe(normalized_api_json_response)


#Adding logic to connect to snowflake account

my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
#my_cur.execute("select current_user(), current_account(), current_region()")
my_cur.execute("select * from fruit_load_list")
my_data_rows=my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.text("The Fruit load list contains:")
streamlit.dataframe(my_data_rows)


#Allow user to add a fruit in the Fruits table

add_my_fruit=streamlit.text_input("What fruit would you like to add")
streamlit.write("Thanks for adding", add_my_fruit)















