from pandasai.llm.local_llm import LocalLLM  # Importing LocalLLM for local Meta Llama 3 model
import streamlit as st
import pandas as pd  # Pandas for data manipulation
from pandasai import SmartDataframe  # SmartDataframe for interacting with data using LLM


# Function to chat with CSV data
def chat_with_csv(df, query):
    # Initialize LocalLLM with Meta Llama 3 model
    try:
        llm = LocalLLM(
            api_base="http://localhost:11434/v1",
            model="llama3"
        )
        # Initialize SmartDataframe with DataFrame and LLM configuration
        pandas_ai = SmartDataframe(df, config={"llm": llm})
        
        # Chat with the DataFrame using the provided query
        result = pandas_ai.chat(query)
        
        # Log the raw result for debugging
        print("Raw result from pandasai:", result)
        
        # If result is a string response, return it directly
        if isinstance(result, str):
            return result
        else:
            return "No valid response found."

    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Error: {e}"


# Set layout configuration for the Streamlit page
st.set_page_config(layout='wide')

# Set title for the Streamlit application
st.title("Multiple-CSV ChatApp powered by LLM")

# Upload multiple CSV files
input_csvs = st.sidebar.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)

# Check if CSV files are uploaded
if input_csvs:
    # Select a CSV file from the uploaded files using a dropdown menu
    selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)

    # Load and display the selected csv file
    st.info("CSV uploaded successfully")
    data = pd.read_csv(input_csvs[selected_index])
    st.dataframe(data.head(3), use_container_width=True)

    # Enter the query for analysis
    st.info("Chat Below")
    input_text = st.text_area("Enter the query")

    # Perform analysis
    if input_text:
        if st.button("Chat with CSV"):
            st.info("Your Query: " + input_text)
            
            # Call the function to get the result
            result = chat_with_csv(data, input_text)
            
            # Display the result on Streamlit UI
            if "Error" in result:
                st.error(result)  # Display error message if any
            else:
                st.success(result)  # Display success message with result

            # Log the result for debugging in the terminal
            print(f"Displayed result: {result}")
