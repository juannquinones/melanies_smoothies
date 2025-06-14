# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("🥤 Customize Your Smoothie!🥤")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your smoothie will be: ', name_on_order)

#session = get_active_session()
cnx= st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()


ingredients_list= st.multiselect('Choose up to 5 ingredients: ', 
                                 my_dataframe, max_selections = 5)
if ingredients_list:
    ingredients_string =''
    for i in ingredients_list:
        ingredients_string += i+' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', i,' is ', search_on, '.')
        st.subheader(i+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+str(search_on))
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width= True)

    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
    #st.write(my_insert_stmt)


