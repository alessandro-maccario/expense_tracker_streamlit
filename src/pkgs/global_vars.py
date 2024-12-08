import datetime
import streamlit as st

# define the start date and end date
today = datetime.date.today()
# get the last 30 days starting from today
past = today - datetime.timedelta(days=30)


BACKGROUND_COLOR = "white"
COLOR = "black"
