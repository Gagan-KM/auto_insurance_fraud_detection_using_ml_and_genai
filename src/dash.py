from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier
from sql_generator import query_sql, run_query
from fraud_detector import *
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = html.Div([
    # Typing animation for welcome message
    html.Div(id='typing-text-1', style={"fontSize": "2.5em", "fontFamily": "'Roboto', sans-serif", "color": "white"}),
    html.Div(id='typing-text-2', style={"fontSize": "1.6em", "fontFamily": "'Roboto', sans-serif", "color": "white"}),

    # Input box for user query
    dcc.Input(id='user-query', type='text', placeholder='e.g. Compare the average claim amounts between fraud and non-fraud cases',
              style={"width": "80%", "height": "40px", "fontSize": "16px"}),

    # Task selection
    dcc.RadioItems(id='task-option', options=[
        {'label': 'Run Prediction', 'value': 'Run Prediction'},
        {'label': 'Generate Visualizations', 'value': 'Generate Visualizations'},
        {'label': 'Retrieve Data', 'value': 'Retrieve Data'}
    ], value='Run Prediction'),

    # Run button
    html.Button('Run Query', id='run-button', n_clicks=0),

    # Sidebar for user inputs
    dbc.Col([
        html.H1("TrueClaimLLama", style={"fontSize": "2em"}),
        html.H4(id="model-name", children=f"Model used: DefaultModel: DefaultParameters"),
        html.Hr(),

        # Inputs for claim data
        html.Label("Enter Claim Information"),
        dcc.Input(id='months-as-customer', type='number', placeholder="Months as Customer", value=12, min=0, max=500),
        dcc.Input(id='age', type='number', placeholder="Age", value=30, min=18, max=100),
        dcc.Input(id='policy-deductable', type='number', placeholder="Policy Deductible", value=500, min=0, max=10000),
        dcc.Input(id='policy-annual-premium', type='number', placeholder="Annual Premium", value=1000, min=0, max=20000),
        dcc.Input(id='umbrella-limit', type='number', placeholder="Umbrella Limit", value=0, min=0, max=1000000),
        dcc.Input(id='capital-gains', type='number', placeholder="Capital Gains", value=0, min=0, max=100000),
        dcc.Input(id='capital-loss', type='number', placeholder="Capital Loss", value=0, min=0, max=100000),
        dcc.Slider(id='incident-hour-of-the-day', min=0, max=23, step=1, value=12),
        dcc.Slider(id='number-of-vehicles-involved', min=1, max=5, step=1, value=1),
        dcc.Slider(id='bodily-injuries', min=0, max=5, step=1, value=0),
        dcc.Slider(id='witnesses', min=0, max=5, step=1, value=1),
        dcc.Input(id='total-claim-amount', type='number', placeholder="Total Claim Amount", value=5000, min=0, max=100000),
        dcc.Input(id='injury-claim', type='number', placeholder="Injury Claim", value=2000, min=0, max=100000),
        dcc.Input(id='property-claim', type='number', placeholder="Property Claim", value=1000, min=0, max=100000),
        dcc.Input(id='vehicle-claim', type='number', placeholder="Vehicle Claim", value=2000, min=0, max=100000),
    ], width=3),

    # Output area for results
    html.Div(id='output-area')
])

# Callback to update typing animation and prediction
@app.callback(
    [Output('typing-text-1', 'children'),
     Output('typing-text-2', 'children')],
    Input('run-button', 'n_clicks')
)
def update_typing_animation(n_clicks):
    typing_html_1 = """
    <span id="typed-text-1"></span><span id="cursor-1">|</span>
    <script>
      const text1 = "Hello, How can I assist you today?";
      let i1 = 0;
      const speed1 = 60;

      function typeWriter1() {
        if (i1 < text1.length) {
          document.getElementById("typed-text-1").innerHTML += text1.charAt(i1);
          i1++;
          setTimeout(typeWriter1, speed1);
        }
      }

      setTimeout(typeWriter1, 300);
      setInterval(() => {
        const cursor = document.getElementById("cursor-1");
        cursor.style.visibility = (cursor.style.visibility === 'hidden') ? 'visible' : 'hidden';
      }, 500);
    </script>
    """
    
    typing_html_2 = """
    <span id="typed-text-2"></span><span id="cursor-2">|</span>
    <script>
      const messages = ["Predicting insurance fraud with confidence...", "Analyzing claim patterns for anomalies..."];
      let messageIndex = 0;
      let charIndex = 0;
      const speed = 50;
      const pauseTime = 1600;

      function typeWriter2() {
        const currentText = messages[messageIndex];
        if (charIndex < currentText.length) {
          document.getElementById("typed-text-2").innerHTML += currentText.charAt(charIndex);
          charIndex++;
          setTimeout(typeWriter2, speed);
        } else {
          setTimeout(() => {
            document.getElementById("typed-text-2").innerHTML = "";
            charIndex = 0;
            messageIndex = (messageIndex + 1) % messages.length;
            setTimeout(typeWriter2, speed);
          }, pauseTime);
        }
      }
      setTimeout(typeWriter2, 500);
      setInterval(() => {
        const cursor = document.getElementById("cursor-2");
        cursor.style.visibility = (cursor.style.visibility === 'hidden') ? 'visible' : 'hidden';
      }, 500);
    </script>
    """
    
    return typing_html_1, typing_html_2

# Run Flask app
if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8080)
