from uuid import UUID, uuid4
from typing import List, Dict

from app.models import Tag, Prompt


# ======================================================
# Custom Exceptions
# ======================================================

class TagAlreadyExistsError(Exception):
    pass


class TagNotFoundError(Exception):
    pass


class InvalidTagNameError(Exception):
    pass


# ======================================================
# TagService Implementation
# ======================================================

class TagService:
    def __init__(self):
        self._tags: Dict[str, Tag] = {}  # key is string now

    def create_tag(self, name: str, description: str | None = None) -> Tag:
        if not name.strip():
            raise InvalidTagNameError("Tag name cannot be blank.")

        # Check for duplicates (case-insensitive)
        for tag in self._tags.values():
            if tag.name.lower() == name.lower():
                raise TagAlreadyExistsError(f"Tag '{name}' already exists.")

        tag = Tag(name=name, description=description)  # ✅ let Pydantic generate string id
        self._tags[tag.id] = tag
        return tag

    def rename_tag(self, tag_id: str, new_name: str) -> Tag:
        if not new_name.strip():
            raise InvalidTagNameError("Tag name cannot be blank.")

        for tag in self._tags.values():
            if tag.name.lower() == new_name.lower():
                raise TagAlreadyExistsError(f"Tag '{new_name}' already exists.")

        tag = self._tags.get(tag_id)
        if not tag:
            raise TagNotFoundError()

        tag.name = new_name
        return tag

    def delete_tag(self, tag_id: str, prompts: List[Prompt] = None):
        tag = self._tags.pop(tag_id, None)
        if not tag:
            raise TagNotFoundError()
        if prompts:
            for prompt in prompts:
                prompt.tags = [t for t in prompt.tags if t.id != tag_id]

    def get_tag(self, tag_id: str) -> Tag:
        tag = self._tags.get(tag_id)
        if not tag:
            raise TagNotFoundError()
        return tag

    def assign_tag_to_prompt(self, prompt: Prompt, tag_id: str):
        tag = self._tags.get(tag_id)
        if not tag:
            raise TagNotFoundError()
        if tag not in prompt.tags:
            prompt.tags.append(tag)

    def remove_tag_from_prompt(self, prompt: Prompt, tag_id: str):
        prompt.tags = [t for t in prompt.tags if t.id != tag_id]

    def filter_prompts_by_tags(
        self,
        prompts: List[Prompt],
        tag_ids: List[str],
        match_all: bool = False
    ) -> List[Prompt]:
        results = []
        for prompt in prompts:
            prompt_tag_ids = {t.id for t in prompt.tags}
            if match_all:
                if all(tid in prompt_tag_ids for tid in tag_ids):
                    results.append(prompt)
            else:
                if any(tid in prompt_tag_ids for tid in tag_ids):
                    results.append(prompt)
        return results