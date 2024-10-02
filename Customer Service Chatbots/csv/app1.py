import os
import csv
import google.generativeai as genai

# Set your API key directly or ensure it's set as an environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAp4JRRx-q25y1BPkqk4gaHPUsPuz7mqqY")
genai.configure(api_key=API_KEY)

def extract_csv(pathname: str) -> list[dict]:
    """Extracts the content of the CSV into a list of dictionaries with headers as keys."""
    data = []
    with open(pathname, "r", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)  # Reads CSV into a list of dicts, with headers as keys
        for row in csv_reader:
            data.append(row)
    return data

# Create the model with configuration
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

# Extract data from CSV
csv_data = extract_csv("data.csv")  # Path to the CSV file

# Format the history correctly for the API
history_data = [
    {
        "role": "user",
        "parts": [
            {"text": str(csv_data)}  # Convert CSV data to string and pass it as 'text'
        ]
    }
]

# Start a chat session using the formatted history data
chat_session = model.start_chat(
    history=history_data
)

# Send a message to the model
response = chat_session.send_message("order id from karnatak")

# Print the model's response
print(response.text)
   