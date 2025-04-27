from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain.schema import Document, BaseRetriever
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from pydantic import Field, BaseModel

@dataclass
class SearchResult:
    """Store search results with score and document"""
    document: Document
    score: float

class CustomHybridRetriever(BaseRetriever, BaseModel):
    """Custom retriever using hybrid search and re-ranking"""
    
    vectordb: Chroma = Field(description="Vector database for semantic search")
    documents: List[Document] = Field(description="List of documents for BM25 search")
    top_k: int = Field(default=3, description="Number of documents to retrieve")
    vector_weight: float = Field(default=0.6, description="Weight for vector search results")
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_relevant_documents(self, query: str, *, run_manager: Optional[Any] = None) -> List[Document]:
        """Main method to get relevant documents"""
        # 1. Vector search
        vector_results = self.vectordb.similarity_search_with_score(query, k=self.top_k*2)
        
        # Convert to SearchResult
        vector_search_results = [
            SearchResult(document=doc, score=score)
            for doc, score in vector_results
        ]
        
        # 2. Keyword search with BM25
        bm25_retriever = BM25Retriever.from_documents(self.documents, k=self.top_k*2)
        bm25_results = bm25_retriever.get_relevant_documents(query)
        
        # Create a dict for quick document lookup
        doc_lookup = {}
        for doc in self.documents:
            key = (doc.metadata.get("id"), doc.metadata.get("type", ""))
            doc_lookup[key] = doc
        
        # Convert to SearchResult (assuming score from 0.5 to 1.0 for BM25)
        bm25_search_results = []
        for i, doc in enumerate(bm25_results):
            normalized_score = 1.0 - (i / len(bm25_results)) * 0.5  # From 1.0 to 0.5
            bm25_search_results.append(SearchResult(document=doc, score=normalized_score))
        
        # 3. Combine and re-rank results
        all_results = {}
        
        # Add vector search results
        for result in vector_search_results:
            doc_id = result.document.metadata.get("id")
            doc_type = result.document.metadata.get("type", "")
            key = (doc_id, doc_type)
            
            if key not in all_results:
                all_results[key] = {
                    "document": result.document,
                    "vector_score": result.score,
                    "bm25_score": 0.0
                }
            else:
                all_results[key]["vector_score"] = result.score
        
        # Add BM25 search results
        for result in bm25_search_results:
            doc_id = result.document.metadata.get("id")
            doc_type = result.document.metadata.get("type", "")
            key = (doc_id, doc_type)
            
            if key not in all_results:
                all_results[key] = {
                    "document": result.document,
                    "vector_score": 0.0,
                    "bm25_score": result.score
                }
            else:
                all_results[key]["bm25_score"] = result.score
        
        # Calculate final scores
        for key, result in all_results.items():
            result["final_score"] = (
                result["vector_score"] * self.vector_weight +
                result["bm25_score"] * (1 - self.vector_weight)
            )
        
        # Sort by final score and get top_k results
        sorted_results = sorted(
            all_results.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )
        
        # Filter unique documents by ID (prioritize higher scoring ones)
        unique_doc_ids = set()
        final_results = []
        
        for result in sorted_results:
            doc_id = result["document"].metadata.get("id")
            if doc_id not in unique_doc_ids:
                unique_doc_ids.add(doc_id)
                
                # Get original document from lookup
                original_doc_id = result["document"].metadata.get("id")
                original_content = result["document"].metadata.get("original_content")
                
                # If original_content exists, use it
                if original_content:
                    doc = Document(
                        page_content=original_content,
                        metadata=result["document"].metadata
                    )
                    final_results.append(doc)
                else:
                    final_results.append(result["document"])
                    
                # Stop when we have enough results
                if len(final_results) >= self.top_k:
                    break
        
        return final_results
    
    async def _aget_relevant_documents(self, query: str, *, run_manager: Optional[Any] = None) -> List[Document]:
        """Async version of get_relevant_documents"""
        return self._get_relevant_documents(query, run_manager=run_manager)

class Retrieval:
    def __init__(self, vectordb: Chroma, documents: List[Document], 
                 vector_weight: float = 0.6, k: int = 3):
        self.vectordb = vectordb
        self.documents = documents
        self.vector_weight = vector_weight
        self.k = k

    def create_hybrid_retriever(self) -> BaseRetriever:
        """Create hybrid retriever combining BM25 and vector search"""
        return CustomHybridRetriever(
            vectordb=self.vectordb,
            documents=self.documents,
            top_k=self.k,
            vector_weight=self.vector_weight
        ) 