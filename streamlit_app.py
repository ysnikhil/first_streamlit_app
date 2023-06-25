import streamlit
import pandas
import requests 
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
  #Use the user input to append in the api response
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + fruit_input)
    normalized_api_json_response=pandas.json_normalize(fruityvice_response.json())
    return normalized_api_json_response 
  
#Take inputs from user
try:
  fruit_input=streamlit.text_input('What fruit would you like to get more details about:')
  if not fruit_input:
    streamlit.error('Please select a fruit to get a information.')
    
  else:
    streamlit.write('You have entered',fruit_input)
    back_from_function=get_fruityvice_data(fruit_input)
    streamlit.dataframe(back_from_function)
    
    
except URLError as e :
  streamlit.error()

#Adding logic to connect to snowflake account
streamlit.header('The Fruit load list contains:')

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get list of Fruits'):
  my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  streamlit.text("The Fruit load list contains:")
  streamlit.dataframe(my_data_rows)

#streamlit.stop()

#Allow user to add a fruit in the Fruits table

add_my_fruit=streamlit.text_input("What fruit would you like to add")

def insert_newrow_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+ new_fruit +"')")  
  return "Thanks for adding : " + new_fruit
  
  
if streamlit.button('Add a fruit to the list'):
  my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  return_from_function=insert_newrow_snowflake(add_my_fruit)
  streamlit.text(return_from_function)



