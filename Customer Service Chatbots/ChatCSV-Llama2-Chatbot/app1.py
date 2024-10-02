import streamlit as st 
from streamlit_chat import message
import tempfile
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain

DB_FAISS_PATH = 'vectorstore/db_faiss'

# Loading the model
def load_llm():
    llm = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens=256,  # Reduced to avoid exceeding context
        temperature=0.5
    )
    return llm

# Title and header
st.title("Chat with CSV using Llama2 🦙🦜")
st.markdown("<h3 style='text-align: center; color: white;'>Built by <a href='https://github.com/AIAnytime'>AI Anytime with ❤️ </a></h3>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload your Data", type="csv")

if uploaded_file:
    # Use tempfile because CSVLoader only accepts a file path
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Load CSV data and embeddings
    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ','})
    data = loader.load()

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
    db = FAISS.from_documents(data, embeddings)
    db.save_local(DB_FAISS_PATH)

    # Load the LLM and create the retrieval chain
    llm = load_llm()
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

    # Define the function for conversational chat
    def conversational_chat(query):
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Truncate history to avoid exceeding token limit
        MAX_CONTEXT_TOKENS = 512
        def get_truncated_history(history, max_tokens=MAX_CONTEXT_TOKENS):
            total_tokens = 0
            truncated_history = []
            for question, answer in reversed(history):
                tokens = len(question.split()) + len(answer.split())
                if total_tokens + tokens > max_tokens:
                    break
                truncated_history.insert(0, (question, answer))  # Insert at the start to maintain order
                total_tokens += tokens
            return truncated_history

        truncated_history = get_truncated_history(st.session_state['history'])
        
        # Invoke the chain with the query and truncated history
        result = chain.invoke({"question": query, "chat_history": truncated_history})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]

    # Initialize session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about " + uploaded_file.name + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    # Containers for chat history and user input
    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Talk to your csv data here (:", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversational_chat(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    # Displaying the chat history
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
