import React from "react";

export default function CollectionCard({ collection, onClick }) {
  return (
    <div
      className="p-3 rounded-md bg-gray-100 hover:bg-gray-200 cursor-pointer transition"
      onClick={onClick}
    >
      <p className="font-medium">{collection.name}</p>
    </div>
  );
}