"""
In-memory database for dictionary entries.

This module provides an in-memory database implementation for dictionary entries.
"""
from typing import Dict, List, Optional

from dictionary import Dictionary, Entry, EntryCreate
from log import logger


class DictionaryDB:
    """
    In-memory database for dictionary entries.
    """
    def __init__(self):
        """
        Initialize an empty dictionary database.
        """
        self.dictionary = Dictionary()
        self.entries: Dict[str, Entry] = {}
    
    def load_dictionary(self, dictionary: Dictionary) -> None:
        """
        Load a dictionary into the database.
        
        Args:
            dictionary: Dictionary to load
        """
        self.dictionary = dictionary
        self.entries = {entry.id: entry for entry in dictionary.wordbank}
        logger.info(f"Loaded dictionary with {len(self.entries)} entries")
    
    def get_dictionary(self) -> Dictionary:
        """
        Get the current dictionary.
        
        Returns:
            Current dictionary
        """
        return self.dictionary
    
    def get_entries(self, skip: int = 0, limit: int = 100) -> List[Entry]:
        """
        Get a list of entries with pagination.
        
        Args:
            skip: Number of entries to skip
            limit: Maximum number of entries to return
            
        Returns:
            List of entries
        """
        return list(self.entries.values())[skip:skip + limit]
    
    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """
        Get an entry by ID.
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            Entry if found, None otherwise
        """
        return self.entries.get(entry_id)
    
    def create_entry(self, entry: EntryCreate) -> Entry:
        """
        Create a new entry.
        
        Args:
            entry: Entry to create
            
        Returns:
            Created entry with ID
        """
        new_entry = self.dictionary.add_entry(entry)
        self.entries[new_entry.id] = new_entry
        logger.info(f"Created entry: {new_entry.word}")
        return new_entry
    
    def update_entry_tags(self, entry_id: str, tags: List[str]) -> Optional[Entry]:
        """
        Update tags for an entry.
        
        Args:
            entry_id: ID of the entry to update
            tags: New tags for the entry
            
        Returns:
            Updated entry if found, None otherwise
        """
        updated_entry = self.dictionary.update_entry_tags(entry_id, tags)
        if updated_entry:
            self.entries[entry_id] = updated_entry
            logger.info(f"Updated tags for entry: {updated_entry.word}")
        return updated_entry
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete an entry.
        
        Args:
            entry_id: ID of the entry to delete
            
        Returns:
            True if entry was deleted, False otherwise
        """
        if self.dictionary.delete_entry(entry_id):
            if entry_id in self.entries:
                del self.entries[entry_id]
                logger.info(f"Deleted entry with ID: {entry_id}")
                return True
        return False


# Create a singleton instance
db = DictionaryDB()