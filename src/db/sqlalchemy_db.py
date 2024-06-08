"""
    This script will connect to MySQL db using SQLAlchemy and using ORM 
    (object relational mapping) creating the MySQL objects based on Python classes.

"""

# --- Import packages --- #
from sqlalchemy import create_engine
from dotenv import load_dotenv  # to load the variables stored in the .env file
import os

load_dotenv()  # to load the variables stored in the .env file

# db credentials
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")


# create the sql engine: needed to connect to the DB
# https://www.geeksforgeeks.org/connecting-to-sql-database-using-sqlalchemy-in-python/
engine = create_engine(f"mysql://{db_user}:{db_password}@{db_host}:{db_port}")
