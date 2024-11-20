# pysrc/document_processor.py
"""
Document Processing Module

Handles document loading and text splitting operations.

Author: Lay Sheth
Email: laysheth1@gmail.com

Dependencies:
- langchain
- python standard libraries (os, logging)

Key Features:
- Document loading from directory
- Text splitting into manageable chunks
- Document metadata handling
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import logging
import os
from typing import List

# -----------------------------------------
# Logger Setup
# -----------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------
# DocumentProcessor Class Definition
# -----------------------------------------

class DocumentProcessor:
    """
    Class to handle loading text documents from a directory,
    splitting them into chunks, and preparing them for further processing.
    """

    def __init__(self, directory_path: str):
        """
        Initialize the DocumentProcessor with the directory containing text files.

        Args:
            directory_path (str): The path to the directory with .txt files.
        """
        self.directory_path = directory_path

        # Initialize the text splitter with specified parameters
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,          # Maximum size of each text chunk
            chunk_overlap=200,        # Overlap between chunks to maintain context
            length_function=len,      # Function to measure the length of text
            separators=["\n\n", "\n", ".", "!", "?", ",", " "]  # Preferred points to split text
        )

    def load_and_split_documents(self) -> List[Document]:
        """
        Load text documents from the directory, split them into chunks,
        and return a list of Document objects.

        Returns:
            List[Document]: A list of Document objects containing the split text chunks.

        Raises:
            ValueError: If the directory does not exist or no valid documents are found.
        """
        try:
            documents = []

            # Ensure the directory exists
            if not os.path.exists(self.directory_path):
                raise ValueError(f"Directory not found: {self.directory_path}")

            # Iterate over all files in the directory
            for filename in os.listdir(self.directory_path):
                # Process only .txt files
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.directory_path, filename)
                    logger.info(f"Processing file: {file_path}")

                    try:
                        # Open and read the content of the file
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()

                            # Check if the file is not empty
                            if text.strip():
                                # Create a Document object with the text content and metadata
                                doc = Document(
                                    page_content=text,
                                    metadata={"source": filename}
                                )

                                # Split the document into smaller chunks
                                split_docs = self.text_splitter.split_documents([doc])

                                # Add the split documents to the list
                                documents.extend(split_docs)
                                logger.info(f"Successfully processed {filename}")
                            else:
                                # Log a warning if the file is empty
                                logger.warning(f"Empty file: {file_path}")
                    except Exception as e:
                        # Log any exceptions that occur while processing a file
                        logger.error(f"Error processing file {file_path}: {str(e)}")
                        continue  # Skip to the next file

            # Raise an error if no documents were processed successfully
            if not documents:
                raise ValueError("No valid documents found or all documents were empty")

            logger.info(f"Successfully processed {len(documents)} document chunks")
            return documents

        except Exception as e:
            # Log any exceptions that occur during the document loading and splitting process
            logger.error(f"Error in load_and_split_documents: {str(e)}")
            raise
