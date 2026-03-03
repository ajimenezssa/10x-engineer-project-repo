import pytest
import uuid
from app.storage import Storage
from app.models import Prompt, Collection


# ============== Fixtures ==============
@pytest.fixture
def storage():
    s = Storage()
    yield s
    s.clear()


@pytest.fixture
def sample_prompt():
    return Prompt(
        id=str(uuid.uuid4()),
        title="Sample Prompt",
        content="Review this code snippet.",
        description="A sample prompt for testing."
    )


@pytest.fixture
def sample_collection():
    return Collection(
        id=str(uuid.uuid4()),
        name="Sample Collection"
    )


# ============== Prompt CRUD ==============
class TestPromptsCRUDStorage:
    def test_create_prompt(self, storage, sample_prompt):
        stored = storage.create_prompt(sample_prompt)
        assert stored.id == sample_prompt.id
        assert storage.get_prompt(stored.id) == stored

    def test_get_prompt_nonexistent(self, storage):
        assert storage.get_prompt("nonexistent") is None

    def test_update_prompt(self, storage, sample_prompt):
        storage.create_prompt(sample_prompt)
        updated_prompt = Prompt(
            id=sample_prompt.id,
            title="Updated Title",
            content="Updated content",
            description="Updated description"
        )
        result = storage.update_prompt(sample_prompt.id, updated_prompt)
        assert result.title == "Updated Title"
        # Updating a nonexistent prompt returns None
        assert storage.update_prompt("nonexistent", updated_prompt) is None

    def test_delete_prompt(self, storage, sample_prompt):
        storage.create_prompt(sample_prompt)
        assert storage.delete_prompt(sample_prompt.id) is True
        assert storage.get_prompt(sample_prompt.id) is None
        # Deleting again returns False
        assert storage.delete_prompt(sample_prompt.id) is False

    def test_get_all_prompts(self, storage, sample_prompt):
        storage.create_prompt(sample_prompt)
        all_prompts = storage.get_all_prompts()
        assert len(all_prompts) == 1
        assert all_prompts[0].id == sample_prompt.id


# ============== Collection CRUD ==============
class TestCollectionsCRUDStorage:
    def test_create_collection(self, storage, sample_collection):
        stored = storage.create_collection(sample_collection)
        assert stored.id == sample_collection.id
        assert storage.get_collection(stored.id) == stored

    def test_get_collection_nonexistent(self, storage):
        assert storage.get_collection("nonexistent") is None

    def test_delete_collection(self, storage, sample_collection):
        storage.create_collection(sample_collection)
        assert storage.delete_collection(sample_collection.id) is True
        assert storage.get_collection(sample_collection.id) is None
        assert storage.delete_collection(sample_collection.id) is False

    def test_get_all_collections(self, storage, sample_collection):
        storage.create_collection(sample_collection)
        all_collections = storage.get_all_collections()
        assert len(all_collections) == 1
        assert all_collections[0].id == sample_collection.id


# ============== Persistence ==============
class TestStoragePersistence:
    def test_storage_persistence(self, storage, sample_prompt, sample_collection):
        # Create prompt and collection
        storage.create_prompt(sample_prompt)
        storage.create_collection(sample_collection)
        # Re-fetch
        assert storage.get_prompt(sample_prompt.id) == sample_prompt
        assert storage.get_collection(sample_collection.id) == sample_collection
        # Delete prompt and verify
        storage.delete_prompt(sample_prompt.id)
        assert storage.get_prompt(sample_prompt.id) is None


# ============== Edge Cases ==============
class TestPromptsEdgeCasesStorage:
    def test_create_prompt_whitespace_strings(self, storage):
        prompt = Prompt(
            id=str(uuid.uuid4()),
            title="   ",
            content="   ",
            description="   "
        )
        stored = storage.create_prompt(prompt)
        assert stored.title == "   "
        assert stored.content == "   "
        assert stored.description == "   "

    def test_create_prompt_special_characters(self, storage):
        prompt = Prompt(
            id=str(uuid.uuid4()),
            title="!@#$%^&*()",
            content="<script>alert('xss')</script>",
            description="Special chars description"
        )
        stored = storage.create_prompt(prompt)
        assert stored.title == "!@#$%^&*()"
        assert stored.content == "<script>alert('xss')</script>"


class TestCollectionsEdgeCasesStorage:
    def test_create_collection_whitespace_name(self, storage):
        collection = Collection(
            id=str(uuid.uuid4()),
            name="   "
        )
        stored = storage.create_collection(collection)
        assert stored.name == "   "

    def test_create_collection_special_characters(self, storage):
        collection = Collection(
            id=str(uuid.uuid4()),
            name="!@#$%^&*()_+"
        )
        stored = storage.create_collection(collection)
        assert stored.name == "!@#$%^&*()_+"