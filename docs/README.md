# DOCUMENT / 文档 / ドキュメント

## Overview

The server does not store all versions of an entry. However, it writes to a log whenever an entry is created or modified. The log contains all information about an entry and can generate one-line outputs using its method. 

Additionally, a webhook can be triggered if needed. To build a history tree, you can rely on the full log or use the webhook.

---

## SERVER API

### Endpoints

#### `GET /entry/["all"|condition]`
- Retrieve entries matching the specified condition, or all entries if `"all"` is used.

#### `GET /entry/[id]`
- Retrieve the details of a specific entry by its ID.

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
- **Responses**:
  - `200`: Update successful.
  - `404`: Entry not found on the server.
  - `409`: Server refused to update due to an unknown version.
  - `403`: Attempt to update a historical version.
  - `417`: Attempt to update a future version.
  - `***`: Invalid JSON format in the request.
- **Optional Parameter**:
  - If `--future` is set to `True`, warnings are ignored, and blank versions can be created to bridge the gap between the server and the specified version.

#### `DELETE /entry/update/[id]`
- Delete an entry by its ID. Must include the latest version in the request.
  - `404`: Entry not found on the server.
  - `401`: Entry creation failed (no permission or locked).
  - `400`: Server refused for an unknown reason.
---

## Notes
- The log and webhook mechanism allows tracking changes and reconstructing version history.
