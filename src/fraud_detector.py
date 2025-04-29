import streamlit as st
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
'''
def main():
    st.title("Auto Insurance Fraud Detection")
    
    st.write("Check claim status or get fraud prediction.")

    user_input = st.text_input("Enter claim details or ID:")

    if user_input:
        with st.spinner('Processing...'):
            response = query(user_input)
            st.write("Result:")
            st.write(response)

if __name__ == "__main__":
    main()
'''