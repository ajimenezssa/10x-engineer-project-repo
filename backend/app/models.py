"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4

# ==============Functionality ==============

def generate_id() -> str:
    """Generate a unique identifier for models.

    Returns:
        str: A unique UUID4 string.

    Example:
        id = generate_id()
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC datetime.

    Returns:
        datetime: The current UTC datetime.

    Example:
        current_time = get_current_time()
    """
    return datetime.utcnow()

# ============== Tag Model ==============
class Tag(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for Prompt with common fields.

    Attributes:
        title (str): The title of the prompt, required, min length 1, max length 200.
        content (str): The main content of the prompt, required, min length 1.
        description (Optional[str]): A brief description of the prompt, optional, max length 500.
        collection_id (Optional[str]): ID of the associated collection, optional.
    """
    
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PromptCreate(PromptBase):
    """Model for creating a new Prompt, inheriting from PromptBase."""
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing Prompt, identical to PromptBase."""
    pass


class Prompt(PromptBase):
    """Model representing a complete Prompt with metadata.

    Attributes:
        id (str): Unique identifier for the Prompt, auto-generated.
        created_at (datetime): Timestamp when the Prompt was created.
        updated_at (datetime): Timestamp when the Prompt was last updated.

    Example:
        prompt = Prompt(title="Example Title", content="This is the content.")
    """
    
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    tags: List[Tag] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for Collection with common fields.

    Attributes:
        name (str): The name of the collection, required, min length 1, max length 100.
        description (Optional[str]): A brief description of the collection, optional, max length 500.
    """
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)


class CollectionCreate(CollectionBase):
    """Model for creating a new Collection, inheriting from CollectionBase."""
    pass


class Collection(CollectionBase):
    """Model representing a complete Collection with metadata.

    Attributes:
        id (str): Unique identifier for the Collection, auto-generated.
        created_at (datetime): Timestamp when the Collection was created.

    Example:
        collection = Collection(name="Example Collection")
    """
    
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)

# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for listing Prompts.

    Attributes:
        prompts (List[Prompt]): List of Prompt objects.
        total (int): Total number of prompts.
    """
    
    prompts: List[Prompt]
    total: int

    model_config = ConfigDict(from_attributes=True)


class CollectionList(BaseModel):
    """Response model for listing Collections.

    Attributes:
        collections (List[Collection]): List of Collection objects.
        total (int): Total number of collections.
    """
    
    collections: List[Collection]
    total: int

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    """Response model for health checks.

    Attributes:
        status (str): The status of the service, typically "ok" or "error".
        version (str): The current version of the service.
    """
    
    status: str
    version: str

    model_config = ConfigDict(from_attributes=True)
