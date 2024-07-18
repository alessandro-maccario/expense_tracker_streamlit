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
    df: pd.DataFrame
    today_date: str
    past_date: str
    delta: Optional[float] = field(default=None)  # optional paramater
    delta_color: str = "inverse"  # optional paramater
    help_text: str = "vs. previous 30 days"  # optional paramater
    label_text: str = "Expenses in the timeframe"

    def filter_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        return self.df.loc[
            (self.df["date"].dt.date >= start_date) & (self.df["date"].dt.date <= end_date)
        ]

    def calculate_total_expenses(self, df_filtered: pd.DataFrame) -> float:
        return round(
            df_filtered.loc[
                ~df_filtered["expense_category"].isin(["income", "investment", "savings"])
            ]["value"].sum(),
            2,
        )

    def calculate_total_expenses_per_category(
        self, df_filtered: pd.DataFrame, category: str
    ) -> float:
        return round(
            df_filtered[df_filtered["expense_category"] == category]
            .groupby(["expense_category"])["value"]
            .sum(),
            2,
        )[0]

    def calculate_total_income(self, df_filtered: pd.DataFrame) -> float:
        return df_filtered.loc[df_filtered["expense_category"] == "income"]["value"].sum()

    def calculate_diff_expenses(self, current_total: float, previous_total: float):
        return round(current_total - previous_total, 2)

    def display_metric(self, label: str, current_total: float, diff_total: float) -> None:
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
        # Filter the data based on the current timeframe selection
        df_current_filtered = self.filter_data(self.past_date, self.today_date)
        current_total_expenses = self.calculate_total_expenses(df_current_filtered)

        # calculate previous 30 days data
        # from the past date (start date), go back another month
        previous_30_days = self.past_date - datetime.timedelta(days=30)
        df_previous_filtered = self.filter_data(previous_30_days, self.past_date)
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
        # Filter the data based on the current timeframe selection
        df_current_filtered = self.filter_data(self.past_date, self.today_date)
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

    def total_expenses_timeframe(self, year: str, month: str) -> float:
        df_expenses_filtered = self.df.loc[(self.df["year"] == year) & (self.df["month"] == month)]
        df_expenses_filtered = df_expenses_filtered.loc[
            ~df_expenses_filtered["expense_category"].isin(["income", "investment", "savings"])
        ]

        # calculate total amount spent in the current timeframe selected
        current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)
        return current_total_expenses

    # TODO:
    # CONTINUE FROM HERE
    # The class gives an odd results. Check again with the same filters directly into the Excel
    def compute_metrics_by_category(self, category: str) -> None:
        # filter the dataframe
        df_expenses_filtered = self.filter_data(self.past_date, self.today_date)
        # calculate total amount ONLY for the category selected (for the selected timeframe)
        total_expenses_category = self.calculate_total_expenses_per_category(
            df_expenses_filtered, category
        )

        previous_30_days = self.past_date - datetime.timedelta(days=30)
        df_previous_filtered = self.filter_data(previous_30_days, self.past_date)

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
