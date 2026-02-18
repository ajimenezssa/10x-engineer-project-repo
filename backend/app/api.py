"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check the health status of the API.

    Returns:
        HealthResponse: A JSON response with the current status and version
        of the API.

    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Retrieve a list of prompts, optionally filtered by collection or search query.

    Args:
        collection_id (Optional[str]): An optional collection ID to filter prompts.
        search (Optional[str]): An optional search query to filter prompts by text.

    Returns:
        PromptList: A list of prompts with total count, filtered and sorted.

    Raises:
        HTTPException: If any error occurs during filtering or retrieval.

    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    # BUG #1: This will raise a 500 error if prompt doesn't exist
    # because we're accessing .id on None
    # Should return 404 instead!
    """Retrieve a specific prompt by its ID.

    Args:
        prompt_id (str): The unique identifier of the prompt.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: If the prompt with given ID is not found, raises 404.

    """
    prompt = storage.get_prompt(prompt_id)
    # SOLUTION #1:
    # If prompt is None, return a 404 error
    if prompt is None:
        raise HTTPException(status_code=404, detail=f"Prompt with ID {prompt_id} not found")

    # The following line will no longer cause the bug
    if prompt.id:
        return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    # Validate collection exists if provided
    """Create a new prompt.

    Args:
        prompt_data (PromptCreate): The data required to create a new prompt.

    Returns:
        Prompt: The created prompt object.

    Raises:
        HTTPException: If the collection ID doesn't exist, raises 400.

    """
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update an existing prompt with new data.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The updated data for the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or collection is not found, raises 404/400.

    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2: We're not updating the updated_at timestamp!
    # The updated prompt keeps the old timestamp
    # SOLUTION: Set updated_at to the current time to reflect the update operation.
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,  # Unchanged creation date
        updated_at=get_current_time()  # Correctly updating the updated_at timestamp
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def partial_update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update an existing Prompt record. Only updates provided fields.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): A PromptUpdate object with optional fields for update.

    Returns:
        Prompt: The updated Prompt object.

    Raises:
        HTTPException: If the prompt or collection is not found, raises 404/400.

    """
    # Step 1: Fetch the existing prompt to be updated
    existing = storage.get_prompt(prompt_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Step 2: Validate the collection if collection_id is provided
    if prompt_data.collection_id is not None:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Step 3: Update only the fields provided by the user
    # Create a dictionary of the updates to perform
    updates = {key: value for key, value in prompt_data.__dict__.items() if value is not None}

    # Update the existing prompt object with the new values
    for key, value in updates.items():
        setattr(existing, key, value)

    # Always update the updated_at field
    existing.updated_at = get_current_time()
    # Step 4: Save the updated prompt using storage method
    return storage.update_prompt(prompt_id, existing)

@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None: Indicates successful deletion with no content.

    Raises:
        HTTPException: If the prompt is not found, raises 404.

    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Retrieve a list of all collections.

    Returns:
        CollectionList: A list of collections with total count.

    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a specific collection by its ID.

    Args:
        collection_id (str): The unique identifier of the collection.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found, raises 404.

    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data (CollectionCreate): The data required to create a new collection.

    Returns:
        Collection: The created collection object.

    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    # BUG #4: We delete the collection but don't handle the prompts!
    # Prompts with this collection_id become orphaned with invalid reference
    # Should either: delete the prompts, set collection_id to None, or prevent deletion
    # SELECTED SOLUTION: Nullify references
    # Step 1: Check if the collection exists. If not, raise a 404.
    """Delete a collection by ID and handle associated prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None: Indicates successful deletion with no content.

    Raises:
        HTTPException: If the collection is not found, raises 404.

    """
    collection = storage.get_collection(collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Step 2: Fetch all prompts and update the ones belonging to this collection.
    prompts = storage.get_all_prompts()
    for prompt in prompts:
        if prompt.collection_id == collection_id:
            # Step 2a: Set collection_id to None and update updated_at timestamp.
            prompt.collection_id = None
            prompt.updated_at = get_current_time()
            # Step 2b: Update the prompt in storage.
            storage.update_prompt(prompt.id, prompt)
    
    # Step 3: Delete the collection since prompts have been handled.
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    # Step 4: Return None, using status_code=204 to indicate success with no content.
    return None

