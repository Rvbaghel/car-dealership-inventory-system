const BASE_URL = 'https://car-dealership-inventory-system-rouge.vercel.app';

// Helper function to dynamically append authorization headers
const getHeaders = (isJson = true) => {
  const token = localStorage.getItem('token');
  const headers = {};
  
  if (isJson) {
    headers['Content-Type'] = 'application/json';
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`; // 🟢 Inject the security token here
  }
  
  return headers;
};

const handleResponse = async (requestPromise) => {
  const res = await requestPromise;
  if (!res.ok) {
    if (res.status === 401) {
      localStorage.clear(); // Clear bad/expired sessions
    }
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Network response error');
  }
  return res.json();
};

export const api = {
  auth: {
    register: (data) => handleResponse(fetch(`${BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })),
  },
  vehicles: {
    getAll: () => handleResponse(fetch(`${BASE_URL}/api/vehicles`, {
      headers: getHeaders(false) 
    })),
    create: (data) => handleResponse(fetch(`${BASE_URL}/api/vehicles`, {
      method: 'POST',
      headers: getHeaders(true),
      body: JSON.stringify(data)
    })),
    update: (id, data) => handleResponse(fetch(`${BASE_URL}/api/vehicles/${id}`, {
      method: 'PUT',
      headers: getHeaders(true),
      body: JSON.stringify(data)
    })),
    delete: (id) => handleResponse(fetch(`${BASE_URL}/api/vehicles/${id}`, {
      method: 'DELETE',
      headers: getHeaders(false)
    })),
    // 🟢 Fix: Update to pass raw JSON matching the backend's VehiclePurchaseRequest model
    purchase: (id, quantityRequested) => handleResponse(fetch(`${BASE_URL}/api/vehicles/${id}/purchase`, {
      method: 'POST',
      headers: getHeaders(true), // Content-Type: application/json + Bearer token
      body: JSON.stringify({ quantity: quantityRequested }) 
    }))
  } 
};