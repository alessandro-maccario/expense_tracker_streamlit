# --- Import packages --- #
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pkgs.sqlalchemy_db import (
    TEST_Expense,
    engine,
)

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to commit changes to the database
def commit_to_database(input_date, expense_category, expense_type, expense_price):
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
            # store=store,
            # city=city,
            # month_number=month_number,
            # year_number=year_number,
            # day_number=day_number,
            # isoweek_day=isoweek_day,
            # day_of_the_week=day_of_the_week,
            # month_short=month_short,
        )
        session.add(expense)
        logger.info("About to commit session")
        session.commit()
        logger.info("Session committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error during commit: {e}", exc_info=True)
        st.error(f"An error occurred: {e}")
    finally:
        session.close()
