import React from "react";
import PromptCard from "./PromptCard";

function PromptList({ prompts, onPromptClick, onPromptEdit, onPromptDelete }) {
  if (!prompts || prompts.length === 0) {
    return <p className="text-dark">No prompts available.</p>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          onClick={() => onPromptClick && onPromptClick(prompt)}
          onEdit={() => onPromptEdit && onPromptEdit(prompt)}
          onDelete={() => onPromptDelete && onPromptDelete(prompt)}
        />
      ))}
    </div>
  );
}

export default PromptList;