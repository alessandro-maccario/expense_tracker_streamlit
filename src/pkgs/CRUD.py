# --- Import packages --- #
import pandas as pd
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pkgs.sqlalchemy_db import (
    TEST_Expense,
    engine,
)
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to commit changes to the database
def commit_to_database(
    input_date: datetime,
    expense_category: str,
    expense_type: str,
    expense_price: float,
    store: str,
    city: str,
    month_number: str,
    year_number: str,
    day_number: str,
    isoweek_day: str,
    day_of_the_week: str,
    month_short: str,
    created_at: datetime,
):
    """Connect to MySQL DB and the "expenses" table to save the data when the user,
    after inserting the data into the UI, press the "Submit" button.

    Parameters
    ----------
    input_date : datetime.date
        The date that the user decides as input of the purchase.
    expense_category : str
        The expense category to which the purchase belongs to. (e.g.: food, transportation)
    expense_type : str
        The specific name of the item purchased. (e.g.: for a food element, then coffee cups)
    expense_price : float
        The price of the item.

    Return
    ------
    None

    """
    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        expense = TEST_Expense(
            input_date=input_date,
            expense_category=expense_category,
            expense_type=expense_type,
            expense_price=expense_price,
            store=store,
            city=city,
            month_number=month_number,
            year_number=year_number,
            day_number=day_number,
            isoweek_day=isoweek_day,
            day_of_the_week=day_of_the_week,
            month_short=month_short,
            created_at=created_at,
        )
        session.add(expense)  # use .add_all if you want to add more rows at a time
        logger.info("About to commit session")
        session.commit()
        logger.info("Session committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error during commit: {e}", exc_info=True)
        st.error(f"An error occurred: {e}")
    finally:
        session.close()

    return


def read_from_database():
    """Function to read the expenses table.


    Return
    ------
    None
    """
    # Create a configured "Session" class.
    # The bind tells the session where it should be making these transactions,
    # therefore which database it should be connected to perform all the actions.
    Session = sessionmaker(bind=engine)
    # The session will return an actual session object that we can use to perform
    # actions on.
    session = Session()

    # query all the expenses available in the Class TEST_Expense
    # and extract the information
    expenses = session.query(TEST_Expense).all()

    # create a dictionary to store the information from each row
    # of the database based on the id used as a key
    dict_expenses = dict()

    # loop through each user that we get from the expenses and extract
    # the information from SQLAlchemy data type
    for expense in expenses:
        # save the id to be used as a key for the dictionary
        row_id_expense = expense.id

        # if the key not in the dictionary, then add it and
        # add all the information regarding the specific row
        if row_id_expense not in dict_expenses:
            dict_expenses[row_id_expense] = [
                expense.id,
                expense.input_date,
                expense.expense_category,
                expense.expense_type,
                expense.expense_price,
                expense.store,
                expense.city,
                expense.month_number,
                expense.year_number,
                expense.day_number,
                expense.isoweek_day,
                expense.day_of_the_week,
                expense.month_short,
                expense.created_at,
            ]

    # convert the dict to a dataframe
    df_expenses = pd.DataFrame.from_dict(
        dict_expenses,
        orient="index",
        columns=[
            "id",
            "input_date",
            "expense_category",
            "expense_type",
            "expense_price",
            "store",
            "city",
            "month_number",
            "year_number",
            "day_number",
            "isoweek_day",
            "day_of_the_week",
            "month_short",
            "created_at",
        ],
    )

    return df_expenses


def update_database(
    idx: int,
    input_date: datetime,
    expense_category: str,
    expense_type: str,
    expense_price: float,
    store: str,
    city: str,
    month_number: str,
    year_number: str,
    day_number: str,
    isoweek_day: str,
    day_of_the_week: str,
    month_short: str,
    created_at: datetime,
) -> None:
    """
    Function to update the database if any rows has been changed.

    Parameters
    ----------
    idx : int
        Row index to use for updating the correct row

    Returns
    -------
    None

    """
    # Create a configured "Session" class.
    # The bind tells the session where it should be making these transactions,
    # therefore which database it should be connected to perform all the actions.
    Session = sessionmaker(bind=engine)
    # The session will return an actual session object that we can use to perform
    # actions on.
    session = Session()

    # query all the expenses available in the Class TEST_Expense that corresponds to a
    # single id value and update that single row with the newest information
    expense = session.query(TEST_Expense).filter(TEST_Expense.id == idx).first()
    print(expense)

    changes = {
        "id": idx,
        "input_date": input_date,
        "expense_category": expense_category,
        "expense_type": expense_type,
        "expense_price": expense_price,
        "store": store,
        "city": city,
        "month_number": month_number,
        "year_number": year_number,
        "day_number": day_number,
        "isoweek_day": isoweek_day,
        "day_of_the_week": day_of_the_week,
        "month_short": month_short,
        "created_at": created_at,
    }

    # https://stackoverflow.com/questions/47735329/updating-a-row-using-sqlalchemy-orm
    # assign the new values to the previous row
    for key, value in changes.items():
        # print("KEY, VALUE:", key, value)
        # this read as: set the attribute to the object "expense"
        # assigning to the "key" the specific "value"
        setattr(expense, key, value)

    # commit the changes
    # For a broader explanation, check:
    # - https://medium.com/@oba2311/sqlalchemy-whats-the-difference-between-a-flush-and-commit-baec6c2410a9
    session.commit()

    # session.flush()
    # expense = session.query(TEST_Expense).filter_by(id=idx).one_or_none()

    return


def delete_from_database(idx) -> None:
    """
        Function to delete a single/multiple rows from the database table
        via indexes.

    Parameters
    ----------
    idx : int
        Index of the row to be deleted.

    Returns
    -------
    None

    """
    # Create a configured "Session" class.
    # The bind tells the session where it should be making these transactions,
    # therefore which database it should be connected to perform all the actions.
    Session = sessionmaker(bind=engine)
    # The session will return an actual session object that we can use to perform
    # actions on.
    session = Session()

    # delete SQLAlchemy constructor
    # https://docs.sqlalchemy.org/en/20/tutorial/data_update.html
    deletion_query = session.query(TEST_Expense).filter(TEST_Expense.id == idx).delete()
    print("DELETED ROW:", deletion_query)
    # delete_expense = session.query(TEST_Expense).filter(TEST_Expense.id == idx).first()
    # session.delete(delete_expense)

    # commit the changes
    # For a broader explanation, check:
    # - https://medium.com/@oba2311/sqlalchemy-whats-the-difference-between-a-flush-and-commit-baec6c2410a9
    session.commit()

    return
