import json
import re
from typing import List, Tuple
from langchain.schema import Document

def load_faq_data(file_path: str) -> List[Document]:
    """Load FAQ data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    documents = []
    for item in data:
        doc = Document(
            page_content=item['content'],
            metadata={
                "id": item.get("id"),
                "feature_tag": item.get("meta_data", {}).get("feature_tag", ""),
                "methods": item.get("meta_data", {}).get("methods", []),
                "application_values": item.get("meta_data", {}).get("application_values", [])
            }
        )
        documents.append(doc)
    return documents

def extract_qa_from_faq(content: str) -> Tuple[str, str]:
    """Extract question and answer from FAQ content"""
    # Since our data doesn't have Q&A format, we'll split by first period
    parts = content.split('.', 1)
    if len(parts) > 1:
        return parts[0].strip(), parts[1].strip()
    return content.strip(), ""

def preprocess_faq_data(documents: List[Document]) -> List[Document]:
    """Preprocess FAQ data into appropriate format"""
    processed_docs = []
    for doc in documents:
        # Split content into parts for better context
        parts = doc.page_content.split('.')
        for i, part in enumerate(parts):
            if part.strip():
                processed_doc = Document(
                    page_content=part.strip(),
                    metadata={
                        "id": doc.metadata.get("id"),
                        "part_index": i,
                        "feature_tag": doc.metadata.get("feature_tag", ""),
                        "methods": doc.metadata.get("methods", []),
                        "application_values": doc.metadata.get("application_values", []),
                        "original_content": doc.page_content
                    }
                )
                processed_docs.append(processed_doc)
    return processed_docs

def load_and_preprocess_faq_data(file_path: str = "data/TinhNangApp.json") -> List[Document]:
    """Load and preprocess FAQ data in one step"""
    documents = load_faq_data(file_path)
    return preprocess_faq_data(documents)

if __name__ == "__main__":
    # Test loading and preprocessing FAQ data
    print("Testing FAQ data loader...")
    
    # Test with sample data
    test_file_path = "data/TinhNangApp.json"
    
    try:
        # Load and preprocess data
        documents = load_and_preprocess_faq_data(test_file_path)
        
        # Print results
        print(f"\nTotal documents loaded: {len(documents)}")
        print("\nSample documents:")
        for i, doc in enumerate(documents[:2]):  # Show first 2 documents
            print(f"\nDocument {i+1}:")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            
        # Test content splitting
        print("\nTesting content splitting:")
        sample_content = "Learn - Gồm có 2 lộ trình chính. Lộ trình giao tiếp và lộ trình từ vựng."
        question, answer = extract_qa_from_faq(sample_content)
        print(f"Sample content: {sample_content}")
        print(f"Extracted part 1: {question}")
        print(f"Extracted part 2: {answer}")
        
    except FileNotFoundError:
        print(f"Error: Test file not found at {test_file_path}")
        print("Please ensure the data directory and test file exist.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the test file")
    except Exception as e:
        print(f"Error during testing: {str(e)}") 