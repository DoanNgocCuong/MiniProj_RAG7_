from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from langchain.schema import Document, BaseRetriever
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

@dataclass
class SearchResult:
    """Store search results with score and document"""
    document: Document
    score: float

def create_bm25_retriever(documents: List[Document], k: int = 3) -> BM25Retriever:
    """Create BM25 Retriever from documents"""
    return BM25Retriever.from_documents(documents, k=k)

def create_hybrid_retriever(vectordb: Chroma, bm25_retriever: BM25Retriever, 
                           vector_weight: float = 0.5, k: int = 3) -> EnsembleRetriever:
    """Create Hybrid Retriever combining BM25 and Vector Search"""
    # Create vector retriever
    vector_retriever = vectordb.as_retriever(search_kwargs={"k": k})
    
    # Create ensemble retriever
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[1-vector_weight, vector_weight]
    )
    
    return ensemble_retriever

def custom_hybrid_search(query: str, vectordb: Chroma, documents: List[Document], 
                       top_k: int = 5, vector_weight: float = 0.6) -> List[Document]:
    """
    Search using combination of vector search and semantic matching, then re-rank results
    
    Args:
        query: Query string
        vectordb: Vector database
        documents: List of original documents
        top_k: Number of results to return
        vector_weight: Weight for vector search (from 0 to 1)
    
    Returns:
        List[Document]: List of documents sorted by relevance
    """
    # 1. Vector search
    vector_results = vectordb.similarity_search_with_score(query, k=top_k*2)
    
    # Convert to SearchResult
    vector_search_results = [
        SearchResult(document=doc, score=score)
        for doc, score in vector_results
    ]
    
    # 2. Keyword search with BM25
    bm25_retriever = BM25Retriever.from_documents(documents, k=top_k*2)
    bm25_results = bm25_retriever.get_relevant_documents(query)
    
    # Create a dict for quick document lookup
    doc_lookup = {}
    for doc in documents:
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
            result["vector_score"] * vector_weight +
            result["bm25_score"] * (1 - vector_weight)
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
            if len(final_results) >= top_k:
                break
    
    return final_results

@dataclass
class CustomHybridRetriever(BaseRetriever):
    """Custom retriever using hybrid search and re-ranking"""
    
    vectordb: Chroma
    documents: List[Document]
    top_k: int = field(default=3)
    vector_weight: float = field(default=0.6)
    
    def _get_relevant_documents(self, query: str, *, run_manager: Optional[Any] = None) -> List[Document]:
        """Main method to get relevant documents"""
        return custom_hybrid_search(
            query=query,
            vectordb=self.vectordb,
            documents=self.documents,
            top_k=self.top_k,
            vector_weight=self.vector_weight
        )
    
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