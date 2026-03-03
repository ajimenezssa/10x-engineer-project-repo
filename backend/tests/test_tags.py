import pytest
from uuid import uuid4

from app.models import Prompt
from app.tags import TagService, TagAlreadyExistsError, TagNotFoundError, InvalidTagNameError


# ======================================================
# Prompt ↔ Tag Assignment
# ======================================================

class TestPromptTagAssignment:

    def test_assign_tag_to_prompt(self):
        service = TagService()

        prompt = Prompt(id=str(uuid4()), title="Test", content="Content")
        tag = service.create_tag(name="python")

        service.assign_tag_to_prompt(prompt, tag.id)

        assert len(prompt.tags) == 1
        assert prompt.tags[0].name == "python"

    def test_assign_invalid_tag_should_fail(self):
        service = TagService()

        prompt = Prompt(id=str(uuid4()), title="Test", content="Content")

        with pytest.raises(TagNotFoundError):
            service.assign_tag_to_prompt(prompt, str(uuid4()))

    def test_prevent_duplicate_prompt_tag_assignment(self):
        service = TagService()

        prompt = Prompt(id=str(uuid4()), title="Test", content="Content")
        tag = service.create_tag(name="ai")

        service.assign_tag_to_prompt(prompt, tag.id)
        service.assign_tag_to_prompt(prompt, tag.id)

        assert len(prompt.tags) == 1

    def test_remove_tag_from_prompt(self):
        service = TagService()

        prompt = Prompt(id=str(uuid4()), title="Test", content="Content")
        tag = service.create_tag(name="backend")

        service.assign_tag_to_prompt(prompt, tag.id)
        service.remove_tag_from_prompt(prompt, tag.id)

        assert len(prompt.tags) == 0


# ======================================================
# Cascade Behavior
# ======================================================

class TestCascadeBehavior:

    def test_deleting_tag_removes_it_from_all_prompts(self):
        service = TagService()

        prompt1 = Prompt(id=str(uuid4()), title="P1", content="C1")
        prompt2 = Prompt(id=str(uuid4()), title="P2", content="C2")

        tag = service.create_tag(name="shared")

        service.assign_tag_to_prompt(prompt1, tag.id)
        service.assign_tag_to_prompt(prompt2, tag.id)

        # Pass prompts to delete_tag for cascade removal
        service.delete_tag(tag.id, prompts=[prompt1, prompt2])

        assert len(prompt1.tags) == 0
        assert len(prompt2.tags) == 0


# ======================================================
# Filtering Logic
# ======================================================

class TestFiltering:

    def test_filter_by_single_tag(self):
        service = TagService()

        prompt1 = Prompt(id=str(uuid4()), title="AI", content="C1")
        prompt2 = Prompt(id=str(uuid4()), title="Backend", content="C2")

        tag_ai = service.create_tag(name="ai")

        service.assign_tag_to_prompt(prompt1, tag_ai.id)

        results = service.filter_prompts_by_tags(
            prompts=[prompt1, prompt2],
            tag_ids=[tag_ai.id],
            match_all=False
        )

        assert len(results) == 1
        assert results[0].title == "AI"

    def test_filter_match_all(self):
        service = TagService()

        prompt = Prompt(id=str(uuid4()), title="Full", content="C")

        tag1 = service.create_tag(name="ai")
        tag2 = service.create_tag(name="backend")

        service.assign_tag_to_prompt(prompt, tag1.id)
        service.assign_tag_to_prompt(prompt, tag2.id)

        results = service.filter_prompts_by_tags(
            prompts=[prompt],
            tag_ids=[tag1.id, tag2.id],
            match_all=True
        )

        assert len(results) == 1

    def test_filter_match_all_fail_if_not_all_present(self):
        service = TagService()

        prompt = Prompt(id=str(uuid4()), title="Partial", content="C")

        tag1 = service.create_tag(name="ai")
        tag2 = service.create_tag(name="backend")

        service.assign_tag_to_prompt(prompt, tag1.id)

        results = service.filter_prompts_by_tags(
            prompts=[prompt],
            tag_ids=[tag1.id, tag2.id],
            match_all=True
        )

        assert len(results) == 0