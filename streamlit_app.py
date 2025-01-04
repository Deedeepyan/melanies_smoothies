# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your Smoothies! :cup_with_straw:")
st.write(
    """ Choose the fruit you want in custom smoothies!
    """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('Name on the order will be ', name_on_order)
cnx= st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list=st.multiselect('choose upto 5 ingredients:', my_dataframe, max_selections=5)
if ingredients_list:
    
        ingredients_string =''
        for fruit_chosen in ingredients_list:
            ingredients_string+= fruit_chosen + ' '
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
            sf_df= st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
            
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""
        time_to_insert = st.button('Submit Order')
        if time_to_insert:
             session.sql(my_insert_stmt).collect()
             st.success('Your Smoothie is ordered, ' +name_on_order + '!', icon="✅")


