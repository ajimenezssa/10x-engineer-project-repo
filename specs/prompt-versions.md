# Prompt Version Specification

## Overview

The prompt versioning feature in the PromptLab API is designed to provide robust version control capabilities for managing the lifecycle of prompts within the system. This feature offers a structured approach to track modifications, compare changes across different versions, and ensure better management of prompts' evolution over time.

### Key Benefits:

- **History Tracking:**
  - Each modification to a prompt is recorded, creating a comprehensive history that provides insights into how the content has evolved. Users can easily navigate through previous versions to understand changes and the reasoning behind them, fostering transparency and informed decision-making.

- **Rollback Capability:**
  - Versioning allows users to revert to any previous state of a prompt, ensuring that unintended changes or errors can be quickly corrected. This rollback capability provides a powerful safeguard against accidental data loss or undesirable edits.

- **Auditability:**
  - The versioning system enhances the auditability of the content by maintaining precise records of all changes. This facilitates accountability and compliance by providing a clear, accessible trail of all updates and modifications made over time.

- **Comparison and Collaboration:**
  - Users can compare different versions of a prompt to spot differences and assess the impact of changes. This is particularly beneficial in collaborative environments where multiple contributors might propose edits, as it helps in maintaining consistency and agreement on final content.

This feature enriches the PromptLab API's functionality, making it a valuable tool for developers and teams who rely on consistent and editable prompt designs to meet dynamic content requirements. By incorporating prompt versioning, users gain better control and flexibility, ensuring the highest quality and reliability of their prompt data.

### User Stories

1. **As a user, I want to view the version history of a prompt, so that I can track changes over time.**
   - **Acceptance Criteria:**
     - Given a prompt with multiple versions, when I navigate to the version history page, then I should see a list of all versions in chronological order.
     - Each version entry should display the version number, creation date, and a brief description of changes if available.

2. **As a user, I want to rollback a prompt to a previous version, so that I can easily correct any mistakes or undesired changes.**
   - **Acceptance Criteria:**
     - Given I am viewing a specific version of a prompt, when I click on the "Rollback" button, then the current prompt is updated to match the selected version's content.
     - I should receive a confirmation message indicating the rollback was successful.
     - The version history should record the rollback as a new entry.

3. **As a user, I want to compare two versions of a prompt, so I can understand the changes made between them.**
   - **Acceptance Criteria:**
     - Given a prompt with multiple versions, when I select two versions to compare, then the differences should be highlighted using a visual diff tool.
     - Unchanged, added, and removed sections should each be clearly labeled or color-coded.

4. **As a user, I want to be able to create a new version of a prompt when saving changes, so I can keep track of every update made.**
   - **Acceptance Criteria:**
     - When I save changes to a prompt, a new version entry is automatically created in the version history.
     - The new version should capture the timestamp, changes made, and optionally, a user-provided description of the update.

5. **As a user, I want auditability of prompt changes, so that I can review who made what changes and why.**
   - **Acceptance Criteria:**
     - The version history should include metadata for each version, such as the author of the changes and an optional comment on why the changes were made.
     - Each entry in the history must be immutable to ensure accurate auditing.

### Data Model Changes

To support prompt versioning in PromptLab, you will need to introduce a data model specifically for handling version history, which includes version tracking, rollback, and comparison.

#### New Data Model: `PromptVersion`
This model will maintain a history of all versions of a prompt.

- **Fields:**
  - `version_id` (String, UUID): A unique identifier for each version entry.
  - `prompt_id` (String, UUID): A reference to the original prompt to which this version belongs, establishing a relationship between each version and its prompt.
  - `version_number` (Integer): A sequential number indicating the version order.
  - `content_snapshot` (Text or JSON): Stores the content of the prompt and any other fields that need versioning as they were in this version.
  - `created_at` (Datetime): Timestamp indicating when this version was created.
  - `author_id` (String, UUID): (Optional) A reference to the user who created or saved changes for this version.
  - `change_summary` (String, Text): A brief summary or description of the changes made in this version.
  
#### Changes to Existing Data Model: `Prompt`
- **Fields:**
  - Ensure the `Prompt` model has a `current_version` field, if necessary, to track the latest version within the main prompt table/collection. This could be a relationship or a foreign key reference to the `PromptVersion`.
  
