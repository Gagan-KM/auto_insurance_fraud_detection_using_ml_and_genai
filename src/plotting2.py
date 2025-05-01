import streamlit as st
import pandas as pd
import traceback
import re
import seaborn as sns
import matplotlib.pyplot as plt
from langchain.prompts import PromptTemplate

# Optimize data loading
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\gagan\Desktop\auto_insurance_fraud_detection_using_ml_and_genai\data\insurance_claims.csv")

df = load_data()

# Optimize model loading
@st.cache_resource
def load_llm():
    from langchain_ollama import OllamaLLM
    return OllamaLLM(model="mistral:7b")

llm = load_llm()

# Prompt Template (trimmed context version)
base_prompt = '''
You are a data scientist. Given the following user question and dataset columns, generate Python code using pandas and seaborn to create a plot.

Do NOT use backticks, comments, or markdown formatting. Just return valid Python code only.

Dataset Columns: {columns}
User Question: {question}
'''

# Generate Python code from LLM
def generate_code(question, columns):
    prompt = PromptTemplate.from_template(base_prompt)
    formatted_prompt = prompt.format(question=question, columns=", ".join(columns[:20]))  # Trim columns
    code = llm.invoke(formatted_prompt)
    code = re.sub(r"#.*", "", code).strip()
    return code

# Streamlit App UI
st.title("🚗 Insurance Claims Visualizer (Mistral LLM)")

question = st.text_input("Ask your question (e.g., 'Get average total claim for each fraud category')")

if st.button("Generate Plot"):
    if question.strip():
        try:
            st.write("🧠 Generating Python code using Mistral...")
            code = generate_code(question, df.columns)

            st.subheader("🧾 Generated Python Code")
            st.code(code, language="python")

            plt.clf()
            local_vars = {"df": df.copy()}
            exec(code, {"pd": pd, "sns": sns, "plt": plt}, local_vars)

            st.pyplot(plt.gcf())
            plt.clf()

        except Exception:
            st.error("❌ An error occurred while running the generated code:")
            st.text(traceback.format_exc())
    else:
        st.warning("Please enter a question to generate the plot.")
