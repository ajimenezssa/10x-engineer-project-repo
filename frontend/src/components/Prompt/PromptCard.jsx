import React from "react";

function PromptCard({ prompt, onClick, onEdit, onDelete }) {
  return (
    <div
      className="border p-4 rounded shadow hover:shadow-lg cursor-pointer"
      onClick={onClick}
    >
      <h3 className="text-lg font-bold mb-2">{prompt.title}</h3>
      <p className="text-gray-700 mb-2">{prompt.content}</p>

      <div className="flex gap-2 mt-2">
        {onEdit && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onEdit();
            }}
            className="px-2 py-1 bg-yellow-400 text-white rounded hover:bg-yellow-500"
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
            className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
}

export default PromptCard;