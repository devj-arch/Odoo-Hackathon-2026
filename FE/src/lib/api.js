const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  let body = null;
  try {
    body = await response.json();
  } catch {
    // Response had no JSON body (e.g. a network-level failure).
  }

  if (!response.ok) {
    const message = body?.detail || "Something went wrong. Try again.";
    throw new ApiError(message, response.status);
  }

  return body;
}

export function login({ email, password, role }) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password, role }),
  });
}

export function getCurrentUser(token) {
  return request("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export { ApiError };