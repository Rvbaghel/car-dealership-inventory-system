// 🔌 Centralized API Client Layer 
// Dynamically switches endpoints based on the deployment execution runtime environment.

const LOCAL_API_URL = 'http://127.0.0.1:8000';
const LIVE_API_URL = 'https://car-dealership-inventory-system-rouge.vercel.app';

// Detect whether Vite is running locally ('development') or in production
export const BASE_URL = import.meta.env.MODE === 'development' 
  ? LOCAL_API_URL 
  : LIVE_API_URL;

/**
 * Reusable Core Request Wrapper to enforce global auth tokens and JSON headers.
 */
async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  
  // Set default JSON headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Automatically inject the JWT token from localStorage if the user is logged in
  const token = localStorage.getItem('token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  // Convert body payload to standard JSON strings automatically if provided
  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  const response = await fetch(url, config);

  // If request hits validation errors or expired tokens, throw clean debug details
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
  }

  // Check if response is empty (e.g., 204 No Content)
  if (response.status === 204) return null;

  return response.json();
}

// 🌐 Structured Domain Endpoint Routing Bundles
export const api = {
  auth: {
    login: (credentials) => request('/api/auth/login', { method: 'POST', body: credentials }),
    register: (userData) => request('/api/auth/register', { method: 'POST', body: userData }),
  },
  vehicles: {
    getAll: () => request('/api/vehicles', { method: 'GET' }),
    create: (vehicleData) => request('/api/vehicles', { method: 'POST', body: vehicleData }),
    update: (id, vehicleData) => request(`/api/vehicles/${id}`, { method: 'PUT', body: vehicleData }),
    delete: (id) => request(`/api/vehicles/${id}`, { method: 'DELETE' }),
  }
};