# PromptLab API Reference

This document provides a comprehensive reference for the PromptLab API, detailing each endpoint, its parameters, expected request and response bodies, and potential error responses.

## Summary of Endpoints

| Method | Endpoint                       | Description                         | Authentication        |
|--------|--------------------------------|-------------------------------------|-----------------------|
| GET    | `/health`                      | Check the API health status         | Not required          |
| GET    | `/prompts`                     | Retrieve a list of prompts          | Not required          |
| GET    | `/prompts/{prompt_id}`         | Retrieve a specific prompt          | Not required          |
| POST   | `/prompts`                     | Create a new prompt                 | Not required          |
| PUT    | `/prompts/{prompt_id}`         | Update an existing prompt           | Not required          |
| PATCH  | `/prompts/{prompt_id}`         | Partially update an existing prompt | Not required          |
| DELETE | `/prompts/{prompt_id}`         | Delete a specific prompt            | Not required          |
| GET    | `/collections`                 | Retrieve a list of collections      | Not required          |
| GET    | `/collections/{collection_id}` | Retrieve a specific collection      | Not required          |
| POST   | `/collections`                 | Create a new collection             | Not required          |
| DELETE | `/collections/{collection_id}` | Delete a specific collection        | Not required          |

---

## Detailed Endpoint Documentation

### GET /health

- **Description:** Check the health status of the API.
- **Response Example:**

```json
{
    "status": "healthy",
    "version": "1.0.0"
}
```

- **Error Responses:** None

### GET /prompts

- **Description:** Retrieve a list of prompts, optionally filtered by collection or search query.
- **Query Parameters:**
  - `collection_id` (Optional, `str`): Filter prompts by collection ID.
  - `search` (Optional, `str`): Search query for filtering prompts by text.
- **Fields:**
  - `id` (Required, `str`)
  - `title` (Required, `str`, minimum length: 1)
  - `content` (Required, `str`, minimum length: 10)
  - `description` (Optional, `str`)
  - `collection_id` (Optional, `str`)
  - `created_at` (Required, `datetime`, ISO 8601)
  - `updated_at` (Required, `datetime`, ISO 8601)
- **Example URL:**
  - `GET /prompts?collection_id=123&search=example`
- **Response Example:**

```json
{
    "prompts": [
        {
            "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
            "title": "Example Title 1",
            "content": "This is a sample prompt content.",
            "description": "A brief description.",
            "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
            "created_at": "2023-10-31T10:00:00Z",
            "updated_at": "2023-10-31T12:00:00Z"
        }
    ],
    "total": 1
}
```

- **Error Responses:**
  - `500 Internal Server Error`: If any error occurs during filtering or retrieval.
    - **Response Example:**

    ```json
    {
        "error": "Internal Server Error",
        "code": 500
    }
    ```

### GET /prompts/{prompt_id}

- **Description:** Retrieve a specific prompt by its ID.
- **Path Parameters:**
  - `prompt_id` (Required, `str`): The unique identifier of the prompt.
- **Response Example:**

```json
{
    "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "title": "Example Title",
    "content": "This is a sample prompt content.",
    "description": "A brief description.",
    "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "created_at": "2023-10-31T10:00:00Z",
    "updated_at": "2023-10-31T12:00:00Z"
}
```

- **Error Responses:**
  - `404 Not Found`: Prompt with given ID not found.
    - **Response Example:**

    ```json
    {
        "error": "Prompt not found",
        "code": 404
    }
    ```

### POST /prompts

- **Description:** Create a new prompt.
- **Request Body:**

```json
{
    "title": "Example Title",
    "content": "This is a sample prompt content.",
    "description": "A brief description.",
    "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e"
}
```

- **Fields:**
  - `title` (Required, `str`, minimum length: 1)
  - `content` (Required, `str`, minimum length: 10)
  - `description` (Optional, `str`)
  - `collection_id` (Required, `str`)
- **Response Example:**

```json
{
    "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "title": "Example Title",
    "content": "This is a sample prompt content.",
    "description": "A brief description.",
    "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "created_at": "2023-10-31T10:00:00Z",
    "updated_at": "2023-10-31T12:00:00Z"
}
```

- **Error Responses:**
  - `400 Bad Request`: If collection ID is invalid.
    - **Response Example:**

    ```json
    {
        "error": "Invalid collection ID",
        "code": 400
    }
    ```

### PUT /prompts/{prompt_id}

- **Description:** Update an existing prompt with new data.
- **Path Parameters:**
  - `prompt_id` (Required, `str`)

- **Request Body:**

```json
{
    "title": "Updated Title",
    "content": "Updated prompt content.",
    "description": "An updated description.",
    "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e"
}
```

