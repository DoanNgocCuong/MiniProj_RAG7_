"""
This module helps find relevant documents based on user questions.
It uses different methods to search and rank documents.
"""

from typing import List, Dict, Any, Optional, Union
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_community.retrievers import BM25Retriever
from langchain_community.retrievers.ensemble import EnsembleRetriever
from langchain_community.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class DocumentRetriever:
    """
    A class that helps find relevant documents based on questions.
    
    This class can:
    - Find documents using vector search
    - Find documents using keyword search (BM25)
    - Combine different search methods
    - Filter and rank results
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        documents: Optional[List[Document]] = None,
        retriever_type: str = "vector"
    ):
        """
        Start the DocumentRetriever with optional vector store and documents.
        
        Args:
            vector_store: Optional vector store for semantic search
            documents: Optional list of documents for BM25 search
            retriever_type: Type of retriever to use ('vector', 'bm25', 'ensemble', 'compression')
            
        Example:
            >>> from langchain_community.vectorstores import FAISS
            >>> vector_store = FAISS.from_documents(documents, embeddings)
            >>> retriever = DocumentRetriever(vector_store=vector_store)
        """
        self.vector_store = vector_store
        self.documents = documents
        self.retriever_type = retriever_type
        self.retriever = None
        
        # Initialize the retriever based on type
        self._initialize_retriever()
    
    def _initialize_retriever(self):
        """Set up the retriever based on the chosen type."""
        if self.retriever_type == "vector" and self.vector_store:
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
        elif self.retriever_type == "bm25" and self.documents:
            self.retriever = BM25Retriever.from_documents(self.documents)
            self.retriever.k = 4
        elif self.retriever_type == "ensemble" and self.vector_store and self.documents:
            vector_retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            bm25_retriever = BM25Retriever.from_documents(self.documents)
            bm25_retriever.k = 4
            self.retriever = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=[0.7, 0.3]
            )
        elif self.retriever_type == "compression" and self.vector_store:
            llm = ChatOpenAI(model="gpt-3.5-turbo")
            compressor = LLMChainExtractor.from_llm(llm)
            vector_retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            self.retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=vector_retriever
            )
        else:
            raise ValueError(
                "Invalid retriever configuration. Please provide necessary components."
            )
    
    def retrieve_documents(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """
        Find documents related to the query.
        
        Args:
            query: The question to search for
            k: Number of documents to return (optional)
            
        Returns:
            List of relevant documents
            
        Example:
            >>> docs = retriever.retrieve_documents("What is RAG?")
            >>> print(f"Found {len(docs)} relevant documents")
        """
        if k is not None:
            if self.retriever_type == "bm25":
                self.retriever.k = k
            elif hasattr(self.retriever, "search_kwargs"):
                self.retriever.search_kwargs["k"] = k
                
        return self.retriever.invoke(query)
    
    def get_relevant_documents(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """
        Another way to find relevant documents.
        This is an alias for retrieve_documents.
        
        Args:
            query: The question to search for
            k: Number of documents to return (optional)
            
        Returns:
            List of relevant documents
        """
        return self.retrieve_documents(query, k)

if __name__ == "__main__":
    """
    This part runs when you run this file directly.
    It shows examples of how to use the DocumentRetriever class.
    """
    from langchain_core.documents import Document
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    # Create sample documents
    sample_docs = [
        Document(
            page_content="This is a sample document about RAG architecture.",
            metadata={"source": "test1"}
        ),
        Document(
            page_content="Another document explaining vector databases.",
            metadata={"source": "test2"}
        )
    ]
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create vector store
    vector_store = FAISS.from_documents(sample_docs, embeddings)
    
    # Test vector retriever
    print("\nTesting vector retriever...")
    try:
        retriever = DocumentRetriever(
            vector_store=vector_store,
            retriever_type="vector"
        )
        docs = retriever.retrieve_documents("What is RAG?")
        print(f"Found {len(docs)} relevant documents using vector search")
    except Exception as e:
        print(f"Vector retriever test failed: {e}")
    
    # Test BM25 retriever
    print("\nTesting BM25 retriever...")
    try:
        retriever = DocumentRetriever(
            documents=sample_docs,
            retriever_type="bm25"
        )
        docs = retriever.retrieve_documents("What is RAG?")
        print(f"Found {len(docs)} relevant documents using BM25")
    except Exception as e:
        print(f"BM25 retriever test failed: {e}")
    
    # Test ensemble retriever
    print("\nTesting ensemble retriever...")
    try:
        retriever = DocumentRetriever(
            vector_store=vector_store,
            documents=sample_docs,
            retriever_type="ensemble"
        )
        docs = retriever.retrieve_documents("What is RAG?")
        print(f"Found {len(docs)} relevant documents using ensemble search")
    except Exception as e:
        print(f"Ensemble retriever test failed: {e}")
    
    # Test compression retriever
    print("\nTesting compression retriever...")
    try:
        retriever = DocumentRetriever(
            vector_store=vector_store,
            retriever_type="compression"
        )
        docs = retriever.retrieve_documents("What is RAG?")
        print(f"Found {len(docs)} relevant documents using compression")
    except Exception as e:
        print(f"Compression retriever test failed: {e}")
