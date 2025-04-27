import os
import json
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import re
from pydantic import Field, BaseModel

from layers._01_data_ingestion.loader import DataIngestion
from layers._02_chunking.chunker import Chunking
from layers._03_embedding.embedder import Embedding
from layers._04_retrieval.retriever import Retrieval
from layers._05_generation.generator import Generation
from layers._06_evaluation.evaluator import Evaluation
from test_data import TEST_DATA

# Cài đặt thư viện cần thiết
# pip install langchain langchain-openai langchain-community chromadb rank_bm25 jq

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document, BaseRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import JSONLoader
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

@dataclass
class SearchResult:
    """Lưu trữ kết quả tìm kiếm với score và document"""
    document: Document
    score: float

def main():
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    top_k = int(os.getenv("TOP_K", "3"))
    vector_weight = float(os.getenv("VECTOR_WEIGHT", "0.6"))
    
    # Verify API key is set
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please create a .env file with your API key.")
    
    # Set API key
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Data Ingestion Layer
    data_ingestion = DataIngestion()
    documents = data_ingestion.load_and_preprocess_faq_data()
    
    # Chunking Layer
    chunking = Chunking()
    chunked_documents = chunking.chunk_documents(documents)
    
    # Embedding Layer
    embedding = Embedding(model_name=embedding_model)
    vectordb = embedding.create_vector_db(chunked_documents)
    
    # Retrieval Layer
    retrieval = Retrieval(vectordb=vectordb, documents=chunked_documents, k=top_k, vector_weight=vector_weight)
    hybrid_retriever = retrieval.create_hybrid_retriever()
    
    # Generation Layer
    generation = Generation(model_name=model_name)
    qa_chain = generation.create_qa_chain(hybrid_retriever)
    
    # Evaluation Layer
    evaluation_results = Evaluation.evaluate_qa_system(qa_chain, TEST_DATA)
    Evaluation.print_evaluation_results(evaluation_results)

if __name__ == "__main__":
    main()