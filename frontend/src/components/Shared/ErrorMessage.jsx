import React from "react";

export default function ErrorMessage({ message }) {
  return (
    <p className="text-red-500 bg-red-100 p-2 rounded-md border border-red-200">
      {message}
    </p>
  );
}