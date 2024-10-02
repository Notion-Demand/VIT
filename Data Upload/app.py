from flask import Flask, render_template, jsonify, request
import plotly.graph_objects as go
import os
import csv
import google.generativeai as genai

app = Flask(__name__)

# Function to create graph 1: Current Week Graph
# Function to create graph 1: Current Week Graph (Line Graph)
def create_current_week_graph():
    fig = go.Figure()

    # Add traces for each day of the week
    fig.add_trace(go.Scatter(
        x=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        y=[1, 2, 3, 4, 5, 6, 7],
        mode='lines+markers',
        name='Metric 1'
    ))

    fig.add_trace(go.Scatter(
        x=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        y=[3, 1, 2, 4, 5, 6, 7],
        mode='lines+markers',
        name='Metric 2'
    ))

    fig.add_trace(go.Scatter(
        x=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        y=[2, 3, 1, 4, 6, 5, 7],
        mode='lines+markers',
        name='Metric 3'
    ))

    fig.add_trace(go.Scatter(
        x=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        y=[2, 3, 4, 1, 6, 5, 7],
        mode='lines+markers',
        name='Metric 4'
    ))

    fig.update_layout(title='Current Week Overview', xaxis_title='Days of the Week', yaxis_title='Values')
    return fig.to_html(full_html=False)


# Function to create graph 2: Data Origin Breakdown
def create_data_origin_graph():
    fig = go.Figure(data=go.Bar(
        x=[100, 200, 300, 400, 500],
        y=['Email', 'Manual Entry', 'Phone Call', 'Web'],
        orientation='h'
    ))
    fig.update_layout(title='Data Origin Breakdown')
    return fig.to_html(full_html=False)

# Function to create graph 3: Average Resolution Time
def create_avg_resolution_graph():
    fig = go.Figure(data=go.Bar(
        x=[20, 40, 60, 80],
        y=['Under 1 hour', '1-2 hours', 'Over 2 hours'],
        orientation='h'
    ))
    fig.update_layout(title='Average Resolution Time')
    return fig.to_html(full_html=False)

# Route for the main dashboard page
@app.route('/')
def index():
    graphs = {
        'current_week': create_current_week_graph(),
        'data_origin': create_data_origin_graph(),
        'avg_resolution': create_avg_resolution_graph()
    }
    
    cards = {
        'retailers': 100,
        'customers': 200,
        'escalations': 6,
        'issues': 50
    }

    return render_template('dashboard_with_chatbot.html', graphs=graphs, cards=cards)

# Function to extract data from CSV
def extract_csv(pathname: str) -> list[dict]:
    """Extracts the content of the CSV into a list of dictionaries with headers as keys."""
    data = []
    with open(pathname, "r", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)  # Reads CSV into a list of dicts, with headers as keys
        for row in csv_reader:
            data.append(row)
    return data

# Set your API key for Google Generative AI
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAp4JRRx-q25y1BPkqk4gaHPUsPuz7mqqY")
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Predefined answers from cards
cards_data = {
    'total retailers': 100,
    'total customers': 200,
    'total escalations': 6,
    'total issues': 50
}

# Helper function to check for key terms in the question
def check_for_precise_answer(question: str):
    """Returns a precise answer if the question matches predefined ones."""
    question_lower = question.lower()
    for key, value in cards_data.items():
        if key in question_lower:
            return value
    return None

# Chatbot route for answering questions using Google Generative AI
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_question = request.json.get('question')
    
    # First, check for precise answers in predefined data
    precise_answer = check_for_precise_answer(user_question)
    if precise_answer is not None:
        return jsonify({'answer': precise_answer})
    
    # If no precise answer is found, use Google Generative AI
    # Extract CSV data (assumes 'data.csv' is present in the same directory)
    csv_data = extract_csv("data.csv")
    
    # Format the CSV data as history to send to the model
    history_data = [
        {
            "role": "user",
            "parts": [
                {"text": str(csv_data)}  # Convert CSV data to string and pass it as 'text'
            ]
        }
    ]

    # Start a chat session with the model using CSV data
    chat_session = model.start_chat(
        history=history_data
    )
    
    # Send the user's question to the model
    response = chat_session.send_message(user_question)
    
    return jsonify({'answer': response.text})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)