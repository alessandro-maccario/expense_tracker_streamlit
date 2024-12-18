# use streamlit
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import Optional
from pkgs.metrics_dataclasses import ExpenseMetric


@dataclass
class ExpensePlot:
    df: pd.DataFrame
    past_date: str
    today_date: str

    def plot_bar_chart_category_total(
        self, df: pd.DataFrame, today_date: str, past_date: str
    ) -> None:
        df_filtered = ExpenseMetric.filter_data(self, df, past_date, today_date)

        df_expenses_within_date_range = df_filtered.loc[
            ~df_filtered["expense_category"].isin(["income", "investment", "savings"])
        ]

        # instantiate the bar chart with the expense categories
        fig_bar_chart = px.bar(
            df_expenses_within_date_range.groupby("expense_category")["value"].sum().reset_index(),
            x="expense_category",
            y="value",
            color="expense_category",
        )
        fig_bar_chart.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
        # Update layout (optional)
        fig_bar_chart.update_layout(
            title="Expenses per category",
            xaxis_title="Category",
            yaxis_title="Expenses",
        )

        # plot
        bar_chart_category_total = st.plotly_chart(
            fig_bar_chart,
            use_container_width=True,
        )

        return bar_chart_category_total

    def plot_donut_chart_store_total(
        self, df: pd.DataFrame, today_date: str, past_date: str
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
        df_filtered = ExpenseMetric.filter_data(self, df, past_date, today_date)

        df_expenses_within_date_range = df_filtered.loc[
            ~df_filtered["expense_category"].isin(["income", "investment", "savings"])
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


@dataclass
class ExpensePlotMonth:
    df: pd.DataFrame
    year: str
    month: Optional[str] = None
    side: Optional[str] = None

    def monthly_report_plot(self, df: pd.DataFrame, year: str, month: str, side: str) -> None:
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

        # filter out the income, it's not an expense
        df = df.loc[~df["expense_category"].isin(["income", "investment", "savings"])]

        # TODO:
        # You should be able to reduce this to one row by filtering both for the year and the month
        # filter the df based on the selection of the user
        df_monthly_report_choose_year = df[df["year"] == year]

        # filter the df based on the selection of the user
        df_monthly_report_choose_month = df_monthly_report_choose_year[
            df_monthly_report_choose_year["month"] == month
        ]

        # create the horizontal bar plot
        fig_bar_chart_monthly_report_plot = px.bar(
            df_monthly_report_choose_month.groupby("expense_category")["value"].sum().reset_index(),
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
            yaxis_title="Categories",
        )

        # plot
        plot1 = st.plotly_chart(
            fig_bar_chart_monthly_report_plot,
            use_container_width=True,
        )

        return plot1

    def plot_bar_chart_expenses_per_month(self, df: pd.DataFrame, year: str, side: str) -> None:
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

        # filter out the income from the plot, it's not an expense
        df = df.loc[~df["expense_category"].isin(["income", "investment", "savings"])]

        #  Filter data for year
        df_expenses_filtered_year = df.loc[(df["year"] == int(year))]
        # filter the df out using the "choose_year" filter for the year
        df_expenses_subdf_by_month_per_year = df[df["year"] == year]
        # get only the month and the values
        df_expenses_subdf_by_month = df_expenses_subdf_by_month_per_year[["months_text", "value"]]

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

    def plot_waterfall_per_month(
        self,
        df,
        year,
        month,
        title="",
        annotation=None,
        icolor="#8fcf00",
        dcolor="#ff6b7f",
        tcolor="#4c5982",
        ccolor="Dark Grey",
        color=None,
        measure=None,
    ):
        """
        Create a waterfall chart using Plotly.

        Parameters:
            labels (list):
                A list of labels for the data points.

            data (list):
                A list of numerical values representing the data points.

            title (str, optional):
                The title of the chart. Defaults to an empty string.

            annotation (list, optional):
                A list of annotations for each data point. Defaults to None.

            icolor (str, optional):
                Color for increasing values. Defaults to "Green".

            dcolor (str, optional):
                Color for decreasing values. Defaults to "Red".

            tcolor (str, optional):
                Color for the total value. Defaults to "Blue".

            ccolor (str, optional):
                Connector line color. Defaults to 'Dark Grey'.

            color (str, optional):
                Common color for all elements. Defaults to None.

            measure (list, optional):
                A list specifying whether each data point is 'relative' or 'total'. Defaults to None.

        Returns:
            plotly.graph_objs._figure.Figure: A Plotly Figure containing the waterfall chart.
        """
        # plot title
        title = "Waterfall Breakdown Monthly Expenses"

        # plot the waterfall diagram with the remaining income per month
        labels = [
            "Income",
            "Household & Personal Care",
            "Apparel",
            "Entertainment & Leisure",
            "Food",
            "Restaurant",
            "Home & Living",
            "Transportation",
            "Education & Learning",
            "Others",
            "Remaining Income",
        ]

        # filter the df based on the selection of the user
        df_monthly_report_choose_year = df[df["year"] == year]

        # filter the df based on the selection of the user
        df_monthly_report_choose_month = df_monthly_report_choose_year[
            df_monthly_report_choose_year["month"] == month
        ]

        ###########################################
        ##### Bar selection for each category #####
        # filter in only the income for the first bar
        df_income = df_monthly_report_choose_month.loc[df["expense_category"].isin(["income"])][
            "value"
        ].sum()

        # filter in only the household & personal care for the second bar
        df_household_personalCare = df_monthly_report_choose_month.loc[
            df["expense_category"].isin(["household & personal care"])
        ]["value"].sum()

        # filter in only the Apparel for the third bar
        df_apparel = df_monthly_report_choose_month.loc[df["expense_category"].isin(["Apparel"])][
            "value"
        ].sum()

        # filter in only the entertainment & leisure for the fourth bar
        df_entertainment_leisure = df_monthly_report_choose_month.loc[
            df["expense_category"].isin(["entertainment & leisure"])
        ]["value"].sum()

        # filter in only the food for the fifth bar
        df_food = df_monthly_report_choose_month.loc[df["expense_category"].isin(["food"])][
            "value"
        ].sum()

        # filter in only the restaurant for the sixth bar
        df_restaurant = df_monthly_report_choose_month.loc[
            df["expense_category"].isin(["restaurant"])
        ]["value"].sum()

        # filter in only the home & living for the seventh bar
        df_home_living = df_monthly_report_choose_month.loc[
            df["expense_category"].isin(["home & living"])
        ]["value"].sum()

        # filter in only the transportation for the eigth bar
        df_transportation = df_monthly_report_choose_month.loc[
            df["expense_category"].isin(["transportation"])
        ]["value"].sum()

        # filter in only the education & learning for the ninth bar
        df_education_learning = df_monthly_report_choose_month.loc[
            df["expense_category"].isin(["education & learning"])
        ]["value"].sum()

        # filter in only the others for the tenth bar
        df_others = df_monthly_report_choose_month.loc[df["expense_category"].isin(["others"])][
            "value"
        ].sum()

        ###########################################

        # create the data based on the dataframe and the main categories
        data = [
            df_income,
            -df_household_personalCare,
            -df_apparel,
            -df_entertainment_leisure,
            -df_food,
            -df_restaurant,
            -df_home_living,
            -df_transportation,
            -df_education_learning,
            -df_others,
            0,
        ]

        # Set default measure values if not provided
        if measure is None:
            # Docs: https://plotly.com/python/waterfall-charts/
            # Explanation: all measures are relative, except the last one that is a total meausure
            measure = ["relative"] * (len(labels) - 1)
            # Append the last measurement as total
            measure.append("total")

        # Set default annotation values if not provided
        if annotation is None:
            # do not consider the total, and slice the list of values excluding the last element
            annotation = data[:-1]
            # just append the total given by the sum of all the elements in the list
            annotation.append(round(sum(data), 2))

        # Create the waterfall chart figure
        fig = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=measure,
                textposition="outside",
                text=annotation,
                y=data,
                x=labels,
                connector={"line": {"color": ccolor}},
                decreasing={"marker": {"color": dcolor}},
                increasing={"marker": {"color": icolor}},
                totals={"marker": {"color": tcolor}},
            )
        ).update_layout(
            title=title,
            height=510,
        )

        # plot
        plot_waterfall = st.plotly_chart(
            fig,
            use_container_width=True,
        )

        return plot_waterfall
