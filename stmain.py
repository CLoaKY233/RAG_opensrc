"""
RAG (Retrieval Augmented Generation) Streamlit Application

A web interface for document processing and Q&A using Mistral LLM.

This module serves as the main entry point for the Streamlit application.
It handles the UI components, file processing, and interaction with the RAG system.

Author: Lay Sheth, Rishav Raj


Dependencies:
- streamlit: Web interface framework
- langchain: LLM operations and chains
- chromadb: Vector store
- sentence-transformers: Text embeddings
- ollama: LLM interface

Main Features:
- Document upload and processing
- Interactive chat interface
- Document management
- Configurable settings

Usage:
    Run with: streamlit run stmain.py
"""

import streamlit as st
import time
from pysrc.document_processor import DocumentProcessor
from pysrc.embeddings_manager import EmbeddingsManager
from pysrc.rag_engine import RAGEngine
import logging
import os
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_files(files) -> bool:
    """
    Process uploaded files and initialize the RAG engine.

    Args:
        files: List of uploaded file objects from Streamlit

    Returns:
        bool: True if processing was successful

    Raises:
        Exception: If there's an error during file processing

    This function:
    1. Creates a temporary directory for file storage
    2. Saves uploaded files
    3. Initializes document processing and embedding components
    4. Creates vector store from processed documents
    5. Initializes RAG engine with the vector store
    """
    try:
        temp_dir = tempfile.mkdtemp()
        data_path = os.path.join(temp_dir, "data")
        os.makedirs(data_path, exist_ok=True)

        # Save uploaded files
        for uploaded_file in files:
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
        st.session_state.doc_stats["processed"] = len(files)
        st.session_state.doc_stats["chunks"] = len(documents)

        return True

    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        raise

# Initialize Streamlit page configuration
st.set_page_config(
    page_title="RAG with Mistral",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states for persistent data storage
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None  # Stores RAG engine instance
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Stores chat messages
if 'doc_stats' not in st.session_state:
    st.session_state.doc_stats = {"processed": 0, "chunks": 0}  # Stores document statistics

# UI Components are organized in sections:
# 1. Sidebar: Shows app title and document statistics
# 2. Tab1 (Chat): Handles chat interface and message display
# 3. Tab2 (Documents): Manages document upload and processing
# 4. Tab3 (Settings): Controls for RAG engine parameters
# 5. Footer: Credits and additional information

def process_files(files) -> bool:
    """Process uploaded files and initialize RAG engine"""
    try:
        temp_dir = tempfile.mkdtemp()
        data_path = os.path.join(temp_dir, "data")
        os.makedirs(data_path, exist_ok=True)

        # Save uploaded files
        for uploaded_file in files:
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
        st.session_state.doc_stats["processed"] = len(files)
        st.session_state.doc_stats["chunks"] = len(documents)

        return True

    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        raise

# Sidebar
with st.sidebar:
    st.title("🤖 RAG with Mistral")

    # Document Statistics
    if st.session_state.doc_stats["processed"] > 0:
        st.metric("Documents Processed", st.session_state.doc_stats["processed"])
        st.metric("Text Chunks", st.session_state.doc_stats["chunks"])

# Main content area
tab1, tab2, tab3 = st.tabs(["Chat", "Documents", "Settings"])

with tab1:
    st.header("💬 Chat Interface")

    # Chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question..." if st.session_state.rag_engine else "Please upload documents first..."):
        if st.session_state.rag_engine:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.rag_engine.answer_question(prompt)
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.warning("Please upload documents first")

with tab2:
    st.header("📁 Document Management")

    uploaded_files = st.file_uploader(
        "Upload your documents",
        type=['txt', 'pdf', 'docx'],
        accept_multiple_files=True,
        help="Supported formats: TXT, PDF, DOCX"
    )

    if uploaded_files:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Selected {len(uploaded_files)} files")
            for file in uploaded_files:
                st.text(f"• {file.name}")

        with col2:
            if st.button("Process Documents", type="primary"):
                with st.status("Processing documents...") as status:
                    try:
                        progress = st.progress(0)
                        for idx, _ in enumerate(uploaded_files):
                            progress.progress((idx + 1) / len(uploaded_files))
                            time.sleep(0.1)

                        success = process_files(uploaded_files)
                        if success:
                            status.update(label="✅ Processing complete!", state="complete")
                            st.success("Documents processed successfully!")
                            st.balloons()
                    except Exception as e:
                        status.update(label="❌ Error occurred!", state="error")
                        st.error(f"Error processing documents: {str(e)}")

with tab3:
    st.header("⚙️ Settings")

    temperature = st.slider(
        "Response Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Higher values make responses more creative"
    )

    context_length = st.number_input(
        "Context Window Size",
        min_value=1,
        max_value=5,
        value=3,
        help="Number of document chunks to consider"
    )

    if st.button("Save Settings"):
        if st.session_state.rag_engine:
            st.session_state.rag_engine.update_settings(
                temperature=temperature,
                context_length=context_length
            )
            st.success("Settings updated!")

    st.divider()

    if st.button("Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center'>Powered by Mistral</div>",
    unsafe_allow_html=True
)
