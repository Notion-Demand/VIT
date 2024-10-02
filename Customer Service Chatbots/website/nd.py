from flask import Flask, render_template, jsonify, request
import plotly.graph_objects as go
import os
import csv
import google.generativeai as genai

app = Flask(__name__)

# Function to create graph 1: Current Week Graph
def create_current_week_graph():
    fig = go.Figure(data=go.Heatmap(
        z=[[1, 2, 3, 4, 5, 6, 7], [3, 1, 2, 4, 5, 6, 7], [2, 3, 1, 4, 6, 5, 7], [2, 3, 4, 1, 6, 5, 7]],
        x=['None', 'Low', 'Medium', 'High'],
        y=['Weekstart', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
    ))
    fig.update_layout(title='Current Week Overview')
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

# Simple responses for common questions
def get_simple_response(user_question: str) -> str:
    simple_responses = {
        "how many retailers": "Total retailers onboarded: 100",
        "how many customers": "Total customers: 200",
        "how many escalations": "Performance escalations: 6",
        "how many issues": "Total issues resolved: 50",
        "what is the average resolution time": "The average resolution time is: Under 1 hour"
    }
    
    # Check if the user's question matches any simple response
    for key, response in simple_responses.items():
        if key in user_question.lower():
            return response
    return None

# Chatbot route for answering questions
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_question = request.json.get('question')
    
    # First, try to answer with a basic response
    simple_response = get_simple_response(user_question)
    if simple_response:
        return jsonify({'answer': simple_response})
    
    # If no simple response, pass the question to Google Generative AI
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
