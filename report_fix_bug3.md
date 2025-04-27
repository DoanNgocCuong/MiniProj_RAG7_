# Bug Report: OpenAIEmbeddings Proxy Configuration Error

## Issue Description
The application failed with a `ValidationError` when trying to initialize the `OpenAIEmbeddings` class. The error indicated an unexpected `proxies` argument being passed to the OpenAI client, suggesting interference from proxy settings.

## Error Message
```
pydantic.v1.error_wrappers.ValidationError: 1 validation error for OpenAIEmbeddings 
__root__
  Client.__init__() got an unexpected keyword argument 'proxies' (type=type_error)
```

## Root Cause
The error was caused by proxy settings in the environment that were automatically being passed to the OpenAI client. This is a common issue when:
1. System-wide proxy settings are configured
2. Environment variables for proxies are set
3. The OpenAI client tries to use these settings automatically

## Solution Implemented
Updated the `Embedding` class to:
1. Clear any existing proxy environment variables
2. Explicitly set the HTTP client to None
3. Ensure clean initialization of the OpenAI client

```python
def __init__(self, model_name: str = "text-embedding-ada-002"):
    self.model_name = model_name
    # Clear any existing proxy settings
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    if "https_proxy" in os.environ:
        del os.environ["https_proxy"]
        
    self.embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        # Explicitly set proxy to None
        http_client=None
    )
```

## Testing
The fix was verified by:
1. Running the application with proxy settings in the environment
2. Confirming that the `ValidationError` no longer occurs
3. Verifying that the embeddings are generated correctly

## Prevention
To prevent similar issues in the future:
1. Be aware of system-wide proxy settings
2. Clear proxy settings before initializing OpenAI clients if not needed
3. Use explicit configuration for network settings
4. Document any required proxy configurations in the project documentation

## Additional Notes
If you actually need to use a proxy with OpenAI, you should configure it explicitly using the `http_client` parameter with a properly configured HTTP client instance. 