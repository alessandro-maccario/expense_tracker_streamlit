"""
    This script will connect to MySQL db using SQLAlchemy and using ORM 
    (object relational mapping) creating the MySQL objects based on Python classes.

    Reference:
        - https://www.youtube.com/watch?v=Z2zD3EdjpNo&list=PLKm_OLZcymWhtiM-0oQE2ABrrbgsndsn0
"""

# --- Import packages --- #
from sqlalchemy import create_engine, Column, Float, Integer, String, Date
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv  # to load the variables stored in the .env file
import os

# to load the variables stored in the .env file
load_dotenv()

# db credentials
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")


# create the sql engine: needed to connect to the DB
# https://www.geeksforgeeks.org/connecting-to-sql-database-using-sqlalchemy-in-python/
# https://docs.sqlalchemy.org/en/20/core/engines.html#postgresql
engine = create_engine(
    f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/db_expense_tracker"
)

# Creating a Base Class: this base class is like a template for your table definitions.
Base = declarative_base()


# --- Creating the tables --- #
# Every time you want to create a table you need to create a class object
# Continue from here minute 6:15
# https://www.youtube.com/watch?v=Z2zD3EdjpNo&list=PLKm_OLZcymWhtiM-0oQE2ABrrbgsndsn0


class Expense(Base):  # class name, usually singular
    __tablename__ = "expenses"  # table name, usually plural

    # create columns
    id = Column(Integer, primary_key=True)
    input_date = Column(Date)
    expense_category = Column(String(15))
    expense_type = Column(String(30))
    expense_price = Column(Float)
    store = Column(String(30))
    city = Column(String(30))
    month_number = Column(String(2))
    year_number = Column(String(4))
    day_number = Column(String(2))
    isoweek_day = Column(String(1))
    day_of_the_week = Column(String(15))
    month_short = Column(String(3))


# --- Enforcing all the changes --- #
# You are telling SQLAlchemy to create the actual tables in your database
# based on the table definitions you have provided in your Python classes.
Base.metadata.create_all(engine)
