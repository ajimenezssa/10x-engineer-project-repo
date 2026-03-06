import { useEffect, useState } from "react";
import {
  getPrompts,
  createPrompt,
  updatePrompt,
  deletePrompt,
} from "./api/prompts";
import {
  getCollections,
  createCollection,
  deleteCollection,
} from "./api/collections";

import Layout from "./components/Layout/Layout";
import PromptList from "./components/Prompt/PromptList";
import PromptForm from "./components/Prompt/PromptForm";
import PromptDetail from "./components/Prompt/PromptDetail";

import CollectionList from "./components/Collection/CollectionList";
import CollectionForm from "./components/Collection/CollectionForm";

import LoadingSpinner from "./components/Shared/LoadingSpinner";
import ErrorMessage from "./components/Shared/ErrorMessage";

function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Prompt state ---
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [showPromptForm, setShowPromptForm] = useState(false);

  // --- Collection filter ---
  const [selectedCollectionId, setSelectedCollectionId] = useState("");

  // --- Fetch prompts and collections ---
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const [promptsData, collectionsData] = await Promise.all([
          getPrompts(),
          getCollections(),
        ]);

        setPrompts(Array.isArray(promptsData) ? promptsData : []);
        setCollections(Array.isArray(collectionsData) ? collectionsData : []);
      } catch (err) {
        console.error(err);
        setError(err.message || "Failed to load data.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // --- Collections CRUD ---
  const handleAddCollection = async (newCollection) => {
    try {
      const created = await createCollection(newCollection);
      setCollections((prev) => [...prev, created]);
    } catch (err) {
      alert("Failed to create collection: " + err.message);
    }
  };

  const handleDeleteCollection = async (collection) => {
    if (!window.confirm(`Delete collection "${collection.name}"?`)) return;

    try {
      await deleteCollection(collection.id);
      setCollections((prev) => prev.filter((c) => c.id !== collection.id));
    } catch (err) {
      alert("Failed to delete collection: " + err.message);
    }
  };

  // --- Prompts CRUD ---
  const handleCreatePrompt = () => {
    setEditingPrompt(null);
    setShowPromptForm(true);
  };

  const handleEditPrompt = (prompt) => {
    setEditingPrompt(prompt);
    setShowPromptForm(true);
  };

  const handleSubmitPrompt = async (data) => {
    try {
      let result;
      if (editingPrompt) {
        result = await updatePrompt(editingPrompt.id, data);

        if (result.collection_id) {
          const collectionObj = collections.find(c => c.id === result.collection_id);
          result.collection = collectionObj || null;
        }

        setPrompts((prev) =>
          prev.map((p) => (p.id === result.id ? result : p))
        );
      } else {
        result = await createPrompt(data);
        const newPrompt = result.prompt || result;

        if (newPrompt.collection_id) {
          const collectionObj = collections.find(c => c.id === newPrompt.collection_id);
          newPrompt.collection = collectionObj || null;
        }

        setPrompts((prev) => [...prev, newPrompt]);
      }
    } catch (err) {
      alert("Failed to save prompt: " + err.message);
    } finally {
      setShowPromptForm(false);
      setEditingPrompt(null);
    }
  };

  const handleDeletePrompt = async (prompt) => {
    if (!window.confirm(`Delete prompt "${prompt.title}"?`)) return;

    try {
      await deletePrompt(prompt.id);
      setPrompts((prev) => prev.filter((p) => p.id !== prompt.id));
      if (selectedPrompt?.id === prompt.id) setSelectedPrompt(null);
    } catch (err) {
      alert("Failed to delete prompt: " + err.message);
    }
  };

  const handleViewPrompt = (prompt) => setSelectedPrompt(prompt);
  const handleClosePromptDetail = () => setSelectedPrompt(null);

  // --- Filter prompts ---
  const filteredPrompts = selectedCollectionId
    ? prompts.filter(p => p.collection?.id === selectedCollectionId)
    : prompts;

  return (
    <Layout>
      {/* Collections Section */}
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

          {/* Prompts Section */}
          <div className="mt-6 mb-4">
            {/* Filter */}
            <h2 className="text-xl font-semibold mb-2">Filter</h2>
            <select
              className="border p-2 rounded mb-4"
              value={selectedCollectionId}
              onChange={(e) => setSelectedCollectionId(e.target.value)}
            >
              <option value="">All Collections</option>
              {collections.map(c => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>

            {/* Prompts Title + New Prompt Button */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Prompts</h2>
              <button
                className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                onClick={handleCreatePrompt}
              >
                New Prompt
              </button>
            </div>

            {/* Prompt Form */}
            {showPromptForm && (
              <PromptForm
                prompt={editingPrompt}
                onSubmit={handleSubmitPrompt}
                onCancel={() => setShowPromptForm(false)}
                collections={collections}
              />
            )}

            {/* Prompt List */}
            <PromptList
              prompts={filteredPrompts || []}
              onPromptClick={handleViewPrompt}
              onPromptEdit={handleEditPrompt}
              onPromptDelete={handleDeletePrompt}
            />

            {/* Prompt Detail */}
            {selectedPrompt && (
              <PromptDetail
                prompt={selectedPrompt}
                onClose={handleClosePromptDetail}
                onEdit={handleEditPrompt}
                onDelete={handleDeletePrompt}
              />
            )}
          </div>
        </>
      )}
    </Layout>
  );
}

export default App;