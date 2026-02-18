# Tagging System Specification

## Overview
The tagging system in PromptLab is a pivotal feature designed to empower users in efficiently managing and organizing their AI prompts. By introducing tags, users can categorize prompts in a meaningful way, enriching the metadata associated with each item and facilitating sophisticated search and retrieval operations.

The system serves multiple roles: it acts as a dynamic organizational tool, a search enhancement mechanism, and a collaborative facilitator. With tags, teams can label prompts according to various criteria such as theme, project, or usage context, enabling a high degree of personalization and control. This flexibility is essential for users dealing with extensive prompt libraries where quick access and management are paramount.

Importantly, the tagging feature also future-proofs the platform by allowing seamless scalability. As the volume of prompts grows, the system's ability to incorporate new tags without degrading performance ensures that users can continue to manage their datasets effectively. Through an intuitive UI, users engage with tags effortlessly, maintaining a streamlined workflow and consistent prompt management practices across teams.

### Purpose
The main objective of the tagging system is to provide users with the ability to assign meaningful descriptors to prompts, facilitating better organization and quicker retrieval. This system supports users in efficiently managing large sets of prompts and enables a more dynamic interaction with the PromptLab platform.

### Key Benefits
1. **Streamlined Prompt Organization and Management**: Users can assign multiple tags to each prompt, allowing for versatile categorization across diverse themes and projects. This reduces clutter and simplifies navigation within large datasets, providing users with a snapshot of prompt relevance at a glance.

2. **Advanced Search and Filter Capabilities**: By supporting tag-based searches, the system empowers users to filter prompts based on specific criteria, thereby speeding up the retrieval process and enhancing user productivity. This capability is particularly beneficial for teams needing to operate swiftly and accurately within fast-paced environments.

3. **Enhanced Collaborative Workflows**: The use of standardized tags promotes uniformity in prompt categorization across team members, which is crucial for effective collaboration. By harmonizing how prompts are grouped and accessed, teams can minimize miscommunications and misunderstandings, leading to smoother collaborative efforts.

4. **Optimized Workflow Efficiency**: Tags offer an on-the-fly filtering and sorting mechanism, which is less rigid compared to traditional hierarchical organization methods. This flexibility allows users to adapt prompt categorization to their evolving needs without restructuring their entire dataset.

5. **Scalability and Flexibility**: The tagging system is designed to grow with user needs, supporting a broad range of tags without impacting performance, thanks to optimized data handling and indexing strategies.

### Implementation Considerations
- **Data Model**: Implement a many-to-many relationship between prompts and tags to enable flexible tagging capabilities.

- **User Interface**: Design an intuitive UI for tagging operations, allowing users to add, edit, and manage tags easily.

- **Performance Optimization**: Ensure that the tagging system is optimized for performance, with indexing and efficient query handling for fast search and retrieval operations.

# User Stories


1. **As a user, I want to create new tags, so that I can categorize my prompts effectively.**
   - **Acceptance Criteria:**
     - Given I am on the tags management page, when I input a new tag name and click "Create Tag," then a new tag should be created and appear on the tags list.
     - Given the tag name already exists, when I attempt to create the tag, then I should see an error message indicating the tag is a duplicate.
     - Given I leave the tag name field blank, when I attempt creation, then I should see an error message prompting me to input a tag name.

2. **As a user, I want to assign tags to my prompts, so that I can categorize and organize them better.**
   - **Acceptance Criteria:**
     - Given I am editing a prompt, when I select one or more tags from a dropdown menu and save the prompt, then the selected tags should be associated with the prompt.
     - Given I attempt to assign a non-existing tag, when I save the prompt, then I should see an error or prompt to create a new tag.

3. **As a user, I want to remove tags from my prompts, so that I can update the categorization of my data as needed.**
   - **Acceptance Criteria:**
     - Given I am editing a prompt with existing tags, when I deselect one or more tags and save the prompt, then those tags should no longer be associated with the prompt.
     - Given I attempt to remove all tags, when I save the prompt, then the prompt should reflect having no associated tags in the system.

4. **As a user, I want to filter or search prompts by tags, so that I can quickly find specific prompts relevant to my needs.**
   - **Acceptance Criteria:**
     - Given I am on the prompts page, when I select one or more tags as filter criteria, then I should see only prompts associated with those tags.
     - Given no prompts match the selected tags, when I apply the filter, then I should see a message indicating no results found.
     - Given I deselect all filters, when I refresh the page, then I should see the full list of prompts without tag-based filtering.

