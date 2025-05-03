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
import plotly.express as px

# Adjust padding for the Streamlit app layout
st.markdown("""
    <style>
    .block-container {
        padding-top: 4.7rem !important;
        padding-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Typing animation for the welcome message
import streamlit as st
import streamlit.components.v1 as components

typing_html = """
<div style="display: flex; justify-content: flex-start; align-items: center; height: 50px">
  <h3 style="font-size: 3em; font-family: 'Roboto', sans-serif; color: white;">
    <span id="typed-text"></span><span id="cursor">|</span>
  </h3>
</div>

<script>
  const text = "How can I assist you today?";
  let i = 0;
  const speed = 60;

  function typeWriter() {
    if (i < text.length) {
      document.getElementById("typed-text").innerHTML += text.charAt(i);
      i++;
      setTimeout(typeWriter, speed);
    }
  }

  setTimeout(typeWriter, 500);

  // Optional blinking cursor
  setInterval(() => {
    const cursor = document.getElementById("cursor");
    cursor.style.visibility = (cursor.style.visibility === 'hidden') ? 'visible' : 'hidden';
  }, 500);
</script>
"""

# Render the animated heading
components.html(typing_html, height=70)

# User input for query
user_query = st.text_input(
    "Enter your question:",
    placeholder="e.g. Compare the average claim amounts between fraud and non-fraud cases",
)

# Task selection options
task_option = st.radio(
    "Choose a task:",
    ("Prediction", "Plotting", "SQL Query"),
    key="task_option",
    format_func=lambda x: f"{x}",
)

# Button to execute the selected task
run_button = st.button("Run Query", key="run_button", help="Click to execute your selected task")

# Sidebar for user inputs and additional options
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
st.sidebar.markdown('<h2><strong>Auto Insurance Fraud Detection</strong></h2>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Load and train the model for car insurance fraud detection
if True:
    model, model_features = train_car_insurance_model()
    
    st.sidebar.subheader("Enter Claim Information")

    # Collect numeric inputs from the user
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

    # Collect categorical inputs and encode them
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

    # Get user inputs for categorical fields
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

    # Merge numeric and categorical inputs
    for k, v in categorical_defaults.items():
        input_data[k] = v

    # Convert inputs to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure input matches model features
    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_features]

# Execute the selected task when the button is clicked
if run_button:
    if task_option:
        if task_option == "Prediction" and user_query == '':
            prediction = model.predict(input_df)[0]
            #st.success("Prediction complete.")

            if prediction == 1:
                st.error("This claim is predicted to be **FRAUDULENT**.")
            else:
                st.success("This claim is predicted to be **LEGITIMATE**.")

            explanation_prompt = "Given the following insurance claim details, explain why a machine learning model might predict it as "
            explanation_prompt += "fraudulent:\n" if prediction == 1 else "legitimate:\n"
            explanation_prompt += "\n".join([f"- {k}: {v}" for k, v in input_data.items()])

            with st.spinner("Generating explanation using LLM..."):
                explanation = query(explanation_prompt)
                st.markdown("Explanation from LLM")
                st.write(explanation)
        if task_option == "Plotting":
            with st.spinner("Thinking..."):
                try:
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
        elif task_option == "SQL Query":
            with st.spinner("Thinking..."):
                try:
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
        st.warning("Please select a task before running the query.")
