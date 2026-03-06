import { useEffect, useState } from "react";
import { getPrompts } from "./api/prompts";
import { getCollections, createCollection, deleteCollection } from "./api/collections";
import Layout from "./components/Layout/Layout";
import PromptList from "./components/Prompt/PromptList";
import CollectionList from "./components/Collection/CollectionList";
import CollectionForm from "./components/Collection/CollectionForm";
import LoadingSpinner from "./components/Shared/LoadingSpinner";
import ErrorMessage from "./components/Shared/ErrorMessage";

function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch prompts and collections
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);

        const [promptsData, collectionsData] = await Promise.all([
          getPrompts(),
          getCollections(),
        ]);

        console.log("Prompts API response:", promptsData);
        console.log("Collections API response:", collectionsData);

        // Ensure arrays
        setPrompts(
          Array.isArray(promptsData)
            ? promptsData
            : Array.isArray(promptsData.prompts)
            ? promptsData.prompts
            : []
        );

        setCollections(
          Array.isArray(collectionsData)
            ? collectionsData
            : Array.isArray(collectionsData.collections)
            ? collectionsData.collections
            : []
        );
      } catch (err) {
        console.error(err);
        setError(err.message || "Failed to load data.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // Add collection
  const handleAddCollection = async (newCollection) => {
    try {
      const created = await createCollection(newCollection); // backend returns object with id
      setCollections((prev) => [...prev, created]);
    } catch (err) {
      alert("Failed to create collection: " + err.message);
    }
  };

  // Delete collection permanently
  const handleDeleteCollection = async (id) => {
    if (!window.confirm("Are you sure you want to delete this collection?")) return;

    try {
      await deleteCollection(id); // delete from backend
      setCollections((prev) => prev.filter((c) => c.id !== id)); // remove from frontend state
    } catch (err) {
      alert("Failed to delete collection: " + err.message);
    }
  };

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-4">Collections</h2>
      <CollectionForm onSubmit={handleAddCollection} />

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} />}

      {!loading && !error && (
        <>
          <CollectionList
            collections={collections || []}
            onDeleteCollection={handleDeleteCollection}
          />

          <h2 className="text-2xl font-bold my-6">Prompts</h2>
          <PromptList prompts={prompts || []} />
        </>
      )}
    </Layout>
  );
}

export default App;