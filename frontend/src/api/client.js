const BASE_URL = "/api"; // Vite proxy

export async function apiClient(endpoint, options = {}) {
  const config = {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    body: options.body ? JSON.stringify(options.body) : null,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, config);

  // Throw error if response is not ok
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "API request failed");
  }

  // Only parse JSON if there is a body
  if (response.status !== 204) {
    try {
      return await response.json();
    } catch {
      return null; // safe fallback for empty or invalid JSON
    }
  }

  return null; // DELETE / 204 No Content
}