import streamlit as st
import pandas as pd
import traceback
import requests
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r"C:\Users\gagan\Desktop\auto_insurance_fraud_detection_using_ml_and_genai\data\insurance_claims.csv")

# Initialize Ollama LLM
llm = Ollama(model="mistral:7b")  # or codellama if you prefer

# Define the prompt template
prompt_template = '''

You are a data scientist. Given the following user question and dataset columns, generate Python code using pandas and seaborn to create a plot.

You are restricted from using backticks or markdown formatting. You must not include comments, documentation, or any explanation; only generate valid Python code.

Dataset Columns: {columns}
User Question: {question}

You will have access to the unique values for some categorical columns to help with constructing the query:

policy_state = ['OH', 'IN', 'IL']
policy_csl = ['250/500', '100/300', '500/1000']
policy_deductable = [1000, 2000, 500]
umbrella_limit = [0, 5000000, 6000000, 4000000, 3000000, 8000000, 7000000, 9000000, 10000000, -1000000, 2000000]
insured_sex = ['MALE', 'FEMALE']
insured_education_level = ['MD', 'PhD', 'Associate', 'Masters', 'High School', 'College', 'JD']
insured_occupation = ['craft-repair', 'machine-op-inspct', 'sales', 'armed-forces', 'tech-support',
 'prof-specialty', 'other-service', 'priv-house-serv', 'exec-managerial',
 'protective-serv', 'transport-moving', 'handlers-cleaners', 'adm-clerical',
 'farming-fishing']
insured_hobbies = ['sleeping', 'reading', 'board-games', 'bungie-jumping', 'base-jumping', 'golf',
 'camping', 'dancing', 'skydiving', 'movies', 'hiking', 'yachting', 'paintball',
 'chess', 'kayaking', 'polo', 'basketball', 'video-games', 'cross-fit',
 'exercise']
insured_relationship = ['husband', 'other-relative', 'own-child', 'unmarried', 'wife', 'not-in-family']
incident_type = ['Single Vehicle Collision', 'Vehicle Theft', 'Multi-vehicle Collision', 'Parked Car']
collision_type = ['Side Collision', '?', 'Rear Collision', 'Front Collision']
incident_severity = ['Major Damage', 'Minor Damage', 'Total Loss', 'Trivial Damage']
authorities_contacted = ['Police', 'nan', 'Fire', 'Other', 'Ambulance']
incident_state = ['SC', 'VA', 'NY', 'OH', 'WV', 'NC', 'PA']
incident_city = ['Columbus', 'Riverwood', 'Arlington', 'Springfield', 'Hillsdale', 'Northbend', 'Northbrook']
incident_hour_of_the_day = [5, 8, 7, 20, 19, 0, 23, 21, 14, 22, 9, 12, 15, 6, 16, 4, 10, 1, 17, 3, 11, 13, 18, 2]
number_of_vehicles_involved = [1, 3, 4, 2]
property_damage = ['YES', '?', 'NO']
bodily_injuries = [1, 0, 2]
witnesses = [2, 0, 3, 1]
police_report_available = ['YES', '?', 'NO']
auto_make = ['Saab', 'Mercedes', 'Dodge', 'Chevrolet', 'Accura', 'Nissan', 'Audi', 'Toyota',
 'Ford', 'Suburu', 'BMW', 'Jeep', 'Honda', 'Volkswagen']
auto_model = ['92x', 'E400', 'RAM', 'Tahoe', 'RSX', '95', 'Pathfinder', 'A5', 'Camry', 'F150',
 'A3', 'Highlander', 'Neon', 'MDX', 'Maxima', 'Legacy', 'TL', 'Impreza',
 'Forrestor', 'Escape', 'Corolla', '3 Series', 'C300', 'Wrangler', 'M5', 'X5',
 'Civic', 'Passat', 'Silverado', 'CRV', '93', 'Accord', 'X6', 'Malibu', 'Fusion',
 'Jetta', 'ML350', 'Ultima', 'Grand Cherokee']
auto_year = [2004, 2007, 2014, 2009, 2003, 2012, 2015, 1996, 2002, 2006, 2000, 2010, 1999, 2011,
 2005, 2008, 1995, 2001, 1998, 1997, 2013]
fraud_reported = ['Y', 'N']

'''

# Function to generate Python code using LLM
def generate_code(question, columns):
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(question=question, columns=", ".join(columns))
    code = llm(formatted_prompt)

    # Remove backticks and extra markdown formatting by splitting the response
    code_lines = code.strip().splitlines()

    # Remove the first and last lines containing backticks
    if code_lines:
        code_lines = code_lines[1:-1]  # Remove first and last lines

    # Join the remaining lines back together
    code = "\n".join(code_lines).strip()

    # Remove any comments (lines starting with #)
    code = re.sub(r"#.*", "", code).strip()

    return code

# Streamlit UI
st.title("LLM-Powered Insurance Claims Visualizer")

question = st.text_input("Ask a question (e.g., 'Show average claim per policy state')")

if st.button("Generate Plot"):
    if question:
        try:
            st.write("Generating Python code using LLM...")
            code = generate_code(question, df.columns)
            st.code(code, language="python")

            # Safely execute the generated code
            local_vars = {"df": df.copy()}
            exec(code, {
                "pd": pd,
                "sns": sns,
                "plt": plt,
            }, local_vars)

            # Display the plot
            if 'plot' in local_vars:
                st.pyplot(local_vars['plot'])
        except Exception:
            st.error("Error occurred while running the generated code:")
            st.text(traceback.format_exc())
