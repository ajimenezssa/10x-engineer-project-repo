import React, { useState } from "react";

function PromptForm({ prompt = {}, onSubmit, onCancel }) {
  const [title, setTitle] = useState(prompt.title || "");
  const [content, setContent] = useState(prompt.content || "");
  const [description, setDescription] = useState(prompt.description || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !content) {
      setError("Title and content are required.");
      return;
    }
    setLoading(true);
    try {
      await onSubmit({ title, content, description });
    } catch (err) {
      setError("Failed to submit prompt.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="bg-light p-6 rounded shadow-md space-y-4" onSubmit={handleSubmit}>
      {error && <p className="text-red-500">{error}</p>}

      <div>
        <label className="block text-dark font-medium mb-1">Title</label>
        <input
          type="text"
          className="w-full p-2 border border-dark rounded"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block text-dark font-medium mb-1">Content</label>
        <textarea
          className="w-full p-2 border border-dark rounded"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block text-dark font-medium mb-1">Description</label>
        <textarea
          className="w-full p-2 border border-dark rounded"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <div className="flex space-x-2">
        <button
          type="submit"
          className="px-4 py-2 bg-primary text-white rounded hover:bg-accent transition"
          disabled={loading}
        >
          {loading ? "Saving..." : "Save"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-secondary text-white rounded hover:bg-accent transition"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

export default PromptForm;