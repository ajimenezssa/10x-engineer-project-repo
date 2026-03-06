import React, { useState } from "react";

function PromptForm({ prompt = null, onSubmit, onCancel, collections = [] }) {
  // Initialize state safely from props
  // Using prompt?.id as key forces React to remount when prompt changes
  const [title, setTitle] = useState(prompt?.title || "");
  const [content, setContent] = useState(prompt?.content || "");
  const [collectionId, setCollectionId] = useState(prompt?.collection?.id || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Include collection_id in payload; null if no collection selected
    onSubmit({ title, content, collection_id: collectionId || null });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 mb-4" key={prompt?.id}>
      <input
        className="border p-2 rounded"
        type="text"
        placeholder="Prompt Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        className="border p-2 rounded"
        placeholder="Prompt Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        required
      />

      {/* Collection selector */}
      <select
        value={collectionId}
        onChange={(e) => setCollectionId(e.target.value || "")}
        className="border p-2 rounded"
      >
        <option value="">No collection</option>
        {collections.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}
      </select>

      <div className="flex gap-2">
        <button
          type="submit"
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {prompt ? "Update" : "Create"}
        </button>
        {onCancel && (
          <button
            type="button"
            className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
            onClick={onCancel}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

export default PromptForm;