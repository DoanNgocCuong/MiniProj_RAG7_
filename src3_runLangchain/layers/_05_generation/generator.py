"""
This module helps generate answers using AI models.
It combines retrieved documents with user questions to create good answers.
"""

from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class AnswerGenerator:
    """
    A class that helps generate answers using AI models.
    
    This class can:
    - Combine documents with questions
    - Use AI models to generate answers
    - Format answers nicely
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ):
        """
        Start the AnswerGenerator with optional model settings.
        
        Args:
            model_name: Name of the AI model to use
            temperature: How creative the answers should be (0.0 to 1.0)
            
        Example:
            >>> generator = AnswerGenerator(model_name="gpt-4")
            >>> answer = generator.generate_answer("What is RAG?", documents)
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that answers questions based on the given context.
            If you don't know the answer, say you don't know.
            Use only the information from the context to answer.
            Keep your answers clear and simple."""),
            ("human", """Context: {context}
            
            Question: {question}
            
            Answer:""")
        ])
        
        # Create the chain
        self.chain = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def format_context(self, documents: List[Document]) -> str:
        """
        Combine documents into a single context string.
        
        Args:
            documents: List of documents to combine
            
        Returns:
            Combined context as a string
            
        Example:
            >>> context = generator.format_context(documents)
            >>> print(f"Combined {len(documents)} documents into context")
        """
        return "\n\n".join(doc.page_content for doc in documents)
    
    def generate_answer(
        self,
        question: str,
        documents: List[Document],
        format_context: bool = True
    ) -> str:
        """
        Generate an answer using the AI model.
        
        Args:
            question: The question to answer
            documents: List of relevant documents
            format_context: Whether to format the context (default: True)
            
        Returns:
            The generated answer
            
        Example:
            >>> answer = generator.generate_answer("What is RAG?", documents)
            >>> print(f"Generated answer: {answer}")
        """
        if format_context:
            context = self.format_context(documents)
        else:
            context = documents[0].page_content if documents else ""
            
        return self.chain.invoke({
            "context": context,
            "question": question
        })
    
    def generate_answer_with_sources(
        self,
        question: str,
        documents: List[Document]
    ) -> Dict[str, Any]:
        """
        Generate an answer with source information.
        
        Args:
            question: The question to answer
            documents: List of relevant documents
            
        Returns:
            Dictionary with answer and sources
            
        Example:
            >>> result = generator.generate_answer_with_sources("What is RAG?", documents)
            >>> print(f"Answer: {result['answer']}")
            >>> print(f"Sources: {result['sources']}")
        """
        answer = self.generate_answer(question, documents)
        
        # Extract sources from document metadata
        sources = []
        for doc in documents:
            if "source" in doc.metadata:
                sources.append(doc.metadata["source"])
                
        return {
            "answer": answer,
            "sources": list(set(sources))  # Remove duplicates
        }

if __name__ == "__main__":
    """
    This part runs when you run this file directly.
    It shows examples of how to use the AnswerGenerator class.
    """
    from langchain_core.documents import Document
    
    # Create sample documents
    sample_docs = [
        Document(
            page_content="RAG stands for Retrieval-Augmented Generation. It combines retrieval of relevant documents with language model generation.",
            metadata={"source": "test1"}
        ),
        Document(
            page_content="RAG helps language models provide more accurate and up-to-date answers by using external knowledge.",
            metadata={"source": "test2"}
        )
    ]
    
    # Test basic answer generation
    print("\nTesting basic answer generation...")
    try:
        generator = AnswerGenerator()
        answer = generator.generate_answer("What is RAG?", sample_docs)
        print(f"Generated answer: {answer}")
    except Exception as e:
        print(f"Basic generation test failed: {e}")
    
    # Test answer with sources
    print("\nTesting answer with sources...")
    try:
        result = generator.generate_answer_with_sources("What is RAG?", sample_docs)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
    except Exception as e:
        print(f"Source generation test failed: {e}")
    
    # Test with different model
    print("\nTesting with different model...")
    try:
        generator = AnswerGenerator(model_name="gpt-4", temperature=0.5)
        answer = generator.generate_answer("What is RAG?", sample_docs)
        print(f"Generated answer with GPT-4: {answer}")
    except Exception as e:
        print(f"Model test failed: {e}")
