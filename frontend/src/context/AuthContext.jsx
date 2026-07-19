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

  // 🔑 Updated Global Login Handler inside AuthContext.jsx to match standard JSON payloads
  const login = async (email, password) => {
    setLoading(true);
    try {
      // 🟢 Update: Switch from form-urlencoded data to a clean backend-ready JSON call
      const data = await fetch(`https://car-dealership-inventory-system-rouge.vercel.app/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, password: password }) // Match backend parameters exactly
      }).then(res => {
        if (!res.ok) throw new Error('Invalid email or password');
        return res.json();
      });

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