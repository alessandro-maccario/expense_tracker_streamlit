"""
    Expense tracker: get information about your monthly expenses, in detail.
    This is the first step to start implementing your personal 
    budget management strategy.
"""

# use streamlit
import datetime
import pandas as pd
import streamlit as st

from pkgs.global_vars import today, past
import plotly.express as px
import plotly.graph_objects as go


# --- Metric functions --- #


def metric_total_amount_spent(df, today_date, past_date):
    """
    Function to calculate the total amount spent in a specific timeframe.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe
    today_date : str
        "To" date. Most recent date until which you want to filter.
    past_date : str
        "From" date. Past date from which you want to start filtering.

    Returns
    -------
    None
        Return the metrics computed for the metric to be displayed.
    """

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date < today_date)
    ]

    # calculate total amount spent in the current timeframe selected
    current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)

    ##################################################
    # --- Create columns to position the metrics --- #
    # metric1_total_amount_spent = st.columns((1))

    # from the past date (start date), go back another month
    previous_30_days = past_date - datetime.timedelta(days=30)

    # Filter data between the past date and 30 days earlier.
    # Useful to get the DELTA underneath the amount spent during the current timeframe
    df_previous_30_days = df.loc[
        (df["date"].dt.date >= previous_30_days) & (df["date"].dt.date < past_date)
    ]

    total_expenses_previous_30_days = round(df_previous_30_days["value"].sum(), 2)

    # take the difference between the current timeframe and the previous 30 days, then show the value
    # as a metric
    diff_total_expenses = round(
        current_total_expenses - total_expenses_previous_30_days, 2
    )

    # --- Metric that shows the total amount spent in the previous 30 days from past_date --- #
    metric1_total_amount_spent.metric(
        label="Expenses in the timeframe",
        value=current_total_expenses,
        delta=diff_total_expenses,
        delta_color="inverse",
    )

    return metric_total_amount_spent


def metric_total_amount_spent_category(df, category, today_date, past_date):
    """
    Function to calculate all the metrics shown in the Streamlit app.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe
    category : str
        Category to filter the df with
    today_date : str
        "To" date. Most recent date until which you want to filter.
    past_date : str
        "From" date. Past date from which you want to start filtering.

    Returns
    -------
    None
        Return the metrics computed for each element.
    """

    ##################################################
    # --- Create columns to position the metrics --- #
    # metric2_total_amount_spent_category = st.columns((1))

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date < today_date)
    ]

    # calculate total amount ONLY for the category selected (for the selected timeframe)
    # try-except: if no expenses for the selected category has been found for the selected timeframe
    # then show 0 as value for both the total_expenses_category and total_expenses_previous_30_days_category
    try:
        total_expenses_category = round(
            df_expenses_filtered[df_expenses_filtered["expense_category"] == category]
            .groupby(["expense_category"])["value"]
            .sum(),
            2,
        )[0]
    except IndexError:
        total_expenses_category = 0

    # from the past date (start date), go back another month
    previous_30_days = past_date - datetime.timedelta(days=30)

    # Filter data between the past date and 30 days earlier.
    # Useful to get the DELTA underneath the amount spent during the current timeframe
    df_previous_30_days = df.loc[
        (df["date"].dt.date >= previous_30_days) & (df["date"].dt.date < past_date)
    ]

    # calculate total amount ONLY for food (for the 30 days before the "From" date)
    # try-except: if no expenses for the selected category has been found for the selected timeframe
    # then show 0 as value for both the total_expenses_category and total_expenses_previous_30_days_category
    try:
        total_expenses_previous_30_days_category = round(
            df_previous_30_days[df_previous_30_days["expense_category"] == category]
            .groupby(["expense_category"])["value"]
            .sum(),
            2,
        )[0]
    except IndexError:
        total_expenses_previous_30_days_category = 0

    # take the difference between the current timeframe and the previous 30 days, then show the value
    # as a metric ONLY for the chosen category
    diff_total_expenses_category = round(
        total_expenses_category - total_expenses_previous_30_days_category, 2
    )

    # --- Metric that shows the total amount spent in the previous 30 days from past_date --- #
    metric2_total_amount_spent_category.metric(
        label=f"Expenses for {category}",
        value=total_expenses_category,
        delta=diff_total_expenses_category,
        delta_color="inverse",
    )

    return metric2_total_amount_spent_category


