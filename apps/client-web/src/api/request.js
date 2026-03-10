const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    let normalizedMessage = message;
    try {
      const parsed = JSON.parse(message);
      normalizedMessage = parsed.detail || parsed.message || message;
    } catch {
      normalizedMessage = message;
    }
    throw new Error(normalizedMessage || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
