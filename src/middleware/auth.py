from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional

# In a real application, this would be stored securely
API_KEYS = {"test_api_key": "admin"}

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )
    
    # Check if the header has the correct format (Bearer <token>)
    if not api_key_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key format. Use 'Bearer <api_key>'",
        )
    
    # Extract the token
    api_key = api_key_header.replace("Bearer ", "")
    
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    
    return api_key