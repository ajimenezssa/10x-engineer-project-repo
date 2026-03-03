import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse
)


# ===================== Prompt Models =====================

class TestPromptModels:
    """Tests for Prompt models."""

    def test_prompt_create_valid(self):
        prompt = PromptCreate(title="Test Title", content="Test content", description="Optional desc")
        assert prompt.title == "Test Title"
        assert prompt.content == "Test content"
        assert prompt.description == "Optional desc"
        assert prompt.collection_id is None

    def test_prompt_create_invalid_empty_title(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="", content="Some content")

    def test_prompt_create_invalid_empty_content(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="Valid Title", content="")

    def test_prompt_defaults(self):
        prompt = Prompt(title="Test", content="Content")
        assert isinstance(prompt.id, str) and len(prompt.id) > 0
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)
        # Check created_at and updated_at are close
        delta = prompt.updated_at - prompt.created_at
        assert delta.total_seconds() >= 0

    def test_prompt_serialization(self):
        prompt = Prompt(title="Test", content="Content")
        data = prompt.dict()
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["title"] == "Test"


# ===================== Collection Models =====================

class TestCollectionModels:
    """Tests for Collection models."""

    def test_collection_create_valid(self):
        collection = CollectionCreate(name="My Collection", description="Optional desc")
        assert collection.name == "My Collection"
        assert collection.description == "Optional desc"

    def test_collection_create_invalid_empty_name(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="")

    def test_collection_defaults(self):
        collection = Collection(name="Test Collection")
        assert isinstance(collection.id, str) and len(collection.id) > 0
        assert isinstance(collection.created_at, datetime)

    def test_collection_serialization(self):
        collection = Collection(name="Test Collection")
        data = collection.dict()
        assert "id" in data
        assert "created_at" in data
        assert data["name"] == "Test Collection"


# ===================== Response Models =====================

class TestResponseModels:
    """Tests for response models serialization."""

    def test_prompt_list_serialization(self):
        prompt = Prompt(title="A", content="B")
        pl = PromptList(prompts=[prompt], total=1)
        data = pl.dict()
        assert data["total"] == 1
        assert len(data["prompts"]) == 1

    def test_collection_list_serialization(self):
        collection = Collection(name="C")
        cl = CollectionList(collections=[collection], total=1)
        data = cl.dict()
        assert data["total"] == 1
        assert len(data["collections"]) == 1

    def test_health_response_serialization(self):
        health = HealthResponse(status="ok", version="1.0.0")
        data = health.dict()
        assert data["status"] == "ok"
        assert data["version"] == "1.0.0"