"""
    Expense tracker: get information about your monthly expenses, in detail.
    This is the first step to start implementing your personal 
    budget management strategy.
"""

# use streamlit
import datetime
import pandas as pd
import streamlit as st
from io import BytesIO
from pkgs.global_vars import today, past
import plotly.express as px
import plotly.graph_objects as go


# --- Metric functions --- #


def monthly_report_metric_total_amount_spent(
    df: pd.DataFrame, year: str, month: str
) -> None:
    """
    Function to calculate the total amount spent in a specific timeframe.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe
    year : str
        The user selects a year with which the dataframe is filtered.
    past_date : str
        The user selects a month with which the dataframe is filtered.

    Returns
    -------
    current_total_expenses: float
        Actual total value of the expenses for the month selected
    None
        Return the metrics computed for the metric to be displayed.
    """

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[(df["year"] == year) & (df["month"] == month)]

    # calculate total amount spent in the current timeframe selected
    current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)

    # --- Metric that shows the total amount spent in the previous 30 days from past_date --- #
    monthly_report_metric1 = monthly_report_metric_left_side.metric(
        label="Monthly Report - Total",
        value=current_total_expenses,
    )

    return current_total_expenses, monthly_report_metric1


def monthly_report_right_metric_total_amount_spent(
    df: pd.DataFrame, year: str, month: str
) -> None:
    """
    Function to calculate the total amount spent in a specific timeframe.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe
    year : str
        The user selects a year with which the dataframe is filtered.
    past_date : str
        The user selects a month with which the dataframe is filtered.

    Returns
    -------
    current_total_expenses: float
        Actual total value of the expenses for the month selected
    None
        Return the metrics computed for the metric to be displayed.
    """

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[(df["year"] == year) & (df["month"] == month)]

    # calculate total amount spent in the current timeframe selected
    current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)

    # --- Metric that shows the total amount spent in the timeframe selected --- #
    monthly_report_metric1 = monthly_report_metric_right_side.metric(
        label="Monthly Report - Total",
        value=current_total_expenses,
    )

    return current_total_expenses, monthly_report_metric1


def monthly_report_plot(df: pd.DataFrame, year: str, month: str, side: str) -> None:
    """_summary_

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe to be sliced.
    year : str
        Year selected by the user.
    month : str
        Month selected by the user.
    side : str
        The side in which the plot should be inserted based on the container created.

    Returns
    -------
    None
        Stacked bar chart will be returned.
    """
    # filter the df based on the selection of the user
    df_monthly_report_choose_year = df_expenses[df_expenses["year"] == year]

    # filter the df based on the selection of the user
    df_monthly_report_choose_month = df_monthly_report_choose_year[
        df_monthly_report_choose_year["month"] == month
    ]

    # instantiate the bar chart with the expense categories
    fig_bar_chart_monthly_report_plot = px.histogram(
        df_monthly_report_choose_month,
        x="months_text",
        y="value",
        color="expense_category",
        barnorm="percent",
        text_auto=".2f",
    )
    # Update layout (optional)
    fig_bar_chart_monthly_report_plot.update_layout(
        title="Expenses per category",
        xaxis_title="Month",
        yaxis_title="Total amount spent - %",
    )

    # plot
    plot1 = side.plotly_chart(
        fig_bar_chart_monthly_report_plot,
        use_container_width=True,
    )

    return plot1


def metric_total_amount_spent(
    df: pd.DataFrame, today_date: str, past_date: str
) -> None:
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
    # print(max(df_expenses_filtered["date"]))

    # calculate total amount spent in the current timeframe selected
    current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)
    # print(current_total_expenses)

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


def metric_total_amount_spent_category(
    df: pd.DataFrame, category: str, today_date: str, past_date: str
) -> None:
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

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date <= today_date)
    ]

    # calculate total amount ONLY for the category selected (for the selected timeframe)
    total_expenses_category = round(
        df_expenses_filtered[df_expenses_filtered["expense_category"] == category]
        .groupby(["expense_category"])["value"]
        .sum(),
        2,
    )[0]

    # from the past date (start date), go back another month
    previous_30_days = past_date - datetime.timedelta(days=30)

    # Filter data between the past date and 30 days earlier.
    # Useful to get the DELTA underneath the amount spent during the current timeframe
    df_previous_30_days = df.loc[
        (df["date"].dt.date >= previous_30_days) & (df["date"].dt.date <= past_date)
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


def plot_bar_chart_category_total(
    df: pd.DataFrame, today_date: str, past_date: str
) -> None:
    """
    Bar chart to show all the categories availbable in a specific
    timeframe and the total amount spent for each category

    """

    # Filter data between two dates, "From" and "To" date
    df_expenses_within_date_range = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date < today_date)
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

    # plot
    plot1 = st.plotly_chart(
        fig_bar_chart,
        use_container_width=True,
    )

    return plot1


