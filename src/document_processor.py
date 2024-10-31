# src/document_processor.py
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def load_and_split_documents(self):
        try:
            documents = []

            # Ensure directory exists
            if not os.path.exists(self.directory_path):
                os.makedirs(self.directory_path)
                logger.info(f"Created directory: {self.directory_path}")

            # Load each .txt file in the directory
            for filename in os.listdir(self.directory_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.directory_path, filename)
                    logger.info(f"Loading file: {file_path}")
                    try:
                        loader = TextLoader(file_path, encoding='utf-8')
                        documents.extend(loader.load())
                    except Exception as e:
                        logger.error(f"Error loading file {file_path}: {str(e)}")

            if not documents:
                logger.warning("No documents found or loaded")
                return []

            # Split documents
            splits = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(splits)} text chunks")
            return splits

        except Exception as e:
            logger.error(f"Error in load_and_split_documents: {str(e)}")
            raise
