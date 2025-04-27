"""
This module helps find relevant documents based on user questions.
It uses different methods to search and rank documents.
"""

from typing import List, Dict, Any, Optional, Union
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
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
    - Combine different search methods (hybrid search)
    - Filter and rank results
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        documents: Optional[List[Document]] = None,
        retriever_type: str = "vector",
        embeddings_model: Optional[HuggingFaceEmbeddings] = None,
        hybrid_weights: List[float] = [0.7, 0.3]  # [vector_weight, keyword_weight]
    ):
        """
        Start the DocumentRetriever with optional vector store and documents.
        
        Args:
            vector_store: Optional vector store for semantic search
            documents: Optional list of documents for BM25 search
            retriever_type: Type of retriever to use ('vector', 'bm25', 'hybrid', 'compression')
            embeddings_model: Optional HuggingFace embeddings model
            hybrid_weights: Weights for hybrid search [vector_weight, keyword_weight]
            
        Example:
            >>> from langchain_community.vectorstores import FAISS
            >>> vector_store = FAISS.from_documents(documents, embeddings)
            >>> retriever = DocumentRetriever(vector_store=vector_store)
        """
        self.vector_store = vector_store
        self.documents = documents
        self.retriever_type = retriever_type
        self.hybrid_weights = hybrid_weights
        
        # Initialize HuggingFaceEmbeddings with a small, fast model
        if embeddings_model is None:
            self.embeddings_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            self.embeddings_model = embeddings_model
            
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
        elif self.retriever_type == "hybrid" and self.vector_store and self.documents:
            # Create vector retriever
            vector_retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            # Create BM25 retriever
            bm25_retriever = BM25Retriever.from_documents(self.documents)
            bm25_retriever.k = 4
            
            # Create hybrid retriever
            self.retriever = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=self.hybrid_weights
            )
        elif self.retriever_type == "compression" and self.vector_store:
            try:
                # Initialize ChatOpenAI with minimal configuration
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.0,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                compressor = LLMChainExtractor.from_llm(llm)
                vector_retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
                )
                self.retriever = ContextualCompressionRetriever(
                    base_compressor=compressor,
                    base_retriever=vector_retriever
                )
            except Exception as e:
                print(f"Warning: Could not initialize compression retriever: {e}")
                print("Falling back to vector retriever")
                self.retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
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
                
        return self.retriever.get_relevant_documents(query)
    
    def get_relevant_documents(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """
        Alias for retrieve_documents to match LangChain interface.
        
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
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
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
    
    # Test hybrid retriever
    print("\nTesting hybrid retriever...")
    try:
        retriever = DocumentRetriever(
            vector_store=vector_store,
            documents=sample_docs,
            retriever_type="hybrid",
            hybrid_weights=[0.7, 0.3]  # 70% vector, 30% keyword
        )
        docs = retriever.retrieve_documents("What is RAG?")
        print(f"Found {len(docs)} relevant documents using hybrid search")
    except Exception as e:
        print(f"Hybrid retriever test failed: {e}")
    

