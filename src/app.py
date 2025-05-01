import streamlit as st
import requests
import mysql.connector
import pandas as pd
import json
from sql_generator import query_ollama, conn, cursor
from fraud_detector import query
from plotting import question, generate_code
import seaborn as sns
import matplotlib.pyplot as plt
import traceback
from plotting import df, generate_code

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
        if user_query.strip():
            try:
                st.write("🧠 Querying Mistral and generating Python code...")
                code = generate_code(user_query, df.columns)
                st.subheader("🧾 Generated Python Code")
                st.code(code, language="python")

                # Clear previous plots
                plt.clf()

                # Execute the code safely
                local_vars = {"df": df.copy()}
                exec(code, {
                    "pd": pd,
                    "sns": sns,
                    "plt": plt
                }, local_vars)

                # Display the new plot
                st.pyplot(plt.gcf())
                plt.clf()  # Optional: to avoid ghost plots when switching questions

            except Exception:
                st.error("❌ An error occurred while running the generated code:")
                st.text(traceback.format_exc())
        else:
            st.warning("Please enter a question to generate the plot.")
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
