import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.text('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(current_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + current_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','')
  streamlit.write('the user entered ', fruit_choice)
  streamlit.dataframe(get_fruityvice_data(fruit_choice))
  if not fruit_choice:
    streamlit.error("please select a fruit to get information")
  else:
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
    
streamlit.header("The fruit load list contains:")
def get_fruit_from_snowflake():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list") 
        return my_cur.fetchall()

if streamlit.button('Get List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_from_snowflake()
    streamlit.dataframe(my_data_rows)

def add_fruit_to_snowflake_list(fruit_to_add):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('" + add_my_fruit + "')") 
        return "Thanks for adding a " + add_my_fruit
        
add_my_fruit = streamlit.text_input('What would you like to add?','jackfruit')
if streamlit.button('Add Fruit'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    added_fruit = add_fruit_to_snowflake_list(add_my_fruit)
    streamlit.text(added_fruit)
