# Bug Report: OpenAI Client Proxy Configuration Issue

## Issue Description
The application continued to fail with a `ValidationError` related to proxy settings in the OpenAI client, despite previous attempts to fix the issue.

## Error Message
```
ERROR:layers._03_embedding.embedder:Failed to create OpenAI embeddings: 1 validation error for OpenAIEmbeddings
__root__
  Client.__init__() got an unexpected keyword argument 'proxies' (type=type_error)
```

## Root Cause Analysis
The issue was more complex than initially thought:
1. System-wide proxy settings were still being automatically applied
2. The OpenAI client was automatically detecting and using proxy settings
3. Previous solutions didn't fully address all proxy-related environment variables
4. The client initialization needed more explicit control

## Solution Implemented
Implemented a more comprehensive solution:

1. **Environment Cleanup**
```python
proxy_vars = [
    "http_proxy", "https_proxy", 
    "HTTP_PROXY", "HTTPS_PROXY",
    "ALL_PROXY", "all_proxy",
    "no_proxy", "NO_PROXY"
]
for var in proxy_vars:
    if var in os.environ:
        del os.environ[var]
```

2. **Custom Client Creation**
```python
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=None,
    proxies=None
)
```

3. **Explicit Embeddings Configuration**
```python
return OpenAIEmbeddings(
    model=self.model_name,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    client=client,
    http_client=None,
    request_timeout=60,
    max_retries=3
)
```

## Testing
The fix was verified by:
1. Running the application in different environments
2. Testing with and without proxy settings
3. Verifying that embeddings are generated correctly
4. Checking error handling and logging

## Prevention
To prevent similar issues in the future:
1. Always create custom OpenAI clients with explicit configurations
2. Clear all proxy-related environment variables
3. Use explicit error handling and logging
4. Document all environment requirements
5. Consider implementing a configuration management system

## Additional Notes
This solution:
- Provides more control over the OpenAI client
- Handles proxy settings more comprehensively
- Improves error handling and logging
- Makes the system more robust against environment changes 