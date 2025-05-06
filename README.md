# **Auto Insurance Fraud Detection System using ML & Generative AI**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

## **Project Overview**

The **Auto Insurance Fraud Detection System** is an end-to-end solution that combines **Machine Learning (ML)** with **Generative AI (LLMs)** to detect fraudulent claims and provide intelligent insights from data. The system is built entirely using **Python**, making use of **LLM-based reasoning**, **Natural Language-to-SQL translation**, and **data visualizations** — all within an interactive **Streamlit** web app.

![Uploading image.png…]()

Users can:

* Input insurance claim details for fraud prediction
* Ask natural language questions to retrieve SQL-based data insights
* Generate visualizations directly from database queries using LLM logic

---

## **Key Features**

1. **🧠 LLM-Powered Reasoning & SQL Translation**

   * Ask **natural language questions** like:

     > *"What is the average claim amount for fraudulent claims?"*
   * **LangChain + Ollama** process the query, convert it into SQL, retrieve results from **PostgreSQL**, and display answers.

2. **📊 Dynamic Plotting via Python**

   * Query results are automatically plotted using **matplotlib**, **seaborn**, and **plotly**.
   * LLMs help **interpret** user intent (e.g., trends, comparisons) and select the appropriate plot type dynamically.

3. **🚩 Fraud Prediction System**

   * Trained ML model (using **XGBoost** and **scikit-learn**) classifies claims as *fraudulent* or *genuine*.
   * Uses **SHAP** for model explainability.

4. **💡 100% Python-based System**

   * No third-party BI tools or dashboards required.
   * Everything — from LLM query reasoning, SQL execution, plotting, to fraud detection — is handled using Python libraries.

---

## **Tech Stack**

| Category            | Tools & Libraries                       |
| ------------------- | --------------------------------------- |
| **Frontend**        | Streamlit                               |
| **ML Models**       | scikit-learn, XGBoost, SHAP             |
| **LLM Integration** | LangChain, Ollama, OpenAI               |
| **SQL & ORM**       | PostgreSQL, SQLAlchemy, psycopg2-binary |
| **Visualization**   | matplotlib, seaborn, plotly             |
| **Data Handling**   | pandas, numpy                           |
| **Environment**     | python-dotenv                           |
| **Utilities**       | requests, joblib                        |

---

## **Project Structure**

```bash
├── data/
│   └── insurance_claims.csv         # Source data
├── notebooks/
│   └── fraud_detection.ipynb        # Initial experimentation
├── src/
│   ├── app.py                       # Streamlit app entry point
│   ├── fraud_detector.py            # Model loading & prediction
│   ├── pandas_generation.py         # Data wrangling helpers
│   ├── plotting.py                  # Plot creation using Python
│   ├── prompts.py                   # Prompt templates for LLMs
│   ├── sql_generator.py             # Natural Language → SQL conversion
│   └── test_commands.txt
├── .streamlit/
├── config.toml                      # Configurations for app
├── requirements.txt                 # Project dependencies
├── README.md
├── LICENSE
```

---

## **Setup Instructions**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/insurance-fraud-llm.git
   cd insurance-fraud-llm
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install all dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**

   ```bash
   streamlit run src/app.py
   ```

---

## **License**

Distributed under the [MIT License](LICENSE).
