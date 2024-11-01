# src/embeddings_manager.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import logging
import os

logger = logging.getLogger(__name__)

class EmbeddingsManager:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_vector_store(self, documents):
        try:
            logger.info("Creating vector store...")
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info("Vector store created successfully")
            return vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
