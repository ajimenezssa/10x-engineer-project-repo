"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient
import string


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.
        
        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion will fail due to Bug #2!
        # The updated_at should be different from original
        # assert data["updated_at"] != original_updated_at  # Uncomment after fix
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.
        
        NOTE: This test might fail due to Bug #3!
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed

    def test_patch_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        assert create_response.status_code == 201
        prompt_id = create_response.json()["id"]
        original_title = create_response.json()["title"]
        original_content = create_response.json()["content"]

        # Partially update the content, assuming PATCH endpoint accepts partial updates
        updated_content = "Partially updated content"
        patch_data = {"content": updated_content}
        patch_response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert patch_response.status_code == 200

        # Get the updated prompt
        get_response = client.get(f"/prompts/{prompt_id}")
        data = get_response.json()
        assert data["id"] == prompt_id
        assert data["title"] == original_title
        assert data["content"] == updated_content
        assert data["content"] != original_content  # Ensure the content field was updated

class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.
        
        NOTE: Bug #4 - prompts become orphaned after collection deletion.
        This test documents the current (buggy) behavior.
        After fixing, update the test to verify correct behavior.

        Verifies that prompts are not orphaned, and their collection_id is set to None after collection deletion.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        # The prompt still exists but has invalid collection_id
        # This is Bug #4 - should be handled properly

        # Verify that the prompt still exists
        prompts = client.get("/prompts").json()["prompts"]
        assert any(prompt["id"] == prompt_id for prompt in prompts), "The prompt should still exist."

        # Verify that the prompt’s collection_id is now None
        for prompt in prompts:
            if prompt["id"] == prompt_id:
                assert prompt["collection_id"] is None, "The prompt's collection_id should be None."

    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        # Create a new collection
        create_response = client.post("/collections", json=sample_collection_data)
        assert create_response.status_code == 201
        created_collection = create_response.json()
        
        # Retrieve the collection by its ID
        collection_id = created_collection["id"]
        get_response = client.get(f"/collections/{collection_id}")
        
        # Assert the status code
        assert get_response.status_code == 200
        
        # Assert fields match
        retrieved_collection = get_response.json()
        assert retrieved_collection["id"] == created_collection["id"]
        assert retrieved_collection["name"] == created_collection["name"]
        # Add additional assertions if there are more fields, e.g., description, created_at, etc.
        # assert retrieved_collection["description"] == created_collection["description"]
        # assert retrieved_collection["created_at"] == created_collection["created_at"]

