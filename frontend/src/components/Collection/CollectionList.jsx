import React from "react";

function CollectionList({ collections = [], onDeleteCollection }) {
  if (!collections.length) return <p className="text-dark">No collections yet.</p>;

  return (
    <ul className="flex flex-wrap gap-3">
      {collections.map((collection) => (
        <li
          key={collection.id}
          className="border p-2 rounded flex items-center gap-2"
        >
          <span>{collection.name}</span>
          {onDeleteCollection && (
            <button
            onClick={() => onDeleteCollection(collection)}
            className="text-red-500 hover:text-red-700"
            >
            Delete
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}

export default CollectionList;