- **Fields:**
  - `title` (Required, `str`)
  - `content` (Required, `str`)
  - `description` (Optional, `str`)
  - `collection_id` (Required, `str`)

- **Response Example:**

```json
{
    "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "title": "Updated Title",
    "content": "Updated prompt content.",
    "description": "An updated description.",
    "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "created_at": "2023-10-31T10:00:00Z",
    "updated_at": "2023-10-31T12:00:00Z"
}
```

- **Error Responses:**
  - `404 Not Found`: Prompt not found.
    - **Response Example:**

    ```json
    {
        "error": "Prompt not found",
        "code": 404
    }
    ```
  - `400 Bad Request`: Collection not found.
    - **Response Example:**

    ```json
    {
        "error": "Collection not found",
        "code": 400
    }
    ```

### PATCH /prompts/{prompt_id}

- **Description:** Partially update an existing prompt. Only updates fields provided in the request, leaving others unchanged.
- **Path Parameters:**
  - `prompt_id` (Required, `str`)

- **Request Body:**

```json
{
    "content": "Partially updated content."
}
```

- **Response Example:**

```json
{
    "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "title": "Example Title",
    "content": "Partially updated content.",
    "description": "A brief description.",
    "collection_id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "created_at": "2023-10-31T10:00:00Z",
    "updated_at": "2023-10-31T12:00:00Z"
}
```

- **Error Responses:**
  - `404 Not Found`: Prompt not found.
    - **Response Example:**

    ```json
    {
        "error": "Prompt not found",
        "code": 404
    }
    ```
  - `400 Bad Request`: Collection not found.
    - **Response Example:**

    ```json
    {
        "error": "Collection not found",
        "code": 400
    }
    ```

### DELETE /prompts/{prompt_id}

- **Description:** Delete a prompt by ID.
- **Path Parameters:**
  - `prompt_id` (Required, `str`): The ID of the prompt to delete.
- **Response:** No content
- **Error Responses:**
  - `404 Not Found`: Prompt not found.
    - **Response Example:**

    ```json
    {
        "error": "Prompt not found",
        "code": 404
    }
    ```

### GET /collections

- **Description:** Retrieve a list of all collections.
- **Response Example:**

```json
{
    "collections": [
        {
            "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
            "name": "Example Collection",
            "description": "A brief collection description.",
            "created_at": "2023-10-31T10:00:00Z"
        }
    ],
    "total": 1
}
```

- **Error Responses:** None

### GET /collections/{collection_id}

- **Description:** Retrieve a specific collection by its ID.
- **Path Parameters:**
  - `collection_id` (Required, `str`): The unique identifier of the collection.
- **Response Example:**

```json
{
    "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "name": "Example Collection",
    "description": "A brief collection description.",
    "created_at": "2023-10-31T10:00:00Z"
}
```

- **Error Responses:**
  - `404 Not Found`: Collection not found.
    - **Response Example:**

    ```json
    {
        "error": "Collection not found",
        "code": 404
    }
    ```

### POST /collections

- **Description:** Create a new collection.
- **Request Body:**

```json
{
    "name": "New Collection",
    "description": "Description of the new collection."
}
```

- **Fields:**
  - `name` (Required, `str`)
  - `description` (Optional, `str`)

- **Response Example:**

```json
{
    "id": "e4d909c2-5dcb-40f0-9e92-8c90a58b2f5e",
    "name": "New Collection",
    "description": "Description of the new collection.",
    "created_at": "2023-10-31T10:00:00Z"
}
```

- **Error Responses:** None

### DELETE /collections/{collection_id}

- **Description:** Delete a collection by ID and handle associated prompts.
- **Path Parameters:**
  - `collection_id` (Required, `str`): The ID of the collection to delete.
- **Response:** No content
- **Error Responses:**
  - `404 Not Found`: Collection not found.
    - **Response Example:**

    ```json
    {
        "error": "Collection not found",
        "code": 404
    }
    ```

## Authentication

Currently, PromptLab API does not require authentication for accessing its endpoints.

### Future Authentication Plans
For future implementations, the following authentication methods might be supported:

- **API Key:** Include an API key in the headers for access authentication.
  - Example: `Authorization: Bearer YOUR_API_KEY`

- **OAuth:** Utilize OAuth tokens for secure access.
  - Example Request Header: `Authorization: Bearer OAUTH_TOKEN`

For updates on authentication mechanisms, please check the [API Change Log](api_change_log.md).

## Notes

- **Filters & Queries:**
  - Endpoints like `GET /prompts` allow filtering by `collection_id` and searching by text using `search` query.
  - Example URL: `GET /prompts?collection_id=123&search=example`

- **Sorting:**
  - Prompts are sorted by date in descending order by default.

- **Validation Rules:**
  - Prompt content must have at least 10 characters.