5. **As a user, I want to manage my existing tags, so that I can keep my tagging system organized and relevant.**
   - **Acceptance Criteria:**
     - Given I am on the tags management page, when I choose to rename an existing tag and save changes, then the updated tag should reflect across all associated prompts.
     - Given I select a tag for deletion, when I confirm the action, then the tag should be removed and no longer available for new or existing prompts.
     - Given a tag is associated with one or more prompts, when I attempt to delete it, then I should be prompted with a warning about its associations.

# Tagging System Data Model

The tagging system involves creating a data model that supports flexible many-to-many relationships between prompts and tags. This model facilitates efficient tagging, retrieval, and management of prompt data.

## Tables and Relationships

### Table: Tags
- **Description**: Stores unique tags used to categorize prompts.
- **Fields**:
  - `tag_id` (UUID): Primary key, unique identifier for the tag.
  - `name` (VARCHAR(100)): The name of the tag, unique to prevent duplicates.
  - `description` (TEXT): Optional field providing additional details about the tag.

### Table: PromptsTags
- **Description**: Junction table to establish a many-to-many relationship between prompts and tags.
- **Fields**:
  - `prompt_id` (UUID): Foreign key referencing `Prompts(id)`.
  - `tag_id` (UUID): Foreign key referencing `Tags(tag_id)`.
  - **Composite Key**: (`prompt_id`, `tag_id`) to ensure uniqueness of each prompt-tag pairing.

### Relationships
- **Prompts to Tags**: Many-to-Many relationship established through the `PromptsTags` junction table.

## Sample SQL Schema

```sql
CREATE TABLE Tags (
    tag_id UUID PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Prompts (
    id UUID PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    description VARCHAR(500),
    collection_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
    -- Additional fields as necessary
);

CREATE TABLE PromptsTags (
    prompt_id UUID,
    tag_id UUID,
    PRIMARY KEY (prompt_id, tag_id),
    FOREIGN KEY (prompt_id) REFERENCES Prompts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
);
```

## Explanation

- **Tags Table**: Holds data for each tag, ensuring tag names are unique to avoid confusion.
- **PromptsTags Table**: Serves as a junction to express the many-to-many relationship between prompts and tags. The composite primary key ensures that each prompt-tag pair is unique, while foreign key constraints maintain referential integrity.
- **Data Integrity and Navigation**: The schema allows for efficient querying of prompts by tag and vice versa, supporting complex retrieval, filtering, and categorization needs.

# Tagging System API Endpoint Specifications

All API endpoints should adhere to RESTful conventions and utilize standard HTTP methods. Endpoints should return appropriate status codes and adhere to common practices for request and response format.

## Endpoints

### 1. List Tags

- **HTTP Method:** GET
- **Endpoint Path:** `/api/tags`
- **Description:** Retrieves a list of all available tags.
- **Response Body:**
  ```json
  {
    "tags": [
      {
        "tag_id": "uuid",
        "name": "example tag name",
        "description": "optional tag description"
      }
      // ... more tags
    ]
  }
  ```
- **Example Error Response:**
  - **500 Internal Server Error:** When the server encounters an unexpected condition.

### 2. Create Tag

- **HTTP Method:** POST
- **Endpoint Path:** `/api/tags`
- **Description:** Creates a new tag.
- **Request Body:**
  ```json
  {
    "name": "new tag name",
    "description": "optional tag description"
  }
  ```
- **Response Body:**
  ```json
  {
    "tag_id": "uuid",
    "name": "new tag name",
    "description": "optional tag description"
  }
  ```
- **Example Error Response:**
  - **400 Bad Request:** When the tag name is missing or already exists.
    ```json
    { "error": "Tag name is required and must be unique" }
    ```

### 3. Update Tag

- **HTTP Method:** PUT
- **Endpoint Path:** `/api/tags/{tag_id}`
- **Description:** Updates an existing tag.
- **Request Body:**
  ```json
  {
    "name": "updated tag name",
    "description": "updated tag description"
  }
  ```
- **Response Body:**
  ```json
  {
    "tag_id": "uuid",
    "name": "updated tag name",
    "description": "updated tag description"
  }
  ```
- **Example Error Response:**
  - **404 Not Found:** When the tag by `tag_id` does not exist.
    ```json
    { "error": "Tag not found" }
    ```

### 4. Delete Tag

