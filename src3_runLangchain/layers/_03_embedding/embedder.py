from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
import os
import logging
import sys
from dotenv import load_dotenv
import openai

# Add parent directory to path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from layers._01_data_ingestion.loader import load_and_preprocess_faq_data
from layers._02_chunking.chunker import Chunking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CustomEmbeddings:
    """Custom embeddings class using direct openai.embeddings"""
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
        # Set API key directly
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        try:
            response = openai.embeddings.create(
                model=self.model,
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Error embedding documents: {str(e)}")
            raise
            
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        try:
            response = openai.embeddings.create(
                model=self.model,
                input=[text]
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error embedding query: {str(e)}")
            raise

class Embedder:
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        """Initialize the embedder with specified model"""
        self.model_name = model_name
        self.embeddings = None
        self._validate_environment()
        
    def _validate_environment(self):
        """Validate that required environment variables are set"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        logger.info("OpenAI API key found in environment")
        
    def create_embeddings(self) -> CustomEmbeddings:
        """Create and return embeddings instance"""
        try:
            logger.info(f"Initializing embeddings with model: {self.model_name}")
            self.embeddings = CustomEmbeddings(model=self.model_name)
            logger.info("Embeddings initialized successfully")
            return self.embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    def create_vector_db(self, documents: List[Document], persist_directory: str = "./chroma_db") -> Chroma:
        """Create vector database from documents"""
        try:
            if not self.embeddings:
                self.create_embeddings()
                
            logger.info(f"Creating vector database with {len(documents)} documents")
            
            # Create Chroma database
            vectordb = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=persist_directory
            )
            
            logger.info(f"Vector database created successfully at {persist_directory}")
            return vectordb
            
        except Exception as e:
            logger.error(f"Error creating vector database: {str(e)}")
            raise

if __name__ == "__main__":
    print("Testing Embedding functionality...")
    
    try:
        # Load and preprocess data
        print("\nLoading and preprocessing data...")
        documents = load_and_preprocess_faq_data()
        print(f"Loaded {len(documents)} documents")
        
        # Chunk documents
        print("\nChunking documents...")
        chunker = Chunking(chunk_size=500, chunk_overlap=100)
        chunked_docs = chunker.chunk_documents(documents)
        print(f"Created {len(chunked_docs)} chunks")
        
        # Initialize embedder
        print("\nInitializing embedder...")
        embedder = Embedder()
        
        # Create vector database
        print("\nCreating vector database...")
        vectordb = embedder.create_vector_db(chunked_docs)
        
        # Test similarity search
        print("\nTesting similarity search...")
        query = "What are the main features of the app?"
        results = vectordb.similarity_search(query, k=3)
        
        print(f"\nSearch results for query: '{query}'")
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise