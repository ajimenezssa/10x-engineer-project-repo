"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:

    """Sort prompts by their creation date.

    Sorts a list of `Prompt` objects by their creation date. 
    By default, it sorts in descending order (newest first).
    The behavior can be altered using the `descending` parameter.

    Args:
        prompts (List[Prompt]): List of prompts to sort.
        descending (bool, optional): If True, sorts newest first. Defaults to True.

    Returns:
        List[Prompt]: List of prompts sorted by creation date.

    Example:
        sorted_prompts = sort_prompts_by_date(prompts, descending=False)
    """
    # BUG #3: This sorts ascending (oldest first) when it should sort descending (newest first)
    # The 'descending' parameter is ignored!  
    # SOLUTION: This function now properly respects the 'descending' parameter. When descending=True (default), it sorts newest first. When descending=False, it sorts oldest first.
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts that belong to a specific collection.

    Filters the provided prompts to include only those 
    which match the given collection ID.

    Args:
        prompts (List[Prompt]): List of prompts to filter.
        collection_id (str): The ID of the collection to filter by.

    Returns:
        List[Prompt]: List of prompts that belong to the specified collection.

    Example:
        filtered_prompts = filter_prompts_by_collection(prompts, '12345')
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description.

    Searches for prompts where the search query is present in the title 
    or the description. Case insensitive.

    Args:
        prompts (List[Prompt]): List of prompts to search through.
        query (str): The search query string, case-insensitive.

    Returns:
        List[Prompt]: List of prompts matching the search query.

    Example:
        matched_prompts = search_prompts(prompts, 'interesting')
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
 
    """Validate the content of a prompt.

    Ensures that a prompt's content is not empty, not just whitespace, 
    and has at least 10 characters after trimming.

    Args:
        content (str): The content of the prompt.

    Returns:
        bool: True if the content is valid, False otherwise.

    Example:
        is_valid = validate_prompt_content("A valid prompt")
    """

    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Extracts variables in the format `{{variable_name}}` from the 
    content string.

    Args:
        content (str): The string from which to extract variables.

    Returns:
        List[str]: List of variable names found within the content.

    Example:
        variables = extract_variables("Hello {{name}}, welcome!")
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
