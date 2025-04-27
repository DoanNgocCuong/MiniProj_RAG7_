import os
from flashrag import FlashRAG
from flashrag.retriever import IndexBuilder
from flashrag.utils import load_jsonl
import json

class SimpleRAGPipeline:
    def __init__(self, config_path="config.yaml"):
        """
        Initialize the RAG pipeline with FlashRAG
        """
        self.rag = FlashRAG.from_config(config_path)
        
    def process_pdf(self, pdf_path, output_jsonl="corpus.jsonl"):
        """
        Process PDF file and convert to JSONL format for FlashRAG
        """
        # TODO: Implement PDF processing
        # For now, create a dummy JSONL file
        with open(output_jsonl, 'w', encoding='utf-8') as f:
            json.dump({"id": "doc1", "contents": "Sample content from PDF"}, f)
        return output_jsonl

    def build_index(self, corpus_path, index_dir="indexes"):
        """
        Build index using FlashRAG's IndexBuilder
        """
        builder = IndexBuilder(
            retrieval_method="e5",
            model_path="intfloat/e5-base-v2",
            corpus_path=corpus_path,
            save_dir=index_dir
        )
        builder.build()
        return index_dir

    def query(self, question, top_k=3):
        """
        Query the RAG system
        """
        result = self.rag.query(
            question=question,
            top_k=top_k
        )
        return result

def main():
    # Initialize pipeline
    pipeline = SimpleRAGPipeline()
    
    # Process PDF and build index
    pdf_path = "sample.pdf"  # Replace with your PDF path
    corpus_path = pipeline.process_pdf(pdf_path)
    index_dir = pipeline.build_index(corpus_path)
    
    # Example query
    question = "What is the main topic of the document?"
    result = pipeline.query(question)
    
    print("Query:", question)
    print("Answer:", result['answer'])
    print("Retrieved documents:", result['retrieved_documents'])

if __name__ == "__main__":
    main() 