import streamlit as st
import mysql.connector
import pandas as pd
import requests
from prompts import system_prompt_sql
'''
# Streamlit UI
st.title("🕵️ SQL Retriever - Fraud Detection Insights")
user_query = st.text_input("Enter your question:", placeholder="e.g. Compare the average claim amounts between fraud and non-fraud cases")
'''

# Ollama configuration
OLLAMA_MODEL = "llama3.2"  # Ensure this model is pulled using: `ollama pull llama3`
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ensure the Ollama API is running at this URL

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="20220288002",
    database="fraud_detection"
)
cursor = conn.cursor()

def query_ollama(prompt):
    """
    system_prompt = '''
    You are an expert MySQL query generator. Convert the user's natural language question into a valid MySQL query using the `insurance_claims` table, 
   
    which has the following columns:
    months_as_customer, age, policy_number, policy_bind_date, policy_state, policy_csl, policy_deductable, 
    policy_annual_premium, umbrella_limit, insured_zip, insured_sex, insured_education_level, 
    insured_occupation, insured_hobbies, insured_relationship, capital-gains, capital-loss, incident_date, 
    incident_type, collision_type, incident_severity, authorities_contacted, incident_state, incident_city, 
    incident_location, incident_hour_of_the_day, number_of_vehicles_involved, property_damage, bodily_injuries, 
    witnesses, police_report_available, total_claim_amount, injury_claim, property_claim, vehicle_claim, 
    auto_make, auto_model, auto_year, fraud_reported, _c39

    Only respond with the raw SQL query. No explanations or markdown.
    '''
    """
    data = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt_sql}\n\nUser question: {prompt}\nSQL: ",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=data)
    if response.status_code == 200:
        sql = response.json().get("response", "").strip().split("```")[0]
        return sql
    else:
        raise ValueError(f"Failed to fetch SQL query. Status code: {response.status_code}, Response: {response.text}")
    
    
'''
if user_query:
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

# Close the MySQL connection
cursor.close()
conn.close()
'''