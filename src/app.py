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

# define the start date and end date
today = datetime.date.today()
# get the last 30 days starting from today
past = today - datetime.timedelta(days=30)

# set the page default setting to wide
st.set_page_config(layout="wide")


# sidebar
with st.sidebar:

    # add sidebar title
    st.sidebar.title("Expense Tracker")
    # st.sidebar.subheader(
    #     """TEST EXPENSE TRACKER
    # """
    # )

    # choose the excel file to load
    uploaded_file = st.file_uploader("Choose a file")

    # separator
    st.divider()

    if uploaded_file is not None:
        # load the expenses file
        df_expenses = pd.read_excel(
            uploaded_file,
            converters={"date": pd.to_datetime},
        )

        # --- Create columns to position the plots --- #
        # plots
        date1, date2, date3 = st.columns((1, 0.1, 1))
        # define start and end date
        past_date = date1.date_input("From", past)
        today_date = date3.date_input("To", today)

        # separator
        st.divider()

        # select the year to filter out
        choose_year = st.selectbox(
            "Select the year to filter the Bar Plot for the expense for month and category",
            df_expenses["year"].unique(),
        )

        # separator
        st.divider()

    else:
        # load the expenses file
        df_expenses = pd.read_excel(
            r"C:\solutions\learning_python\expense_tracker\data\data_example.xlsx",
            converters={"date": pd.to_datetime},
        )

        # --- Create columns to position the plots --- #
        # plots
        date1, date2, date3 = st.columns((1, 0.1, 1))
        # define start and end date
        past_date = date1.date_input("From", past)
        today_date = date3.date_input("To", today)

        # separator
        st.divider()

        # select the year to filter out
        choose_year = st.selectbox(
            "Select the year to filter the Bar Plot for the expense for month and category",
            df_expenses["year"].unique(),
        )

        # separator
        st.divider()


# sort the data by date
df_expenses.sort_values(by=["date"], inplace=True)
print(df_expenses.head())

previous_30_days = past_date - datetime.timedelta(days=30)
# Filter data between the past date and 30 days earlier.
# Useful to get the DELTA underneath the amount spent during the current timeframe
df_expenses_previous_30_days = df_expenses.loc[
    (df_expenses["date"].dt.date >= previous_30_days)
    & (df_expenses["date"].dt.date < past_date)
]

#  Filter data between two dates
df_expenses_filtered = df_expenses.loc[
    (df_expenses["date"].dt.date >= past_date)
    & (df_expenses["date"].dt.date < today_date)
]

#  Filter data for year
df_expenses_filtered_year = df_expenses.loc[(df_expenses["year"] == int(choose_year))]

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
fig_line_chart = px.line(
    df_expenses,
    x="date",
    y="value",
    color="year",
    title="Expenses per month and year",
)

# get statistics per months, using a bar plot
fig_bar_chart_months = px.bar(
    df_expenses_filtered_year,
    x="month",
    y="value",
    color="expense_category",
    title="Expenses per month and category",
)

# --- Metrics --- #
# calculate total amount spent in the current timeframe selected
current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)
# calculate the total amount spent in the previous 30 days from past_date
total_expenses_previous_30_days = round(df_expenses_previous_30_days["value"].sum(), 2)

# take the difference between the current timeframe and the previous 30 days, then show the value
# as a metric
diff_total_expenses = round(current_total_expenses - total_expenses_previous_30_days, 2)

# --- Metric that shows the total amount spent in the previous 30 days from past_date --- #
st.metric(
    label="Total amount spent in the timeframe selected",
    value=current_total_expenses,
    delta=diff_total_expenses,
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

option = st.selectbox(
    "Select the store",
    df_expenses_filtered_year.sort_values(by="store", ascending=True)["store"]
    .str.lower()
    .unique(),
    placeholder="Select the store...",
)

df_expenses_filtered_year_bar_plot = df_expenses_filtered_year.loc[
    (df_expenses_filtered_year["store"] == option)
]

# --- Dropdown menu to select the store for the bar plot --- #

# DOES NOT WORK WITH THE FILTERING! --> https://discuss.streamlit.io/t/filter-dataframe-by-selections-made-in-select-box/6627
# get statistics per months, using a bar plot
fig_bar_chart_week = px.bar(
    df_expenses_filtered_year_bar_plot.groupby(["weekday_text"])["value"]
    .agg(["mean"])
    .reset_index(),
    # df_expenses,
    x="weekday_text",
    y="mean",
    # color="expense_category",
    title="Expenses per weekday",
)
fig_bar_chart_week.update_xaxes(
    categoryorder="array",
    categoryarray=[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
)

st.plotly_chart(
    fig_bar_chart_week,
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

# TODO:
# Add metric that computes the difference between the current timeframe
# selected for total expenses and prior 30 days

# TODO:
# Add a line plot that plots the average spending for the week!

# TODO:
# in the plot for the weekday and the stores, groupby and show only the first 10 stores
# with the highest values!

# TODO:
# add a metric to show the most expensive category of the timeframe selected
# and the amount spent in the timeframe selected compared to the previous month
