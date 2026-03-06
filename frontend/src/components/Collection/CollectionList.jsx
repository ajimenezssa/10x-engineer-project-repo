import React from "react";
import CollectionCard from "./CollectionCard";

export default function CollectionList({ collections, onSelectCollection }) {
  if (!collections.length) {
    return <p className="text-gray-500">No collections yet.</p>;
  }

  return (
    <div className="flex flex-col gap-2">
      {collections.map((collection) => (
        <CollectionCard
          key={collection.id}
          collection={collection}
          onClick={() => onSelectCollection(collection)}
        />
      ))}
    </div>
  );
}