#### Relationships
- **Prompt to PromptVersion:**
  - This will be a one-to-many relationship. A single prompt can have multiple versions, each represented by an entry in the `PromptVersion` table.

#### Database Schema Example
```sql
CREATE TABLE Prompts (
    id UUID PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    description VARCHAR(500),
    collection_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
    -- Add other necessary fields
);

CREATE TABLE PromptVersions (
    version_id UUID PRIMARY KEY,
    prompt_id UUID REFERENCES Prompts(id),
    version_number INTEGER,
    content_snapshot TEXT, -- or JSON depending on your database capabilities
    created_at TIMESTAMP,
    author_id UUID, -- optionally referencing a Users table
    change_summary TEXT
);
```

### API Specification for Prompt Versioning

This section outlines the API endpoints related to prompt versioning in the PromptLab API. Each endpoint allows for specific operations related to managing prompt versions, including listing, retrieving, rolling back, creating, and comparing prompt versions.

---

#### List All Versions of a Prompt

- **HTTP Method:** GET
- **Endpoint Path:** `/api/prompts/{prompt_id}/versions`
- **Description:** Retrieves a list of all versions of a specified prompt, ordered chronologically.

- **Response Body Schema:**
  - **Field:** `versions` (Array)
    - **Type:** Array of Version Objects
  - **Version Object Fields:**
    - `version_id` (String, UUID)
    - `version_number` (Integer)
    - `created_at` (Datetime)
    - `change_summary` (String)

- **Response Example:**
  ```json
  {
    "versions": [
      {
        "version_id": "123e4567-e89b-12d3-a456-426614174000",
        "version_number": 1,
        "created_at": "2023-10-01T10:00:00Z",
        "change_summary": "Initial version"
      },
      {
        "version_id": "123e4567-e89b-12d3-a456-426614174001",
        "version_number": 2,
        "created_at": "2023-10-02T12:00:00Z",
        "change_summary": "Updated content"
      }
    ]
  }
  ```

- **Error Responses:**
  - **404 Not Found:** When the prompt does not exist.
    - Example Message: `{"error": "Prompt not found"}`

---

#### Retrieve a Specific Version

- **HTTP Method:** GET
- **Endpoint Path:** `/api/prompts/versions/{version_id}`
- **Description:** Retrieves details of a specific version of a prompt using its version ID.

- **Response Body Schema:**
  - **Field:** `version` (Object)
  - **Fields:**
    - `version_id` (String, UUID)
    - `version_number` (Integer)
    - `content_snapshot` (Text or JSON)
    - `created_at` (Datetime)
    - `author_id` (String, UUID)
    - `change_summary` (String)

- **Response Example:**
  ```json
  {
    "version": {
      "version_id": "123e4567-e89b-12d3-a456-426614174000",
      "version_number": 1,
      "content_snapshot": "...",
      "created_at": "2023-10-01T10:00:00Z",
      "author_id": "user-uuid",
      "change_summary": "Initial version"
    }
  }
  ```

- **Error Responses:**
  - **404 Not Found:** When the version does not exist.
    - Example Message: `{"error": "Version not found"}`

---

#### Roll Back to a Previous Version

- **HTTP Method:** POST
- **Endpoint Path:** `/api/prompts/{prompt_id}/rollback`
- **Description:** Rolls back the prompt to a specified previous version by version ID.

- **Request Body Schema:**
  - **Field:** `version_id` (String, UUID, Required)
    - **Type:** String

- **Response Body Example:**
  ```json
  {
    "message": "Rollback to version 2 successful",
    "current_version_number": 2
  }
  ```

- **Error Responses:**
  - **400 Bad Request:** When the requested version is invalid or does not exist.
    - Example Message: `{"error": "Invalid version ID"}`
  - **409 Conflict:** If rollback would cause inconsistencies.
    - Example Message: `{"error": "Rollback conflict detected"}`

---

#### Create a New Version Manually

- **HTTP Method:** POST
- **Endpoint Path:** `/api/prompts/{prompt_id}/versions`
- **Description:** Manually creates a new version for a prompt, capturing the current state.

- **Request Body Schema:**
  - **Fields:**
    - `content_snapshot` (Text or JSON, Required)
    - `change_summary` (String, Optional)
    - `author_id` (String, UUID, Optional)

