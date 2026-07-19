import React from 'react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-[--color-brand-bg] p-6">
      <div className="mx-auto max-w-7xl rounded-2xl border border-[--color-brand-border] bg-[--color-brand-card] p-8 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-100 pb-5">
          <div>
            <h1 className="text-2xl font-bold text-[--color-brand-text]"> Dealership Panel</h1>
            <p className="text-sm text-slate-500">Welcome back, {user?.username || 'User'}</p>
          </div>
          <button 
            onClick={logout}
            className="rounded-xl bg-red-50 px-4 py-2 text-sm font-semibold text-red-600 transition-colors hover:bg-red-100 cursor-pointer"
          >
            Sign Out
          </button>
        </div>
        <div className="mt-8 text-center text-slate-400 py-12">
          Vehicle grid loading here soon...
        </div>
      </div>
    </div>
  );
};

export default Dashboard;