import streamlit as st
import pandas as pd
import requests
import json
import traceback
import mysql.connector

# MySQL credentials
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "20220288002",
    "database": "fraud_detection"
}

def query_sql(user_prompt):
    url = 'http://localhost:11434/api/generate'
    sys_prompt = '''
    You are a helpful assistant that only responds with valid MySQL SELECT statements on this table: `insurance_claims` from the database `fraud_detection`.

    generate correct SQL query based on the user question and the dataset columns provided.
    
    
    RULES:
    - DO NOT use markdown syntax (no ```sql, no ``` at all).
    - DO NOT add comments, explanations, or formatting.
    - ONLY return the raw SQL query — just one clean SELECT statement.

    GENERAL INSTRUCTIONS:
    - Use only the table `insurance_claims`.
    - Your entire response must be the SQL query only.

    Use only the following columns:
    months_as_customer, age, policy_number, policy_bind_date, policy_state, policy_csl, policy_deductable, 
    policy_annual_premium, umbrella_limit, insured_zip, insured_sex, insured_education_level, 
    insured_occupation, insured_hobbies, insured_relationship, capital-gains, capital-loss, incident_date, 
    incident_type, collision_type, incident_severity, authorities_contacted, incident_state, incident_city, 
    incident_location, incident_hour_of_the_day, number_of_vehicles_involved, property_damage, bodily_injuries, 
    witnesses, police_report_available, total_claim_amount, injury_claim, property_claim, vehicle_claim, 
    auto_make, auto_model, auto_year, fraud_reported.

    Unique values for some categorical columns:

    policy_state = ['OH', 'IN', 'IL']
    insured_sex = ['MALE', 'FEMALE']
    insured_education_level = ['MD', 'PhD', 'Associate', 'Masters', 'High School', 'College', 'JD']
    insured_occupation = ['craft-repair', 'machine-op-inspct', 'sales', 'armed-forces', 'tech-support',
                        'prof-specialty', 'other-service', 'priv-house-serv', 'exec-managerial',
                        'protective-serv', 'transport-moving', 'handlers-cleaners', 'adm-clerical',
                        'farming-fishing']
    insured_hobbies = ['sleeping', 'reading', 'board-games', 'bungie-jumping', 'base-jumping', 'golf',
                    'camping', 'dancing', 'skydiving', 'movies', 'hiking', 'yachting', 'paintball',
                    'chess', 'kayaking', 'polo', 'basketball', 'video-games', 'cross-fit', 'exercise']
    insured_relationship = ['husband', 'other-relative', 'own-child', 'unmarried', 'wife', 'not-in-family']
    incident_type = ['Single Vehicle Collision', 'Vehicle Theft', 'Multi-vehicle Collision', 'Parked Car']
    collision_type = ['Side Collision', '?', 'Rear Collision', 'Front Collision']
    incident_severity = ['Major Damage', 'Minor Damage', 'Total Loss', 'Trivial Damage']
    authorities_contacted = ['Police', 'nan', 'Fire', 'Other', 'Ambulance']
    incident_state = ['SC', 'VA', 'NY', 'OH', 'WV', 'NC', 'PA']
    incident_city = ['Columbus', 'Riverwood', 'Arlington', 'Springfield', 'Hillsdale', 'Northbend', 'Northbrook']
    property_damage = ['YES', '?', 'NO']
    police_report_available = ['YES', '?', 'NO']
    auto_make = ['Saab', 'Mercedes', 'Dodge', 'Chevrolet', 'Accura', 'Nissan', 'Audi', 'Toyota',
                'Ford', 'Suburu', 'BMW', 'Jeep', 'Honda', 'Volkswagen']
    auto_model = ['92x', 'E400', 'RAM', 'Tahoe', 'RSX', '95', 'Pathfinder', 'A5', 'Camry', 'F150',
                'A3', 'Highlander', 'Neon', 'MDX', 'Maxima', 'Legacy', 'TL', 'Impreza',
                'Forrestor', 'Escape', 'Corolla', '3 Series', 'C300', 'Wrangler', 'M5', 'X5',
                'Civic', 'Passat', 'Silverado', 'CRV', '93', 'Accord', 'X6', 'Malibu', 'Fusion',
                'Jetta', 'ML350', 'Ultima', 'Grand Cherokee']
    fraud_reported = ['Y', 'N']
'''

    payload = {
        'model': 'llama3.2',
        'prompt': user_prompt,
        'system': sys_prompt
    }

    try:
        response = requests.post(url=url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            result = response.text
            lines = result.strip().split("\n")
            full_response = "".join(json.loads(line)["response"] for line in lines)
            return full_response.strip()
        else:
            return "Error: Unable to reach the AI model service."
    except Exception as e:
        return f"Error: {str(e)}"

def run_query(sql_query):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        return f"SQL Execution Error:\n{traceback.format_exc()}"

def main():
    st.set_page_config(layout="wide")
    st.title("Gemma3 - SQL Data Explorer (MySQL Edition)")

    user_query = st.text_input("Ask your data question (SQL will be generated and run):")

    if user_query:
        with st.spinner("Generating SQL query..."):
            sql = query_sql(user_query)
            st.subheader("Generated SQL Query")
            st.code(sql, language="sql")

        with st.spinner("Running query..."):
            result = run_query(sql)
            if isinstance(result, pd.DataFrame):
                st.subheader("Query Result")
                st.dataframe(result)
            else:
                st.error("An error occurred while executing the SQL:")
                st.text(result)

if __name__ == "__main__":
    main()
