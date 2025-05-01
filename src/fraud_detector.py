import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score
import requests
import json

def query(user_prompt):
    url = 'http://localhost:11434/api/generate'
    sys_prompt = '''
    You are a chatbot designed solely to provide detailed explanations for the questions posed by the user.
    Your role is not to offer direct solutions, but to clarify concepts, elaborate on ideas, and guide the user to a better understanding of their query.
    '''
    payload = {'model' : 'llama3.2', 'prompt' : user_prompt, 'system' : sys_prompt}
    try:
        response = requests.post(url = url, json = payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            result = response.text
            lines = result.strip().split("\n")
            full_response = "".join(json.loads(line)["response"] for line in lines)
            return full_response
        else:
            return "Error: Unable to reach the AI model service."
    except Exception as e:
        return f"Error: {str(e)}"

st.set_page_config(page_title="Insurance Fraud Detection", layout="wide")

@st.cache_resource
def train_car_insurance_model():
    df = pd.read_excel(r"C:\Users\gagan\Downloads\insurance_dataset.xlsx")

    # Visualize class distribution
    #st.subheader("Class Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='fraud_reported', ax=ax)
    #st.pyplot(fig)

    # Drop irrelevant columns
    df = df.drop(columns=['policy_number', 'policy_bind_date', 'incident_date', 'incident_location', 'auto_model'])

    # Fill missing and encode
    df.fillna('MISSING', inplace=True)
    df = pd.get_dummies(df, drop_first=True)

    target = 'fraud_reported_Y'
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=109)

    clf = DecisionTreeClassifier(max_depth=4, random_state=109)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)

    #st.write("### Model Performance on Validation Set")
    #st.write(f"**Accuracy:** {accuracy_score(y_val, y_pred):.2f}")
    #st.write(f"**Recall:** {recall_score(y_val, y_pred):.2f}")
    #st.write(f"**Precision:** {precision_score(y_val, y_pred):.2f}")
    
    return clf, X.columns.tolist()