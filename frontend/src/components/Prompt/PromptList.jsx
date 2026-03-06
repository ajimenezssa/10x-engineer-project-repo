// src/components/Prompts/PromptList.jsx
function PromptList({ prompts }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {prompts.map((prompt) => (
        <div
          key={prompt.id}
          className="bg-light p-4 rounded shadow-sm hover:shadow-md transition"
        >
          <h3 className="text-dark font-semibold">{prompt.title}</h3>
          <p className="text-dark mt-1">{prompt.content}</p>
          {prompt.description && (
            <p className="text-dark mt-1 text-sm">{prompt.description}</p>
          )}
        </div>
      ))}
    </div>
  );
}

export default PromptList;