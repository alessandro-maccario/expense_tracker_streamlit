"""
    This script built in Streamlit gives the user the possibility
    to insert the data manually into the database.
"""

# --- Import packages --- #
import pandas as pd
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
        # create the needed columns
        left_space, text_input_item, text_input_price, right_space = st.columns(
            (1, 2, 1, 1)
        )
        left_space1, left_space2, left_space3, save_the_data_button = st.columns(
            (1, 1, 1, 1)
        )

        # with notation
        with text_input_item:
            text_input_item.text_input("Item")

        with text_input_price:
            text_input_price.text_input("Price")

        # Every form must have a submit button.
        submitted = save_the_data_button.form_submit_button(
            "Submit", help="Submit the data to the database."
        )

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
