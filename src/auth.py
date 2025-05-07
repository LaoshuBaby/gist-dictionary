"""
Authentication utilities for GitHub Gist access and API key validation.
"""
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional

from log import logger
from utils import get_github_token

# In a real application, this would be stored securely
API_KEYS = {"test_api_key": "admin"}

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Validate API key from request header.
    
    Args:
        api_key_header: The Authorization header value
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
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


def get_token() -> str:
    """
    Get GitHub token for Gist access.
    
    Returns:
        GitHub token string
    """
    token = get_github_token()
    if token:
        logger.success(f"GitHub token retrieved successfully")
        return token
    
    logger.error("Failed to retrieve GitHub token")
    return ""
