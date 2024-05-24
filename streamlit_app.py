# Import python packages
import requests
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# session = get_active_session() #used in snowflake
cnx = st.connection("snowflake") #used out of snowflake
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()                                                                      
#st.write("You selected:", options)

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

name_on_order = st.text_input("Name on Smoothie", "")
st.write("The name of your smoothie will be", name_on_order)

ingredients_list = st.multiselect(
"Choose up to 5 ingredients:"
, my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += (fruit) + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit,' is ', search_on, '.')

        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +  """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop

    # if ingredients_string:
    #     session.sql(my_insert_stmt).collect()
    #     st.success('Your Smoothie is ordered!', icon="✅")

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + name_on_order+ '!', icon="✅")
