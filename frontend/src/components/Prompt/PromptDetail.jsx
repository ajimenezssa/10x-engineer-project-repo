import React from "react";

function PromptDetail({ prompt, onEdit, onDelete }) {
  return (
    <div className="bg-light p-6 rounded shadow-md space-y-4">
      <h2 className="text-2xl font-bold text-dark">{prompt.title}</h2>
      <p className="text-dark">{prompt.content}</p>
      {prompt.description && <p className="text-dark text-sm">{prompt.description}</p>}

      <div className="flex space-x-2 mt-4">
        {onEdit && (
          <button
            onClick={onEdit}
            className="px-4 py-2 bg-primary text-white rounded hover:bg-accent transition"
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            onClick={onDelete}
            className="px-4 py-2 bg-secondary text-white rounded hover:bg-accent transition"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
}

export default PromptDetail;