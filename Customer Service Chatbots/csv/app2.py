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
    "temperature": 0.7,  # Control randomness of responses
    "top_p": 0.9,        # Top P sampling
    "top_k": 50,         # Top K sampling
    "max_output_tokens": 512,  # Limit the number of tokens
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def create_context_from_csv(csv_data: list[dict]) -> str:
    """Create a structured context from CSV data."""
    context = "Here is the available data from the CSV file:\n\n"
    for idx, row in enumerate(csv_data, 1):
        context += f"Record {idx}:\n"
        for key, value in row.items():
            context += f"{key}: {value}\n"
        context += "\n"
    return context

# Extract data from CSV
csv_data = extract_csv("data.csv")  # Path to the CSV file

# Create a structured context from the CSV data
csv_context = create_context_from_csv(csv_data)

# Prepare the conversation history
history_data = [
    {
        "role": "system",
        "parts": [
            {"text": csv_context}  # Pass structured CSV context as part of system message
        ]
    },
    {
        "role": "user",
        "parts": [
            {"text": "Can you find the order ID from Karnataka?"}  # User's query
        ]
    }
]

# Start a chat session using the formatted history data
chat_session = model.start_chat(
    history=history_data
)

# Send a message to the model
response = chat_session.send_message("Can you find the order ID from Karnataka?")

# Print the model's response
print(response.text)
