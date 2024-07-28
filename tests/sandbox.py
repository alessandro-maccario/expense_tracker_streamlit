"""Script to test different elements before applying them to the code

Error:
    ModuleNotFoundError: No module named 'src'

    - What's Happening?
        Running sandbox.py directly:

        When you run sandbox.py directly (e.g., python tests/sandbox.py), Python sets the script's directory (tests) as the current working directory.
        Python doesn't recognize src as a module because it's looking for src in the tests directory and not at the project root.

    - Running test_metric.py via a test runner:

        When you run tests using a test runner (like pytest or unittest), the test runner adjusts the Python path to include the project root.
        Thus, src is found and the import works.

"""

import pandas as pd
from faker import Faker  # to create dummy/fake data
from datetime import datetime
import sys
import os

# This line is designed to add the parent directory of the current script to the Python path.
# __file__: This is a special variable in Python that contains the path to the current script.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# if no standard provider from Faker is sufficient, you create your own
from faker.providers import DynamicProvider
from src.pkgs.metrics_dataclasses import ExpenseMetric

# expense_category_types = DynamicProvider(
#     provider_name="expense_category",
#     elements=["food", "gas", "entertainment", "income", "income"],
# )

# # instantiate Faker and use a seed to have fixed elements
# fake = Faker()
# Faker.seed(0)
# # then add new provider to faker instance
# fake.add_provider(expense_category_types)
# fake_expense_category_list = list()
# fake_value_list = list()

# # now you can use:
# for idx in range(0, 5):
#     fake_expense_category_list.append(fake.expense_category())

# for idx in range(0, 5):
#     fake_value_list.append(fake.pyint())

# # create a fake pandas dataframe based on the fake_dict
# fake_dict = {"expense_category": fake_expense_category_list, "value": fake_value_list}
# fake_df = pd.DataFrame(fake_dict)

# category = "entertainment"
# # Apply the function to test it
# result_df = ExpenseMetric(df=fake_df)
# result_df = result_df.calculate_total_income(result_df.df)
# print(result_df)
# # print(
# #     fake_df[fake_df["expense_category"] == category].groupby(["expense_category"])["value"].sum(),
# #     2,
# # )

# # 3.ASSERT: the expected result is the dataframe stripped of the "income", "investment", "savings"
# expected_value = (
#     fake_df.loc[fake_df["expense_category"] == "income"]["value"].sum(),
#     2,
# )[0]
# print(result_df == expected_value)
# return assertTrue(result_df == expected_value)
# return assertTrue(0 <= result_value <= expected_value)

# 1.ARRANGE
# Sample DataFrame for testing and convert it to df
df = pd.DataFrame({"date": pd.date_range(start="2024-01-01", freq="D", periods=90)}).reset_index(
    drop=True
)
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

# now you can use:
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
result_df = result_df.total_expenses_timeframe(df=result_df.df, year=year, month=month)

# 3.ASSERT: the expected result is the dataframe stripped of the "income", "investment", "savings"
expected_df = df_concat.loc[(df_concat["year"] == year) & (df_concat["month"] == month)]
expected_value = expected_df[
    ~expected_df["expense_category"].isin(["income", "investment", "savings"])
]["value"].sum()
