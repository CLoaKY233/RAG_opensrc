# pysrc/document_processor.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " "]
        )

    def load_and_split_documents(self) -> List[Document]:
        try:
            documents = []

            # Ensure directory exists
            if not os.path.exists(self.directory_path):
                raise ValueError(f"Directory not found: {self.directory_path}")

            # Load each .txt file in the directory
            for filename in os.listdir(self.directory_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.directory_path, filename)
                    logger.info(f"Processing file: {file_path}")

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()
                            if text.strip():  # Check if file has content
                                # Create Document objects directly
                                doc = Document(
                                    page_content=text,
                                    metadata={"source": filename}
                                )
                                split_docs = self.text_splitter.split_documents([doc])
                                documents.extend(split_docs)
                                logger.info(f"Successfully processed {filename}")
                            else:
                                logger.warning(f"Empty file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {str(e)}")
                        continue

            if not documents:
                raise ValueError("No valid documents found or all documents were empty")

            logger.info(f"Successfully processed {len(documents)} document chunks")
            return documents

        except Exception as e:
            logger.error(f"Error in load_and_split_documents: {str(e)}")
            raise
