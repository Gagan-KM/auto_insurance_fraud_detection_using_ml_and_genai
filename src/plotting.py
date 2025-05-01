import streamlit as st
import pandas as pd
import traceback
import re
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from prompts import system_prompt_plotting
from langchain.prompts import PromptTemplate

# Load dataset
df = pd.read_csv(r"C:\Users\gagan\Desktop\auto_insurance_fraud_detection_using_ml_and_genai\data\insurance_claims.csv")

# Initialize LLM
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3.2")

# Generate Python code
def generate_code(question, columns):
    prompt = PromptTemplate.from_template(system_prompt_plotting)
    formatted_prompt = prompt.format(question=question, columns=", ".join(columns))
    #code = llm(formatted_prompt)
    code = llm.invoke(formatted_prompt)
    code = re.sub(r"#.*", "", code).strip()
    return code