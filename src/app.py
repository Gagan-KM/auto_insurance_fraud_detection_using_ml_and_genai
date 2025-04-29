import streamlit as st
import requests
import mysql.connector
import pandas as pd
import json
from sql_generator import query_ollama, conn, cursor
from fraud_detector import query
from plotting import question, generate_code

# Streamlit UI
st.title("Auto Insurance Fraud Detection")

st.write("Check claim status or get fraud prediction.")
# Input for user query
user_query = st.text_input("Enter your question:", placeholder="e.g. Compare the average claim amounts between fraud and non-fraud cases")

task_option = st.radio("Choose a task:", ("Prediction", "Plotting"))

# Classify and process the query
if user_query:
    if task_option == "Prediction":
        # Fraud prediction or claim status
        with st.spinner("Processing fraud detection or claim status..."):
            response = query(user_query)
            st.write("Result:")
            st.write(response)
    elif task_option == "Plotting":
        if question:
            try:
                st.write("Generating Python code using LLM...")
                code = generate_code(question, df.columns)
                st.code(code, language="python")

                # Execute the generated code safely (in a restricted namespace)
                local_vars = {"df": df.copy()}
                exec(code, {"pd": pd, "sns": __import__("seaborn"), "plt": __import__("matplotlib.pyplot")}, local_vars)
            except Exception as e:
                st.error("Error in running generated code:")
                st.text(traceback.format_exc())
    else:
        # SQL-related query
        with st.spinner("Generating SQL and retrieving data..."):
            try:
                # Get the SQL query from Ollama
                sql_query = query_ollama(user_query)
                st.code(sql_query, language="sql")

                # Ensure the query is targeting the insurance_claims table
                if "insurance_claims" not in sql_query.lower():
                    raise ValueError("Generated query does not target the `insurance_claims` table.")

                # Execute the query in MySQL
                cursor.execute(sql_query)
                rows = cursor.fetchall()

                # Get column names
                columns = [col[0] for col in cursor.description]

                # Create a DataFrame to display
                df = pd.DataFrame(rows, columns=columns)

                # Display the results in Streamlit as a table
                st.write("### Query Results")
                st.dataframe(df)

            except Exception as e:
                st.error(f"Error: {e}")
                st.error("Ensure the Ollama API is running and accessible at the specified URL.")
