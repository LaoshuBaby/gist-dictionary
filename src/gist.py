"""
GitHub Gist API wrapper for retrieving and updating gists.

This module provides functions to interact with GitHub Gist API for dictionary storage.
"""
import json
from typing import Optional, Dict, Any

import requests

from log import logger

# Implementation selection
IMPLEMENT = "local"

# Available implementations:
# "local": Custom implementation using requests
# "witherredaway": Third-party library (github-gists from PyPI)


def get_github_headers(auth_token: str) -> Dict[str, str]:
    """
    Create headers for GitHub API requests.
    
    Args:
        auth_token: GitHub authentication token
        
    Returns:
        Dictionary of HTTP headers
    """
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {auth_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_gist(auth_token: str, gist_id: str, file_name: str = "wordbank.json") -> Optional[str]:
    """
    Retrieve a gist from GitHub.
    
    Args:
        auth_token: GitHub authentication token
        gist_id: ID of the gist to retrieve
        file_name: Name of the file to retrieve from the gist
        
    Returns:
        Content of the gist file or None if retrieval failed
        
    Official API: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist
    """
    if IMPLEMENT == "local":
        url = f"https://api.github.com/gists/{gist_id}"
        headers = get_github_headers(auth_token)

        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                gist_metadata = response.json()
                logger.trace(gist_metadata)
                return gist_metadata.get("files", {}).get(file_name, {}).get("content")
            else:
                logger.error(f"Failed to retrieve gist: {response.status_code}")
                logger.warning(response.text)
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving gist: {e}")
            return None
            
    elif IMPLEMENT == "witherredaway":
        import asyncio
        import gists

        async def main_get():
            client = gists.Client()
            gist = await client.get_gist(gist_id)
            return gist

        try:
            return asyncio.run(main_get())
        except Exception as e:
            logger.error(f"Error retrieving gist with witherredaway: {e}")
            return None
    else:
        logger.error(f"Unknown implementation: {IMPLEMENT}")
        return None


def update_gist(
    auth_token: str,
    gist_id: str,
    gist_data: str,
    file_name: str = "wordbank.json",
) -> Optional[int]:
    """
    Update a gist on GitHub.
    
    Args:
        auth_token: GitHub authentication token
        gist_id: ID of the gist to update
        gist_data: New content for the gist file
        file_name: Name of the file to update
        
    Returns:
        HTTP status code or None if update failed
        
    Official API: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#update-a-gist
    """
    if IMPLEMENT == "local":
        url = f"https://api.github.com/gists/{gist_id}"
        headers = get_github_headers(auth_token)

        # Prepare payload
        gist_data_payload = {
            "files": {
                file_name: {
                    "content": gist_data
                }
            }
        }
        
        logger.trace(f"Updating gist with data: {gist_data}")

        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(
                    gist_data_payload,
                    ensure_ascii=False,
                    indent=0,
                    sort_keys=False,
                ),
            )
            
            if response.status_code == 200:
                logger.trace(f"Gist updated successfully: {response.text}")
                return response.status_code
            else:
                logger.error(f"Failed to update gist: {response.status_code}")
                logger.warning(response.text)
                return response.status_code
                
        except Exception as e:
            logger.error(f"Error updating gist: {e}")
            return None
            
    elif IMPLEMENT == "witherredaway":
        # Implementation for witherredaway library would go here
        logger.error("witherredaway implementation for update_gist not implemented")
        return None
    else:
        logger.error(f"Unknown implementation: {IMPLEMENT}")
        return None
