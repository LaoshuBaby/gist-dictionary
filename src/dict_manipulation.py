"""
Dictionary manipulation utilities for entries and tags.

This module provides functions to manipulate dictionary entries and their tags.
"""
import json
from typing import Dict, List, Optional, Union, Any

from dictionary import Dictionary, Entry, EntryCreate
from log import logger


def parse_dictionary(dictionary_data: Union[str, Dict[str, Any]]) -> Dictionary:
    """
    Parse dictionary data from string or dict into a Dictionary object.
    
    Args:
        dictionary_data: Dictionary data as JSON string or dict
        
    Returns:
        Dictionary object
    """
    if isinstance(dictionary_data, str):
        try:
            data = json.loads(dictionary_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse dictionary JSON: {e}")
            return Dictionary()
    else:
        data = dictionary_data
    
    # Create Dictionary object
    dictionary = Dictionary()
    
    # Parse entries
    for entry_data in data.get("wordbank", []):
        try:
            entry = Entry(
                id=entry_data.get("id"),
                word=entry_data.get("word"),
                tags=entry_data.get("tags", [])
            )
            dictionary.wordbank.append(entry)
        except Exception as e:
            logger.error(f"Failed to parse entry: {e}")
    
    return dictionary


def add_entry(dictionary_data: Union[str, Dict[str, Any], Dictionary], 
              word: str, 
              tags: Optional[List[str]] = None) -> str:
    """
    Add a new entry to the dictionary.
    
    Args:
        dictionary_data: Dictionary data as JSON string, dict, or Dictionary object
        word: Word to add
        tags: Optional list of tags
        
    Returns:
        Updated dictionary as JSON string
    """
    # Parse dictionary if needed
    if not isinstance(dictionary_data, Dictionary):
        dictionary = parse_dictionary(dictionary_data)
    else:
        dictionary = dictionary_data
    
    # Create and add entry
    entry = EntryCreate(word=word, tags=tags or [])
    dictionary.add_entry(entry)
    
    # Return updated dictionary
    return dictionary.to_json()


def update_entry_tags(dictionary_data: Union[str, Dict[str, Any], Dictionary],
                      entry_id: str,
                      tags: List[str]) -> str:
    """
    Update tags for a specific entry.
    
    Args:
        dictionary_data: Dictionary data as JSON string, dict, or Dictionary object
        entry_id: ID of the entry to update
        tags: New tags for the entry
        
    Returns:
        Updated dictionary as JSON string
    """
    # Parse dictionary if needed
    if not isinstance(dictionary_data, Dictionary):
        dictionary = parse_dictionary(dictionary_data)
    else:
        dictionary = dictionary_data
    
    # Update entry tags
    updated_entry = dictionary.update_entry_tags(entry_id, tags)
    if not updated_entry:
        logger.warning(f"Entry with ID {entry_id} not found")
    
    # Return updated dictionary
    return dictionary.to_json()


def delete_entry(dictionary_data: Union[str, Dict[str, Any], Dictionary],
                 entry_id: str) -> str:
    """
    Delete an entry from the dictionary.
    
    Args:
        dictionary_data: Dictionary data as JSON string, dict, or Dictionary object
        entry_id: ID of the entry to delete
        
    Returns:
        Updated dictionary as JSON string
    """
    # Parse dictionary if needed
    if not isinstance(dictionary_data, Dictionary):
        dictionary = parse_dictionary(dictionary_data)
    else:
        dictionary = dictionary_data
    
    # Delete entry
    success = dictionary.delete_entry(entry_id)
    if not success:
        logger.warning(f"Entry with ID {entry_id} not found")
    
    # Return updated dictionary
    return dictionary.to_json()