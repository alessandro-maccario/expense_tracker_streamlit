"""
    Expense tracker: get information about your monthly expenses, in detail.
    This is the first step to start implementing your personal 
    budget management strategy.
"""

# use streamlit
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import plotly.graph_objects as go


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
            "Bar plot - Expenses per month",
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
# print(df_expenses.head())

previous_30_days = past_date - datetime.timedelta(days=30)
# Filter data between the past date and 30 days earlier.
# Useful to get the DELTA underneath the amount spent during the current timeframe
df_expenses_previous_30_days = df_expenses.loc[
    (df_expenses["date"].dt.date >= previous_30_days)
    & (df_expenses["date"].dt.date < past_date)
]

#  Filter data between two dates for the expense_category bar plot
df_expenses_filtered = df_expenses.loc[
    (df_expenses["date"].dt.date >= past_date)
    & (df_expenses["date"].dt.date < today_date)
]

#  Filter data for year
df_expenses_filtered_year = df_expenses.loc[(df_expenses["year"] == int(choose_year))]

# set the index using the expense_category column
df_expenses_filtered_for_category = df_expenses_filtered.set_index("expense_category")
df_expenses_filtered_year_grouped = df_expenses_filtered.groupby(
    "expense_category",
)[["value"]].sum()

fig_bar_chart = px.bar(
    df_expenses_filtered.groupby("expense_category")["value"].sum().reset_index(),
    x="expense_category",
    y="value",
    color="expense_category",
    title="Expenses per category",
)

# get the list of unique element in the index
x_coords = list(set(df_expenses_filtered_year_grouped.index))

# Create a DataFrame with the desired order of the categories
category_order_df = pd.DataFrame(index=x_coords)

fig_bar_chart.add_trace(
    go.Scatter(
        x=x_coords,
        # used the previous df to sort the categories as the reordered one
        y=df_expenses_filtered_year_grouped["value"].reindex(category_order_df.index),
        text=df_expenses_filtered_year_grouped["value"].reindex(
            category_order_df.index
        ),
        mode="text",
        textposition="top center",
        textfont=dict(
            size=11,
        ),
        showlegend=False,
    )
)

fig_pie_plot = px.pie(
    df_expenses_filtered,
    values="value",
    names="store",
    title="Expenses per store",
)

# get statistics using a line chart
fig_line_chart = px.line(
    df_expenses.groupby("date").sum().reset_index(),
    x="date",
    y="value",
    # color="year",
    title="Expenses per month",
)
# Calculate monthly averages
# Resample to month and calculate average value for each month
df_expenses_subdf = df_expenses[["date", "value"]]
df_expenses_subdf["value"] = pd.to_numeric(df_expenses_subdf["value"])
# take the average daily expenses per month
monthly_avg_values_per_day = df_expenses_subdf.resample("ME", on="date").sum() / 30
# print(monthly_avg_values_per_day)

# add horizontal line as the average line
# fig_line_chart.add_hline(
#     y=df_expenses.groupby("date").sum().reset_index()["value"].mean(),
#     line_color="red",
#     annotation_text="average",
# )
# Plot the average expenses per day in a month
fig_line_chart.add_trace(
    go.Scatter(
        x=monthly_avg_values_per_day.index,
        y=monthly_avg_values_per_day["value"],
        mode="lines",
        name="Daily Average per month",
        line=dict(color="#FF0000"),
    )
)
# Update layout (optional)
fig_line_chart.update_layout(
    title="Expenses Over Time", xaxis_title="Date", yaxis_title="Expenses"
)


