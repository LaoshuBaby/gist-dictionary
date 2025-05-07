"""
FastAPI server entrypoint that registers API routes for the dictionary service.
"""
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from auth import get_api_key, get_token
from const import API_VERSION, DEFAULT_GIST_FILENAME
from db import db
from dictionary import Dictionary, Entry, EntryCreate, TagUpdate
from dict_manipulation import parse_dictionary
from gist import get_gist, update_gist
from log import logger
from utils import get_config

# Create FastAPI app
app = FastAPI(
    title="Gist Dictionary API",
    description="API for managing a dictionary stored in GitHub Gists",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API routes
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to Gist Dictionary API"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

# Protected routes requiring API key
@app.get(f"/{API_VERSION}/dictionary", response_model=Dictionary)
async def get_dictionary(api_key: str = Depends(get_api_key)):
    """
    Get the entire dictionary.
    """
    try:
        # Get configuration
        config = get_config()
        gist_id = config.get("config", {}).get("gist_name")
        if not gist_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gist ID not configured"
            )
        
        # Get GitHub token
        token = get_token()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitHub token not available"
            )
        
        # Get dictionary from Gist
        gist_data = get_gist(token, gist_id, DEFAULT_GIST_FILENAME)
        if not gist_data:
            # Return empty dictionary if no data found
            return Dictionary()
        
        # Parse dictionary
        dictionary = parse_dictionary(gist_data)
        
        # Load dictionary into database
        db.load_dictionary(dictionary)
        
        return dictionary
    except Exception as e:
        logger.error(f"Error retrieving dictionary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving dictionary: {str(e)}"
        )

@app.post(f"/{API_VERSION}/dictionary/entries", response_model=Entry)
async def create_entry(entry: EntryCreate, api_key: str = Depends(get_api_key)):
    """
    Create a new dictionary entry.
    """
    try:
        # Create entry in database
        new_entry = db.create_entry(entry)
        
        # Update Gist
        await update_dictionary_gist()
        
        return new_entry
    except Exception as e:
        logger.error(f"Error creating entry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating entry: {str(e)}"
        )

@app.put(f"/{API_VERSION}/dictionary/entries/{{entry_id}}/tags", response_model=Entry)
async def update_entry_tags(entry_id: str, tag_update: TagUpdate, api_key: str = Depends(get_api_key)):
    """
    Update tags for a dictionary entry.
    """
    try:
        # Update entry tags in database
        updated_entry = db.update_entry_tags(entry_id, tag_update.tags)
        if not updated_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entry with ID {entry_id} not found"
            )
        
        # Update Gist
        await update_dictionary_gist()
        
        return updated_entry
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating entry tags: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating entry tags: {str(e)}"
        )

@app.delete(f"/{API_VERSION}/dictionary/entries/{{entry_id}}")
async def delete_entry(entry_id: str, api_key: str = Depends(get_api_key)):
    """
    Delete a dictionary entry.
    """
    try:
        # Delete entry from database
        success = db.delete_entry(entry_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entry with ID {entry_id} not found"
            )
        
        # Update Gist
        await update_dictionary_gist()
        
        return {"message": f"Entry {entry_id} deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting entry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting entry: {str(e)}"
        )

async def update_dictionary_gist() -> bool:
    """
    Update the dictionary in GitHub Gist.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get configuration
        config = get_config()
        gist_id = config.get("config", {}).get("gist_name")
        if not gist_id:
            logger.error("Gist ID not configured")
            return False
        
        # Get GitHub token
        token = get_token()
        if not token:
            logger.error("GitHub token not available")
            return False
        
        # Get dictionary from database
        dictionary = db.get_dictionary()
        
        # Update Gist
        status_code = update_gist(
            token, 
            gist_id, 
            dictionary.to_json(), 
            DEFAULT_GIST_FILENAME
        )
        
        return status_code == 200
    except Exception as e:
        logger.error(f"Error updating dictionary in Gist: {e}")
        return False
