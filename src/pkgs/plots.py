# use streamlit
import datetime
import pandas as pd
import streamlit as st
from io import BytesIO
from pkgs.global_vars import today, past
import plotly.express as px
import plotly.graph_objects as go


def monthly_report_plot(df: pd.DataFrame, year: str, month: str, side: str) -> None:
    """
    ------------------------------
    --- Monthly Comparison Tab ---
    ------------------------------
    Monthly report horizontal bar chart available in the Monthly Comparison tab.

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
    df_monthly_report_choose_year = df[df["year"] == year]

    # filter the df based on the selection of the user
    df_monthly_report_choose_month = df_monthly_report_choose_year[
        df_monthly_report_choose_year["month"] == month
    ]

    # create the horizontal bar plot
    fig_bar_chart_monthly_report_plot = px.bar(
        df_monthly_report_choose_month.groupby("expense_category")["value"]
        .sum()
        .reset_index(),
        y="expense_category",
        x="value",
        color="expense_category",
        orientation="h",  # horizontal side. Remember to flip the x and the y axis
    )

    # define the descending order of the barplots
    fig_bar_chart_monthly_report_plot.update_layout(
        barmode="stack", yaxis={"categoryorder": "total ascending"}
    )
    # Update layout (optional)
    fig_bar_chart_monthly_report_plot.update_layout(
        title="Expenses per category",
        xaxis_title="Total amount spent",
        yaxis_title="Month",
    )

    # plot
    plot1 = st.plotly_chart(
        fig_bar_chart_monthly_report_plot,
        use_container_width=True,
    )

    return plot1


def plot_bar_chart_category_total(
    df: pd.DataFrame, today_date: str, past_date: str
) -> None:
    """
    Bar chart to show all the categories available in a specific
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


def plot_bar_chart_expenses_per_month(df: pd.DataFrame, year: str, side: str) -> None:
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
    plot3 = side.plotly_chart(
        fig_bar_chart_months,
        use_container_width=True,
        sharing="streamlit",
        theme="streamlit",
    )

    return plot3