class TestPromptsErrors:
    """Error tests for prompt endpoints."""
    
    # GET
    def test_get_prompt_404(self, client: TestClient):
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404

    # POST
    def test_post_prompt_invalid_collection_id(self, client: TestClient, sample_prompt_data):
        invalid_data = {**sample_prompt_data, "collection_id": "invalid-id"}
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 400

    def test_post_prompt_missing_fields(self, client: TestClient):
        incomplete_data = {}  # Assuming required fields are missing
        response = client.post("/prompts", json=incomplete_data)
        assert response.status_code == 422

    # PUT
    def test_put_prompt_404(self, client: TestClient, sample_prompt_data):
        response = client.put(f"/prompts/nonexistent-id", json=sample_prompt_data)
        assert response.status_code == 404

    def test_put_prompt_invalid_collection_id(self, client: TestClient, sample_prompt_data, sample_collection_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        invalid_data = {**sample_prompt_data, "collection_id": "invalid-id"}
        response = client.put(f"/prompts/{prompt_id}", json=invalid_data)
        assert response.status_code == 400

    # PATCH
    def test_patch_prompt_404(self, client: TestClient):
        patch_data = {"title": "New Title"}
        response = client.patch("/prompts/nonexistent-id", json=patch_data)
        assert response.status_code == 404

    def test_patch_prompt_invalid_collection_id(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        invalid_data = {"collection_id": "invalid-id"}
        response = client.patch(f"/prompts/{prompt_id}", json=invalid_data)
        assert response.status_code == 400

    # DELETE
    def test_delete_prompt_404(self, client: TestClient):
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404

class TestPromptsEdgeCases:
    """Edge-case tests for prompt endpoints."""

    def test_create_prompt_empty_strings(self, client: TestClient):
        data = {"title": "", "content": "", "description": ""}
        response = client.post("/prompts", json=data)
        assert response.status_code == 422  # Should fail validation

    def test_create_prompt_whitespace_strings(self, client: TestClient):
        data = {"title": "   ", "content": "   ", "description": "   "}
        response = client.post("/prompts", json=data)
        assert response.status_code == 201  # API allows whitespace strings

    def test_create_prompt_special_characters(self, client: TestClient):
        data = {
            "title": "!@#$%^&*()_+{}|:\"<>?",
            "content": "<script>alert('x')</script>",
            "description": "~`[];',./"
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        resp_data = response.json()
        assert resp_data["title"] == data["title"]
        assert resp_data["content"] == data["content"]

    def test_create_prompt_unicode_emojis(self, client: TestClient):
        data = {
            "title": "💡🔥🚀",
            "content": "Content with emojis 📝🎯",
            "description": "Description ✨"
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        resp_data = response.json()
        assert resp_data["title"] == data["title"]
        assert resp_data["content"] == data["content"]

    def test_create_prompt_very_long_strings(self, client: TestClient):
        long_string = "x" * 5000  # Adjust length depending on DB limits
        data = {"title": long_string, "content": long_string, "description": long_string}
        response = client.post("/prompts", json=data)
        assert response.status_code in [201, 422]  # 422 if too long for DB
        

class TestCollectionsEdgeCases:
    """Edge-case tests for collection endpoints."""

    def test_create_collection_empty_name(self, client: TestClient):
        data = {"name": ""}
        response = client.post("/collections", json=data)
        assert response.status_code == 422

    def test_create_collection_whitespace_name(self, client: TestClient):
        data = {"name": "   "}
        response = client.post("/collections", json=data)
        assert response.status_code == 201  # API allows whitespace strings

    def test_create_collection_special_characters(self, client: TestClient):
        data = {"name": "!@#$%^&*()_+{}|:\"<>?"}
        response = client.post("/collections", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == data["name"]

    def test_create_collection_unicode_emojis(self, client: TestClient):
        data = {"name": "📚🖊️"}
        response = client.post("/collections", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == data["name"]

    def test_create_collection_very_long_name(self, client: TestClient):
        long_name = "x" * 5000
        data = {"name": long_name}
        response = client.post("/collections", json=data)
        assert response.status_code in [201, 422]  # 422 if too long for DB

class TestPromptsQueryParams:
    """Tests for query parameters on prompt endpoints (sorting, filtering)."""

    def test_sort_prompts_desc(self, client: TestClient, sample_prompt_data):
        """Prompts should be sorted newest first (descending) by default."""
        import time

        # Create two prompts with slight delay
        prompt1 = {**sample_prompt_data, "title": "First Prompt"}
        prompt2 = {**sample_prompt_data, "title": "Second Prompt"}
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        assert prompts[0]["title"] == "Second Prompt"
        assert prompts[1]["title"] == "First Prompt"

    def test_sort_prompts_asc(self, client: TestClient, sample_prompt_data):
        """Prompts should be returned newest first (descending) because asc not supported yet."""
        import time

        prompt1 = {**sample_prompt_data, "title": "Oldest Prompt"}
        prompt2 = {**sample_prompt_data, "title": "Newest Prompt"}
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts?sort=asc")  # API ignores 'asc'
        prompts = response.json()["prompts"]
        # Newest comes first because API only supports descending
        assert prompts[0]["title"] == "Newest Prompt"
        assert prompts[1]["title"] == "Oldest Prompt"

    def test_filter_by_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        """Filter prompts by collection_id."""
        # Create collections
        col1 = client.post("/collections", json={"name": "Col 1"}).json()
        col2 = client.post("/collections", json={"name": "Col 2"}).json()

        # Create prompts in different collections
        prompt1 = {**sample_prompt_data, "title": "Prompt 1", "collection_id": col1["id"]}
        prompt2 = {**sample_prompt_data, "title": "Prompt 2", "collection_id": col2["id"]}
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)

        response = client.get(f"/prompts?collection_id={col1['id']}")
        prompts = response.json()["prompts"]
        assert all(p["collection_id"] == col1["id"] for p in prompts)
        assert any(p["title"] == "Prompt 1" for p in prompts)
        assert all(p["title"] != "Prompt 2" for p in prompts)

    def test_filter_by_search(self, client: TestClient, sample_prompt_data):
        """Filter prompts by search query in title/content."""
        prompt1 = {**sample_prompt_data, "title": "Alpha Prompt", "content": "Content A"}
        prompt2 = {**sample_prompt_data, "title": "Beta Prompt", "content": "Content B"}
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts?search=Alpha")
        prompts = response.json()["prompts"]
        assert all("Alpha" in p["title"] or "Alpha" in p["content"] for p in prompts)
        assert any(p["title"] == "Alpha Prompt" for p in prompts)
        assert all(p["title"] != "Beta Prompt" for p in prompts)

    def test_combined_filter_sort(self, client: TestClient, sample_prompt_data, sample_collection_data):
        """Filter by collection and sort descending."""
        import time

        # Create collection
        collection = client.post("/collections", json={"name": "Col"}).json()

        # Create prompts in collection
        prompt1 = {**sample_prompt_data, "title": "Old Prompt", "collection_id": collection["id"]}
        prompt2 = {**sample_prompt_data, "title": "New Prompt", "collection_id": collection["id"]}
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)

        response = client.get(f"/prompts?collection_id={collection['id']}&sort=desc")
        prompts = response.json()["prompts"]
        assert all(p["collection_id"] == collection["id"] for p in prompts)
        assert prompts[0]["title"] == "New Prompt"
        assert prompts[1]["title"] == "Old Prompt"