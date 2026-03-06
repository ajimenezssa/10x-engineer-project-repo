import React, { useState } from "react";

function PromptForm({ prompt = null, onSubmit, onCancel }) {
  // Initialize state from backend fields
  const [title, setTitle] = useState(prompt ? prompt.title : "");
  const [content, setContent] = useState(prompt ? prompt.content : "");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Send data matching backend model
    onSubmit({ title, content });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 mb-4">
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