// src/api/collections.js
import { apiClient } from "./client";

// GET all collections
export async function getCollections() {
  return apiClient("/collections");
}

// CREATE new collection
export async function createCollection(data) {
  return apiClient("/collections", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// DELETE collection by ID
export async function deleteCollection(id) {
  await apiClient(`/collections/${id}`, { method: "DELETE" });
  return true; // frontend can update state after this
}