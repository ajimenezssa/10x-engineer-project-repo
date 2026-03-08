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

  // --- Collection state ---
  const [editingCollection, setEditingCollection] = useState(null);
  const [showCollectionForm, setShowCollectionForm] = useState(false);
  const [selectedCollectionId, setSelectedCollectionId] = useState("");

  // --- Prompt search ---
  const [promptSearchQuery, setPromptSearchQuery] = useState("");

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
  const handleSubmitCollection = async (data) => {
    try {
      let result;
      if (editingCollection) {
        // For simplicity, let's reuse createCollection as updateCollection
        // You can replace with real updateCollection API call
        result = await createCollection({ ...editingCollection, ...data });
        setCollections((prev) =>
          prev.map((c) => (c.id === result.id ? result : c))
        );
      } else {
        result = await createCollection(data);
        setCollections((prev) => [...prev, result]);
      }
    } catch (err) {
      alert("Failed to save collection: " + err.message);
    } finally {
      setShowCollectionForm(false);
      setEditingCollection(null);
    }
  };

  const handleDeleteCollection = async (collection) => {
    if (!window.confirm(`Delete collection "${collection.name}"?`)) return;

    try {
      await deleteCollection(collection.id);
      setCollections((prev) => prev.filter((c) => c.id !== collection.id));

      // If the deleted collection was selected, reset filter
      if (selectedCollectionId === collection.id) {
        setSelectedCollectionId("");
      }
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

  // --- Filter prompts ---
  const filteredPrompts = prompts
    .filter(p => !selectedCollectionId || p.collection?.id === selectedCollectionId)
    .filter(p => p.title.toLowerCase().includes(promptSearchQuery.toLowerCase()));

  return (
    <Layout>
      {/* Collections Section */}
      <h2 className="text-2xl font-bold mb-2">Collections</h2>
      <div className="flex items-center gap-2 mb-4 flex-wrap">
        {/* Collections Dropdown */}
        <select
          className="border border-gray-300 p-1 rounded text-sm"
          value={selectedCollectionId}
          onChange={(e) => setSelectedCollectionId(e.target.value)}
        >
          <option value="">All Collections</option>
          {collections.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>

        {/* Edit/Delete buttons */}
        {selectedCollectionId && (
          <>
            <button
              className="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
              onClick={() => {
                const collection = collections.find(c => c.id === selectedCollectionId);
                setEditingCollection(collection);
                setShowCollectionForm(true);
              }}
            >
              Edit
            </button>
            <button
              className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              onClick={() => handleDeleteCollection(collections.find(c => c.id === selectedCollectionId))}
            >
              Delete
            </button>
          </>
        )}

        {/* New Collection button */}
        {!showCollectionForm && (
          <button
            className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
            onClick={() => {
              setEditingCollection(null);
              setShowCollectionForm(true);
            }}
          >
            New Collection
          </button>
        )}

        {/* Collection Form */}
        {showCollectionForm && (
          <CollectionForm
            collection={editingCollection}
            onSubmit={handleSubmitCollection}
            onCancel={() => setShowCollectionForm(false)}
          />
        )}
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} />}

      {!loading && !error && (
        <>
          {/* Prompts Section */}
          <div className="mt-6 mb-4">
            {/* Prompts Header + New Button */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 gap-2">
                <div className="flex items-center gap-2">
                  <h2 className="text-2xl font-bold">Prompts</h2>

                  {/* New Prompt Button */}
                  {!showPromptForm && (
                    <button
                      className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                      onClick={handleCreatePrompt}
                    >
                      New Prompt
                    </button>
                  )}
                </div>

                {/* Search Prompt Box */}
                {!showPromptForm && (
                  <input
                    type="text"
                    value={promptSearchQuery}
                    onChange={(e) => setPromptSearchQuery(e.target.value)}
                    placeholder="Search prompts..."
                    className="border border-gray-300 p-1 rounded text-sm w-full sm:w-64 mt-2 sm:mt-0"
                  />
                )}
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
              onPromptEdit={handleEditPrompt}
              onPromptDelete={handleDeletePrompt}
            />

            {/* Prompt Detail */}
            {selectedPrompt && (
              <PromptDetail
                prompt={selectedPrompt}
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