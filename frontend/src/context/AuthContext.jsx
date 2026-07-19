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

  // 🔑 Global Login Handler utilizing the unified API service
  const login = async (email, password) => {
    setLoading(true);
    try {
      // 🟢 FIXED: Switched from a hardcoded manual fetch to our updated api handler
      const data = await api.auth.login({ email, password });

      // Save credentials to localStorage
      localStorage.setItem('token', data.access_token);
      
      const userProfile = {
        email: email,
        role: email.toLowerCase().includes('admin') ? 'ADMIN' : 'USER'
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