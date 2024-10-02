import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the CSV file
data = pd.read_csv('./data.csv')

# Function to get data from the CSV file for specific columns
def get_csv_data(column_name):
    if column_name in data.columns:
        return data[column_name].sum()
    else:
        return "Column not found in the CSV."

# Chatbot logic with CSV data integration
def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Respond based on specific keywords in user input
    if "retailer" in user_input:
        total_retailers = get_csv_data('Total Retailers')  # Replace with the appropriate column name
        return f"Total retailers onboarded: {total_retailers}"
    
    elif "customer" in user_input:
        total_customers = get_csv_data('Customer')  # Replace with the appropriate column name
        return f"Total customers: {total_customers}"
    
    elif "escalation" in user_input:
        performance_escalations = get_csv_data('Performance Escalations')  # Replace with the appropriate column name
        return f"Performance escalations: {performance_escalations}"
    
    elif "issue" in user_input:
        total_issues = get_csv_data('Total Issues')  # Replace with the appropriate column name
        return f"Total issues resolved: {total_issues}"
    
    # Answer based on the current week chart (static data for now)
    elif "current week" in user_input or "week start" in user_input:
        return "For this week, resolution trends show low activity on Day 1 and higher activity towards the end of the week."
    
    # Default response if nothing matches
    else:
        return "I'm not sure, please ask something related to the graphs or data."

# Route for chatbot communication
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    bot_message = chatbot_response(user_message)
    return jsonify({"response": bot_message})

# Route for main page with embedded chatbot
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
