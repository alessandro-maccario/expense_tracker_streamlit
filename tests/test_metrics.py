"""
Script to test the metrics_dataclasses.py class and methods.
"""

import unittest
import pandas as pd
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


# To run the test from the CLI:
# python -m unittest tests.test_metrics
