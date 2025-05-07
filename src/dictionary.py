"""
Dictionary data models for entries and wordbank.

This module defines Pydantic models for dictionary entries and related operations.
"""
import json
import uuid
from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


class EntryBase(BaseModel):
    """
    Base model for dictionary entries.
    """
    word: str
    tags: Optional[List[str]] = Field(default_factory=list)


class EntryCreate(EntryBase):
    """
    Model for creating new dictionary entries.
    """
    pass


class Entry(EntryBase):
    """
    Complete dictionary entry model with ID.
    """
    id: str
    
    @classmethod
    def create(cls, word: str, tags: Optional[List[str]] = None) -> "Entry":
        """
        Create a new Entry with a generated UUID.
        
        Args:
            word: The word for the entry
            tags: Optional list of tags
            
        Returns:
            New Entry instance
        """
        return cls(
            id=str(uuid.uuid4()),
            word=word,
            tags=tags or []
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entry to a dictionary.
        
        Returns:
            Dictionary representation of the entry
        """
        return {
            "id": self.id,
            "word": self.word,
            "tags": self.tags
        }
    
    def to_json(self) -> str:
        """
        Convert the entry to a JSON string.
        
        Returns:
            JSON string representation of the entry
        """
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            indent=0,
            sort_keys=False
        )


class Dictionary(BaseModel):
    """
    Model for the complete dictionary (collection of entries).
    """
    wordbank: List[Entry] = Field(default_factory=list)
    
    def add_entry(self, entry: Union[Entry, EntryCreate]) -> Entry:
        """
        Add a new entry to the dictionary.
        
        Args:
            entry: Entry to add
            
        Returns:
            The added entry with ID
        """
        if isinstance(entry, EntryCreate):
            new_entry = Entry.create(word=entry.word, tags=entry.tags)
        else:
            new_entry = entry
            
        self.wordbank.append(new_entry)
        return new_entry
    
    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """
        Get an entry by ID.
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            Entry if found, None otherwise
        """
        for entry in self.wordbank:
            if entry.id == entry_id:
                return entry
        return None
    
    def update_entry_tags(self, entry_id: str, tags: List[str]) -> Optional[Entry]:
        """
        Update tags for an entry.
        
        Args:
            entry_id: ID of the entry to update
            tags: New tags for the entry
            
        Returns:
            Updated entry if found, None otherwise
        """
        entry = self.get_entry(entry_id)
        if entry:
            entry.tags = tags
            return entry
        return None
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete an entry by ID.
        
        Args:
            entry_id: ID of the entry to delete
            
        Returns:
            True if entry was deleted, False otherwise
        """
        for i, entry in enumerate(self.wordbank):
            if entry.id == entry_id:
                self.wordbank.pop(i)
                return True
        return False
    
    def to_json(self) -> str:
        """
        Convert the dictionary to a JSON string.
        
        Returns:
            JSON string representation of the dictionary
        """
        return json.dumps(
            {"wordbank": [entry.to_dict() for entry in self.wordbank]},
            ensure_ascii=False,
            indent=2,
            sort_keys=False
        )


class TagUpdate(BaseModel):
    """
    Model for updating tags on an entry.
    """
    tags: List[str]
