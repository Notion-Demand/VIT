import os
import time
import csv
import google.generativeai as genai

# Set your API key directly or ensure it's set as an environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAp4JRRx-q25y1BPkqk4gaHPUsPuz7mqqY")
genai.configure(api_key=API_KEY)

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready\n")

def extract_csv(pathname: str) -> list[str]:
    """Extracts the content of the CSV into a list of strings."""
    parts = [f" --- START OF CSV {pathname} --- "]
    with open(pathname, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            parts.append("".join(row))
    return parts

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

# Chat session setup using data from CSV
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": extract_csv("data.csv")  # CSV file path
        },
    ]
)

# Send a message to the model
response = chat_session.send_message("total customers")

# Print the model's response
print(response.text)

