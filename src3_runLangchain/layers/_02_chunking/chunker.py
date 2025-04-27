from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
import os

# Add parent directory to path to import loader
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from layers._01_data_ingestion.loader import load_and_preprocess_faq_data

class Chunking:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk documents based on size and overlap"""
        all_chunks = []
        for doc in documents:
            chunks = self.text_splitter.split_documents([doc])
            # Preserve metadata for each chunk
            for chunk in chunks:
                chunk.metadata.update(doc.metadata)
            all_chunks.extend(chunks)
        return all_chunks

if __name__ == "__main__":
    print("Testing Chunking functionality...")
    
    try:
        # Load test data
        print("\nLoading test data...")
        documents = load_and_preprocess_faq_data()
        print(f"Loaded {len(documents)} documents")
        
        # Initialize chunker with custom parameters
        chunker = Chunking(chunk_size=500, chunk_overlap=100)
        
        # Test chunking
        print("\nChunking documents...")
        chunked_docs = chunker.chunk_documents(documents)
        
        # Print results
        print(f"\nTotal chunks created: {len(chunked_docs)}")
        print("\nSample chunks:")
        for i, chunk in enumerate(chunked_docs[:3]):  # Show first 3 chunks
            print(f"\nChunk {i+1}:")
            print(f"Content: {chunk.page_content}")
            print(f"Length: {len(chunk.page_content)}")
            print(f"Metadata: {chunk.metadata}")
            
        # Print statistics
        print("\nChunking Statistics:")
        print(f"Original documents: {len(documents)}")
        print(f"Total chunks: {len(chunked_docs)}")
        print(f"Average chunks per document: {len(chunked_docs)/len(documents):.2f}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}") 