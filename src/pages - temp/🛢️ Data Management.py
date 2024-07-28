"""
This script built in Streamlit gives the user the possibility
to insert the data manually into the database.
"""

# --- Import packages --- #
import streamlit as st
from pkgs.CRUD import (
    commit_to_database,
    read_from_database,
    update_database,
    delete_from_database,
)
from datetime import datetime

# TODO:
# Need to integrate this code as another tab/page into the main app!

# --- Main code --- #

# set the page default setting to wide
st.set_page_config(layout="wide", page_title="Data Management", page_icon="🛢️")

# # sidebar
with st.sidebar:
    #     # add sidebar title
    st.sidebar.title("Expense Tracker")
    st.markdown("Manage your data: create, read, update and delete rows from the database!")


# CRUD operations
create_read_data_db, update_read_data_db = st.tabs(["➕​ CREATE", "🔄 UPDATE"])

# using the first tab
with create_read_data_db:
    # read the data from the DB and display the dataframe
    # print(read_from_database())

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
        left_space1, left_space2, left_space3, save_the_data_button = st.columns((1, 1, 1, 1))

    # with notation
    with input_date:
        input_date_value = input_date.date_input("Date of the purchase", "today", key="purchase_date")
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
    submitted = save_the_data_button.form_submit_button("Submit", help="Submit to database.")

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
    # create the form to add an item and send the data to the db
    with st.form("update_read_data_db", clear_on_submit=True):
        st.markdown("##### Edit the dataframe")

        # read from the database
        db_dataframe = read_from_database().sort_values(by=["created_at"], ascending=False).reset_index(drop=True)
        edited_df = st.data_editor(
            db_dataframe,
            disabled=["index", "created_at"],
            key="editable_dataframe",
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "id": None,  # hide the column even though it's there,
                "month_number": None,
                "year_number": None,
                "day_number": None,
                "isoweek_day": None,
                "day_of_the_week": None,
                "month_short": None,
                "input_date": st.column_config.DateColumn(format="YYYY-MM-DD", required=True),
                "expense_category": st.column_config.SelectboxColumn(
                    options=[
                        "Cleaning Producs",
                        "Clothes",
                        "Drugstore product",
                        "Entertainement",
                        "Food",
                        "Gaming",
                        "Gas",
                        "Hairdresser",
                        "Home Expenses",
                        "Hotel",
                        "Knowledge",
                        "Others",
                        "Restaurants",
                        "Transportation",
                    ],
                    required=True,
                    default="Food",
                ),
            },
        )
        st.write("Here's the value in Session State:")
        st.write(st.session_state["editable_dataframe"])

        ###############################

        # if the button is pressed, then save the changes to the db
        # if submit_data_editor_changes:
        for key in st.session_state["editable_dataframe"]["edited_rows"]:
            if key in st.session_state["editable_dataframe"]["edited_rows"]:
                print("------ ID KEYS AVAILABLE -------")

                # INPUT DATE
                # get the data in the corresponding cell for the "key" and the corresponding column
                default_value_input_date = db_dataframe.at[key, "input_date"]
                # use the default value as default in case nothing as been found in the session_state
                session_input_date = (
                    st.session_state["editable_dataframe"]["edited_rows"].get(key, {}).get("input_date", default_value_input_date)
                )

                # EXPENSE TYPE
                # get the data in the corresponding cell for the "key" and the corresponding column
                default_value_expense_type = db_dataframe.at[key, "expense_type"]
                # use the default value as default in case nothing as been found in the session_state
                session_expense_type = (
                    st.session_state["editable_dataframe"]["edited_rows"].get(key, {}).get("expense_type", default_value_expense_type)
                )

                # EXPENSE PRICE
                # get the data in the corresponding cell for the "key" and the corresponding column
                default_value_expense_price = db_dataframe.at[key, "expense_price"]
                # use the default value as default in case nothing as been found in the session_state
                session_expense_price = (
                    st.session_state["editable_dataframe"]["edited_rows"].get(key, {}).get("expense_price", default_value_expense_price)
                )

                # STORE
                # get the data in the corresponding cell for the "key" and the corresponding column
                default_value_store = db_dataframe.at[key, "store"]
                # use the default value as default in case nothing as been found in the session_state
                session_expense_store = st.session_state["editable_dataframe"]["edited_rows"].get(key, {}).get("store", default_value_store)

                # CITY
                # get the data in the corresponding cell for the "key" and the corresponding column
                default_value_city = db_dataframe.at[key, "city"]
                # use the default value as default in case nothing as been found in the session_state
                session_expense_city = st.session_state["editable_dataframe"]["edited_rows"].get(key, {}).get("city", default_value_city)

                # get automatically the month
                month_number = str(default_value_input_date.month)
                # get automatically the year
                year_number = str(default_value_input_date.year)
                # get automatically the day
                day_number = str(default_value_input_date.day)
                # get the day of the week as a number (using isoweek): 1-Monday, 7-Sunday
                isoweek_day = str(default_value_input_date.isoweekday())
                # get the day of the week as a string
                day_of_the_week = default_value_input_date.strftime("%A")
                # get the month as a three letter string
                month_short = default_value_input_date.strftime("%b")

                #### END #####

        # show the edited table
        st.table(edited_df)

        (
            left_space_submit2db,
            right_space_submit2db,
        ) = st.columns((6, 1))

        # save the edited df before it gets modified to keep the
        # id of each row. This will be used with the "deleted" ids,
        # joined and the right id table is then fetched and used for removing
        # the specific row from the database table
        temp_edited_df = db_dataframe.copy(deep=True)

        # Every form must have a submit button.
        submit_data_editor_changes = right_space_submit2db.form_submit_button("Submit", help="Submit the changes to the database.")

    if submit_data_editor_changes:
        # problem: sqlalchemy.exc.OperationalError: (MySQLdb.OperationalError) (1292...
        # This is due to the fact that you are sending pandas dataframe to SQLAlchemy, not
        # raw data. Need to loop through it to get only the raw input to load into the DB.
        print(
            "SESSION STATE IS:",
            st.session_state["editable_dataframe"]["edited_rows"],
            "DELETED ROWS ARE:",
            st.session_state["editable_dataframe"],
        )

        # save the indexes from the edited_df that have to be then dropped
        temp_index_list_to_drop = []
        if st.session_state["editable_dataframe"]["deleted_rows"]:
            print("###### INSIDE ######")
            for each_deleted_row in st.session_state["editable_dataframe"]["deleted_rows"]:
                print("###### INSIDE THE LOOP ######")
                # Pandas filter() by index
                edited_df_index_filtered = temp_edited_df.filter(items=[each_deleted_row], axis=0)
                # get only the index value connected to each row
                temp_index_list_to_drop.append(edited_df_index_filtered["id"].iloc[0])
        else:
            pass
        print("LIST OF INDEXES TO BE DROPPED:", temp_index_list_to_drop)

        # ADDING NEW ROWS
        # if some new rows have been added, then, let's add them to the database table
        if st.session_state["editable_dataframe"]["added_rows"]:
            # check if each element is not None
            for attribute in st.session_state["editable_dataframe"]["added_rows"]:
                # attribute = to a single row. Need to loop on each single item in each single row
                # PROBLEM: https://realpython.com/iterate-through-dictionary-python/
                for key in attribute:
                    print("KEY:", key, ",", "ATTRIBUTE:", attribute[key])
                    if key == "input_date":
                        input_date_value = attribute[key]
                    elif key == "expense_category":
                        expense_category = attribute[key]
                    elif key == "expense_type":
                        input_item_name = attribute[key]
                    elif key == "expense_price":
                        input_price = attribute[key]
                    elif key == "store":
                        store = attribute[key]
                    elif key == "city":
                        city = attribute[key]
                    else:
                        expense_category = None
                        input_item_name = None
                        input_price = None
                        store = None
                        city = None

                # get the month
                month_number = datetime.strptime(input_date_value, "%Y-%m-%d").month
                # get the year
                year_number = datetime.strptime(input_date_value, "%Y-%m-%d").year
                # get the day_number
                day_number = datetime.strptime(input_date_value, "%Y-%m-%d").day
                # get the isoweek
                isoweek_day = datetime.strptime(input_date_value, "%Y-%m-%d").isoweekday()
                # get the day of the week
                day_of_the_week = datetime.strptime(input_date_value, "%Y-%m-%d").strftime("%A")
                # get the short name of the month (for instance: "Jan")
                month_short = datetime.strptime(input_date_value, "%Y-%m-%d").strftime("%b")
                # get the current time
                created_at = datetime.now()

                # commit the new row to the database table
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

        ####### END ADDING ROWS#########

        ####### UPDATING ROWS ##########
        # if some new rows have been added, then, let's add them to the database table
        if st.session_state["editable_dataframe"]["edited_rows"]:
            # need for a for loop (optimization later)
            for index, row in edited_df.iterrows():
                # update the database row
                update_database(
                    idx=row["id"],
                    input_date=row["input_date"],
                    expense_category=row["expense_category"],
                    expense_type=row["expense_type"],
                    expense_price=row["expense_price"],
                    store=row["store"],
                    city=row["city"],
                    month_number=row["month_number"],
                    year_number=row["year_number"],
                    day_number=row["day_number"],
                    isoweek_day=row["isoweek_day"],
                    day_of_the_week=row["day_of_the_week"],
                    month_short=row["month_short"],
                    created_at=row["created_at"],
                )

        # check if a row/some rows has/have been deleted
        if st.session_state["editable_dataframe"]["deleted_rows"]:
            for each_row_idx in temp_index_list_to_drop:
                # then call the function to delete the row
                delete_from_database(each_row_idx)
        else:
            pass

        st.success("Changes committed successfully to the database.")
        st.rerun()

# TODO:
# - think (using gpt as well) how to rebuild the database!


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
