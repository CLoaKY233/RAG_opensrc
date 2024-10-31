from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import logging

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = Ollama(model="mistral")

    def answer_question(self, question: str):
        try:
            logger.info(f"Processing question: {question}")

            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            )

            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )

            response = qa_chain({"query": question})
            return response["result"]

        except Exception as e:
            logger.error(f"Error in answer_question: {str(e)}")
            raise
