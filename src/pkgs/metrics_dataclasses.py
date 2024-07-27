"""
This script contains the metrics.py functionalities to convert the current development
from functional programming style to OOP.
"""

# --- Import packages --- #
import datetime
import pandas as pd
import streamlit as st
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExpenseMetric:
    """
    A class to represent and calculate expense metrics over specified timeframes.

    Attributes:
        df (pd.DataFrame): DataFrame containing expense data.
        today_date (str): The end date for the current period in 'YYYY-MM-DD' format.
        past_date (str): The start date for the comparison period in 'YYYY-MM-DD' format.
        delta (Optional[float]): The calculated change in expenses between the two periods. Default is None.
        delta_color (str): Color indicator for the delta value, usually for visualization purposes. Default is 'inverse'.
        help_text (str): Additional text to describe the metric. Default is 'vs. previous 30 days'.
        label_text (str): Label for the metric, used for display purposes. Default is 'Expenses in the timeframe'.

    Methods:
        calculate_delta():
            Calculates and updates the delta attribute based on the expense data in the DataFrame.
    """

    df: pd.DataFrame
    today_date: Optional[str] = None
    past_date: Optional[str] = None
    delta: Optional[float] = field(default=None)  # optional paramater
    delta_color: str = "inverse"  # optional paramater
    help_text: str = "vs. previous 30 days"  # optional paramater
    label_text: str = "Expenses in the timeframe"

    def filter_data(self, df: pd.DataFrame, past_date: str, today_date: str) -> pd.DataFrame:
        """
        Filters the DataFrame to include only the rows within the specified date range.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing the expense data to be filtered. Must have a 'date' column with datetime values.
        past_date : str
            The start date for the filter in 'YYYY-MM-DD' format.
        today_date : str
            The end date for the filter in 'YYYY-MM-DD' format.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing only the rows where the 'date' is between `past_date` and `today_date`, inclusive.
        """
        return self.df.loc[
            (self.df["date"].dt.date >= past_date) & (self.df["date"].dt.date <= today_date)
        ].reset_index(drop=True)

    def calculate_total_expenses(self, df: pd.DataFrame) -> float:
        """
        Calculates the total expenses from the filtered DataFrame, excluding specified categories.

        Parameters
        ----------
        df_filtered : pd.DataFrame
            The filtered DataFrame containing the expense data. Must have 'expense_category' and 'value' columns.

        Returns
        -------
        float
            The total expenses rounded to two decimal places, excluding 'income', 'investment', and 'savings' categories.
        """
        return round(
            df.loc[~df["expense_category"].isin(["income", "investment", "savings"])][
                "value"
            ].sum(),
            2,
        )

    def calculate_total_expenses_per_category(self, df: pd.DataFrame, category: str) -> float:
        """
        Calculates the total expenses for a specific category from the filtered DataFrame.

        Parameters
        ----------
        df_filtered : pd.DataFrame
            The filtered DataFrame containing the expense data. Must have 'expense_category' and 'value' columns.
        category : str
            The expense category for which to calculate the total expenses.

        Returns
        -------
        float
            The total expenses for the specified category, rounded to two decimal places.
        """
        try:
            return round(
                df[df["expense_category"] == category].groupby(["expense_category"])["value"].sum(),
                2,
            )[0]
        except IndexError:
            pass

    def calculate_total_income(self, df: pd.DataFrame) -> float:
        """
        Calculates the total income from the filtered DataFrame.

        Parameters
        ----------
        df_filtered : pd.DataFrame
            The filtered DataFrame containing the expense data. Must have 'expense_category' and 'value' columns.

        Returns
        -------
        float
            The total income calculated from the DataFrame.
        """
        try:
            return df.loc[df["expense_category"] == "income"]["value"].sum()
        except TypeError:
            pass

    def calculate_diff_expenses(self, current_total: float, previous_total: float) -> float:
        """
        Calculates the difference between current and previous total expenses.

        Parameters
        ----------
        current_total : float
            The total expenses for the current period.
        previous_total : float
            The total expenses for the previous period.

        Returns
        -------
        float
            The difference between the current and previous total expenses, rounded to two decimal places.
        """
        try:
            return round(current_total - previous_total, 2)
        except TypeError:
            pass

    def display_metric(self, label: str, current_total: float, diff_total: float) -> None:
        """
        Displays a metric using Streamlit, showing the current total and the difference from a previous total.

        Parameters
        ----------
        label : str
            The label to display for the metric.
        current_total : float
            The current total value to display.
        diff_total : float
            The difference value to display.

        Returns
        -------
        None
            This method does not return any value. It displays the metric using Streamlit.
        """
        label_value = label if self.label_text is not None else self.label_text
        delta_value = diff_total if self.delta is None else self.delta
        return st.metric(
            label=label_value,
            value=current_total,
            delta=delta_value,
            delta_color=self.delta_color,
            help=self.help_text,
        )

    def compute_metrics(self):
        """
        Computes and displays expense metrics for the current timeframe compared to the previous 30 days.

        This method filters the expense data for the current and previous timeframes,
        calculates total expenses for each period, computes the difference, and displays the metric.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It computes and displays the metrics using Streamlit.
        """
        # Filter the data based on the current timeframe selection
        df_current_filtered = self.filter_data(self.df, self.past_date, self.today_date)
        current_total_expenses = self.calculate_total_expenses(df_current_filtered)

        # calculate previous 30 days data
        # from the past date (start date), go back another month
        previous_30_days = self.past_date - datetime.timedelta(days=30)
        df_previous_filtered = self.filter_data(self.df, previous_30_days, self.past_date)
        total_expenses_previous_30_days = self.calculate_total_expenses(df_previous_filtered)

        # calculate the difference
        diff_total_expenses = self.calculate_diff_expenses(
            current_total_expenses, total_expenses_previous_30_days
        )

        # display the metric
        self.display_metric(
            current_total=current_total_expenses,
            diff_total=diff_total_expenses,
            label=self.label_text,
        )

    def compute_total_income(self):
        """
        Computes and displays the available income by calculating the difference between total income and total expenses
        for the current timeframe.

        This method filters the expense data for the current timeframe, calculates the total income and total expenses,
        computes the difference between them, and displays the result as "Available income".

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It computes and displays the available income using Streamlit.
        """
        # Filter the data based on the current timeframe selection
        df_current_filtered = self.filter_data(self.df, self.past_date, self.today_date)
        current_total_income = self.calculate_total_income(df_current_filtered)

        # compute totale expenses
        current_total_expenses = self.calculate_total_expenses(df_current_filtered)

        # calculate the difference
        diff_total_income = round(current_total_income - current_total_expenses, 2)

        # display the metric
        self.display_metric(
            label="Available income",
            current_total=diff_total_income,
            diff_total=None,
        )

    def total_expenses_timeframe(self, df: pd.DataFrame, year: str, month: str) -> float:
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
        str : str
            In which container the metric will be placed.

        Returns
        -------
        current_total_expenses: float
            Actual total value of the expenses for the month selected
        None
            Return the metrics computed for the metric to be displayed.
        """
        df_expenses_filtered = df.loc[(df["year"] == year) & (df["month"] == month)]
        df_expenses_filtered = df_expenses_filtered.loc[
            ~df_expenses_filtered["expense_category"].isin(["income", "investment", "savings"])
        ]

        # calculate total amount spent in the current timeframe selected
        current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)
        return current_total_expenses

    def compute_metrics_by_category(self, category: str) -> None:
        """
        --- Overall Overview function ---
        Function to calculate all the category metric in the Overall Overview.

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
        # filter the dataframe
        df_expenses_filtered = self.filter_data(self.df, self.past_date, self.today_date)
        # calculate total amount ONLY for the category selected (for the selected timeframe)
        total_expenses_category = self.calculate_total_expenses_per_category(
            df_expenses_filtered, category
        )

        previous_30_days = self.past_date - datetime.timedelta(days=30)
        df_previous_filtered = self.filter_data(self.df, previous_30_days, self.past_date)

        try:
            total_expenses_previous_30_days_category = self.calculate_total_expenses_per_category(
                df_previous_filtered, category
            )
        except IndexError:
            total_expenses_previous_30_days_category = 0

        # calculate the difference
        diff_total_expenses = self.calculate_diff_expenses(
            total_expenses_category, total_expenses_previous_30_days_category
        )

        # display the metric
        self.display_metric(
            current_total=total_expenses_category,
            diff_total=diff_total_expenses,
            # delta_color=self.delta_color,
            label=f"Expenses for {category}",
        )

        return

    def metric_total_expenses_timeframe_class(
        self, total_amount_spent: callable, delta: float, side: str
    ) -> None:
        """
        Function to display the metric based on the total amount spent in a specific timeframe.

        Parameters
        ----------
        total_amount_spent : Callable
            Call the function "total_expenses_timeframe" to calculate the amount spent in a specific timeframe
        delta : float
            Delta value corresponding to the difference with the adjacent metric.
        side : DeltaGenerator
            The place where the metric should be inserted (for instance, left, center, right)

        Returns
        -------
        None
            Return the metrics computed for the metric to be displayed.
        """
        return side.metric(
            value=total_amount_spent,
            delta=delta,
            label="Total amount spent",
            delta_color="inverse",
        )
