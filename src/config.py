"""
Configuration management for the gist-dictionary application.
"""
from typing import Dict, Any

from log import logger
from utils import get_config, get_config_path, write_json_file


def set_config(new_config: Dict[str, Any]) -> bool:
    """
    Update the configuration file with new settings.
    
    Args:
        new_config: Dictionary containing the new configuration
        
    Returns:
        True if successful, False otherwise
    """
    return write_json_file(get_config_path(), new_config)


def init_config() -> Dict[str, Any]:
    """
    Initialize the configuration.
    
    This function checks if the configuration is valid and prompts the user
    to fill in missing information if needed.
    
    Returns:
        Dictionary containing the configuration
    """
    config = get_config()
    
    # Check if config has required fields
    if not config.get("GH_TOKEN") or not config.get("config", {}).get("gist_name"):
        logger.warning("Configuration is incomplete. Please set your GitHub token and Gist name.")
    
    return config
