import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import VehicleCard from '../components/VehicleCard';
import VehicleModal from '../components/VehicleModal';
import { PlusCircle, LogOut, Car, ShieldAlert, Layers, BarChart3, Loader2 } from 'lucide-react';

const Dashboard = () => {
  const { user, logout, isAdmin } = useAuth();
  
  // State Pipeline Matrix
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal State Triggers
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState(null);

  // Fetch Inventory on Mount
  const fetchInventory = async () => {
    setLoading(true);
    try {
      const data = await api.vehicles.getAll();
      setVehicles(data || []);
    } catch (err) {
      setError('Could not establish a clean stream with inventory records.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  // ➕/✏️ Handler: Create or Update Records
  const handleSaveVehicle = async (formData) => {
    try {
      if (selectedVehicle) {
        // Run update query
        await api.vehicles.update(selectedVehicle.id, formData);
      } else {
        // Run instantiation insertion
        await api.vehicles.create(formData);
      }
      setIsModalOpen(false);
      setSelectedVehicle(null);
      fetchInventory(); // Refresh live dashboard grid state
    } catch (err) {
      alert(err.message || 'Operation failed. Verify system authorization profiles.');
    }
  };

  // ❌ Handler: Delete Records securely
  const handleDeleteVehicle = async (id) => {
    if (window.confirm('Are you absolute sure you want to remove this vehicle entry?')) {
      try {
        await api.vehicles.delete(id);
        fetchInventory();
      } catch (err) {
        alert('Deletion restricted. Verify administrative account credentials.');
      }
    }
  };

  const handleOpenEdit = (vehicle) => {
    setSelectedVehicle(vehicle);
    setIsModalOpen(true);
  };

  const handleOpenCreate = () => {
    setSelectedVehicle(null);
    setIsModalOpen(true);
  };

  // 📊 Metric Computations
  const totalStock = vehicles.length;
  const totalValue = vehicles.reduce((sum, v) => sum + (Number(v.price) || 0), 0);
  const uniqueMakes = new Set(vehicles.map(v => v.make)).size;

  return (
    <div className="min-h-screen bg-slate-50/50 p-4 md:p-8">
      <div className="mx-auto max-w-7xl space-y-8">
        
        {/* Top Operational Header */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-black text-slate-900 tracking-tight">Dealership Control Center</h1>
              {isAdmin && (
                <span className="flex items-center gap-1 rounded-md bg-amber-50 px-2 py-0.5 text-xs font-bold text-amber-700 border border-amber-200">
                  <ShieldAlert className="h-3 w-3" /> Admin Mode
                </span>
              )}
            </div>
            <p className="text-sm text-slate-500 font-medium mt-0.5">Logged in via: <span className="text-slate-700 font-semibold">{user?.email}</span></p>
          </div>
          
          <div className="flex gap-2.5">
            {isAdmin && (
              <button
                onClick={handleOpenCreate}
                className="flex items-center gap-2 rounded-xl bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-blue-800 shadow-md cursor-pointer"
              >
                <PlusCircle className="h-4 w-4" />
                <span>Add Vehicle</span>
              </button>
            )}
            <button
              onClick={logout}
              className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-50 hover:text-red-600 cursor-pointer"
            >
              <LogOut className="h-4 w-4" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>

        {/* Analytics Infrastructure Ribbon */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="rounded-xl bg-blue-50 p-3 text-blue-600"><Car className="h-6 w-6" /></div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Stock</p>
              <p className="text-2xl font-black text-slate-900">{totalStock} Units</p>
            </div>
          </div>
          <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="rounded-xl bg-green-50 p-3 text-green-600"><BarChart3 className="h-6 w-6" /></div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Inventory Valuation</p>
              <p className="text-2xl font-black text-slate-900">${totalValue.toLocaleString()}</p>
            </div>
          </div>
          <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="rounded-xl bg-purple-50 p-3 text-purple-600"><Layers className="h-6 w-6" /></div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Active Brands</p>
              <p className="text-2xl font-black text-slate-900">{uniqueMakes} Makes</p>
            </div>
          </div>
        </div>

        {/* Main Grid View Controller */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3 text-slate-400">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            <p className="text-sm font-semibold">Synchronizing with cloud inventory matrix...</p>
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-100 bg-red-50 p-6 text-center text-red-700 font-medium">
            {error}
          </div>
        ) : vehicles.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white py-16 text-center">
            <Car className="mx-auto h-12 w-12 text-slate-300 mb-3" />
            <h3 className="text-lg font-bold text-slate-900">Inventory is completely empty</h3>
            <p className="text-sm text-slate-400 mt-1">There are no vehicles cataloged in the cloud database.</p>
            {isAdmin && (
              <button
                onClick={handleOpenCreate}
                className="mt-4 rounded-xl bg-blue-700 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-blue-800 cursor-pointer"
              >
                Provision First Vehicle
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {vehicles.map((vehicle) => (
              <VehicleCard
                key={vehicle.id}
                vehicle={vehicle}
                isAdmin={isAdmin}
                onEdit={handleOpenEdit}
                onDelete={handleDeleteVehicle}
              />
            ))}
          </div>
        )}

        {/* Global Input Form Dialog Control Overlay */}
        <VehicleModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveVehicle}
          vehicle={selectedVehicle}
        />

      </div>
    </div>
  );
};

export default Dashboard;