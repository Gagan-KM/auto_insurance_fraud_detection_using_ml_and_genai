import pandas as pd
import requests
from prompts import system_prompt_pandas  # Your custom instruction

OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Load dataset
DATA_PATH = "C:\\Users\\gagan\\Desktop\\auto_insurance_fraud_detection_using_ml_and_genai\\data\\insurance_claims.csv"
dfs = pd.read_csv(DATA_PATH)

def query_ollama(prompt):
    data = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt_pandas}\n\nUser question: {prompt}\nPython code:",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=data)
    if response.status_code == 200:
        code = response.json().get("response", "").strip().split("```")[0]
        return code
    else:
        raise ValueError(f"Failed to fetch Python code. Status code: {response.status_code}, Response: {response.text}")
