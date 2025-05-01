import streamlit as st
import requests
import mysql.connector
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import traceback
import plotly.express as px
import plotly.graph_objects as go

# Local module imports
from sql_generator import query_ollama, conn, cursor
from fraud_detector import query
from plotting import df, generate_code

# Streamlit UI
st.title("Auto Insurance Fraud Detection")
st.write("Check claim status, visualize data, or generate SQL query results.")

# Input for user query
user_query = st.text_input("Enter your question:", placeholder="e.g. Compare the average claim amounts between fraud and non-fraud cases")

# Task selection
task_option = st.radio("Choose a task:", ("Prediction", "Plotting", "SQL Query"))

run_button = st.button("Run Query")

if run_button:
    if user_query:
        # For Prediction
        if task_option == "Prediction":
            pass
        # For Plotting
        elif task_option == "Plotting":
            with st.spinner("Thinking..."):
                try:
                    # Generate and execute plotting code
                    code = generate_code(user_query, df.columns)
                    st.subheader(f'Here is the result for "{user_query}"')
                    plt.clf()
                    local_vars = {"df": df.copy()}
                    exec(code, {"pd": pd, "sns": sns, "plt": plt}, local_vars)
                    st.pyplot(plt.gcf())
                    plt.clf()
                except Exception:
                    st.error("An error occurred while running the generated code:")
                    st.text(traceback.format_exc())
        # For SQL Query
        elif task_option == "SQL Query":
            with st.spinner("Thinking..."):
                try:
                    # Generate and execute SQL query
                    sql_query = query_ollama(user_query)
                    if "insurance_claims" not in sql_query.lower():
                        raise ValueError("Generated query does not target the `insurance_claims` table.")
                    st.subheader(f'Here is the result for "{user_query}"')
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    result_df = pd.DataFrame(rows, columns=columns)
                    st.write("Query Results")
                    st.dataframe(result_df)
                except Exception as e:
                    st.error("Error occurred during SQL execution:")
                    st.text(traceback.format_exc())
    else:
        st.warning("Please enter a question before running the query.")
