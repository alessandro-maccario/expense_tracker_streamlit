"""
    This script built in Streamlit gives the user the possibility
    to insert the data manually into the database.
"""

# --- Import packages --- #
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pkgs.sqlalchemy_db import (
    TEST_Expense,
    engine,
)
from pkgs.CRUD import commit_to_database, read_from_database
from datetime import datetime

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
create_read_data_db, update_read_data_db = st.tabs(["➕​ CREATE", "🔄 UPDATE"])

# using the first tab
with create_read_data_db:
    # read the data from the DB and display the dataframe
    print(read_from_database())

    # create the form to add an item and send the data to the db
    with st.form("add_data_db", clear_on_submit=True):
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

    # with notation
    with input_date:
        input_date_value = input_date.date_input(
            "Date of the purchase", "today", key="purchase_date"
        )
    with expense_type:
        input_item_name = expense_type.text_input("Name of the item")
    with expense_price:
        input_price = expense_price.number_input(label="Price", step=1.0, format="%.2f")

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

    # Every form must have a submit button.
    submitted = save_the_data_button.form_submit_button(
        "Submit", help="Submit to database."
    )

    if submitted:
        # Automatically create other information useful for the database
        # such as: month, year, weekday_number, weekday_text, months_text, store, city, english_translation, year_month

        # get automatically the month
        month_number = str(input_date_value.month)
        # get automatically the year
        year_number = str(input_date_value.year)
        # get automatically the day
        day_number = str(input_date_value.day)
        # get the day of the week as a number (using isoweek): 1-Monday, 7-Sunday
        isoweek_day = str(input_date_value.isoweekday())
        # get the day of the week as a string
        day_of_the_week = input_date_value.strftime("%A")
        # get the month as a three letter string
        month_short = input_date_value.strftime("%b")
        # get the current timestamp when the item has been inserted in the DB
        created_at = datetime.now()

        # Now commit the data to the database
        commit_to_database(
            input_date_value,
            expense_category,
            input_item_name,
            input_price,
            store,
            city,
            month_number,
            year_number,
            day_number,
            isoweek_day,
            day_of_the_week,
            month_short,
            created_at,
        )

        # read from the database
        db_dataframe = read_from_database()

        # filter the dataframe to get only the last five most recent entries that the user committed
        db_current_session = (
            db_dataframe[(db_dataframe["created_at"].dt.date >= datetime.now().date())]
            .sort_values(by=["created_at"], ascending=False)
            .head()
        )
        st.markdown("#### Last 5 rows inserted in the database.")
        db_current_display = st.table(db_current_session)

        st.success("Changes committed successfully.")


# TODO:
# Need to display the dataframe, then select the row and then do something
# in terms of deleting/editing the row based on the ID.
# Look here:
# - https://gist.github.com/treuille/e8f07ebcd92265a68ecec585f7594918
# - https://discuss.streamlit.io/t/can-you-select-rows-in-a-table/737/2

# Session state:
# https://github.com/streamlit/docs/blob/main/python/api-examples-source/data.data_editor4.py
# https://doc-data-editor-changed.streamlit.app/


