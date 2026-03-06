// src/api/prompts.js
import { apiClient } from "./client";

// GET all prompts
export async function getPrompts() {
  return apiClient("/prompts");
}

// GET single prompt by ID
export async function getPrompt(id) {
  if (!id) throw new Error("Prompt ID is required");
  return apiClient(`/prompts/${id}`);
}

// CREATE a new prompt
export async function createPrompt(data) {
  if (!data) throw new Error("Prompt data is required");
  return apiClient("/prompts", {
    method: "POST",
    body: data, // client.js will stringify JSON
  });
}

// UPDATE an existing prompt
export async function updatePrompt(id, data) {
  if (!id) throw new Error("Prompt ID is required");
  if (!data) throw new Error("Prompt data is required");
  return apiClient(`/prompts/${id}`, {
    method: "PUT",
    body: data,
  });
}

// DELETE a prompt
export async function deletePrompt(id) {
  if (!id) throw new Error("Prompt ID is required");
  await apiClient(`/prompts/${id}`, { method: "DELETE" });
  return true; // frontend can update state
}