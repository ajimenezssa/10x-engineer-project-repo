import { useEffect, useState } from "react";
import { fetchPrompts } from "./api/api";
import Layout from "./components/Layout/Layout";
import PromptList from "./components/Prompt/PromptList"; // placeholder for modular prompt rendering

function App() {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadPrompts() {
      try {
        const promptsData = await fetchPrompts();
        setPrompts(promptsData);
      } catch (err) {
        console.error(err);
        setError("Failed to load prompts.");
      } finally {
        setLoading(false);
      }
    }

    loadPrompts();
  }, []);

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-6 text-dark">
        Prompts
      </h2>

      {loading && <p className="text-dark">Loading prompts...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <PromptList prompts={prompts} />
      )}
    </Layout>
  );
}

export default App;