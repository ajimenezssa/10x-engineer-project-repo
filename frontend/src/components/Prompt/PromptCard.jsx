import React from "react";

function PromptCard({ prompt, onClick, onEdit, onDelete }) {
  return (
    <div
      className="bg-white p-4 rounded shadow-sm hover:shadow-md transition cursor-pointer"
      onClick={onClick}
    >
      <h3 className="text-dark font-semibold text-lg">{prompt.title}</h3>
      <p className="text-dark mt-1">{prompt.content}</p>
      {prompt.description && (
        <p className="text-dark mt-2 text-sm">{prompt.description}</p>
      )}

      {/* Optional action buttons */}
      <div className="mt-3 flex space-x-2">
        {onEdit && (
          <button
            onClick={(e) => { e.stopPropagation(); onEdit(); }}
            className="px-3 py-1 bg-primary text-white rounded hover:bg-accent transition text-sm"
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            onClick={(e) => { e.stopPropagation(); onDelete(); }}
            className="px-3 py-1 bg-secondary text-white rounded hover:bg-accent transition text-sm"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
}

export default PromptCard;
