# main.py
from src.document_processor import DocumentProcessor
from src.embeddings_manager import EmbeddingsManager
from src.rag_engine import RAGEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize components
    doc_processor = DocumentProcessor("data")
    embeddings_manager = EmbeddingsManager("database")

    # Process documents
    try:
        # Load and split documents
        documents = doc_processor.load_and_split_documents()

        # Create vector store
        vector_store = embeddings_manager.create_vector_store(documents)

        # Initialize RAG engine
        rag_engine = RAGEngine(vector_store)

        # Interactive loop
        print("RAG System ready! Type 'quit' to exit.")
        while True:
            question = input("\nWhat's your question? ")
            if question.lower() == 'quit':
                break

            answer = rag_engine.answer_question(question)
            print("\nAnswer:", answer)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
