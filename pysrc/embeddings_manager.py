# pysrc/embeddings_manager.py
"""
Embeddings Management Module

Handles document embeddings and vector store operations.

Author: Lay Sheth
Email: laysheth1@gmail.com

Dependencies:
- langchain_community
- sentence-transformers
- chromadb
- python standard libraries (os, logging)

Key Features:
- Document embedding generation
- Vector store creation and management
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import logging
import os

# -----------------------------------------
# Logger Setup
# -----------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------
# EmbeddingsManager Class Definition
# -----------------------------------------

class EmbeddingsManager:
    """
    Class to handle the creation of document embeddings and manage the vector store.

    Attributes:
        persist_directory (str): The directory where the vector store and models will be persisted.
        embeddings: The embeddings model used to generate document embeddings.
    """

    def __init__(self, persist_directory: str):
        """
        Initialize the EmbeddingsManager with a directory for persistence.

        Args:
            persist_directory (str): The path to the directory for storing embeddings and models.
        """
        self.persist_directory = persist_directory

        # Ensure the persistence directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize the embeddings model using SentenceTransformerEmbeddings
        self.embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2",  # Pretrained model for embedding generation
            cache_folder=os.path.join(self.persist_directory, "models")  # Cache folder for the model
        )

    def create_vector_store(self, documents):
        """
        Create a vector store from the provided documents.

        Args:
            documents (List[Document]): A list of Document objects to be embedded.

        Returns:
            Chroma: An instance of the Chroma vector store containing the document embeddings.

        Raises:
            ValueError: If no documents are provided.
            Exception: Any exception that occurs during vector store creation.
        """
        try:
            logger.info("Creating vector store...")

            # Check if documents are provided
            if not documents:
                raise ValueError("No documents provided")

            # Create the vector store from the documents
            vector_store = Chroma.from_documents(
                documents=documents,            # List of documents to embed
                embedding=self.embeddings,      # Embeddings model
                persist_directory=self.persist_directory  # Directory to persist the vector store
            )

            logger.info("Vector store created successfully")
            return vector_store

        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
