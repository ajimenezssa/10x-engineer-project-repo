# PromptLab

**Your AI Prompt Engineering Platform, providing tools to manage, test, and organize AI prompts, enhancing efficiency for engineering teams**

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation / Development Setup](#installation--development-setup)
- [Quick Start](#quick-start)
- [API Endpoint Summary](#api-endpoint-summary)
- [Contributing](#contributing)

## Overview

PromptLab is an internal tool for AI engineers to **store, organize, and manage their prompts**. Think of it as a "Postman for Prompts" — a professional workspace where teams can:

- 📝 Store prompt templates with variables (`{{input}}`, `{{context}}`)
- 📁 Organize prompts into collections
- 🏷️ Tag and search prompts
- 📜 Track version history
- 🧪 Test prompts with sample inputs

PromptLab is an API server utilizing FastAPI, aimed at the efficient management of AI prompts. Designed as a "Postman for Prompts," it provides a RESTful API that allows AI engineers to store, organize, tag, search, and manage the lifecycle of AI prompts.

... rest of the content ...

The platform exists to facilitate prompt engineering processes by offering a structured environment to handle prompts programmatically. It is intended for AI engineers and development teams dealing with prompt engineering, particularly those needing a programmatic approach to managing prompt data effectively.

### Purpose and Scope

PromptLab is designed to solve the problem of managing and organizing AI prompts efficiently. It addresses the need for a systematic approach to store, retrieve, and manipulate AI-based prompt data through a structured API.

It intentionally does not address user authentication, external integrations, or machine learning model integrations, focusing solely on prompt management functionalities.

## Features

### Current Features

- **Prompt Management**:
  - **CRUD Operations**: Create, view, update, and delete AI prompts via RESTful API.
  - **Filter and Search**: Expedite prompt retrieval through filtering and text-based searches.

- **Collection Organization**:
  - **Manage Collections**: Create and manage collections for streamlined prompt organization.
  - **Automatic Orphan Handling**: Properly manage prompts when their collection is removed.

### Planned Features

- **Tagging and Versioning**: Enhance prompt metadata with tags and maintain version history.
- **Prompt Testing**: Simulate inputs to assess prompt effectiveness before deployment.

## Prerequisites

To run PromptLab locally, ensure you have the following prerequisites:

- **Supported Operating Systems**: PromptLab can be run on Linux, macOS, and Windows.
- **Programming Language**: Python 3.10+
- **Package Manager**: pip (Python package installer)
- **Dependencies**:
  - FastAPI == 0.109.0
  - Uvicorn == 0.27.0
  - Pydantic == 2.5.3
  - Pytest == 7.4.4 (for testing purposes)
  - Pytest-cov == 4.1.0 (for test coverage)
  - HTTPX == 0.26.0 (for making HTTP requests during testing)

## Installation / Development Setup

Set up your local development environment for PromptLab by following the steps below:

### Python Environment Setup

1. **Create a Virtual Environment**

   Navigate to the project root and create a virtual environment to manage dependencies:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**

   Activate your environment to ensure all installs are confined within it:

   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\\venv\\Scripts\\activate
     ```

3. **Install Python Dependencies**

   With the virtual environment activated, proceed to install the necessary packages:

   ```bash
   pip install -r backend/requirements.txt
   ```

### Backend Server Setup

1. **Initialize the Server**

   Launch the backend server using Uvicorn:

   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Node.js Setup (For Future Frontend Development)

Ensure Node.js and npm are ready for potential frontend development:

- Confirm Node.js installation:
  ```bash
  node -v
  ```

- Confirm npm (Node Package Manager) is available:
  ```bash
  npm -v
  ```

These steps will establish a working environment for PromptLab's backend development. Frontend setup details will be introduced along with future project phases.

## Quick Start

Follow these steps to get the backend server up and running:

1. **Setup Python Environment**
   - Ensure your virtual environment is activated. If not yet set up, refer to the Installation section for guidance.

2. **Install Dependencies**
   - With the virtual environment activated, install the required packages:
     ```bash
     pip install -r backend/requirements.txt
     ```

3. **Start the Server**
   - Launch the FastAPI server using Uvicorn:
     ```bash
     uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
     ```
   - **Note**: The `--reload` flag enables hot reload, automatically restarting the server whenever you make code changes. This is useful for development environments.

4. **Access API Documentation**
   - Open your web browser and navigate to the API documentation:
     - [http://localhost:8000/docs]

5. **Test an API Endpoint**
   - Use a tool like `httpx` to test the GET `/prompts` endpoint:
     ```bash
     http GET http://localhost:8000/prompts
     ```

These steps will get you started with the backend server of PromptLab. For more detailed setup instructions and additional context, refer to the rest of the README.

## API Endpoint Summary

| HTTP Method | Endpoint Path        | Description                                            | Example Request                            | Example Response                             | Error Responses                |
|-------------|----------------------|--------------------------------------------------------|--------------------------------------------|----------------------------------------------|--------------------------------|
| GET         | `/health`            | Perform a health check on the API.                     | `curl -X GET http://localhost:8000/health` | `{ "status": "healthy", "version": "1.0.0" }` | `status` (string): health status; `version` (string): API version. | None                           |
| GET         | `/prompts`           | Retrieve a list of prompts, optionally filtered.       | `curl -X GET http://localhost:8000/prompts` | `{ "prompts": [...], "total": 10 }`          | `prompts` (array): list of prompt objects; `total` (int): total prompts count. | None                           |
| GET         | `/prompts/{id}`      | Fetch a single prompt by its ID.                       | `curl -X GET http://localhost:8000/prompts/1` | `{ "id": "1", "title": "Example", "content": "..."}` | `id` (string): prompt identifier; `title` (string): prompt title; `content` (string): prompt content. | 404 if not found              |
| POST        | `/prompts`           | Create a new prompt.                                   | `curl -X POST -H "Content-Type: application/json" -d '{"title": "New", "content": "..." }' http://localhost:8000/prompts` | `{ "id": "1", "title": "New", "content": "..."}` | `id` (string): created prompt ID; `title` (string): prompt title; `content` (string): prompt content. | 400 if collection not found   |
| PUT         | `/prompts/{id}`      | Replace an existing prompt.                            | `curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated", "content": "..." }' http://localhost:8000/prompts/1` | `{ "id": "1", "title": "Updated", "content": "..."}` | `id` (string): prompt ID; `title` (string): updated title; `content` (string): updated content. | 404 if not found; 400 if collection not found |
| PATCH       | `/prompts/{id}`      | Partially update fields of an existing prompt.         | `curl -X PATCH -H "Content-Type: application/json" -d '{"title": "Partial" }' http://localhost:8000/prompts/1` | `{ "id": "1", "title": "Partial", "content": "..."}` | `id` (string): prompt ID; `title` (string): updated title; `content` (string): existing content. | 404 if not found; 400 if collection not found |
| DELETE      | `/prompts/{id}`      | Delete a prompt by its ID.                             | `curl -X DELETE http://localhost:8000/prompts/1` | `204 No Content`                              | `204`: no content on success. | 404 if not found              |
| GET         | `/collections`       | Retrieve a list of all collections.                    | `curl -X GET http://localhost:8000/collections` | `{ "collections": [...], "total": 5 }`       | `collections` (array): list of collection objects; `total` (int): total collections count. | None                           |
| GET         | `/collections/{id}`  | Fetch a specific collection by its ID.                 | `curl -X GET http://localhost:8000/collections/1` | `{ "id": "1", "name": "Collection", "description": "..."}` | `id` (string): collection ID; `name` (string): collection name; `description` (string): collection details. | 404 if not found              |
| POST        | `/collections`       | Create a new collection.                               | `curl -X POST -H "Content-Type: application/json" -d '{"name": "New Collection" }' http://localhost:8000/collections` | `{ "id": "1", "name": "New Collection", "description": "..."}` | `id` (string): new collection ID; `name` (string): collection name; `description` (string): collection details. | None                           |
| DELETE      | `/collections/{id}`  | Delete a collection by its ID.                         | `curl -X DELETE http://localhost:8000/collections/1` | `204 No Content`                              | `204`: no content on success. | 404 if not found              |

## Contributing

We welcome contributions from the community! Please follow these guidelines to ensure a smooth contribution process.

### Reporting Bugs
- **Check Issues First**: Before reporting, check if the issue has already been reported in the [Issues](../../issues) section.
- **New Bug Report**: If it's a new issue, create a detailed report with steps to reproduce, expected vs. actual behavior, and logs if applicable.

### Proposing Features
- **Feature Request**: Start a discussion in the [Issues](../../issues) section. Clearly explain the proposed feature, its benefits, and any potential drawbacks.
- **Discussion**: Engage with maintainers and the community to refine and prioritize the feature proposal.

### Development Workflow
1. **Branching Strategy**: 
   - Create a feature branch: `feature/<feature-name>`, e.g., `feature/add-user-auth`.
   - For bug fixes, create a branch: `bugfix/<bug-name>`, e.g., `bugfix/fix-login-error`.
   - Use the `dev` branch for ongoing development.

2. **Code Style**:
   - Follow PEP8 standards for Python code.
   - Include descriptive docstrings for all public functions and classes.

3. **Testing**:
   - Write tests using `pytest`.
   - Run all tests with `pytest`.
   - Run specific tests with: `pytest -k <test-name>`.

4. **Commit Messages**:
   - Use Conventional Commits, e.g., `feat: add user authentication` or `fix: correct login issue`.

### Pull Request Process
- **Include in PR**:
  - A clear description of changes.
  - Any related issue numbers.
  - Relevant tests and documentation updates.

- **Example PR Checklist**:
  - [ ] Tests added/updated to cover changes
  - [ ] Documentation updated where necessary
  - [ ] All CI checks pass
  - [ ] Reviewed by at least one team member

- **Review Process**:
  - Submit PRs against the `dev` branch.
  - Assign a maintainer or team member for review.

- **Review Requirements**:
  - All CI checks must pass before merging.
  - An approval from at least one reviewer is required.

### Recommended Tools
- **Linters and Formatters**:
  - Use `pylint` for linting.
  - Use `black` for automatic code formatting.

- **IDE Extensions**:
  - Consider Python extensions for Visual Studio Code or PyCharm to enhance your development environment.