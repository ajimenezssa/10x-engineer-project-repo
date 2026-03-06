import React from "react";

export default function LoadingSpinner({ size = 8 }) {
  return (
    <div className="flex justify-center items-center">
      <div
        className={`animate-spin rounded-full border-4 border-t-blue-500 border-b-gray-200`}
        style={{ width: `${size}rem`, height: `${size}rem` }}
      />
    </div>
  );
}