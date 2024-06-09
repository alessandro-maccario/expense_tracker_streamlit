"""
    This script built in Streamlit gives the user the possibility
    to insert the data manually into the database.
"""

# --- Import packages --- #
import pandas as pd
from datetime import datetime
import streamlit as st

# TODO:
# Need to integrate this code as another tab/page into the main app!

# --- Main code --- #

# set the page default setting to wide
st.set_page_config(layout="wide")

# sidebar
with st.sidebar:

    # add sidebar title
    st.sidebar.title("Expense Tracker - CRUD operations - Insert your data")


# CRUD operations
create_read_data_db, delete_read_data_db, update_read_data_db = st.tabs(
    ["➕​ CREATE", "➖​ DELETE", "🔄 UPDATE"]
)

# using the first tab
with create_read_data_db:
    # create the form to add an item and send the data to the db
    with st.form("add_data_db"):
        st.markdown("##### Insert an item with the corresponding price")
        # create the needed columns for inputting the data
        (
            left_space,
            input_date,
            expense_category,
            expense_type,
            expense_price,
            store,
            city,
            right_space,
        ) = st.columns((1, 2, 2, 2, 1, 2, 2, 1))
        # create the save button
        left_space1, left_space2, left_space3, save_the_data_button = st.columns(
            (1, 1, 1, 1)
        )

        # Every form must have a submit button.
        submitted = save_the_data_button.form_submit_button(
            "Submit", help="Submit the data to the database."
        )

# with notation
with input_date:
    input_date_value = input_date.date_input(
        "Date of the purchase", "today", key="purchase_date"
    )
with expense_type:
    input_item_name = expense_type.text_input("Name of the item")
with expense_price:
    input_price = expense_price.text_input("Price")

with expense_category:
    options = [
        "food",
        "cleaning products",
        "clothes",
        "drugstore products",
        "entertainment",
        "gaming",
        "gas",
        "personal care",
        "holiday",
        "transportation",
        "restaurants",
        "others",
    ]
    expense_category = st.selectbox(
        "Choose a category",
        options,
    )

with store:
    store = st.text_input("Store", max_chars=30, key="purchase_store")

with city:
    city = st.text_input("City", max_chars=20, key="city_purchase")

# automatically create the other information useful for the database
# such as: month, year, weekday_number, weekday_text, months_text, store, city, english_translation, year_month

# get automatically the month
month_number = input_date_value.month
# get automatically the year
year_number = input_date_value.year
# get automatically the day
day_number = input_date_value.day
# get the day of the week as a number (using isoweek): 1-Monday, 7-Sunday
isoweek_day = input_date_value.isoweekday()
# get the day of the week as a string
day_of_the_week = input_date_value.strftime("%A")
# get the month as a three letter string
month_short = input_date_value.strftime("%b")

# save all the variable to a list to be sent to the db as a row
insert_data = [
    input_date,
    expense_category,
    expense_type,
    expense_price,
    store,
    city,
    month_number,
    year_number,
    day_number,
    isoweek_day,
    day_of_the_week,
    month_short,
]

# TODO:
# all of this variable should be sent to the "sqlalchemy_db.py" file as soon as the
# submit button is pressed


# TODO:
# Need to display the dataframe, then select the row and then do something
# in terms of deleting the row based on the ID.
# Look here:
# - https://gist.github.com/treuille/e8f07ebcd92265a68ecec585f7594918
# - https://discuss.streamlit.io/t/can-you-select-rows-in-a-table/737/2

# # delete an item
# with st.form("delete_data_db"):
#     st.markdown("##### Select a row and delete it from the database")
#     # create the needed columns
#     (
#         left_space_delete,
#         text_input_item_delete,
#         right_space_delete,
#     ) = st.columns((1, 2, 1))
#     (
#         left_space1_delete,
#         left_space2_delete,
#         left_space3_delete,
#         save_the_data_button_delete,
#     ) = st.columns((1, 1, 1, 1))

#     # with notation
#     with text_input_item_delete:
#         text_input_item_delete.text_input("Delete an item")

#     # Every form must have a submit button.
#     submitted = save_the_data_button_delete.form_submit_button(
#         "Submit", help="Delete the data to the database."
#     )

# TODO:
# For editable dataframes, look here:
# - https://blog.streamlit.io/editable-dataframes-are-here/
# - https://discuss.streamlit.io/t/is-it-possible-to-use-a-button-to-adjust-values-in-an-editable-dataframe/43391
# # update an item
# with st.form("update_data_db"):
#     st.markdown("##### Select a row and delete it from the database")
#     # create the needed columns
#     (
#         left_space_delete,
#         text_input_item_delete,
#         right_space_delete,
#     ) = st.columns((1, 2, 1))
#     (
#         left_space1_delete,
#         left_space2_delete,
#         left_space3_delete,
#         save_the_data_button_delete,
#     ) = st.columns((1, 1, 1, 1))

#     # with notation
#     with text_input_item_delete:
#         text_input_item_delete.text_input("Delete an item")

#     # Every form must have a submit button.
#     submitted = save_the_data_button_delete.form_submit_button(
#         "Submit", help="Delete the data to the database."
#     )