- **HTTP Method:** DELETE
- **Endpoint Path:** `/api/tags/{tag_id}`
- **Description:** Deletes the specified tag.
- **Response Body:** `204 No Content`
- **Example Error Response:**
  - **404 Not Found:** When the tag by `tag_id` does not exist.
    ```json
    { "error": "Tag not found" }
    ```

### 5. Assign Tags to Prompt

- **HTTP Method:** POST
- **Endpoint Path:** `/api/prompts/{prompt_id}/tags`
- **Description:** Assigns one or more tags to a prompt.
- **Request Body:**
  ```json
  {
    "tag_ids": ["uuid1", "uuid2"]
  }
  ```
- **Response Body:**
  ```json
  {
    "prompt_id": "uuid",
    "tags": [
      {
        "tag_id": "uuid1",
        "name": "tag name 1"
      },
      {
        "tag_id": "uuid2",
        "name": "tag name 2"
      }
    ]
  }
  ```
- **Example Error Response:**
  - **400 Bad Request:** When tag_ids include invalid or non-existent IDs.
    ```json
    { "error": "Invalid tag IDs provided" }
    ```

### 6. Filter Prompts by Tags

- **HTTP Method:** GET
- **Endpoint Path:** `/api/prompts`
- **Description:** Retrieves prompts filtered by specified tags.
- **Query Parameters:**
  - `tag_ids`: Comma-separated tag IDs to filter prompts.
  - Example: `/api/prompts?tag_ids=uuid1,uuid2`
- **Response Body:**
  ```json
  {
    "prompts": [
      {
        "prompt_id": "uuid",
        "title": "prompt title",
        "content": "prompt content",
        "tags": [
          {
            "tag_id": "uuid1",
            "name": "tag name 1"
          }
          // ... other tags
        ]
      }
      // ... more prompts
    ]
  }
  ```
- **Example Error Response:**
  - **400 Bad Request:** When no valid tags are provided.
    ```json
    { "error": "At least one valid tag ID is required for filtering" }

# Search and Filter Requirements

## Logic for Filtering Prompts

### Filtering by Single Tag
- **Requirement**: Allow users to filter prompts by a single tag, returning all prompts associated with that tag.
- **Logic**: Query the `PromptsTags` table to retrieve prompt IDs associated with the specified tag ID, then fetch prompts corresponding to those IDs.

### Filtering by Multiple Tags
- **Requirement**: Support filtering by multiple tags, returning prompts that match any or all specified tags based on user preference.
- **Logic**:
  - **Any Match**: Use an `OR` condition in the query to return prompts tagged with any of the provided tag IDs.
  - **All Match**: Use an `AND` condition to fetch prompts that are associated with all specified tag IDs. This may require aggregation and filtering based on the count of matched tags.

## Partial Matches and Search Functionality

### Partial Tag Matches
- **Requirement**: Enable searching for tags using partial strings, useful for auto-complete functionality or flexible search.
- **Logic**: Implement a `LIKE` query or use full-text search capabilities if supported by the database to retrieve tags matching the partial input string.

## Sorting and Ordering

### Sorting Results
- **Requirement**: Allow sorting of filtered prompts by various attributes such as creation date, title, or associated tag names.
- **Logic**: Use SQL `ORDER BY` clause to sort results based on specified criteria. Provide options for ascending or descending order as determined by the user.

## Result Limits and Pagination

### Limiting Results
- **Requirement**: Implement a limit on the number of search results returned to optimize performance and manageability for users.
- **Logic**: Use SQL `LIMIT` clause to specify maximum number of results returned. Allow users to set the limit parameter optionally.

### Pagination for Large Datasets
- **Requirement**: Support pagination to efficiently handle large result sets and provide a manageable navigation experience.
- **Logic**: Implement via SQL `OFFSET` and `LIMIT` clauses to paginate query results. Include metadata like total count, current page, and pages available.

## Behavior for Large Datasets

### Handling Large Datasets
- **Requirement**: Ensure performance scalability by optimizing database queries and supporting asynchronous processing for extensive search requests.
- **Logic**:
  - **Indexing**: Ensure database indexes on critical columns like tag IDs and prompt IDs to maintain fast retrieval times.
  - **Asynchronous Processing**: For large or complex queries that might exceed acceptable response times, consider employing background processing with a status check feature.

Implementing these requirements will ensure that the tagging system in PromptLab supports comprehensive and efficient search, retrieval, and organization capabilities to enhance usability and performance, even with large datasets.

