from uuid import UUID
from typing import List


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
# TagService Skeleton
# ======================================================

class TagService:

    def create_tag(self, name: str, description: str | None = None):
        raise NotImplementedError

    def rename_tag(self, tag_id: UUID, new_name: str):
        raise NotImplementedError

    def delete_tag(self, tag_id: UUID):
        raise NotImplementedError

    def get_tag(self, tag_id: UUID):
        raise NotImplementedError

    def assign_tag_to_prompt(self, prompt, tag_id: UUID):
        raise NotImplementedError

    def remove_tag_from_prompt(self, prompt, tag_id: UUID):
        raise NotImplementedError

    def filter_prompts_by_tags(
        self,
        prompts: List,
        tag_ids: List[UUID],
        match_all: bool = False
    ):
        raise NotImplementedError