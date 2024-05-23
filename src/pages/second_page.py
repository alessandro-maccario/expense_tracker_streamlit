# # use streamlit
# import datetime
# import pandas as pd
# import streamlit as st
# from io import BytesIO
# from pkgs.global_vars import today, past
# import plotly.express as px
# import plotly.graph_objects as go
# from st_pages import Page, show_pages, hide_pages


# def plot_bar_chart_expenses_per_month(df: pd.DataFrame, year: str) -> None:
#     """
#         Bar plot that shows the sum of the expenses for the year selected
#         considering the total number of months in the plot.

#     Parameters
#     ----------
#     df : pd.DataFrame
#         Original dataframe of the expeses.
#     year : str
#         Year that has been selected by the user.

#     Returns
#     -------
#     None
#         Return the plot to be displayed.
#     """

#     #  Filter data for year
#     df_expenses_filtered_year = df.loc[(df["year"] == int(year))]
#     # filter the df out using the "choose_year" filter for the year
#     df_expenses_subdf_by_month_per_year = df[df["year"] == year]
#     # get only the month and the values
#     df_expenses_subdf_by_month = df_expenses_subdf_by_month_per_year[
#         ["months_text", "value"]
#     ]

#     # take the average daily expenses per month
#     monthly_sum_values = df_expenses_subdf_by_month.groupby(["months_text"]).sum()

#     # get statistics per months, using a bar plot
#     fig_bar_chart_months = px.bar(
#         df_expenses_filtered_year.groupby(["expense_category", "months_text"])["value"]
#         .sum()
#         .reset_index(),
#         x="months_text",
#         y="value",
#         color="expense_category",
#     )
#     # Plot the average expenses per month
#     fig_bar_chart_months.add_trace(
#         go.Scatter(
#             x=monthly_sum_values.index,
#             y=monthly_sum_values["value"],
#             mode="text",
#             textposition="top center",
#             text=round(monthly_sum_values["value"], 2),
#             textfont=dict(
#                 color="black",
#                 size=15,
#             ),
#             name="Sum per month",
#         )
#     )
#     # Update layout
#     fig_bar_chart_months.update_layout(
#         title="Expenses per Month", xaxis_title="Months", yaxis_title="Sum of Expenses"
#     )

#     # reorder the months for the barplot
#     fig_bar_chart_months.update_xaxes(
#         categoryorder="array",
#         categoryarray=[
#             "Jan",
#             "Feb",
#             "Mar",
#             "Apr",
#             "May",
#             "Jun",
#             "Jul",
#             "Aug",
#             "Sep",
#             "Oct",
#             "Nov",
#             "Dec",
#         ],
#     )

#     # plot the actual graph
#     plot3 = st.plotly_chart(
#         fig_bar_chart_months,
#         use_container_width=True,
#         sharing="streamlit",
#         theme="streamlit",
#     )

#     return plot3


# # REQUIRED by Streamlit for downloading the data in the correct format:
# # define a function to convert the sample data before using it into the download button.
# def convert_df(df: pd.DataFrame) -> pd.DataFrame:
#     return df.to_csv(sep=";", index=False).encode("utf-8")


# # sidebar
# with st.sidebar:

#     # add sidebar title
#     st.sidebar.title("Expense Tracker")

#     # allow only .csv and .xlsx files to be uploaded
#     uploaded_file = st.file_uploader(
#         "Upload a file (.csv OR .xlsx)", type=["csv", "xlsx"]
#     )

#     # separator
#     st.divider()

#     # Check if file was uploaded
#     if uploaded_file:
#         if uploaded_file.type == "text/csv":
#             # load the expenses file
#             df_expenses = pd.read_csv(
#                 uploaded_file,
#                 converters={"date": pd.to_datetime},
#             )
#         else:
#             # load the expenses file
#             df_expenses = pd.read_excel(
#                 uploaded_file,
#                 converters={"date": pd.to_datetime},
#             )

#     # adding a download button to download sample of the data in a csv file
#     data_example_df = pd.read_csv(
#         r"C:\solutions\learning_python\expense_tracker\data\data_example.csv", sep=";"
#     )
#     # convert the dataframe to be sent to the donwload button
#     data_example_encoded = convert_df(data_example_df)

#     # add a download button for downloading the sample data
#     st.download_button(
#         label=r"Download sample data as CSV",
#         data=data_example_encoded,
#         file_name="sample_data.csv",
#         mime="text/csv",
#     )

#     # Github Badge with link to your Github profile
#     # Linkedin Badge with link to your Linkedin profile
#     """
#         [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/alessandro-maccario)
#         [![Repo](https://badgen.net/badge/icon/Linkedin?icon=linkedin&label)](https://www.linkedin.com/in/alessandro-maccario-7b173377/)

#     """
#     st.markdown("<br>", unsafe_allow_html=True)

# # If the uploaded_file is not None, then show the dashboard;
# # otherwise show the hint to upload it.
# if uploaded_file is not None:
#     # ###############################################
#     # --- Create buttons to swich between pages --- #
#     # Create columns to position the plots: create a container
#     # buttons_container = st.container()

#     # with buttons_container:
#     #     page_00, page_0, page_1, page_2, page_3, page_4, page_5 = st.columns((7))
#     #     with page_1:
#     #         if st.button("Overall Overview"):
#     #             st.switch_page("app.py")
#     #     with page_2:
#     #         if st.button("Detail Overview"):
#     #             st.switch_page("pages/second_page.py")
#     #     with page_3:
#     #         if st.button("Personal Finance"):
#     #             st.switch_page("pages/third_page.py")
#     # ###############################################

#     # sort the data by date
#     df_expenses.sort_values(by=["date"], inplace=True)

#     ###############################################

#     ########################################################
#     # --- Bar plot per year and months --- #
#     # --- Create columns to position the selection box --- #
#     (
#         selectionbox_barplot1,
#         selectionbox_barplot2,
#         selectionbox_barplot3,
#         selectionbox_barplot4,
#     ) = st.columns((0.5, 1, 1, 1))

#     # selection box for letting the user filter the year
#     choose_year = selectionbox_barplot1.selectbox(
#         "Choose the year",
#         df_expenses["year"].unique(),
#     )

#     plot3 = plot_bar_chart_expenses_per_month(df_expenses, choose_year)
