# pysrc/embeddings_manager.py
from langchain_community.embeddings import SentenceTransformerEmbeddings  # Changed this line
from langchain_community.vectorstores import Chroma
import logging
import os

logger = logging.getLogger(__name__)

class EmbeddingsManager:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        # Using SentenceTransformerEmbeddings instead
        self.embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2",
            cache_folder=os.path.join(self.persist_directory, "models")
        )

    def create_vector_store(self, documents):
        try:
            logger.info("Creating vector store...")
            if not documents:
                raise ValueError("No documents provided")

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
