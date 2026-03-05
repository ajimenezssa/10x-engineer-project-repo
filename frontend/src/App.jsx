import { useEffect, useState } from "react";
import { fetchPrompts } from "./api/api";
import "./App.css"; // Can be empty or Tailwind styles

function App() {
  const [prompts, setPrompts] = useState([]);

  useEffect(() => {
    async function loadPrompts() {
      const promptsData = await fetchPrompts();
      setPrompts(promptsData);
    }
    loadPrompts();
  }, []);

  return (
    <div className="min-h-screen bg-white p-8">
      <h1 className="text-3xl font-bold mb-6">Prompts</h1>

      {prompts.length === 0 ? (
        <p>No prompts found</p>
      ) : (
        <ul className="space-y-4">
          {prompts.map((prompt) => (
            <li
              key={prompt.id}
              className="border rounded p-4 shadow-sm hover:shadow-md transition"
            >
              <h2 className="text-xl font-semibold">{prompt.title}</h2>
              <p className="text-gray-700">{prompt.content}</p>
              {prompt.description && (
                <p className="text-gray-500 mt-1">{prompt.description}</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;