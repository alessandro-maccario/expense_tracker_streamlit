"""
Script to test the metrics_dataclasses.py class and methods.
"""

import unittest
from src.pkgs.metrics_dataclasses import ExpenseMetric


# create subclass that imports the unittest.TestCase class to derive its methods (inheritance)
class TestMetric(unittest.TestCase):
    """
    Each methods in this class MUST be called starting with "test_*" so the script will know
    which methods represents a test. Other methods that are not
    called by starting with "test_*".
    The TestCase class provides several assert methods to check for and report failures.
    Check the following out for seeing which assert methods are available in the TestCase
    class:
        - https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug


    Methods
    -------

    test_filter_data()
        Test the filter_data function available in the metrics_dataclasses.py file.

    """

    def test_filter_data(self):
        pass
