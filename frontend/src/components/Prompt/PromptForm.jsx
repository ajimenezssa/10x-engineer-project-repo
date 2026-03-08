import React, { useState } from "react";

function PromptForm({ prompt = null, onSubmit, onCancel, collections = [] }) {
  const [title, setTitle] = useState(prompt?.title || "");
  const [description, setDescription] = useState(prompt?.description || "");
  const [content, setContent] = useState(prompt?.content || "");
  const [collectionId, setCollectionId] = useState(prompt?.collection_id || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      alert("Title and content cannot be empty");
      return;
    }
    onSubmit({
      title: title.trim(),
      content: content.trim(),
      description: description.trim(),
      collection_id: collectionId || null,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 w-full">
      {/* Title */}
      <div className="mb-4 w-full">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Prompt Title"
          className="border p-2 rounded w-full"
          required
        />
      </div>

      {/* Description */}
      <div className="mb-4 w-full">
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Prompt Description (optional)"
          className="border p-2 rounded w-full h-20"
        />
      </div>

      {/* Content */}
      <div className="mb-4 w-full">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Prompt Content"
          className="border p-2 rounded w-full h-32"
          required
        />
      </div>

      {/* Collection Select */}
      <div className="mb-4 w-full">
        <select
          value={collectionId}
          onChange={(e) => setCollectionId(e.target.value)}
          className="border p-2 rounded w-full"
        >
          <option value="">No Collection</option>
          {collections.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {/* Buttons */}
      <div className="flex flex-col gap-2 sm:flex-row sm:gap-2 w-full">
        <button
          type="submit"
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 w-full sm:w-auto"
        >
          {prompt ? "Save" : "Create"}
        </button>
        <button
          type="button"
          className="px-3 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 w-full sm:w-auto"
          onClick={onCancel}
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

export default PromptForm;