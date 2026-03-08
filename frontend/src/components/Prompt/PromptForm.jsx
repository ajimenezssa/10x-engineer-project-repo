import React, { useState } from "react";

function PromptForm({ prompt = null, onSubmit, onCancel, collections = [] }) {
  const [title, setTitle] = useState(prompt?.title || "");
  const [content, setContent] = useState(prompt?.content || "");
  const [collectionId, setCollectionId] = useState(prompt?.collection?.id || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ title, content, collection_id: collectionId || null });
  };

  const commonInputClass =
    "border p-2 rounded w-full text-sm font-sans"; // <-- same font for all

  return (
    <form
      onSubmit={handleSubmit}
      key={prompt?.id}
      className="bg-white shadow rounded p-4 mb-6 space-y-4"
    >
      <div>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Prompt Title"
          className={commonInputClass}
          required
          autoFocus
        />
      </div>

      <div>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Prompt Content"
          className={commonInputClass}
          rows={4}
          required
        />
      </div>

      <div>
        <select
          value={collectionId}
          onChange={(e) => setCollectionId(e.target.value || "")}
          className={commonInputClass}
        >
          <option value="">No collection</option>
          {collections.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

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
            className="px-3 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
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