import React from "react";

export default function SearchBar({ value, onChange, placeholder = "Search..." }) {
  return (
    <input
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
    />
  );
}