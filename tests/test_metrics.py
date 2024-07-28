"""
Script to test the metrics_dataclasses.py class and methods.
"""

import unittest
import pandas as pd
from faker import Faker  # to create dummy/fake data

# if no standard provider from Faker is sufficient, you create your own
from faker.providers import DynamicProvider
from datetime import datetime
from src.pkgs.metrics_dataclasses import ExpenseMetric


# create subclass that imports the unittest.TestCase class to derive its methods (inheritance)
class TestMetric(unittest.TestCase):
    """
    Each methods in this class MUST be called starting with "test_*" so the script will know
    which methods represents a test. Other methods that are not called by starting with "test_*", will not be considered.
    The TestCase class provides several assert methods to check for and report failures.
    Check the following out for seeing which assert methods are available in the TestCase
    class:
        - https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug


    Methods
    -------

    test_filter_data()
        Test the filter_data function available in the metrics_dataclasses.py file.




    Reference
    ---------
    Testing methodology concerns:
        - arrange:
            - everything that is needed for the test, like creating any necessary data or special settings, preparing an in-memory database, or mocking API calls;
        - act:
            - on the function or method to be tested by calling it;
        - assert:
            - the expected outcome.
    """

    def test_filter_data(self):
        """Assert if the two dataframes are the same using the arrange/act/assert testing methodology.

        Reference
        ---------

        - https://dev.to/emotta/pandas-code-testing-101-a-beginners-guide-for-python-developers-449m

        """

        # 1.ARRANGE
        # Sample DataFrame for testing and convert it to df
        df = pd.DataFrame(
            {"date": pd.date_range(start="2024-01-01", freq="D", periods=90)}
        ).reset_index(drop=True)

        # 2.ACT
        past_date = datetime.strptime("2024-02-01", "%Y-%m-%d").date()
        today_date = datetime.strptime("2024-03-01", "%Y-%m-%d").date()
        # create an instance of the ExpenseMetric class to call the .filter_data() on it:
        # without, you get an error because the script will search for a "df" that is not
        # available in the TestMetric, but it is available in the ExpenseMetric.
        # The filter_data method is properly executed on an instance of ExpenseMetric,
        # which includes the df attribute, resolving the AttributeError.
        result_df = ExpenseMetric(df=df, past_date=past_date, today_date=today_date)
        result_df = result_df.filter_data(df, past_date, today_date)

        # 3.ASSERT
        expected_df = pd.DataFrame(
            {"date": pd.date_range(start="2024-02-01", end="2024-03-01", freq="D")}
        ).reset_index(drop=True)

        return pd.testing.assert_frame_equal(result_df, expected_df)

    def test_calculate_total_expenses(self):
        """
        Assert if the calculate_total_expenses() methods yield the expected results
        based on a dataframe that does not contain "income", "investments", "savings"
        using the arrange/act/assert testing methodology.

        """
        # define the expense_category as a custom provider
        # (a custom way of creating custom fake elements based on a built-in faker class)
        expense_category_types = DynamicProvider(
            provider_name="expense_category",
            elements=["income", "investment", "savings", "food", "gas", "entertainment"],
        )

        # instantiate Faker and use a seed to have fixed elements
        fake = Faker()
        Faker.seed(0)
        # then add new provider to faker instance
        fake.add_provider(expense_category_types)
        fake_expense_category_list = list()
        fake_value_list = list()

        # create two lists, one for expense_category and the other to create the values
        for idx in range(0, 10):
            fake_expense_category_list.append(fake.expense_category())

        for idx in range(0, 10):
            fake_value_list.append(fake.pyint())

        # 1.ARRANGE
        # create a fake pandas dataframe based on the fake_dict
        fake_dict = {"expense_category": fake_expense_category_list, "value": fake_value_list}
        fake_df = pd.DataFrame(fake_dict)

        # 2.ACT
        # Apply the function to test it
        result_df = ExpenseMetric(df=fake_df)
        result_value = result_df.calculate_total_expenses(
            result_df.df
        )  # the .df is to get the df in the ExpenseMetric class object

        # 3.ASSERT: the expected result is the dataframe stripped of the "income", "investment", "savings"
        expected_value = fake_df[
            ~fake_df["expense_category"].isin(["income", "investment", "savings"])
        ]["value"].sum()
        return self.assertTrue(result_value == expected_value)

    def test_calculate_total_expenses_per_category(self):
        """
        Assert if the calculate_total_expenses_per_category() methods yield the expected results
        based on a dataframe that contains only the category chosen
        using the arrange/act/assert testing methodology.

        """
        # define the expense_category as a custom provider
        # (a custom way of creating custom fake elements based on a built-in faker class)
        expense_category_types = DynamicProvider(
            provider_name="expense_category",
            elements=["food", "gas", "entertainment"],
        )

        # instantiate Faker and use a seed to have fixed elements
        fake = Faker()
        Faker.seed(0)
        # then add new provider to faker instance
        fake.add_provider(expense_category_types)
        fake_expense_category_list = list()
        fake_value_list = list()

        # create two lists, one for expense_category and the other to create the values
        for idx in range(0, 5):
            fake_expense_category_list.append(fake.expense_category())

        for idx in range(0, 5):
            fake_value_list.append(fake.pyint())

        # 1.ARRANGE
        # create a fake pandas dataframe based on the fake_dict
        fake_dict = {"expense_category": fake_expense_category_list, "value": fake_value_list}
        fake_df = pd.DataFrame(fake_dict)

        category = "entertainment"
        # 2.ACT
        # Apply the function to test it
        result_df = ExpenseMetric(df=fake_df)
        result_df = result_df.calculate_total_expenses_per_category(result_df.df, category)

        # 3.ASSERT: the expected result is the dataframe stripped of the "income", "investment", "savings"
        expected_value = (
            fake_df[fake_df["expense_category"] == category]
            .groupby(["expense_category"])["value"]
            .sum(),
            2,
        )[0][0]
        return self.assertTrue(result_df == expected_value)

    def test_calculate_total_income(self):
        """
        Assert if the calculate_total_income() methods yield the expected results
        based on a dataframe that contains only the "income"
        using the arrange/act/assert testing methodology.

        """
        # define the expense_category as a custom provider
        # (a custom way of creating custom fake elements based on a built-in faker class)
        expense_category_types = DynamicProvider(
            provider_name="expense_category",
            elements=["food", "gas", "entertainment", "income", "income"],
        )

        # instantiate Faker and use a seed to have fixed elements
        fake = Faker()
        Faker.seed(0)
        # then add new provider to faker instance
        fake.add_provider(expense_category_types)
        fake_expense_category_list = list()
        fake_value_list = list()

        # create two lists, one for expense_category and the other to create the values
        for idx in range(0, 5):
            fake_expense_category_list.append(fake.expense_category())

        for idx in range(0, 5):
            fake_value_list.append(fake.pyint())

        # 1.ARRANGE
        # create a fake pandas dataframe based on the fake_dict
        fake_dict = {"expense_category": fake_expense_category_list, "value": fake_value_list}
        fake_df = pd.DataFrame(fake_dict)

        # 2.ACT
        # Apply the function to test it
        result_df = ExpenseMetric(df=fake_df)
        result_df = result_df.calculate_total_income(result_df.df)

        # 3.ASSERT: the expected result is the dataframe stripped of the "income", "investment", "savings"
        expected_value = (
            fake_df.loc[fake_df["expense_category"] == "income"]["value"].sum(),
            2,
        )[0]
        return self.assertTrue(result_df == expected_value)

    def test_total_expenses_timeframe(self):
        """
        Assert if the total_expenses_timeframe() methods yield the expected results
        based on a dataframe filtered by the year and month using the arrange/act/assert testing methodology.

        """
        # 1.ARRANGE
        # Sample DataFrame for testing and convert it to df
        df = pd.DataFrame(
            {"date": pd.date_range(start="2024-01-01", freq="D", periods=90)}
        ).reset_index(drop=True)
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month

        expense_category_types = DynamicProvider(
            provider_name="expense_category",
            elements=["food", "gas", "entertainment", "income", "savings", "investments"],
        )

        # instantiate Faker and use a seed to have fixed elements
        fake = Faker()
        Faker.seed(0)
        # then add new provider to faker instance
        fake.add_provider(expense_category_types)
        fake_expense_category_list = list()
        fake_value_list = list()

        # create two lists, one for expense_category and the other to create the values
        for idx in range(0, 90):
            fake_expense_category_list.append(fake.expense_category())

        for idx in range(0, 90):
            fake_value_list.append(fake.pyint())

        # create a fake pandas dataframe based on the fake_dict
        fake_dict = {"expense_category": fake_expense_category_list, "value": fake_value_list}
        fake_df = pd.DataFrame(fake_dict)
        df_concat = pd.concat([df, fake_df], axis=1)

        # 2.ACT
        year = datetime.strptime("2024", "%Y").year
        month = datetime.strptime("03", "%m").month

        result_df = ExpenseMetric(df=df_concat)
        result_value = result_df.total_expenses_timeframe(df=result_df.df, year=year, month=month)

        # 3.ASSERT: the expected result is the dataframe stripped of the "income", "investment", "savings"
        expected_df = df_concat.loc[(df_concat["year"] == year) & (df_concat["month"] == month)]
        expected_value = expected_df[
            ~expected_df["expense_category"].isin(["income", "investment", "savings"])
        ]["value"].sum()

        return self.assertTrue(result_value == expected_value)
