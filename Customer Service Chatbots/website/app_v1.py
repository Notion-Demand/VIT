from flask import Flask, render_template, jsonify, request
import plotly.graph_objects as go

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

# Chatbot route for answering questions
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_question = request.json.get('question')
    
    # Basic response logic based on graphs (can be more advanced)
    if 'retailers' in user_question.lower():
        answer = f"Total retailers onboarded: {100}"
    elif 'customers' in user_question.lower():
        answer = f"Total customers: {200}"
    elif 'escalations' in user_question.lower():
        answer = f"Performance escalations: {6}"
    elif 'issues' in user_question.lower():
        answer = f"Total issues resolved: {50}"
    else:
        answer = "I'm not sure, please ask something related to the graphs or data."

    return jsonify({'answer': answer})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
