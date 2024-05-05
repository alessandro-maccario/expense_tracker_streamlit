# --- Import packages --- #
import datetime
import streamlit as st

# --- Create columns to position the metrics --- #
(metric1_total_amount_spent, metric2_total_amount_spent_category, metric3, metric4) = (
    st.columns(4)
)


def metric_total_amount_spent(df, today_date, past_date):
    """
    Function to calculate the total amount spent in a specific timeframe.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe
    today_date : str
        "To" date. Most recent date until which you want to filter.
    past_date : str
        "From" date. Past date from which you want to start filtering.

    Returns
    -------
    None
        Return the metrics computed for the metric to be displayed.
    """

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date < today_date)
    ]

    # calculate total amount spent in the current timeframe selected
    current_total_expenses = round(df_expenses_filtered["value"].sum(), 2)

    ##################################################
    # --- Create columns to position the metrics --- #
    # metric1_total_amount_spent = st.columns((1))

    # from the past date (start date), go back another month
    previous_30_days = past_date - datetime.timedelta(days=30)

    # Filter data between the past date and 30 days earlier.
    # Useful to get the DELTA underneath the amount spent during the current timeframe
    df_previous_30_days = df.loc[
        (df["date"].dt.date >= previous_30_days) & (df["date"].dt.date < past_date)
    ]

    total_expenses_previous_30_days = round(df_previous_30_days["value"].sum(), 2)

    # take the difference between the current timeframe and the previous 30 days, then show the value
    # as a metric
    diff_total_expenses = round(
        current_total_expenses - total_expenses_previous_30_days, 2
    )

    # --- Metric that shows the total amount spent in the previous 30 days from past_date --- #
    metric1_total_amount_spent.metric(
        label="Expenses in the timeframe",
        value=current_total_expenses,
        delta=diff_total_expenses,
        delta_color="inverse",
    )

    return metric_total_amount_spent


def metric_total_amount_spent_category(df, category, today_date, past_date):
    """
    Function to calculate all the metrics shown in the Streamlit app.

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

    ##################################################
    # --- Create columns to position the metrics --- #
    # metric2_total_amount_spent_category = st.columns((1))

    # Filter data between two dates for the expense_category bar plot
    df_expenses_filtered = df.loc[
        (df["date"].dt.date >= past_date) & (df["date"].dt.date < today_date)
    ]

    # calculate total amount ONLY for the category selected (for the selected timeframe)
    # try-except: if no expenses for the selected category has been found for the selected timeframe
    # then show 0 as value for both the total_expenses_category and total_expenses_previous_30_days_category
    try:
        total_expenses_category = round(
            df_expenses_filtered[df_expenses_filtered["expense_category"] == category]
            .groupby(["expense_category"])["value"]
            .sum(),
            2,
        )[0]
    except IndexError:
        total_expenses_category = 0

    # from the past date (start date), go back another month
    previous_30_days = past_date - datetime.timedelta(days=30)

    # Filter data between the past date and 30 days earlier.
    # Useful to get the DELTA underneath the amount spent during the current timeframe
    df_previous_30_days = df.loc[
        (df["date"].dt.date >= previous_30_days) & (df["date"].dt.date < past_date)
    ]

    # calculate total amount ONLY for food (for the 30 days before the "From" date)
    # try-except: if no expenses for the selected category has been found for the selected timeframe
    # then show 0 as value for both the total_expenses_category and total_expenses_previous_30_days_category
    try:
        total_expenses_previous_30_days_category = round(
            df_previous_30_days[df_previous_30_days["expense_category"] == category]
            .groupby(["expense_category"])["value"]
            .sum(),
            2,
        )[0]
    except IndexError:
        total_expenses_previous_30_days_category = 0

    # take the difference between the current timeframe and the previous 30 days, then show the value
    # as a metric ONLY for the chosen category
    diff_total_expenses_category = round(
        total_expenses_category - total_expenses_previous_30_days_category, 2
    )

    # --- Metric that shows the total amount spent in the previous 30 days from past_date --- #
    metric2_total_amount_spent_category.metric(
        label=f"Expenses for {category}",
        value=total_expenses_category,
        delta=diff_total_expenses_category,
        delta_color="inverse",
    )

    return metric2_total_amount_spent_category
