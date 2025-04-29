# API Design Documentation

## Overview
This document outlines the API endpoints, request/response formats, and status codes for our RESTful API service.

## Base URL
`/api/v1`

## Authentication
All endpoints require a valid API key to be included in the request header:
```
Authorization: Bearer <api_key>
```

## Endpoints

### Users

#### GET /users
Retrieves a list of all users.

**Response:**
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "users": [
    {
      "id": "string",
      "username": "string",
      "email": "string",
      "created_at": "string (ISO 8601 date format)",
      "updated_at": "string (ISO 8601 date format)"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number"
}
```

#### GET /users/{id}
Retrieves a specific user by ID.

**Parameters:**
- id (path): User ID

**Response:**
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "string (ISO 8601 date format)",
  "updated_at": "string (ISO 8601 date format)"
}
```

#### POST /users
Creates a new user.

**Request:**
- Content-Type: application/json
- Body:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**
- Status Code: 201 Created
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "string (ISO 8601 date format)",
  "updated_at": "string (ISO 8601 date format)"
}
```

#### PUT /users/{id}
Updates an existing user.

**Parameters:**
- id (path): User ID

**Request:**
- Content-Type: application/json
- Body:
```json
{
  "username": "string",
  "email": "string"
}
```

**Response:**
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "string (ISO 8601 date format)",
  "updated_at": "string (ISO 8601 date format)"
}
```

#### DELETE /users/{id}
Deletes a user.

**Parameters:**
- id (path): User ID

**Response:**
- Status Code: 204 No Content

### Products

#### GET /products
Retrieves a list of all products.

**Response:**
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "products": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "price": "number",
      "created_at": "string (ISO 8601 date format)",
      "updated_at": "string (ISO 8601 date format)"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number"
}
```

#### GET /products/{id}
Retrieves a specific product by ID.

**Parameters:**
- id (path): Product ID

**Response:**
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price": "number",
  "created_at": "string (ISO 8601 date format)",
  "updated_at": "string (ISO 8601 date format)"
}
```

#### POST /products
Creates a new product.

**Request:**
- Content-Type: application/json
- Body:
```json
{
  "name": "string",
  "description": "string",
  "price": "number"
}
```

**Response:**
- Status Code: 201 Created
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price": "number",
  "created_at": "string (ISO 8601 date format)",
  "updated_at": "string (ISO 8601 date format)"
}
```

#### PUT /products/{id}
Updates an existing product.

**Parameters:**
- id (path): Product ID

**Request:**
- Content-Type: application/json
- Body:
```json
{
  "name": "string",
  "description": "string",
  "price": "number"
}
```

**Response:**
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price": "number",
  "created_at": "string (ISO 8601 date format)",
  "updated_at": "string (ISO 8601 date format)"
}
```

#### DELETE /products/{id}
Deletes a product.

**Parameters:**
- id (path): Product ID

**Response:**
- Status Code: 204 No Content

## Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - The request was successful |
| 201 | Created - A new resource was successfully created |
| 204 | No Content - The request was successful but there is no representation to return |
| 400 | Bad Request - The request could not be understood or was missing required parameters |
| 401 | Unauthorized - Authentication failed or user does not have permissions |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Request could not be completed due to a conflict |
| 422 | Unprocessable Entity - The request was well-formed but was unable to be followed due to semantic errors |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - An unexpected error occurred on the server |
| 503 | Service Unavailable - The server is currently unavailable |