# set the page default setting to wide
st.set_page_config(layout="wide")

# sidebar
with st.sidebar:

    # add sidebar title
    st.sidebar.title("Expense Tracker")

    # allow only .csv and .xlsx files to be uploaded
    uploaded_file = st.file_uploader(
        "Upload a file (.csv OR .xlsx)", type=["csv", "xlsx"]
    )

    # separator
    st.divider()

    # Check if file was uploaded
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            # load the expenses file
            df_expenses = pd.read_csv(
                uploaded_file,
                converters={"date": pd.to_datetime},
            )
        else:
            # load the expenses file
            df_expenses = pd.read_excel(
                uploaded_file,
                converters={"date": pd.to_datetime},
            )

    # define a comment for the delta value underneath the metrics
    st.markdown(
        """The delta value underneath the metrics, shows the current total minus the last 30 days expenses 
        compare to the 'From' day. If negative, you spent less (green); if positive you spent more (red).""",
        unsafe_allow_html=False,
    )

# If the uploaded_file is not None, then show the dashboard;
# otherwise show the hint to upload it.
if uploaded_file is not None:
    st.subheader("Select the timeframe that you want to analyze")
    # sort the data by date
    df_expenses.sort_values(by=["date"], inplace=True)

    ###############################################
    # define the columns where to insert the datepicker
    dt1, dt2, from_date, to_date, dt5, dt6, dt7 = st.columns(
        (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    )

    # define start and end date
    past_date = from_date.date_input("From", past, key="from_date")
    today_date = to_date.date_input("To", today, key="to_date")
    category_selection = st.selectbox(
        "Select the category:", df_expenses["expense_category"].unique()
    )

    ###############################################

    # Filter data between two dates, "From" and "To" date
    df_expenses_within_date_range = df_expenses.loc[
        (df_expenses["date"].dt.date >= past_date)
        & (df_expenses["date"].dt.date < today_date)
    ]

    # set the index using the expense_category column
    df_expenses_filtered_for_category = df_expenses_within_date_range.set_index(
        "expense_category"
    )
    # group by expenses and sum the value for each category
    df_expenses_filtered_year_grouped = df_expenses_within_date_range.groupby(
        "expense_category",
    )[["value"]].sum()

    # instantiate the bar chart with the expense categories
    fig_bar_chart = px.bar(
        df_expenses_within_date_range.groupby("expense_category")["value"]
        .sum()
        .reset_index(),
        x="expense_category",
        y="value",
        color="expense_category",
        # title="Expenses per category",
    )
    fig_bar_chart.update_layout(
        barmode="stack", xaxis={"categoryorder": "total descending"}
    )
    # Update layout (optional)
    fig_bar_chart.update_layout(
        title="Expenses per category",
        xaxis_title="Category",
        yaxis_title="Expenses",
    )

    # get the list of unique element in the index
    x_coords = list(set(df_expenses_filtered_year_grouped.index))

    # Create a DataFrame with the desired order of the categories
    category_order_df = pd.DataFrame(index=x_coords)

    fig_bar_chart.add_trace(
        go.Scatter(
            x=x_coords,
            # use the previous df to sort the categories as the reordered one
            y=df_expenses_filtered_year_grouped["value"].reindex(
                category_order_df.index
            ),
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

    # instantiate the pie plot with the stores
    fig_pie_plot = px.pie(
        df_expenses_within_date_range,
        values="value",
        names="store",
        title="Expenses per store",
        hole=0.7,
    )
    # Update the pie plot to insert the label inside the slice
    # and to hide those labels that are too small to be read
    fig_pie_plot.update_traces(textposition="inside")
    fig_pie_plot.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")

    # ###################################################
    # --- Metrics --- #

    # --- Create columns to position the metrics --- #
    (
        metric1_total_amount_spent,
        metric2_total_amount_spent_category,
        metric3,
        metric4,
    ) = st.columns(4)

    metric1_total_amount_spent = metric_total_amount_spent(
        df_expenses, today_date, past_date
    )
    metric2_total_amount_spent_category = metric_total_amount_spent_category(
        df_expenses, category_selection, today_date, past_date
    )

    # # Apply the metric_computation function to create the expenses
    # metric1, metric2, metric3, metric4 = metric_computation(
    #     df_expenses,
    #     today_date,
    #     past_date,
    # )

    # ###################################################
    # --- Create columns to position the plots --- #
    # plots
    plot1, plot2, plot3 = st.columns((200, 1, 200))
    # plot the bar category bar chart
    plot1.plotly_chart(
        fig_bar_chart,
        use_container_width=True,
    )
    # plot the store pie plot
    plot3.plotly_chart(
        fig_pie_plot,
        use_container_width=True,
    )

    # separator
    st.divider()

    ########################################################
    # --- Create columns to position the selection box --- #
    (
        selectionbox_barplot1,
        selectionbox_barplot2,
        selectionbox_barplot3,
        selectionbox_barplot4,
    ) = st.columns((0.5, 1, 1, 1))

    # select the year to filter out
    choose_year = selectionbox_barplot1.selectbox(
        "Choose the year",
        df_expenses["year"].unique(),
    )

    ########################################################

    #  Filter data for year
    df_expenses_filtered_year = df_expenses.loc[
        (df_expenses["year"] == int(choose_year))
    ]
    # filter the df out using the "choose_year" filter for the year
    df_expenses_subdf_by_month_per_year = df_expenses[
        df_expenses["year"] == choose_year
    ]
    # get only the month and the values
    df_expenses_subdf_by_month = df_expenses_subdf_by_month_per_year[["month", "value"]]
    # take the average daily expenses per month
    monthly_sum_values = df_expenses_subdf_by_month.groupby(["month"]).sum()

    # get statistics per months, using a bar plot
    fig_bar_chart_months = px.bar(
        df_expenses_filtered_year.groupby(["expense_category", "month"])["value"]
        .sum()
        .reset_index(),
        x="month",
        y="value",
        color="expense_category",
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
    # Update layout
    fig_bar_chart_months.update_layout(
        title="Expenses per Month", xaxis_title="Months", yaxis_title="Expenses"
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
        df_expenses_filtered_year[
            df_expenses_filtered_year["expense_category"] == "food"
        ]
        .groupby(["store"])
        .size()
        .reset_index(name="count")
        .sort_values(by="count")
    )
    grouped_counts = grouped_counts[grouped_counts["count"] > 7]

    # Merge the filtered dataframe with the original one on the "store" column
    # therefore you will get only those stores that appear in the data more than
    # 7 times.
    df_expenses_size_filtering_year = df_expenses_filtered_year.merge(
        grouped_counts[["store"]],
        on=["store"],
        how="inner",
    )

    # --- CSS hacks --- #
    with open(r"C:\solutions\learning_python\expense_tracker\src\pkgs\style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# TODO
# Add the following information: most expensive category, and you want to try to reduce the amount
# spent, for instance on food. Therefore you set a limit of 5/10% of saving on food each month.
# You also need another metric that tells you: how much you spent on food compare to the previous
# month (literally, taken from the month before), how much you saved so far (for instance, after
# a few months later) and how far you are in reaching your goal (if the goal is reaching 500€ per year
# saved, then you can show how much you already saved and how much you still need to reach the goal)!
# You should also record this data, but you have to think how.

# TODO:
# Create the database to stop using the csv file. In the future, record the data directly in
# the DB. In order to do that, you should have another page connected to your db in streamlit that
# gives you the possibility to record the expenses and directly see the results of your new data directly
# in the plots.

# TODO:
# Try to move the plots in two different files and then called them as packages in this
# main one.

# TODO:
# add the Expenses per category in % with, maybe, a radar plot (?)

# TODO:
# add a filter for all the plot to select one category and to show the expenses for that category,
# for instance "food"

# TODO:
# move the explanation about the delta in a specific repo on github with the expense tracker code

# TODO:
# Add an example of the dataset to be downloaded with 5 rows right below the upload file
# instead of the delta explanation

else:
    st.text(
        "To start the dashboard please, upload a file using the button on the sidebar."
    )
