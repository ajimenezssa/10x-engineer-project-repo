import React from "react";
import Modal from "../Shared/Modal"; // optional modal wrapper

function PromptDetail({ prompt, onClose, onEdit, onDelete }) {
  if (!prompt) return null;

  return (
    <Modal onClose={onClose}>
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-2">{prompt.name}</h2>
        <p className="text-gray-700 mb-4">{prompt.description}</p>
        {prompt.template && (
          <pre className="bg-gray-100 p-2 rounded mb-4">{prompt.template}</pre>
        )}

        <div className="flex justify-end gap-2">
          {onEdit && (
            <button
              className="px-3 py-1 bg-yellow-400 rounded hover:bg-yellow-500 text-white"
              onClick={() => onEdit(prompt)}
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              className="px-3 py-1 bg-red-500 rounded hover:bg-red-600 text-white"
              onClick={() => onDelete(prompt)}
            >
              Delete
            </button>
          )}
          <button
            className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </Modal>
  );
}

export default PromptDetail;