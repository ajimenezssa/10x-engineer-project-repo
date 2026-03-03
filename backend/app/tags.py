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
        self._tags: Dict[str, Tag] = {}

    # -------------------------
    # Private Helpers
    # -------------------------

    def _validate_name(self, name: str):
        if not name or not name.strip():
            raise InvalidTagNameError("Tag name cannot be blank.")

    def _ensure_name_unique(self, name: str, exclude_id: str | None = None):
        for tag in self._tags.values():
            if tag.name.lower() == name.lower():
                if exclude_id is None or tag.id != exclude_id:
                    raise TagAlreadyExistsError(f"Tag '{name}' already exists.")

    def _get_or_raise(self, tag_id: str) -> Tag:
        tag = self._tags.get(tag_id)
        if not tag:
            raise TagNotFoundError()
        return tag

    # -------------------------
    # Public API
    # -------------------------

    def create_tag(self, name: str, description: str | None = None) -> Tag:
        self._validate_name(name)
        self._ensure_name_unique(name)

        tag = Tag(name=name.strip(), description=description)
        self._tags[tag.id] = tag
        return tag

    def rename_tag(self, tag_id: str, new_name: str) -> Tag:
        self._validate_name(new_name)

        tag = self._get_or_raise(tag_id)
        self._ensure_name_unique(new_name, exclude_id=tag_id)

        tag.name = new_name.strip()
        return tag

    def delete_tag(self, tag_id: str, prompts: List[Prompt] | None = None):
        tag = self._get_or_raise(tag_id)
        del self._tags[tag_id]

        if prompts:
            for prompt in prompts:
                prompt.tags = [t for t in prompt.tags if t.id != tag_id]

    def get_tag(self, tag_id: str) -> Tag:
        return self._get_or_raise(tag_id)

    def assign_tag_to_prompt(self, prompt: Prompt, tag_id: str):
        tag = self._get_or_raise(tag_id)

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