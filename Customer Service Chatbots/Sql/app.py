from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='2211',
        database='chatbot_db'
    )
    return conn

# Home route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Webhook endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['userInput']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query the database
    cursor.execute("SELECT info FROM users WHERE name = %s", (user_input,))
    result = cursor.fetchone()

    if result:
        response = result[0]
    else:
        response = "Sorry, I don't have information on that."

    cursor.close()
    conn.close()
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
