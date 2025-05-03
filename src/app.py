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
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sql_generator import query_ollama, conn, cursor
from plotting import df, generate_code
from fraud_detector import *

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stTextInput>div>div>input {
        background-color: #333333;
        color: white;
        border: 1px solid #555555;
    }
    .stRadio>div>div>label {
        color: white;
    }
    .stSelectbox>div>div>div>div {
        background-color: #333333;
        color: white;
    }
    .stSidebar {
        background-color: #2e2e2e;
    }
    .stSidebar .stSelectbox>div>div>div>div {
        background-color: #444444;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Auto Insurance Fraud Detection")
st.write("Check claim status, visualize data, or generate SQL query results.")

user_query = st.text_input("Enter your question:", placeholder="e.g. Compare the average claim amounts between fraud and non-fraud cases")

task_option = st.radio("Choose a task:", ("Prediction", "Plotting", "SQL Query"))

run_button = st.button("Run Query")

insurance_type = st.sidebar.selectbox("Select Insurance Type", ["Car Insurance", "Health Insurance"])

if insurance_type == "Car Insurance":
    model, model_features = train_car_insurance_model()

    st.sidebar.subheader("Enter Claim Information")

    input_data = {
        'months_as_customer': st.sidebar.number_input("Months as Customer", 0, 500, 12),
        'age': st.sidebar.number_input("Age", 18, 100, 30),
        'policy_deductable': st.sidebar.number_input("Policy Deductible", 0, 10000, 500),
        'policy_annual_premium': st.sidebar.number_input("Annual Premium", 0, 20000, 1000),
        'umbrella_limit': st.sidebar.number_input("Umbrella Limit", 0, 1000000, 0),
        'capital-gains': st.sidebar.number_input("Capital Gains", 0, 100000, 0),
        'capital-loss': st.sidebar.number_input("Capital Loss", 0, 100000, 0),
        'incident_hour_of_the_day': st.sidebar.slider("Incident Hour", 0, 23, 12),
        'number_of_vehicles_involved': st.sidebar.slider("Number of Vehicles", 1, 5, 1),
        'bodily_injuries': st.sidebar.slider("Bodily Injuries", 0, 5, 0),
        'witnesses': st.sidebar.slider("Witnesses", 0, 5, 1),
        'total_claim_amount': st.sidebar.number_input("Total Claim Amount", 0, 100000, 5000),
        'injury_claim': st.sidebar.number_input("Injury Claim", 0, 100000, 2000),
        'property_claim': st.sidebar.number_input("Property Claim", 0, 100000, 1000),
        'vehicle_claim': st.sidebar.number_input("Vehicle Claim", 0, 100000, 2000),
    }

    categorical_defaults = {
        'policy_state_IL': 0,
        'policy_state_IN': 0,
        'policy_state_OH': 0,
        'incident_type_Single Vehicle Collision': 0,
        'incident_type_Multi-vehicle Collision': 0,
        'incident_type_Vehicle Theft': 0,
        'collision_type_Rear Collision': 0,
        'collision_type_Side Collision': 0,
        'insured_sex_MALE': 0,
        'insured_education_level_High School': 0,
        'insured_education_level_College': 0,
        'police_report_available_YES': 0,
    }

    policy_state = st.sidebar.selectbox("Policy State", ["IL", "IN", "OH"])
    categorical_defaults[f'policy_state_{policy_state}'] = 1

    incident_type = st.sidebar.selectbox("Incident Type", ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft"])
    categorical_defaults[f'incident_type_{incident_type}'] = 1

    collision_type = st.sidebar.selectbox("Collision Type", ["Rear Collision", "Side Collision"])
    categorical_defaults[f'collision_type_{collision_type}'] = 1

    sex = st.sidebar.selectbox("Gender", ["MALE", "FEMALE"])
    if sex == "MALE":
        categorical_defaults['insured_sex_MALE'] = 1

    education = st.sidebar.selectbox("Education", ["High School", "College", "Other"])
    if education in ["High School", "College"]:
        categorical_defaults[f'insured_education_level_{education}'] = 1

    police_report = st.sidebar.radio("Police Report Available?", ["YES", "NO"])
    if police_report == "YES":
        categorical_defaults['police_report_available_YES'] = 1

    for k, v in categorical_defaults.items():
        input_data[k] = v

    input_df = pd.DataFrame([input_data])

    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_features]

if run_button:
    if task_option:
        if task_option == "Prediction" and user_query == '':
            prediction = model.predict(input_df)[0]
            st.success("Prediction complete.")

            if prediction == 1:
                st.error("⚠️ This claim is predicted to be **FRAUDULENT**.")
            else:
                st.success("✅ This claim is predicted to be **LEGITIMATE**.")

        st.warning("Please select a task before running the query.")
