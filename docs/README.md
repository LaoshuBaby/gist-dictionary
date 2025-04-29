# DOCUMENT / 文档 / ドキュメント

## Overview

The server does not store all versions of an entry. However, it writes to a log whenever an entry is created or modified. The log contains all information about an entry and can generate one-line outputs using its method. 

Additionally, a webhook can be triggered if needed. To build a history tree, you can rely on the full log or use the webhook.

服务器不会存储一个条目的所有版本。然而，当一个条目被创建或修改时，服务器会写入日志。日志包含条目的所有信息，并可以通过其方法生成单行输出。

此外，服务器还可以根据需要触发 webhook。如果需要构建历史树，可以依靠完整日志或使用 webhook。

---

## SERVER API

### Endpoints

#### `GET /entry/["all"|condition]`
- Retrieve entries matching the specified condition, or all entries if `"all"` is used.
- 获取符合条件的条目，如果指定 `"all"`，则返回所有条目。

#### `GET /entry/[id]`
- Retrieve the details of a specific entry by its ID.
- 根据 ID 获取指定条目的详细信息。

#### `PUT /entry/create`
- Create a new entry.
- **Responses**:
  - `200`: Entry created successfully.
  - `409`: Entry already exists.
  - `401`: Entry creation failed (no permission or locked).
  - `400`: Server refused for an unknown reason.
  - `***`: Invalid JSON format in the request.

#### `POST /entry/update/[id]`
- Update an existing entry by its ID. Updates must include a version. The version must match the latest version + 1, or the server will reject the request.
- 根据 ID 更新一个已存在的条目。更新必须包含版本号，且版本号必须为最新版本 + 1，否则服务器将拒绝请求。
- **Responses**:
  - `200`: Update successful.
  - `404`: Entry not found on the server.
  - `409`: Server refused to update due to an unknown version.
  - `403`: Attempt to update a historical version.
  - `417`: Attempt to update a future version.
  - `***`: Invalid JSON format in the request.
- **Optional Parameter**:
  - If `--future` is set to `True`, warnings are ignored, and blank versions can be created to bridge the gap between the server and the specified version.
  - 如果设置 `--future` 为 `True`，警告会被忽略，并且可以创建空白版本来填补服务器版本与指定版本之间的空隙。

#### `DELETE /entry/update/[id]`
- 根据 ID 删除条目。请求中必须包含最新版本号。
- Delete an entry by its ID. Must include the latest version in the request.
  - `404`: Entry not found on the server.
  - `401`: Entry creation failed (no permission or locked).
  - `400`: Server refused for an unknown reason.
---

## Notes
- The log and webhook mechanism allows tracking changes and reconstructing version history.



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