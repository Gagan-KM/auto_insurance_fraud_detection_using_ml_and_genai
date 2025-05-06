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
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score


def query(user_prompt):
    url = 'http://localhost:11434/api/generate'
    sys_prompt = '''
    You are an AI model designed to provide only the reasoning behind why the insurance claim was predicted as genuine or fraudulent.
    Your response should strictly focus on explaining the factors or features influencing the prediction, without adding any extra information or context.
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
    # Load dataset
    df = pd.read_excel(r"C:\Users\gagan\Downloads\insurance_dataset.xlsx")

    # Visualize class distribution (optional if not using Streamlit)
    fig, ax = plt.subplots()
    #sns.countplot(data=df, x='fraud_reported', ax=ax)
    plt.title("Class Distribution")
    plt.show()

    # Drop irrelevant columns
    df = df.drop(columns=['policy_number', 'policy_bind_date', 'incident_date', 'incident_location', 'auto_model'])

    # Fill missing values and apply one-hot encoding
    df.fillna('MISSING', inplace=True)
    df = pd.get_dummies(df, drop_first=True)

    # Define features and target
    target = 'fraud_reported_Y'
    X = df.drop(columns=[target])
    y = df[target]

    # Split the dataset
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=109)

    # Train Decision Tree model
    clf = DecisionTreeClassifier(max_depth=4, random_state=109)
    clf.fit(X_train, y_train)

    # Predict on training and validation sets
    y_pred_train = clf.predict(X_train)
    y_pred_val = clf.predict(X_val)


    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")    # Print performance metrics
    print("Training Set Metrics:")
    print(f"Accuracy: {accuracy_score(y_train, y_pred_train):.2f}")

    print("\nValidation Set Metrics:")
    print(f"Accuracy: {accuracy_score(y_val, y_pred_val):.2f}")
    print(f"Recall: {recall_score(y_val, y_pred_val):.2f}")
    print(f"Precision: {precision_score(y_val, y_pred_val):.2f}")
    print(f"F1-Score: {f1_score(y_val, y_pred_val):.2f}")

    # Cross-validation accuracy (optional but insightful)
    cv_scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print(f"\nCross-Validation Accuracy (5 folds): {cv_scores.mean():.2f} ± {cv_scores.std():.2f}")
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    
    # Model Evaluation Summary:
    # 
    # Training Set Metrics:
    # - Accuracy: 86%
    # 
    # Validation Set Metrics:
    # - Accuracy: 90%
    # - Recall: 96%   --> Excellent at identifying fraud cases
    # - Precision: 74% --> Some false positives, which is acceptable in fraud detection
    # - F1-Score: 84%  --> Good balance between precision and recall
    # 
    # Cross-Validation Results (5-Fold):
    # - Mean Accuracy: 84% ± 3%
    # - Indicates the model generalizes well and is stable across different data splits
    # 
    # Conclusion:
    # - No signs of overfitting or underfitting.
    # - High recall makes it suitable for fraud detection (better to catch most frauds, even at the cost of some false positives).
    # - Overall, the model performs well.

    return clf, X.columns.tolist()

