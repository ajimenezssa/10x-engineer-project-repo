"""Tests for models.py"""

import pytest
from datetime import datetime, timedelta
from app.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    Collection,
    CollectionCreate,
    PromptList,
    CollectionList,
    HealthResponse,
)
from pydantic import ValidationError
from uuid import UUID


# ===================== Prompt Models =====================

class TestPromptModels:

    def test_prompt_validation_success(self):
        p = Prompt(title="Test Prompt", content="Some content", description="A description")
        assert p.title == "Test Prompt"
        assert p.content == "Some content"
        assert p.description == "A description"
        assert isinstance(UUID(p.id), UUID)
        assert isinstance(p.created_at, datetime)
        assert isinstance(p.updated_at, datetime)

    def test_prompt_validation_failure_empty_title(self):
        with pytest.raises(ValidationError):
            Prompt(title="", content="Content")

    def test_prompt_validation_failure_empty_content(self):
        with pytest.raises(ValidationError):
            Prompt(title="Title", content="")

    def test_prompt_default_values(self):
        p = Prompt(title="Default Test", content="Content")
        assert p.description is None
        assert p.collection_id is None
        assert p.created_at is not None
        assert p.updated_at is not None
        assert p.id is not None

    def test_prompt_serialization(self):
        p = Prompt(title="Serialize Test", content="Content", description="Desc")
        data = p.model_dump()
        assert data["title"] == "Serialize Test"
        assert data["content"] == "Content"
        assert data["description"] == "Desc"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data


# ===================== Collection Models =====================

class TestCollectionModels:

    def test_collection_validation_success(self):
        c = Collection(name="My Collection", description="Some desc")
        assert c.name == "My Collection"
        assert c.description == "Some desc"
        assert isinstance(UUID(c.id), UUID)
        assert isinstance(c.created_at, datetime)

    def test_collection_validation_failure_empty_name(self):
        with pytest.raises(ValidationError):
            Collection(name="")

    def test_collection_default_values(self):
        c = Collection(name="Defaults Test")
        assert c.description is None
        assert c.id is not None
        assert c.created_at is not None

    def test_collection_serialization(self):
        c = Collection(name="Serialize Test", description="Desc")
        data = c.model_dump()
        assert data["name"] == "Serialize Test"
        assert data["description"] == "Desc"
        assert "id" in data
        assert "created_at" in data


# ===================== Response Models =====================

class TestResponseModels:

    def test_prompt_list_serialization(self):
        prompts = [Prompt(title="A", content="B")]
        pl = PromptList(prompts=prompts, total=1)
        data = pl.model_dump()
        assert data["total"] == 1
        assert len(data["prompts"]) == 1
        assert data["prompts"][0]["title"] == "A"

    def test_collection_list_serialization(self):
        collections = [Collection(name="Col 1")]
        cl = CollectionList(collections=collections, total=1)
        data = cl.model_dump()
        assert data["total"] == 1
        assert len(data["collections"]) == 1
        assert data["collections"][0]["name"] == "Col 1"

    def test_health_response_serialization(self):
        health = HealthResponse(status="ok", version="1.0")
        data = health.model_dump()
        assert data["status"] == "ok"
        assert data["version"] == "1.0"


# ===================== Additional Validation =====================

class TestPromptCreateUpdateModels:

    def test_prompt_create_model(self):
        pc = PromptCreate(title="Create Test", content="Content")
        assert pc.title == "Create Test"
        assert pc.content == "Content"

    def test_prompt_update_model(self):
        pu = PromptUpdate(title="Update Test", content="Content", description="Desc")
        assert pu.title == "Update Test"
        assert pu.description == "Desc"