# filter the df out using the "choose_year" filter for the year
df_expenses_subdf_by_month_per_year = df_expenses[df_expenses["year"] == choose_year]
# get only the month and the values
df_expenses_subdf_by_month = df_expenses_subdf_by_month_per_year[["month", "value"]]
# take the average daily expenses per month
monthly_sum_values = df_expenses_subdf_by_month.groupby(["month"]).sum()
# print(monthly_sum_values)
# get statistics per months, using a bar plot
fig_bar_chart_months = px.bar(
    df_expenses_filtered_year.groupby(["expense_category", "month"])["value"]
    .sum()
    .reset_index(),
    x="month",
    y="value",
    color="expense_category",
    title="Expenses per month and category",
)
# Plot the average expenses per month
fig_bar_chart_months.add_trace(
    go.Scatter(
        x=monthly_sum_values.index,
        y=monthly_sum_values["value"],
        mode="lines",
        name="Sum per month",
        line=dict(color="#FF0000"),
    )
)
# Update layout (optional)
fig_bar_chart_months.update_layout(
    title="Expenses per Month", xaxis_title="Date", yaxis_title="Expenses"
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


# filter the data to keep only those rows where there are multiple days considered
# (filter out all those data that shows only one day purchase - filter out outliers)

# Group by "store" and count the number of how many times a store appears in the data
# If it appears only one, then it has been only a one-time purchase, not useful
# for showing statistics about it.

# Filter out rows where the number of unique store appearance more than 7 related to "food" category
grouped_counts = (
    df_expenses_filtered_year[df_expenses_filtered_year["expense_category"] == "food"]
    .groupby(["store"])
    .size()
    .reset_index(name="count")
    .sort_values(by="count")
)
print(grouped_counts[grouped_counts["count"] > 7])
grouped_counts = grouped_counts[grouped_counts["count"] > 7]

# Merge the filtered dataframe with the original one on the "store" column
# therefore you will get only those stores that appear in the data more than
# 7 times.
df_expenses_size_filtering_year = df_expenses_filtered_year.merge(
    grouped_counts[["store"]],
    on=["store"],
    how="inner",
)

# show the store options
option = st.selectbox(
    "Select the store",
    # show me only those options related to food
    df_expenses_size_filtering_year[
        df_expenses_size_filtering_year["expense_category"] == "food"
    ]
    .sort_values(by="store", ascending=True)["store"]
    .str.lower()
    .unique(),
    placeholder="Select the store...",
)


# filter the dataframe based on the chosen option
df_expenses_filtered_year_bar_plot = df_expenses_filtered_year.loc[
    (df_expenses_filtered_year["store"] == option)
]

# --- Dropdown menu to select the store for the bar plot --- #
# get statistics per months, using a bar plot
fig_bar_chart_week = px.bar(
    df_expenses_filtered_year_bar_plot.groupby(["weekday_text"])["value"]
    .agg(["mean"])
    .reset_index(),
    x="weekday_text",
    y="mean",
    title="Expenses per weekday per store - Food category",
)

st.plotly_chart(
    fig_bar_chart_week,
    use_container_width=True,
    sharing="streamlit",
    theme="streamlit",
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

# TODO
# Need to show the bar plots using only the sum of all the items,
# not to show the single item in the bar plot!

# TODO:
# in the plot for the weekday and the stores, groupby and show only the first 10 stores
# with the highest values!

# TODO:
# add a metric to show the most expensive category of the timeframe selected
# and the amount spent in the timeframe selected compared to the previous month

# TODO
# Add the following information: most expensive category, and you want to try to reduce the amount
# spent, for instance on food. Therefore you set a limit of 5/10% of saving on food each month.
# You also need another metric that tells you: how much you spent on food compare to the previous
# month (literally, taken from the month before), how much you saved so far (for instance, after
# a few months later) and how far you are in reaching your goal (if the goal is reaching 500€ per year
# saved, then you can show how much you already saved and how much you still need to reach the goal)!
# You should also record this data, but you have to think how.

# TODO:
# Create the database underneath to stop using the csv file. In the future, record the data directly in
# the DB. In order to do that, you should have another page connected to your db in streamlit that
# gives you the possibility to record the expenses and directly see the results of your new data directly
# in the plots.
