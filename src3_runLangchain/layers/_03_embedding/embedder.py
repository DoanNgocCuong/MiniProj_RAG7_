from typing import List
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class Embedding:
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(model=model_name)

    def create_vectordb(self, documents: List[Document]) -> Chroma:
        """Create vector database from documents"""
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        ) 