import React from "react";

function PromptDetail({ prompt, onClose, onEdit, onDelete }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h2 className="text-xl font-bold mb-2">{prompt.title}</h2>

        {/* Collection */}
        {prompt.collection?.name && (
          <p className="text-sm text-gray-500 mb-2">
            Collection: {prompt.collection.name}
          </p>
        )}

        <p className="text-gray-700 mb-4">{prompt.content}</p>

        <div className="flex gap-2 justify-end">
          {onEdit && (
            <button
              onClick={onEdit}
              className="px-3 py-1 bg-yellow-400 text-white rounded hover:bg-yellow-500"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={onDelete}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Delete
            </button>
          )}
          <button
            onClick={onClose}
            className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default PromptDetail;