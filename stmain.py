# streamlit_app.py
import streamlit as st
from pysrc.document_processor import DocumentProcessor
from pysrc.embeddings_manager import EmbeddingsManager
from pysrc.rag_engine import RAGEngine
import logging
import os
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration and hide headers/footers
st.set_page_config(page_title="RAG-LLM", layout="wide", initial_sidebar_state="collapsed")
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# Initialize session state
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def process_uploaded_file(uploaded_file):
    """Process uploaded file and initialize RAG engine"""
    try:
        # Create temporary directory for uploaded file
        temp_dir = tempfile.mkdtemp()
        data_path = os.path.join(temp_dir, "data")
        os.makedirs(data_path, exist_ok=True)

        # Save uploaded file
        file_path = os.path.join(data_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Initialize components
        doc_processor = DocumentProcessor(data_path)
        embeddings_manager = EmbeddingsManager("database")

        # Process documents
        documents = doc_processor.load_and_split_documents()
        vector_store = embeddings_manager.create_vector_store(documents)

        # Initialize RAG engine
        st.session_state.rag_engine = RAGEngine(vector_store)
        return True

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        st.error(f"Error processing file: {str(e)}")
        return False

# Main UI
st.title("RAG-LLM")

with st.container(border=True, height=750):
    # File upload section
    with st.container(border=True, height=150):
        uploaded_file = st.file_uploader("Upload your data", type=['txt'])
        if uploaded_file:
            if process_uploaded_file(uploaded_file):
                st.success("File processed successfully!")

    # Chat section
    with st.container(border=True, height=550):
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        prompt = st.chat_input("Ask a question...")

        if prompt:
            if st.session_state.rag_engine:
                # Display user message
                with st.chat_message("user"):
                    st.write(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})

                # Generate and display response
                with st.chat_message("assistant"):
                    try:
                        response = st.session_state.rag_engine.answer_question(prompt)
                        st.write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_message = f"Error generating response: {str(e)}"
                        st.error(error_message)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_message})
            else:
                st.warning("Please upload a document first", icon="⚠️")
