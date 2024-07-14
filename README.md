# Expense Tracker

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
  The reason behind the usage of Streamlit relies on my wish to learn more about this Python package and how far you can achieve using it.

### Future Development

The current release lacks a lot of features that a full-fledge Expense Tracker could have.
It is also a **completely free version** that you can use whenever you want, and that I built in my spare time, therefore it contains the basics capabilities but no more.

If you want to **contribute**, please do not hesitate to open a pull request and ask for features. If possible, I'll see to implement them.

---

**To be improved and finished!**

Did you enjoy using this **Expense Tracker**? Leave a Star on the Github page: it would be helpful for me to understand if this app has some traction and more time could be spent on this side-project.

If you want to _buy me a coffee_ to show your support, you can use the corresponding button in the sidebar. I'm originally from Italy, therefore any _Espresso_ that I can get, it's always appreciated 😉☕☕☕

---

KEEP READING THIS:

- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/

TO ANSWER HERE:
