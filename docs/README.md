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
