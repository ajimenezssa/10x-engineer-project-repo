import pytest
import uuid
from datetime import datetime, timedelta
from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables,
)

# ==================== Test Sort Prompts ====================

class TestSortPrompts:
    def test_sort_descending(self):
        now = datetime.utcnow()
        p1 = Prompt(id=str(uuid.uuid4()), title="A", content="Content", created_at=now)
        p2 = Prompt(id=str(uuid.uuid4()), title="B", content="Content", created_at=now + timedelta(seconds=1))
        sorted_prompts = sort_prompts_by_date([p1, p2])
        assert sorted_prompts[0].id == p2.id  # Newest first
        assert sorted_prompts[1].id == p1.id

    def test_sort_ascending(self):
        now = datetime.utcnow()
        p1 = Prompt(id=str(uuid.uuid4()), title="A", content="Content", created_at=now)
        p2 = Prompt(id=str(uuid.uuid4()), title="B", content="Content", created_at=now + timedelta(seconds=1))
        sorted_prompts = sort_prompts_by_date([p1, p2], descending=False)
        assert sorted_prompts[0].id == p1.id  # Oldest first
        assert sorted_prompts[1].id == p2.id

    def test_sort_empty_list(self):
        sorted_prompts = sort_prompts_by_date([])
        assert sorted_prompts == []

    def test_sort_same_timestamp(self):
        now = datetime.utcnow()
        p1 = Prompt(id=str(uuid.uuid4()), title="A", content="Content", created_at=now)
        p2 = Prompt(id=str(uuid.uuid4()), title="B", content="Content", created_at=now)
        sorted_prompts = sort_prompts_by_date([p1, p2])
        # Order should remain as input (stable sort)
        assert sorted_prompts[0].id == p1.id
        assert sorted_prompts[1].id == p2.id

# ==================== Test Filter Prompts ====================

class TestFilterPrompts:
    def test_filter_empty_list(self):
        result = filter_prompts_by_collection([], "collection123")
        assert result == []

    def test_filter_no_match(self):
        p1 = Prompt(id=str(uuid.uuid4()), title="A", content="Content", collection_id="col1")
        result = filter_prompts_by_collection([p1], "col2")
        assert result == []

    def test_filter_all_match(self):
        p1 = Prompt(id=str(uuid.uuid4()), title="A", content="Content", collection_id="col1")
        p2 = Prompt(id=str(uuid.uuid4()), title="B", content="Content", collection_id="col1")
        result = filter_prompts_by_collection([p1, p2], "col1")
        assert len(result) == 2
        assert p1 in result and p2 in result

# ==================== Test Search Prompts ====================

class TestSearchPrompts:
    def test_search_title_match(self):
        p = Prompt(id=str(uuid.uuid4()), title="Interesting Title", content="Content")
        result = search_prompts([p], "interest")
        assert p in result

    def test_search_description_match(self):
        p = Prompt(id=str(uuid.uuid4()), title="Title", content="Content", description="Interesting Description")
        result = search_prompts([p], "description")
        assert p in result

    def test_search_no_match(self):
        p = Prompt(id=str(uuid.uuid4()), title="Title", content="Content", description="Desc")
        result = search_prompts([p], "notfound")
        assert result == []

    def test_search_empty_query(self):
        p = Prompt(id=str(uuid.uuid4()), title="Title", content="Content", description="Desc")
        result = search_prompts([p], "")
        # Expect all prompts if query is empty
        assert result == [p]

    def test_search_multiple_matches(self):
        p1 = Prompt(id=str(uuid.uuid4()), title="Hello World", content="Content")
        p2 = Prompt(id=str(uuid.uuid4()), title="Hi there", content="Content", description="World is big")
        result = search_prompts([p1, p2], "world")
        assert p1 in result and p2 in result

# ==================== Test Validate Prompt Content ====================

class TestValidatePromptContent:
    def test_valid_content(self):
        assert validate_prompt_content("This is valid content") is True

    def test_short_content(self):
        assert validate_prompt_content("Too short") is False

    def test_exactly_10_chars(self):
        assert validate_prompt_content("1234567890") is True

    def test_whitespace_only(self):
        assert validate_prompt_content("    ") is False

    def test_empty_string(self):
        assert validate_prompt_content("") is False

    def test_none_content(self):
        assert validate_prompt_content(None) is False

# ==================== Test Extract Variables ====================

class TestExtractVariables:
    def test_multiple_variables(self):
        content = "Hello {{name}}, your id is {{id}}"
        variables = extract_variables(content)
        assert set(variables) == {"name", "id"}

    def test_no_variables(self):
        content = "No variables here"
        variables = extract_variables(content)
        assert variables == []

    def test_variables_with_underscores_and_numbers(self):
        content = "Var {{var_1}} and {{var2}}"
        variables = extract_variables(content)
        assert set(variables) == {"var_1", "var2"}

    def test_variables_at_edges(self):
        content = "{{start}} middle {{end}}"
        variables = extract_variables(content)
        assert set(variables) == {"start", "end"}

    def test_malformed_variables(self):
        content = "Broken {{var and {{ok}}"
        variables = extract_variables(content)
        assert variables == ["ok"]