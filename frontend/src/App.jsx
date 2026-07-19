import React from 'react';

function App() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6">
      <div className="w-full max-w-md rounded-2xl border border-[--color-brand-border] bg-[--color-brand-card] p-8 shadow-sm transition-all hover:shadow-md">
        <span className="inline-block rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-[--color-brand-secondary] mb-4">
          API Connection Ready
        </span>
        <h1 className="text-3xl font-extrabold tracking-tight text-[--color-brand-text] mb-2">
          Car Dealership
        </h1>
        <p className="text-sm text-slate-500 mb-6">
          Welcome to your cloud inventory management dashboard. Connect the frontend layers seamlessly.
        </p>
        <button className="w-full rounded-xl bg-[--color-brand-primary] py-3 text-sm font-semibold text-white transition-colors hover:bg-blue-900 shadow-sm">
          Get Started
        </button>
      </div>
    </div>
  );
}

export default App;