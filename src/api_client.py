import requests
import json
from typing import Dict, Any, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in root directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class LangFlowClient:
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize LangFlow API client
        
        Args:
            api_url (str, optional): API endpoint URL. If not provided, will be read from .env
            api_key (str, optional): API key. If not provided, will be read from .env
        """
        self.api_url = api_url or os.getenv("LANGFLOW_API_URL")
        self.api_key = api_key or os.getenv("LANGFLOW_API_KEY")
        
        if not self.api_url or not self.api_key:
            raise ValueError("API URL and API key must be provided either through constructor or .env file")
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_response_text(self, query: str) -> str:
        """
        Get response text from LangFlow API
        
        Args:
            query (str): Query text
            
        Returns:
            str: Response text
        """
        data = {
            "input_value": query,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
            
        response_data = response.json()
        
        # Extract response text from the nested structure
        try:
            return response_data["outputs"][0]["outputs"][0]["outputs"]["message"]["message"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract response text from API response: {str(e)}")

# Create default client instance
default_client = LangFlowClient()

def main():
    """Test the API client directly"""
    print("=== Testing API Client ===")
    
    # Test default client
    print("\n1. Testing default client:")
    query = "Tài liệu này về điều gì?"
    response = default_client.get_response_text(query)
    print(f"Query: {query}")
    print(f"Response: {response}")
    
    # Test error handling
    print("\n2. Testing error handling:")
    error_response = default_client.get_response_text("")
    print(f"Empty query response: {error_response}")
    
    # Test custom client
    print("\n3. Testing custom client:")
    custom_client = LangFlowClient(
        api_url=default_client.api_url,
        api_key="invalid_key"
    )
    error_response = custom_client.get_response_text(query)
    print(f"Invalid key response: {error_response}")

if __name__ == "__main__":
    main() 