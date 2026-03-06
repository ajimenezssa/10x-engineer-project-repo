import React from "react";

function CollectionList({ collections = [], onDeleteCollection }) {
  if (collections.length === 0) {
    return <p className="text-gray-500">No collections yet.</p>;
  }

  return (
    <div className="flex flex-col gap-2">
      {collections.map((collection) => (
        <div
          key={collection.id}
          className="flex justify-between items-center p-2 border rounded hover:bg-gray-50"
        >
          <span>{collection.name}</span>
          {onDeleteCollection && collection.id && (
            <button
              className="text-red-500 hover:text-red-700 font-semibold"
              onClick={() => onDeleteCollection(collection.id)}
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