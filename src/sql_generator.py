import streamlit as st
import mysql.connector
import pandas as pd
import requests
from prompts import system_prompt_sql

# Ollama configuration
OLLAMA_MODEL = "llama3.2" 
OLLAMA_URL = "http://localhost:11434/api/generate"

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="20220288002",
    database="fraud_detection"
)
cursor = conn.cursor()

def query_ollama(prompt):
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