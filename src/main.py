import uvicorn
import os

from server import app


def main():
    """
    Run the FastAPI application with uvicorn
    """
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 12000))
    
    # Run the server
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
