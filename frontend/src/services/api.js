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
    // 🟢 Add this dedicated search function matching your backend query inputs
    search: (filters) => {
      const params = new URLSearchParams();
      if (filters.make) params.append('make', filters.make);
      if (filters.model) params.append('model', filters.model);
      if (filters.category) params.append('category', filters.category);
      if (filters.min_price) params.append('min_price', filters.min_price);
      if (filters.max_price) params.append('max_price', filters.max_price);

      return handleResponse(fetch(`${BASE_URL}/api/vehicles/search?${params.toString()}`, {
        method: 'GET',
        headers: getHeaders(false)
      }));
    },
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
    purchase: (id, quantityRequested) => handleResponse(fetch(`${BASE_URL}/api/vehicles/${id}/purchase`, {
      method: 'POST',
      headers: getHeaders(true),
      body: JSON.stringify({ quantity: quantityRequested }) 
    }))
  } 
};