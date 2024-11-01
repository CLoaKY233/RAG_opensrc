# pysrc/rag_engine.py
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.temperature = 0.7
        self.context_length = 3
        self.llm = self._initialize_llm()
        self.qa_chain = self._setup_qa_chain()

    def _initialize_llm(self):
        return Ollama(
            model="mistral",
            temperature=self.temperature
        )

    def _setup_qa_chain(self):
        prompt_template = """
        Use the following pieces of context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}

        Answer: Let me help you with that.
        """

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": self.context_length}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

    def update_settings(self, temperature: float, context_length: int):
        self.temperature = temperature
        self.context_length = context_length
        self.llm = self._initialize_llm()
        self.qa_chain = self._setup_qa_chain()

    def answer_question(self, question: str) -> str:
        try:
            response = self.qa_chain({"query": question})
            return response["result"]
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