def plot_donut_chart_store_total(
    df: pd.DataFrame, today_date: str, past_date: str
) -> None:
    """
        Plot a donut chart with the percentage of expenses for each
        store in the timeframe selected.

    Parameters
    ----------
    df : pd.DataFrame
        _description_
    today_date : str
        The current date (the "To" date)
    past_date : str
        The previous date (the "From" date)
    """

    # Filter data between two dates, "From" and "To" date
    df_expenses_within_date_range = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date < today_date)
    ]

    # Donut chart
    # instantiate the donut chart with the stores
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

    # plot the pie plot for stores
    plot2 = st.plotly_chart(
        fig_pie_plot,
        use_container_width=True,
    )

    return plot2


def plot_bar_chart_expenses_per_month(df: pd.DataFrame, year: str) -> None:
    """
        Bar plot that shows the sum of the expenses for the year selected
        considering the total number of months in the plot.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe of the expeses.
    year : str
        Year that has been selected by the user.

    Returns
    -------
    None
        Return the plot to be displayed.
    """

    #  Filter data for year
    df_expenses_filtered_year = df.loc[(df["year"] == int(year))]
    # filter the df out using the "choose_year" filter for the year
    df_expenses_subdf_by_month_per_year = df[df["year"] == year]
    # get only the month and the values
    df_expenses_subdf_by_month = df_expenses_subdf_by_month_per_year[
        ["months_text", "value"]
    ]

    # take the average daily expenses per month
    monthly_sum_values = df_expenses_subdf_by_month.groupby(["months_text"]).sum()

    # get statistics per months, using a bar plot
    fig_bar_chart_months = px.bar(
        df_expenses_filtered_year.groupby(["expense_category", "months_text"])["value"]
        .sum()
        .reset_index(),
        x="months_text",
        y="value",
        color="expense_category",
    )
    # Plot the average expenses per month
    fig_bar_chart_months.add_trace(
        go.Scatter(
            x=monthly_sum_values.index,
            y=monthly_sum_values["value"],
            mode="text",
            textposition="top center",
            text=round(monthly_sum_values["value"], 2),
            textfont=dict(
                color="black",
                size=15,
            ),
            name="Sum per month",
        )
    )
    # Update layout
    fig_bar_chart_months.update_layout(
        title="Expenses per Month", xaxis_title="Months", yaxis_title="Sum of Expenses"
    )

    # reorder the months for the barplot
    fig_bar_chart_months.update_xaxes(
        categoryorder="array",
        categoryarray=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    )

    # plot the actual graph
    plot3 = st.plotly_chart(
        fig_bar_chart_months,
        use_container_width=True,
        sharing="streamlit",
        theme="streamlit",
    )

    return plot3


# REQUIRED by Streamlit for donwloading the data in the correct format:
# define a function to convert the sample data before using it into the download button.
def convert_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.to_csv(sep=";", index=False).encode("utf-8")


# --- Main code --- #

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

    # adding a download button to download sample of the data in a csv file
    data_example_df = pd.read_csv(
        r"C:\solutions\learning_python\expense_tracker\data\data_example.csv", sep=";"
    )
    # convert the dataframe to be sent to the donwload button
    data_example_encoded = convert_df(data_example_df)

    # add a download button for downloading the sample data
    st.download_button(
        label=r"Download sample data as CSV",
        data=data_example_encoded,
        file_name="sample_data.csv",
        mime="text/csv",
    )

    # Github Badge with link to your Github profile
    # Linkedin Badge with link to your Linkedin profile
    """
        [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/alessandro-maccario) 
        [![Repo](https://badgen.net/badge/icon/Linkedin?icon=linkedin&label)](https://www.linkedin.com/in/alessandro-maccario-7b173377/) 

    """
    st.markdown("<br>", unsafe_allow_html=True)

