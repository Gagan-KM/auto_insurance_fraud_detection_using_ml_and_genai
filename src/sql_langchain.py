from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Setup the LLM (local Ollama instance)
llm = Ollama(model="llama3")

# SQL generation prompt using LangChain PromptTemplate
prompt = PromptTemplate(
    input_variables=["user_question"],
    template="""
You are a helpful assistant that only responds with valid MySQL SELECT statements on this table: `insurance_claims` from the database `fraud_detection`.

Generate correct SQL query based on the user question and the dataset columns provided.

RULES:
- DO NOT use markdown syntax (no ```sql, no ``` at all).
- DO NOT add comments, explanations, or formatting.
- ONLY return the raw SQL query — just one clean SELECT statement.

Use only the following columns:
months_as_customer, age, policy_number, policy_bind_date, policy_state, policy_csl, policy_deductable, 
policy_annual_premium, umbrella_limit, insured_zip, insured_sex, insured_education_level, 
insured_occupation, insured_hobbies, insured_relationship, capital-gains, capital-loss, incident_date, 
incident_type, collision_type, incident_severity, authorities_contacted, incident_state, incident_city, 
incident_location, incident_hour_of_the_day, number_of_vehicles_involved, property_damage, bodily_injuries, 
witnesses, police_report_available, total_claim_amount, injury_claim, property_claim, vehicle_claim, 
auto_make, auto_model, auto_year, fraud_reported.

Question: {user_question}
"""
)

# Create a chain using LLM and prompt
sql_chain = LLMChain(llm=llm, prompt=prompt)

# Rewritten query_sql function
def query_sql(user_prompt):
    try:
        return sql_chain.run(user_question=user_prompt).strip()
    except Exception as e:
        return f"LangChain Error: {str(e)}"
    
user_prompt = "What is the average total claim amount for each policy state?"

query_sql(user_prompt)