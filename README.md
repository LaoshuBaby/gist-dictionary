# RESTful API Implementation

This project implements a RESTful API service based on the API design documentation in `/docs/api_design.md`.

## Features

- User management (CRUD operations)
- Product management (CRUD operations)
- Authentication using API keys
- Error handling with appropriate status codes
- Pagination for list endpoints

## API Documentation

The API is documented using OpenAPI and can be accessed at `/docs` when the server is running.

## Endpoints

### Base URL

`/api/v1`

### Users

- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{id}` - Get a specific user
- `POST /api/v1/users` - Create a new user
- `PUT /api/v1/users/{id}` - Update a user
- `DELETE /api/v1/users/{id}` - Delete a user

### Products

- `GET /api/v1/products` - Get all products
- `GET /api/v1/products/{id}` - Get a specific product
- `POST /api/v1/products` - Create a new product
- `PUT /api/v1/products/{id}` - Update a product
- `DELETE /api/v1/products/{id}` - Delete a product

## Authentication

All endpoints require authentication using an API key in the Authorization header:

```
Authorization: Bearer <api_key>
```

## Status Codes

The API uses standard HTTP status codes to indicate the success or failure of requests:

- 200 OK - The request was successful
- 201 Created - A new resource was successfully created
- 204 No Content - The request was successful but there is no representation to return
- 400 Bad Request - The request could not be understood or was missing required parameters
- 401 Unauthorized - Authentication failed or user does not have permissions
- 403 Forbidden - Access denied
- 404 Not Found - Resource not found
- 409 Conflict - Request could not be completed due to a conflict
- 422 Unprocessable Entity - The request was well-formed but was unable to be followed due to semantic errors
- 429 Too Many Requests - Rate limit exceeded
- 500 Internal Server Error - An unexpected error occurred on the server
- 503 Service Unavailable - The server is currently unavailable

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python src/main.py
   ```

3. Access the API at http://localhost:12000

## Development

This project uses FastAPI for the API implementation. The code is organized as follows:

- `src/main.py` - Entry point for the application
- `src/server.py` - FastAPI application setup
- `src/db.py` - In-memory database implementation
- `src/models/` - Pydantic models for request/response validation
- `src/routes/` - API route handlers
- `src/middleware/` - Middleware components (authentication, etc.)

## License

MIT