- **Response Body Example:**
  ```json
  {
    "version_id": "123e4567-e89b-12d3-a456-426614174002",
    "version_number": 3,
    "created_at": "2023-10-03T15:00:00Z"
  }
  ```

- **Error Responses:**
  - **400 Bad Request:** If required fields are missing.
    - Example Message: `{"error": "Content snapshot is required"}`

---

#### Compare Two Versions

- **HTTP Method:** GET
- **Endpoint Path:** `/api/prompts/{prompt_id}/compare`
- **Description:** Compares two versions of a prompt and highlights differences.

- **Query Parameters:**
  - `version1_id` (String, UUID, Required)
  - `version2_id` (String, UUID, Required)

- **Response Body Example:**
  ```json
  {
    "differences": "Differences highlighted using a diff format or tool"
  }
  ```

- **Error Responses:**
  - **400 Bad Request:** If either version ID is missing or invalid.
    - Example Message: `{"error": "Both version IDs must be provided"}`
  - **404 Not Found:** If either version does not exist.
    - Example Message: `{"error": "One or both versions not found"}`

---

This API specification provides the necessary details for interacting with the prompt versioning feature in PromptLab, ensuring developers can efficiently implement and utilize version control capabilities.

#### Considerations
- **Indexing:** Consider indexing `prompt_id` and `version_number` in `PromptVersions` to speed up queries related to fetching version histories or specific versions.
- **Data Storage:** Choose appropriate data types for `content_snapshot` based on database capabilities—for example, JSON in databases like PostgreSQL for holistic snapshot storage.
- **Audit Logging:** If detailed audit information is necessary, consider logging additional metadata such as IP addresses, user agent, etc., potentially in a separate audit logs table.

### Edge Cases and Error Scenarios

1. **Concurrent Updates:**
   - **Scenario:** Multiple users attempt to update the same prompt simultaneously.
   - **Handling Strategy:** Implement optimistic locking or use version control conflicts alert mechanisms where the system checks if a prompt has been updated since it was last fetched by a user. Prompt users to resolve conflicts before allowing changes.

2. **Large Version Histories:**
   - **Scenario:** A prompt has an excessively large number of versions, impacting performance.
   - **Handling Strategy:** Implement paginated queries for version history listing, and consider archiving older versions if necessary.

3. **Version Rollback to Unstable State:**
   - **Scenario:** Rolling back to a version that contains known bugs or errors.
   - **Handling Strategy:** Allow users to flag specific versions with issues, and provide warnings when attempting to rollback to such versions.

4. **Missing or Corrupted Version Data:**
   - **Scenario:** Data for a specific version is missing or corrupted.
   - **Handling Strategy:** Implement database integrity checks and backups. Display an error message if a version cannot be retrieved and log these incidents for further investigation.

5. **Unauthorized Access:**
   - **Scenario:** Unauthorized users attempt to view or rollback versions.
   - **Handling Strategy:** Use role-based access control (RBAC) to manage who can view, update, or rollback versions. Ensure API endpoints enforce authentication and authorization checks.

6. **Rollback Leading to Data Inconsistency:**
   - **Scenario:** Rollback causes data inconsistency, especially in linked content or metadata.
   - **Handling Strategy:** Validate integrity constraints before finalizing a rollback. Use transactional operations to ensure atomicity, allowing to revert if inconsistencies are detected.

7. **Excessive Rollbacks:**
   - **Scenario:** Frequent rollbacks are performed on a prompt.
   - **Handling Strategy:** Monitor rollback activity levels and consider alerting administrators or setting usage policies limiting rollbacks over a period.

8. **Version Number Overflow:**
   - **Scenario:** A version number exceeds its storage capacity due to an extremely high number of edits.
   - **Handling Strategy:** Use a data type with sufficient capacity for version numbers, like Integer with a large range, and manage number wraparounds gracefully if needed.

9. **Network or Server Failures:**
   - **Scenario:** Attempting to create or rollback a version fails due to network issues.
   - **Handling Strategy:** Implement retry mechanisms for transient errors and provide meaningful error messages. Ensure atomic operations where incomplete updates or rollbacks do not leave the system in an inconsistent state.

10. **Change Summary Errors:**
    - **Scenario:** Change summary contains inaccurate or inappropriate content.
    - **Handling Strategy:** Allow users to edit version summaries but log changes for audit. Provide guidance on content policies to ensure appropriate, useful change descriptions.