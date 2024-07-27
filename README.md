# Expense Tracker

### Introduction

# **ADD: LINK TO THE STREAMLIT WEBPAGE**

### What is an Expense Tracker? 📊

An Expense Tracker is a tool designed to help users manage and monitor their expenses.
It typically allows users to input their expenses, categorize them, track spending patterns, and generate reports to gain insights into their financial habits.

As a starting point, this project does not contain all the functionalities that a full-fledged Expense Tracker usually has, but it includes a handful of features that can help users get a closer look at where their money goes.

### Why is this useful? 🤔

The entire idea behind using an Expense Tracker is to track in which area you are spending more and to actively decide to reduce the amount spent, in order to be able to save more.
It has been built on the so-called [**FIRE Movement**](https://en.wikipedia.org/wiki/FIRE_movement)🔥 ideology, which is to [_maximize the savings rate by growing the gap between the living expenses and the income, and investing the difference_](https://en.wikipedia.org/wiki/FIRE_movement).

### What does this application do? 💡

Simply put, it provides insight into your financial expenses. Python and Streamlit seemed like the best choices due to their ease of UI implementation.

This tool can immediately answer the following questions:

- How much did you spend in a certain timeframe?
- How much did you spend in a certain timeframe, and in which category?
- How much did you spend in a certain timeframe compared to the last 30 days?
- How much did you spend monthly?
- Comparing two months, in which month did you spend less/more, and on what?
- Based on your monthly income, how much money is left after all the expenses?

### How to use it?

The current application supports a _.csv_, _.xlsx_ filetype (**to be tested!**).
The structure of the file should contain the following columns:

- date
- expense_category
- expense_type
- value
- month
- year
- weekday_number
- weekday_text
- months_text
- store
- city

The columns `month`, `year`, `weekday_number`, `weekday_text`, `months_text` are automatically available by using the sampled data, because the formula needed for those columns are already in place in the Excel itself.

A standard Excel file looks like the following table: (excluding the date columns)
| date | expense_category | expense_type | value | store | city |
| ---------- | ---------------- | ------------ | ------- | ----------- | -------- |
| 01/06/2024 | restaurant | hamburger | 1,70 | McDonald's | New York |

In addition, after firing up the application a `Download sample data as CSV` button is available that helps you understand the needed structure for the application. You can also use it as a template to insert your own data.
**TODO: edit the sample data in order to have all the available columns**.

The datatype of each column is given below:
| date | date |
|------------------|--------|
| expense_category | string |
| expense_type | string |
| value | number |
| store | string |
| city | string |

**To test which columns are not mandatory**

#### Special values for the **expense_category** column

The values for the `income`, `savings` and `investment` are special elements that must be called in this fashion for the Expense Tracker to be able to recognize them and display the metrics in the Web Application.
**TODO: are we using the savings/investments for the current version? If not, delete them from here and check the application!**

#### Category suggestions

In the column `expense_category`, you are free to choose the category names as you like (except for the `income`, `savings` and `investment`, as already pointed out).
Here, there are our suggestions (but feel free to create your own):

- apparel (for anything related to clothes)
- education & learning (for anything related to learning materials such as books, courses, online courses and so on)
- entertainment & leisure (anything related to leisure time, such as going to the movie theather, going to the bowling alley, going to the restaurant and so on)
- food (food related, such as grocery shopping)
- home & living (such as the rent, the electricity bill and so on)
- household & personal care (such as detergents for the washing machine, shampoo, toothpaste and so on)
- restaurant (anything related to a breakfast/lunch/dinner or anything else at a restaurant place, such as getting an espresso, it can considered a _restaurant_ expense as well)
- income (the amount of income, per month)
- others (for anything else that does not fit into the previous categories)

## TO BE ADDED:

- show an example
- what about the **income**, **savings**, **investment** categories? For the income, it really should be called **income**, otherwise it will not be considered for the waterfall diagram and the metric!

### Discover the application 📚

You start the application by simply load the file that contains your data. In the sidebar, you can click on the _Download a sample_ to get an idea of what the file should look like. The only boundary condition, is that the data can be found in the main sheet (for instance, using _Excel_ just one sheet with all the data).

The **delta** value underneath the metrics, shows the current total minus the last 30 days expenses. If negative, you spent less (green), while if positive you spent more (red).

Four tabs are available:

- Overall Overview
- Monthly Overview
- Monthly Comparison
- Monthly Breakdown

#### 📈 Overall Overview

In the overall overview, you can see the _expenses per category_ and _expenses per store_ based on a certain timeframe.

By selecting a specific category, you can see how much you've spent in the selected timeframe and the difference compared to the previous 30 days.

#### 👓 Monthly Overview

In the monthly overview tab, you have an _eagle-eye_ view of your expenses by month. Select the year, and you will automatically see the expenses for each month.

#### 👨🏼‍🤝‍👨🏼 Monthly Comparison

In the monthly comparison, select the year and month for both the left and right plots. Take a look at your expenses for two specific months.

#### 🧾 Monthly Breakdown

The monthly breakdown provides a comprehensive view of your income and spending for a specific month. You can see where you spent most of your earnings and how much is left in the selected timeframe.

### Tech Stack

In this project I've used:

- **Python** 🐍
- **Streamlit**: A popular open-source framework for building data-driven web applications quickly and easily using Python.
  The reason behind the usage of Streamlit relies on my wish to learn more about this Python package and how far you can get by using it.

### Future Development

Here's a refined version of your text:

The current release lacks many features that a full-fledged Expense Tracker could have. It is also a **completely free version** that you can use whenever you want. It has been built during free time, therefore it contains the basic capabilities to be functional.

### Feedbacks

Feedbacks can come in many forms:

- if you want to **contribute**, please do not hesitate to open a pull request
- if you enjoyed using this **Expense Tracker**, leave a star on the Github page
- if you feel very generous, click on the _buy me a coffee_ button to show your support 😉. As a coffee lover, any _Espresso_ that I can get, it's always appreciated 😄☕☕☕

---
