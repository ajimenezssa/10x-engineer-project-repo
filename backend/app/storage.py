"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """Class for storing prompts and collections in memory."""

    def __init__(self):
        """Initializes the Storage class with empty dictionaries for prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Adds a new prompt to the storage.

        Args:
            prompt (Prompt): The prompt to be added.

        Returns:
            Prompt: The added prompt.

        Example:
            >>> storage.create_prompt(new_prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt with the specified ID, or None if not found.

        Example:
            >>> prompt = storage.get_prompt("prompt123")
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Gets all prompts in storage.

        Returns:
            List[Prompt]: A list of all prompts.

        Example:
            >>> all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The new prompt data.

        Returns:
            Optional[Prompt]: The updated prompt, or None if the prompt does not exist.

        Example:
            >>> updated_prompt = storage.update_prompt("prompt123", new_prompt_data)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was successfully deleted, False otherwise.

        Example:
            >>> success = storage.delete_prompt("prompt123")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Adds a new collection to storage.

        Args:
            collection (Collection): The collection to add.

        Returns:
            Collection: The added collection.

        Example:
            >>> storage.create_collection(new_collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieves a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection with the specified ID, or None if not found.

        Example:
            >>> collection = storage.get_collection("collection123")
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Gets all collections in storage.

        Returns:
            List[Collection]: A list of all collections.

        Example:
            >>> all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was successfully deleted, False otherwise.

        Example:
            >>> success = storage.delete_collection("collection123")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Gets all prompts that belong to a specific collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            List[Prompt]: A list of prompts belonging to the collection.

        Example:
            >>> prompts = storage.get_prompts_by_collection("collection123")
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clears all prompts and collections from storage.

        Example:
            >>> storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
