"""
    Expense tracker: get information about your monthly expenses, in detail.
    This is the first step to start implementing your personal 
    budget management strategy.
"""

# TODO
# use streamlit
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime


df_expenses = pd.read_excel(
    r"C:\solutions\learning_python\expense_tracker\data\expense_tracker.xlsx",
    converters={"date": pd.to_datetime},
)
# sort the data by date
df_expenses.sort_values(by=["date"], inplace=True)
print(df_expenses.head())

# add sidebar title
st.sidebar.title("Expense Tracker")
# st.sidebar.subheader(
#     """TEST EXPENSE TRACKER
# """
# )

today = datetime.date.today()
# get the last 30 days starting from today
past = today - datetime.timedelta(days=30)
# date_input_1, date_input_2, date_input_3 = st.columns((0.2, 0.1, 0.2))

with st.sidebar:
    past_date = st.date_input("From", past)
    today_date = st.date_input("To", today)

#  Filter data between two dates
df_expenses_filtered = df_expenses.loc[
    (df_expenses["date"].dt.date >= past_date)
    & (df_expenses["date"].dt.date < today_date)
]

fig_bar_chart = px.bar(
    df_expenses_filtered,
    x="expense_category",
    y="value",
    color="expense_category",
    title="Expenses per category",
)

fig_pie_plot = px.pie(
    df_expenses_filtered,
    values="value",
    names="store",
    title="Expenses per store",
)

# get statistics using a line chart
fig_line_chart = px.line(df_expenses, x="date", y="value", color="year")

# get statistics per months, using a bar plot
fig_bar_chart_months = px.bar(
    df_expenses,
    x="date",
    y="value",
    color="expense_category",
    title="Expenses per month",
)

# --- Metric: total expenses --- #
st.metric(
    label="Total amount spent in the timeframe selected",
    value=round(df_expenses_filtered["value"].sum(), 2),
    # delta="1.2 °F",
)

# --- Create columns to position the plots --- #
# plots
plot1, plot2, plot3 = st.columns((200, 1, 200))
plot1.plotly_chart(
    fig_bar_chart,
    use_container_width=True,
)
plot3.plotly_chart(
    fig_pie_plot,
    use_container_width=True,
)

st.plotly_chart(
    fig_line_chart, use_container_width=True, sharing="streamlit", theme="streamlit"
)
st.plotly_chart(
    fig_bar_chart_months,
    use_container_width=True,
    sharing="streamlit",
    theme="streamlit",
)

# TODO
# Need to show the bar plots using only the sum of all the items,
# not to show the single item in the bar plot!

# TODO
# Add a selector for selecting the category to filter in the plot AND
# in the metric!
# You can calculate the previous month expense value compare to the current month
# and then add a DELTA value in the metric to see if it went up or down.