# If the uploaded_file is not None, then show the dashboard;
# otherwise show the hint to upload it.
if uploaded_file is not None:
    # sort the data by date
    df_expenses.sort_values(by=["date"], inplace=True)

    ###############################################
    # define the columns where to insert the datepicker
    dt1, dt2, from_date, to_date, category_sel, dt6, dt7 = st.columns(
        (0.1, 0.1, 0.12, 0.12, 0.15, 0.1, 0.1)
    )

    # define start and end date
    past_date = from_date.date_input("From", past, key="from_date")
    today_date = to_date.date_input("To", today, key="to_date")

    # define the categories that show some values in it (exclude those categories that are
    # empty with no value). Sort the list from higher to lower sum of expenses.
    # Get only those categories avalailable in the specific timeframe.
    df_expenses_filtered_categories = df_expenses.loc[
        (df_expenses["date"].dt.date >= past_date)
        & (df_expenses["date"].dt.date < today_date)
    ]
    categories_with_data = (
        round(
            df_expenses_filtered_categories.groupby(["expense_category"])[
                "value"
            ].sum(),
            2,
        )
    ).sort_values(ascending=False)

    # let the user select the category
    category_selection = category_sel.selectbox(
        "Select the category:", categories_with_data.index.unique()
    )

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

    # ###################################################
    # --- Plots --- #
    # Create columns to position the plots: create a container
    data_container = st.container()

    with data_container:
        plot1, plot2 = st.columns(2)
        with plot1:
            plot1 = plot_bar_chart_category_total(df_expenses, today_date, past_date)
        with plot2:
            plot2 = plot_donut_chart_store_total(df_expenses, today_date, past_date)

    # separator
    st.divider()

    ########################################################
    # --- Bar plot per year and months --- #
    # --- Create columns to position the selection box --- #
    (
        selectionbox_barplot1,
        selectionbox_barplot2,
        selectionbox_barplot3,
        selectionbox_barplot4,
    ) = st.columns((0.5, 1, 1, 1))

    # selection box for letting the user filter the year
    choose_year = selectionbox_barplot1.selectbox(
        "Choose the year",
        df_expenses["year"].unique(),
    )

    plot3 = plot_bar_chart_expenses_per_month(df_expenses, choose_year)

    # separator
    st.divider()

    #####################################
    # --- Monthly report comparison --- #
    #####################################
    # TODO:
    # Convert later on into a function!

    # Create columns to place the two plots
    # --- Create columns to position the selection box --- #

    # TODO:
    # rename these container accordingly based on the values that they contain
    # Create columns to position the plots: create a container
    monthly_report_data_container = st.container()
    monthly_report_data_container_metrics = st.container()
    monthly_report_data_container_plots = st.container()

    # TODO:
    # add the difference between the other month as the delta value
    # underneath the metric, so it's cleaner.
    with monthly_report_data_container:
        # left side and right side of the screen
        (
            monthly_report_metric_plot_left_side,
            monthly_report_metric_plot_right_side,
        ) = st.columns(2)
        with monthly_report_metric_plot_left_side:
            # selection box for letting the user filter the year
            monthly_report_choose_year = st.selectbox(
                "Monthly Report - Year",
                df_expenses["year"].unique(),
            )
            # filter the df based on the selection of the user
            df_monthly_report_choose_year = df_expenses[
                df_expenses["year"] == monthly_report_choose_year
            ]
            # selection box for letting the user filter the month
            monthly_report_choose_month = st.selectbox(
                "Monthly Report - Month",
                df_monthly_report_choose_year["month"].unique(),
            )
        with monthly_report_metric_plot_right_side:
            # selection box for letting the user filter the year
            monthly_report_choose_year_2 = st.selectbox(
                "Monthly Report - Year 2",
                df_expenses["year"].unique(),
            )
            # filter the df based on the selection of the user
            df_monthly_report_choose_year_2 = df_expenses[
                df_expenses["year"] == monthly_report_choose_year_2
            ]
            # selection box for letting the user filter the month
            monthly_report_choose_month_2 = st.selectbox(
                "Monthly Report - Month 2",
                df_monthly_report_choose_year_2["month"].unique(),
            )
        with monthly_report_data_container_metrics:
            # left side and right side of the screen
            (
                monthly_report_metric_left_side,
                monthly_report_metric_middle_side,
                monthly_report_metric_right_side,
            ) = st.columns((0.8, 0.6, 0.8))

            # display the monthly report metric1
            monthly_report_total_expenses_metric_1, monthly_report_metric1 = (
                monthly_report_metric_total_amount_spent(
                    df_expenses, monthly_report_choose_year, monthly_report_choose_month
                )
            )

            # display the monthly report metric2
            monthly_report_total_expenses_metric_2, monthly_report_metric2 = (
                monthly_report_right_metric_total_amount_spent(
                    df_expenses,
                    monthly_report_choose_year_2,
                    monthly_report_choose_month_2,
                )
            )

            # calculate the difference between the metric on the right
            # compared to the metric on the left
            diff_metric1_metric2 = round(
                monthly_report_total_expenses_metric_2
                - monthly_report_total_expenses_metric_1,
                2,
            )

            # set the metric of the difference in the center
            monthly_report_metric1 = monthly_report_metric_middle_side.metric(
                label="Monthly Report - Total Difference",
                value=diff_metric1_metric2,
            )
        with monthly_report_data_container_plots:
            # left side and right side of the screen
            (
                monthly_report_plot_left_side,
                monthly_report_plot_right_side,
            ) = st.columns(2)

            # display the plot the stacked bar chart - plot 1
            monthly_report_plot(
                df_expenses,
                monthly_report_choose_year,
                monthly_report_choose_month,
                side=monthly_report_plot_left_side,
            )

            # display the plot the stacked bar chart - plot 2
            monthly_report_plot(
                df_expenses,
                monthly_report_choose_year_2,
                monthly_report_choose_month_2,
                side=monthly_report_plot_right_side,
            )

    # --- CSS hacks --- #
    with open(r"C:\solutions\learning_python\expense_tracker\src\pkgs\style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# TODO:
# Continue with the README:
# https://github.com/alessandro-maccario/expense_tracker_streamlit/blob/main/README.md

else:
    st.text(
        "To start the dashboard, please, upload a file using the button on the sidebar."
    )
