# Bug Report: CustomHybridRetriever Class Initialization Error

## Issue Description
- Error occurs during initialization of CustomHybridRetriever class
- Error message: "TypeError: cannot pickle 'mappingproxy' object"
- Error occurs in Pydantic's deepcopy process when handling class fields

## Root Cause
- Conflict between Pydantic and dataclass field handling
- CustomHybridRetriever inherits from BaseRetriever and uses @dataclass decorator
- Pydantic attempts to pickle fields but fails with mappingproxy object

## Solution
1. Remove @dataclass decorator
2. Convert to regular class with __init__ method
3. Maintain existing logic but change class declaration
4. Use typing annotations for type hints

## Changes Made
- Removed @dataclass decorator from CustomHybridRetriever
- Converted to regular class with explicit __init__ method
- Maintained all existing functionality
- Kept type hints using typing annotations

## Verification
- Class initialization should now work without errors
- All existing functionality remains intact
- Type checking still works as expected

## Impact
- No impact on existing functionality
- Improved class initialization reliability
- Better compatibility with Pydantic and BaseRetriever

## Future Considerations
- Consider adding more comprehensive type checking
- Add input validation in __init__ method
- Consider adding more documentation for class usage 