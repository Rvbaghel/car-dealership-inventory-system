import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * Reusable route guard component to secure views based on authentication status and user roles.
 */
const ProtectedRoute = ({ children, requireAdmin = false }) => {
  const { user, loading, isAdmin } = useAuth();

  // ⏳ Hold structural execution while context determines session persistence status
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[--color-brand-bg]">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-[--color-brand-border] border-t-[--color-brand-primary]"></div>
      </div>
    );
  }

  // 🔒 Condition A: User is completely anonymous -> Redirect directly to login view
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // 🔒 Condition B: View requires elevated clearance, but user profile lacks ADMIN privileges -> Redirect
  if (requireAdmin && !isAdmin) {
    return <Navigate to="/" replace />;
  }

  // 🔓 Access Granted: Render shielded children dashboard modules
  return children;
};

export default ProtectedRoute;