# update the database
with update_read_data_db:
    # with st.form("update_read_data_db", clear_on_submit=False):
    st.markdown("##### Edit the dataframe")

    # read from the database
    db_dataframe = (
        read_from_database()
        .sort_values(by=["created_at"], ascending=False)
        .reset_index(drop=True)
    )
    edited_df = st.data_editor(
        db_dataframe,
        disabled=["index", "created_at"],
        key="editable_dataframe",
        num_rows="dynamic",
        use_container_width=True,
    )
    st.write("Here's the value in Session State:")
    st.write(st.session_state["editable_dataframe"])
    # access the key of the dictionary "editable_dataframe"
    # st.write(st.session_state["editable_dataframe"]["edited_rows"])
    # use this index and the column name to change the current df and update it

    ###############################
    #
    # # Every form must have a submit button.
    # submit_data_editor_changes = st.form_submit_button(
    #     "Submit", help="Submit the changes to the database."
    # )

    # if the button is pressed, then save the changes to the db
    # if submit_data_editor_changes:
    for key in st.session_state["editable_dataframe"]["edited_rows"]:
        if key in st.session_state["editable_dataframe"]["edited_rows"]:
            print("------ ID KEYS AVAILABLE -------")
            try:
                # INPUT DATE
                # if found, save the edited value into the session_input_date
                session_input_date = st.session_state["editable_dataframe"][
                    "edited_rows"
                ][key]["input_date"]
                print("ID KEY:", key, session_input_date)

                # EXPENSE TYPE
                # if found, save the edited value into the session_state_expense_type
                session_state_expense_type = st.session_state["editable_dataframe"][
                    "edited_rows"
                ][key]["expense_type"]
                print("ID KEY:", key, session_state_expense_type)

                # EXPENSE PRICE
                # if found, save the edited value into the session_state_expense_price
                session_state_expense_price = st.session_state["editable_dataframe"][
                    "edited_rows"
                ][key]["expense_price"]
                print("ID KEY:", key, session_state_expense_price)

                # TODO:
                # Need to add all of the other columns as done right here above,
                # then call the commit_to_database() function to commit everything
                # to the DB (attention: do not know how to fill up the values that have
                # not been changed by the user into the function)!

                # EXPENSE TYPE BEFORE/AFTER
                print("BEFORE:", db_dataframe.loc[key, "expense_type"])
                edited_df.loc[key, "expense_type"] = session_state_expense_type
                print("AFTER:", edited_df.loc[key, "expense_type"])

                # EXPENSE PRICE BEFORE/AFTER
                print("BEFORE:", db_dataframe.loc[key, "expense_price"])
                edited_df.loc[key, "expense_price"] = session_state_expense_price
                print("AFTER:", edited_df.loc[key, "expense_price"])

                # if db_dataframe.iloc[key, "expense_type"] != session_state_expense_type:
                #     # Update the original dataframe with edited values
                #     st.write("BEFORE:", db_dataframe.iloc[key]["expense_type"])
                #     db_dataframe.iloc[key]["expense_type"] = session_state_expense_type
                #     st.write("AFTER:", db_dataframe.iloc[key]["expense_type"])
                # else:
                #     pass

            # if key not found, then show me the column where the value is missing
            except KeyError as e:
                print(f"{e} not found")

    # show the edited table
    st.table(edited_df)

# TODO:
# use .iloc[key, column] to insert the value if it has been found.
# if not, you should be able to leave the current value has default value.
# To test: insert the value(s) and then st.write the dataframe again.
# In the end, save the data to the DB with a button for instance.
# NOTE:
# need to insert the other columns to be checked and inserted!

# NOTE:
# DELETING ROWS:
# https://discuss.streamlit.io/t/deleting-rows-in-st-data-editor-progmatically/46337

# NOTE:
# SQL CONNECTION
# https://docs.streamlit.io/develop/api-reference/connections/st.connections.sqlconnection

# NOTE:
# STATEFULLNESS:
# https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization

# TODO:
# To save the data to the db: load the current table available in the MySQL db.
# Get only the changes that happens in the st.data_editor: save the changes in the dataframe
# that you read from the database.
# Save the dataframe again to the DB using a callback function based on the "commit_to_database()"
# function available in the CRUD.py file.

# TODO:
# - need to add a button to update the table in the database
# - add another page to upload an excel sheet directly to the database (either by dropping the table completely
# or by adding the rows that were not there before based on the values in the columns to avoid duplicates)

# TODO:
# For editable dataframes, look here:
# - https://blog.streamlit.io/editable-dataframes-are-here/
# - https://discuss.streamlit.io/t/is-it-possible-to-use-a-button-to-adjust-values-in-an-editable-dataframe/43391
