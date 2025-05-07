"""
Common utility functions and shared code for the gist-dictionary application.
"""
import json
import os
from typing import Dict, Any, Optional

from const import CONFIG_FILENAME, ROOT_PATH
from log import logger

def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dict containing the parsed JSON data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except Exception as e:
        logger.error(f"Error reading JSON file {file_path}: {e}")
        return {}

def write_json_file(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        data: Dictionary to be written as JSON
        indent: Indentation level for the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=indent,
                    sort_keys=False,
                )
            )
        return True
    except Exception as e:
        logger.error(f"Error writing JSON file {file_path}: {e}")
        return False

def get_config_path() -> str:
    """
    Get the path to the configuration file.
    
    Returns:
        Absolute path to the configuration file
    """
    return os.path.join(ROOT_PATH, "config", CONFIG_FILENAME)

def get_config() -> Dict[str, Any]:
    """
    Get the configuration from the config file.
    
    Returns:
        Dictionary containing the configuration
    """
    return read_json_file(get_config_path())

def get_github_token() -> Optional[str]:
    """
    Get the GitHub token from environment variables or config file.
    
    Returns:
        GitHub token string or None if not found
    """
    # Try environment variables first (GitHub CLI standard)
    gh_token = os.environ.get("GH_TOKEN")
    if gh_token:
        return gh_token
        
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        return github_token
    
    # Fall back to config file
    config = get_config()
    return config.get("GH_TOKEN")