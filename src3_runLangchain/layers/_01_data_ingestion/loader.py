import json
import re
from typing import List, Tuple
from langchain.schema import Document

class DataIngestion:
    @staticmethod
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
                    "category": item.get("meta_data", {}).get("category", ""),
                    "topic": item.get("meta_data", {}).get("topic", "")
                }
            )
            documents.append(doc)
        return documents

    @staticmethod
    def extract_qa_from_faq(content: str) -> Tuple[str, str]:
        """Extract question and answer from FAQ content"""
        match = re.match(r"Q:\s*(.*?)\s*A:\s*(.*)", content, re.DOTALL)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return "", ""

    @staticmethod
    def preprocess_faq_data(documents: List[Document]) -> List[Document]:
        """Preprocess FAQ data into appropriate format"""
        processed_docs = []
        for doc in documents:
            question, answer = DataIngestion.extract_qa_from_faq(doc.page_content)
            
            question_doc = Document(
                page_content=question,
                metadata={
                    "id": doc.metadata.get("id"),
                    "type": "question",
                    "category": doc.metadata.get("category", ""),
                    "topic": doc.metadata.get("topic", ""),
                    "original_content": doc.page_content
                }
            )
            
            answer_doc = Document(
                page_content=answer,
                metadata={
                    "id": doc.metadata.get("id"),
                    "type": "answer",
                    "category": doc.metadata.get("category", ""),
                    "topic": doc.metadata.get("topic", ""),
                    "original_content": doc.page_content
                }
            )
            
            processed_docs.extend([question_doc, answer_doc])
        return processed_docs 