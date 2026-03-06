import React from "react";

function CollectionList({ collections = [], onDeleteCollection }) {
  if (!collections.length) return <p className="text-dark">No collections yet.</p>;

  return (
    <div className="flex flex-wrap gap-2 mt-2">
      {collections.map((collection) => (
        <div
          key={collection.id}
          className="border p-2 rounded flex items-center justify-between"
        >
          <span>{collection.name}</span>
          {onDeleteCollection && (
            <button
              onClick={() => onDeleteCollection(collection)}
              className="text-red-500 hover:text-red-700 ml-2"
            >
              Delete
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default CollectionList;