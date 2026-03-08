import React, { useState } from "react";
import PromptForm from "./PromptForm";

function PromptList({ prompts, onPromptEditSubmit, onPromptDelete }) {
  const [expandedPrompts, setExpandedPrompts] = useState({});
  const [editingPromptId, setEditingPromptId] = useState(null);

  const togglePrompt = (id) => {
    setExpandedPrompts((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  if (!Array.isArray(prompts) || prompts.length === 0) {
    return <p className="text-dark">No prompts available.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Line separator at the top */}
      <hr className="border-t border-gray-300 mb-2" />

      {prompts.map((prompt) => (
        <div key={prompt.id} className="border rounded">
          {/* Title always visible */}
          <button
            className="w-full text-left p-2 font-bold bg-gray-100 hover:bg-gray-200 rounded-t"
            onClick={() => togglePrompt(prompt.id)}
          >
            {prompt.title} {expandedPrompts[prompt.id] ? "▾" : "▸"}
          </button>

          {/* Expanded content */}
          {expandedPrompts[prompt.id] && (
            <div className="p-2 flex flex-col gap-2 bg-gray-50 rounded-b">
              {/* Edit/Delete buttons next to title inside expanded section */}
              <div className="flex justify-end gap-2">
                <button
                  className="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 text-sm"
                  onClick={() => setEditingPromptId(prompt.id)}
                >
                  Edit
                </button>
                <button
                  className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
                  onClick={() => onPromptDelete && onPromptDelete(prompt)}
                >
                  Delete
                </button>
              </div>

              {/* Inline Edit Form */}
              {editingPromptId === prompt.id ? (
                <PromptForm
                  prompt={prompt}
                  onSubmit={(data) => {
                    onPromptEditSubmit(prompt.id, data);
                    setEditingPromptId(null);
                  }}
                  onCancel={() => setEditingPromptId(null)}
                />
              ) : (
                <>
                  <p>
                    <span className="font-semibold">Collection:</span>{" "}
                    {prompt.collection?.name || "No Collection"}
                  </p>
                  <p>
                    <span className="font-semibold">Description:</span>{" "}
                    {prompt.description || "No description"}
                  </p>
                  <p>
                    <span className="font-semibold">Content:</span> {prompt.content}
                  </p>
                </>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default PromptList;