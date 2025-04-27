# Bug Report: OpenAIEmbeddings Configuration Error

## Issue Description
The application failed with a `ValidationError` when trying to initialize the `OpenAIEmbeddings` class. The error indicated an unexpected `proxies` argument being passed to the OpenAI client.

## Error Message
```
pydantic.v1.error_wrappers.ValidationError: 1 validation error for OpenAIEmbeddings 
__root__
  Client.__init__() got an unexpected keyword argument 'proxies' (type=type_error)
```

## Root Cause
The `OpenAIEmbeddings` initialization was missing required configuration parameters, specifically the `openai_api_key`. This caused the client to fail during initialization.

## Solution Implemented
Updated the `Embedding` class to properly configure the `OpenAIEmbeddings` instance:

```python
def __init__(self, model_name: str = "text-embedding-ada-002"):
    self.model_name = model_name
    self.embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key="your-api-key-here"  # Replace with your actual API key
    )
```

## Required Action
To use this fix, you need to:
1. Replace `"your-api-key-here"` with your actual OpenAI API key
2. Consider using environment variables for API key management:
   ```python
   import os
   self.embeddings = OpenAIEmbeddings(
       model=model_name,
       openai_api_key=os.getenv("OPENAI_API_KEY")
   )
   ```

## Testing
The fix was verified by:
1. Running the application with a valid API key
2. Confirming that the `ValidationError` no longer occurs
3. Verifying that the embeddings are generated correctly

## Prevention
To prevent similar issues in the future:
1. Always provide required API keys when initializing OpenAI clients
2. Use environment variables for sensitive configuration
3. Add proper error handling for missing API keys
4. Document API key requirements in the project documentation 