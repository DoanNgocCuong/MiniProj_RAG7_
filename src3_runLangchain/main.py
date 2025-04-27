import os
import json
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import re
from pydantic import Field, BaseModel

from layers._01_data_ingestion.loader import load_faq_data, preprocess_faq_data
from layers._03_embedding.embedder import create_vectordb
from layers._04_retrieval.retriever import create_bm25_retriever, create_hybrid_retriever, CustomHybridRetriever
from layers._05_generation.generator import create_hybrid_qa_chain
from layers._06_evaluation.evaluator import evaluate_qa_system, print_evaluation_results
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
    documents = load_faq_data("data/TinhNangApp.json")
    processed_documents = preprocess_faq_data(documents)
    
    # Embedding Layer
    vectordb = create_vectordb(processed_documents)
    
    # Retrieval Layer
    bm25_retriever = create_bm25_retriever(processed_documents, k=top_k)
    hybrid_retriever = create_hybrid_retriever(
        vectordb=vectordb,
        bm25_retriever=bm25_retriever,
        vector_weight=vector_weight,
        k=top_k
    )
    
    # Generation Layer
    qa_chain = create_hybrid_qa_chain(hybrid_retriever)
    
    # Evaluation Layer
    evaluation_results = evaluate_qa_system(qa_chain, TEST_DATA)
    print_evaluation_results(evaluation_results)

if __name__ == "__main__":
    main()