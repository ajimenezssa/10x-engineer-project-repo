import React, { useState } from "react";

function CollectionForm({ collection = null, onSubmit, onCancel }) {
  // Initialize name directly from collection prop (or empty for new)
  const [name, setName] = useState(collection?.name || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) {
      alert("Collection name cannot be empty");
      return;
    }
    onSubmit({ name: name.trim() });
    setName(""); // reset input after submit
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 mb-4">
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Collection Name"
        className="border p-2 rounded flex-1"
        autoFocus
        required
      />
      <button
        type="submit"
        className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
      >
        {collection ? "Save" : "Create"}
      </button>
      <button
        type="button"
        className="px-3 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
        onClick={onCancel}
      >
        Cancel
      </button>
    </form>
  );
}

export default CollectionForm;