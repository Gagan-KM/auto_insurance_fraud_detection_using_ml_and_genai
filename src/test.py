import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import json
import traceback

df = pd.read_csv(r'C:\Users\gagan\Desktop\auto_insurance_fraud_detection_using_ml_and_genai\data\insurance_claims.csv')

def query(user_prompt):
    url = 'http://localhost:11434/api/generate'
    
    sys_prompt = '''
Before starting, Avoid using ```python or any markdown-style formatting.
You must use this exact dataset path and no other: 'C:/Users/gagan/Desktop/auto_insurance_fraud_detection_using_ml_and_genai/data/insurance_claims.csv'. Do not alter, abbreviate, or replace it in any way.

IMPORTANT RULES:
- Avoid using ```python or any markdown-style formatting.
- Always generate clean, valid Python code with correct indentation and syntax.
- Avoid declaring unnecessary or unused variables in pandas or plotting.
- Avoid poor syntax in pandas expressions, column names, or matplotlib plotting.
- Avoid declaring variables that are not used later.
- Use only pandas and matplotlib.pyplot with figure size width=18 and height=7.
- Do not use any other libraries (e.g., seaborn) unless explicitly stated.
- Do not include any comments or explanations in the code.
- Dataset path must be exactly: 'C:/Users/gagan/Desktop/auto_insurance_fraud_detection_using_ml_and_genai/data/insurance_claims.csv'

TASK:
Generate clean, valid Python code that reads the dataset and plots data based on the user question using only allowed libraries, without unused variable declarations.

ALLOWED COLUMNS:
months_as_customer, age, policy_number, policy_bind_date, policy_state, policy_csl, policy_deductable, 
policy_annual_premium, umbrella_limit, insured_zip, insured_sex, insured_education_level, 
insured_occupation, insured_hobbies, insured_relationship, capital-gains, capital-loss, incident_date, 
incident_type, collision_type, incident_severity, authorities_contacted, incident_state, incident_city, 
incident_location, incident_hour_of_the_day, number_of_vehicles_involved, property_damage, bodily_injuries, 
witnesses, police_report_available, total_claim_amount, injury_claim, property_claim, vehicle_claim, 
auto_make, auto_model, auto_year, fraud_reported

UNIQUE VALUES FOR CATEGORICAL COLUMNS:
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
            return full_response
        else:
            return "Error: Unable to reach the AI model service."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(layout="wide")
    st.title("Gemma3 - Insurance Fraud Data Explorer")

    user_query = st.text_input("Ask your data plot question:")

    if user_query:
        with st.spinner("Generating code..."):
            code = query(user_query)
            st.subheader(f"Generated Code for: '{user_query}'")
            st.code(code)

        st.subheader("Generated Plot")
        with st.spinner("Rendering..."):
            try:
                plt.clf()
                local_vars = {"df": df.copy()}
                exec(code, {"pd": pd, "sns": sns, "plt": plt}, local_vars)
                st.pyplot(plt.gcf())
                plt.clf()
            except Exception:
                st.error("An error occurred while running the generated code:")
                st.text(traceback.format_exc())

if __name__ == "__main__":
    main()
