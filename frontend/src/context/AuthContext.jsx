import React, { createContext, useState, useEffect, useContext } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if a user is already logged in when the app first loads
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        // Clear corrupt storage
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  // 🔑 Global Login Handler
  const login = async (username, password) => {
    setLoading(true);
    try {
      // Form data parsing depending on your backend authentication format
      // If your FastAPI uses standard OAuth2 Password Bearer, it expects form data/URL encoded parameters:
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      // Make the login API call
      const data = await fetch(`${import.meta.env.MODE === 'development' ? 'http://127.0.0.1:8000' : 'https://car-dealership-inventory-system-rouge.vercel.app'}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      }).then(res => {
        if (!res.ok) throw new Error('Invalid credentials');
        return res.json();
      });

      // Save credentials to localStorage
      localStorage.setItem('token', data.access_token);
      
      // Decrypt/Parse details from the token payload, or set base user profile info
      // Since our backend sets the role, we create a clean base object profile
      const userProfile = {
        username: username,
        role: username.toLowerCase() === 'admin' ? 'ADMIN' : 'USER' // Quick fallback fallback parsing
      };

      localStorage.setItem('user', JSON.stringify(userProfile));
      setUser(userProfile);
      return userProfile;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // 🚪 Global Logout Handler
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading, isAdmin: user?.role === 'ADMIN' }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Custom hook for clean usage in components
export const useAuth = () => useContext(AuthContext);