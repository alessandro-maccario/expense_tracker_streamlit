"""
Expense tracker: get information about your monthly expenses, in detail.
This is the first step to start implementing your personal
budget management strategy.
"""

# use streamlit
import time
import numpy as np
import pandas as pd
import streamlit as st
from style.style import css
from pkgs.global_vars import today, past
from pkgs.metrics_dataclasses import ExpenseMetric
from pkgs.plots_dataclasses import ExpensePlot, ExpensePlotMonth


# REQUIRED by Streamlit for downloading the data in the correct format:
# define a function to convert the sample data before using it into the download button.
def convert_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.to_csv(sep=";", index=False).encode("utf-8")


# --- Main code --- #

# set the page default setting to wide
st.set_page_config(layout="wide", page_title="Dashboard", page_icon="🔎")

# sidebar
with st.sidebar:
    # add sidebar title
    st.sidebar.title("Expense Tracker")

    # allow only .csv and .xlsx files to be uploaded
    uploaded_file = st.file_uploader("Upload a file (.csv OR .xlsx)", type=["csv", "xlsx"])

    # Check if file was uploaded
    if uploaded_file is not None:
        # get only the extension, either csv or txt or xlsx
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "csv":
            # load the expenses file
            df_expenses = pd.read_csv(
                uploaded_file,
                dtype={
                    "value": np.float64
                },  # convert value to float, otherwise the delta does not accept integer
                sep=";",
                parse_dates=[
                    "date"
                ],  # this parse the date column. There is no datetime dtype to be set for read_csv as csv files can only contain strings, integers and floats.
                dayfirst=True,  # read the date as dd/mm/yyyy, and not as mm/dd/yyyy
            )
        else:
            # load the expenses file
            df_expenses = pd.read_excel(
                uploaded_file,
                converters={"date": pd.to_datetime},
            )

    # adding a download button to download sample of the data in a csv file
    data_example_df = pd.read_csv(
        "https://github.com/alessandro-maccario/expense_tracker_streamlit/blob/main/data/data_example.csv?raw=true",
        sep=";",
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
    st.write(
        "[Documentation page](https://github.com/alessandro-maccario/expense_tracker_streamlit)"
    )

# If the uploaded_file is not None, then show the dashboard;
# otherwise show the hint to upload it.
if uploaded_file is not None:
    # define three tabs where to insert the plots
    overall_overview_tab1, monthly_trend_tab2, monthly_comparison_tab3, monthly_breakdown_tab4 = (
        st.tabs(
            [
                "📈 Overall Overview",
                "👓 Monthly Overview",
                "👨🏼‍🤝‍👨🏼 Monthly comparison",
                "🧾 Monthly Breakdown",
            ]
        )
    )

    # if dataframe is completely empty (no data at all), then show a warning to the user
    if df_expenses.index.empty == True:
        st.warning(
            "Empty dataframe! Please, provide a dataframe with data inside it as shown in the _Download sample data as CSV_ button!",
            icon="⚠️",
        )
        with st.spinner("Hungry for data, please upload a file that contains information..."):
            time.sleep(500)

    # sort the data by date
    df_expenses.sort_values(by=["date"], inplace=True)

    # Define what has to be shown in the first tab
    with overall_overview_tab1:
        # Inside the first tab, you need to define columns, in case
        # you need to to show, for instance, two buttons on the same line
        from_selector, to_selector, select_category_dropdown = st.columns((1, 1, 1))

        with from_selector:
            past_date = from_selector.date_input("From", past, key="from_date")
        with to_selector:
            today_date = to_selector.date_input("To", today, key="to_date")
        with select_category_dropdown:
            # define the categories that show some values in it (exclude those categories that are
            # empty with no value). Sort the list from higher to lower sum of expenses.
            # Get only those categories avalailable in the specific timeframe.
            df_expenses_filtered_categories = df_expenses.loc[
                (df_expenses["date"].dt.date >= past_date)
                & (df_expenses["date"].dt.date < today_date)
            ]
            categories_with_data = (
                round(
                    df_expenses_filtered_categories.groupby(["expense_category"])["value"].sum(),
                    2,
                )
            ).sort_values(ascending=False)

            # remove the "income" value
            categories_with_data = categories_with_data[
                ~categories_with_data.index.isin(["income", "investment", "savings"])
            ]
            # let the user select the category
            category_selection = select_category_dropdown.selectbox(
                "Select the category:", categories_with_data.index.unique()
            )

        # --- Metrics --- #
        # --- Create columns to position the metrics --- #
        (
            metric1_total_amount_spent,
            metric2_total_amount_spent_category,
            metric3_income,
        ) = st.columns(3)

        with metric1_total_amount_spent:
            # instantiate the class
            metric1_total_amount_spent = ExpenseMetric(
                df_expenses,
                today_date,
                past_date,
                delta_color="inverse",
                help_text="vs. previous 30 days",
            )
            metric1_total_amount_spent.compute_metrics()
        with metric2_total_amount_spent_category:
            # instantiate the class
            metric2_total_amount_spent_category = ExpenseMetric(
                df_expenses,
                today_date,
                past_date,
                # label="Available income",
            )
            metric2_total_amount_spent_category.compute_metrics_by_category(category_selection)

        with metric3_income:
            # instantiate the class
            metric3_income = ExpenseMetric(
                df_expenses,
                today_date,
                past_date,
                # label="Available income",
            )
            metric3_income.compute_total_income()

        # ###################################################
        # --- Plots --- #
        # Create columns to position the plots: create a container
        bar_plot_expense_per_category, donut_chart_expenses_per_store = st.columns((1, 1))
        # instantiate the class
        plot_bar_chart_category = ExpensePlot(
            df_expenses,
            today_date,
            past_date,
        )

        with bar_plot_expense_per_category:
            plot1 = plot_bar_chart_category.plot_bar_chart_category_total(
                df_expenses, today_date, past_date
            )
        with donut_chart_expenses_per_store:
            plot2 = plot_bar_chart_category.plot_donut_chart_store_total(
                df_expenses, today_date, past_date
            )

    # ########################################################
    # --- Bar plot per year and months --- #

    # selection box for letting the user filter the year
    choose_year = monthly_trend_tab2.selectbox(
        "Choose the year",
        df_expenses["year"].unique(),
    )

    # instantiate the class
    plot_bar_chart_year_month = ExpensePlotMonth(df_expenses, choose_year, side=monthly_trend_tab2)

    plot3 = plot_bar_chart_year_month.plot_bar_chart_expenses_per_month(
        df_expenses, choose_year, side=monthly_trend_tab2
    )

    #####################################
    # --- Monthly report comparison --- #
    #####################################

    # Create columns to place the two plots
    with monthly_comparison_tab3:
        selector_year1, selector_month1, selector_year2, selector_month2 = st.columns((1, 1, 1, 1))

        with selector_year1:
            year_selection = selector_year1.selectbox(
                "Monthly Report - Year - Left",
                df_expenses["year"].unique(),
            )
            # filter the df based on the selection of the user
            df_monthly_report_choose_year = df_expenses[df_expenses["year"] == year_selection]
            # selection box for letting the user filter the month
            monthly_report_choose_month = selector_month1.selectbox(
                "Monthly Report - Month - Left",
                df_monthly_report_choose_year["month"].unique(),
            )
        with selector_year2:
            year_selection2 = selector_year2.selectbox(
                "Monthly Report - Year - Right",
                df_expenses["year"].unique(),
            )
            # filter the df based on the selection of the user
            df_monthly_report_choose_year1 = df_expenses[df_expenses["year"] == year_selection2]
            # selection box for letting the user filter the month
            monthly_report_choose_month1 = selector_month2.selectbox(
                "Monthly Report - Month - Right",
                df_monthly_report_choose_year1["month"].unique(),
            )

        # create the columns for the metrics
        (
            monthly_report_metric_left_side,
            monthly_report_metric_middle_side,
            monthly_report_metric_right_side,
        ) = st.columns((0.8, 0.6, 0.8))

        # instantiate the class
        total_expenses_timeframe_right_metric = ExpenseMetric(
            df_expenses,
            today_date,
            past_date,
        )
        total_expenses_timeframe_left_metric = ExpenseMetric(
            df_expenses,
            today_date,
            past_date,
        )

        # calculate total amount spent for the right side metric
        total_expenses_timeframe_right_metric = (
            total_expenses_timeframe_right_metric.total_expenses_timeframe(
                df_expenses,
                year_selection,
                monthly_report_choose_month,
            )
        )
        # calculate total amount spent for the left side metric
        total_expenses_timeframe_left_metric = (
            total_expenses_timeframe_left_metric.total_expenses_timeframe(
                df_expenses,
                year_selection2,
                monthly_report_choose_month1,
            )
        )

        # calculate difference between right side and left side
        difference_right2left = round(
            total_expenses_timeframe_right_metric - total_expenses_timeframe_left_metric,
            2,
        )
        # calculate difference between left side and right side
        difference_left2right = round(
            total_expenses_timeframe_left_metric - total_expenses_timeframe_right_metric,
            2,
        )

        # set the metric on the left side in the Monthly Comparison tab
        with monthly_report_metric_left_side:
            metric_total_expenses_class_left_metric = ExpenseMetric(
                df_expenses,
                today_date,
                past_date,
            )
            metric_total_expenses_class_left_metric.metric_total_expenses_timeframe_class(
                metric_total_expenses_class_left_metric.total_expenses_timeframe(
                    df_expenses,
                    year_selection,
                    monthly_report_choose_month,
                ),
                delta=difference_right2left,
                side=monthly_report_metric_left_side,
            )
        # set the metric on the right side in the Monthly Comparison tab
        with monthly_report_metric_right_side:
            metric_total_expenses_class_right_metric = ExpenseMetric(
                df_expenses,
                today_date,
                past_date,
            )
            metric_total_expenses_class_right_metric.metric_total_expenses_timeframe_class(
                metric_total_expenses_class_right_metric.total_expenses_timeframe(
                    df_expenses,
                    year_selection2,
                    monthly_report_choose_month1,
                ),
                delta=difference_left2right,
                side=monthly_report_metric_right_side,
            )

        # set the position of the plots
        (
            monthly_report_plot_left_side,
            monthly_report_plot_right_side,
        ) = st.columns(2)

        # instantiate the class
        plot_bar_chart_category = ExpensePlotMonth(
            df_expenses, year_selection, monthly_report_choose_month, monthly_report_plot_left_side
        )

        with monthly_report_plot_left_side:
            # set up the plots
            # display the plot the stacked bar chart - plot 1
            plot_bar_chart_category.monthly_report_plot(
                df_expenses,
                year_selection,
                monthly_report_choose_month,
                monthly_report_plot_left_side,
            )

        with monthly_report_plot_right_side:
            # display the plot the stacked bar chart - plot 2
            plot_bar_chart_category.monthly_report_plot(
                df_expenses,
                year_selection2,
                monthly_report_choose_month1,
                monthly_report_plot_right_side,
            )

    with monthly_breakdown_tab4:
        selector_year3, selector_month3 = st.columns((1, 1))
        # define year and month to be selected
        year_selection_waterfall = selector_year3.selectbox(
            "Monthly Report - Year", df_expenses["year"].unique(), key="waterfall_year"
        )
        # filter the df based on the selection of the user
        df_monthly_report_choose_year_waterfall = df_expenses[
            df_expenses["year"] == year_selection_waterfall
        ]
        # selection box for letting the user filter the month
        monthly_waterfall = selector_month3.selectbox(
            "Monthly Report - Month",
            df_monthly_report_choose_year_waterfall["month"].unique(),
            key="waterfall_month",
        )

        # instantiate the class
        plot_waterfall = ExpensePlotMonth(df_expenses, year_selection_waterfall, monthly_waterfall)

        plot_waterfall.plot_waterfall_per_month(
            df_expenses, year_selection_waterfall, monthly_waterfall
        )

    # --- CSS hacks --- #
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

else:
    st.text("To start the dashboard, please, upload a file using the button on the sidebar.")
