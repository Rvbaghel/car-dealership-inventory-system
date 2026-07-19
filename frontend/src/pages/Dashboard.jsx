import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import VehicleCard from '../components/VehicleCard';
import VehicleModal from '../components/VehicleModal';
import CartDrawer from '../components/CartDrawer';
import { PlusCircle, LogOut, Car, ShieldAlert, Layers, BarChart3, Loader2, ShoppingCart } from 'lucide-react';

const Dashboard = () => {
  const { user, logout, isAdmin } = useAuth();
  
  // App States
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Cart & Drawer States
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  // Administrative Form States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState(null);

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

  // 🛒 Cart Logic 1: Add item to selection list
  const handleAddToCart = (vehicle) => {
    const existing = cart.find(item => item.id === vehicle.id);
    const dynamicQtyInCart = existing ? existing.cartQuantity : 0;

    // 🛑 Check if user tries to select more than available inventory stock limits
    if (dynamicQtyInCart >= vehicle.quantity) {
      alert(`⚠️ Cannot add more units! Only ${vehicle.quantity} items available in stock.`);
      return;
    }

    if (existing) {
      setCart(cart.map(item => item.id === vehicle.id ? { ...item, cartQuantity: item.cartQuantity + 1 } : item));
    } else {
      setCart([...cart, { ...vehicle, cartQuantity: 1 }]);
    }
    setIsCartOpen(true); // Pop cart layout slide open instantly
  };

  // 🛒 Cart Logic 2: Increment/Decrement and stock validation checks
  const handleUpdateCartQty = (id, newQty) => {
    if (newQty <= 0) {
      handleRemoveCartItem(id);
      return;
    }

    const item = cart.find(i => i.id === id);
    const liveVehicleRecord = vehicles.find(v => v.id === id);

    if (item && liveVehicleRecord && newQty > liveVehicleRecord.quantity) {
      alert(`🛑 Restricted request! Only ${liveVehicleRecord.quantity} units are available.`);
      return;
    }

    setCart(cart.map(i => i.id === id ? { ...i, cartQuantity: newQty } : i));
  };

  // 🛒 Cart Logic 3: Delete order item out of selection list
  const handleRemoveCartItem = (id) => {
    setCart(cart.filter(item => item.id !== id));
  };

  // 🛒 Cart Logic 4: Final Purchase confirmation & DB stock adjustments
  // 🛒 Force dynamic POST execution mapping directly inside Dashboard.jsx
  const handleCheckoutPurchase = async () => {
    if (!window.confirm('💳 Confirm Purchase? This will instantly place your order and secure your cars!')) {
      return;
    }

    try {
      // Execute the purchase sequentially across the custom purchase endpoint
      for (const cartItem of cart) {
        // 🟢 Direct call to your backend purchase module to guarantee a POST request
        await api.vehicles.purchase(cartItem.id, cartItem.cartQuantity);
      }

      // 🏆 Success actions! Clear cart array, slide close drawer layout, refresh inventory view
      alert('🎉 Success! Your purchase order went through. The fleet database quantity has been updated.');
      setCart([]); 
      setIsCartOpen(false);
      
      // Force inventory state hydration layout
      fetchInventory(); 
    } catch (err) {
      alert(err.message || 'Transaction could not be verified by server protocols.');
    }
  };

  // ➕/✏️ Admin Handlers
  const handleSaveVehicle = async (formData) => {
    try {
      if (selectedVehicle) {
        await api.vehicles.update(selectedVehicle.id, formData);
      } else {
        await api.vehicles.create(formData);
      }
      setIsModalOpen(false);
      setSelectedVehicle(null);
      fetchInventory();
    } catch (err) {
      alert(err.message || 'Operation failed.');
    }
  };

  const handleDeleteVehicle = async (id) => {
    if (window.confirm('Are you absolute sure you want to remove this vehicle entry?')) {
      try {
        await api.vehicles.delete(id);
        fetchInventory();
      } catch (err) {
        alert('Deletion restricted.');
      }
    }
  };

  const totalStock = vehicles.reduce((sum, v) => sum + (Number(v.quantity) || 0), 0);
  const totalValue = vehicles.reduce((sum, v) => sum + ((Number(v.price) || 0) * (Number(v.quantity) || 0)), 0);
  const uniqueMakes = new Set(vehicles.map(v => v.make)).size;

  return (
    <div className="min-h-screen bg-slate-50/50 p-4 md:p-8">
      <div className="mx-auto max-w-7xl space-y-8">
        
        {/* Top Header */}
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
            {!isAdmin && (
              <button
                onClick={() => setIsCartOpen(true)}
                className="relative flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50 cursor-pointer"
              >
                <ShoppingCart className="h-4 w-4 text-blue-700" />
                <span>View Cart</span>
                {cart.length > 0 && (
                  <span className="absolute -top-1.5 -right-1.5 h-5 w-5 rounded-full bg-red-500 text-[10px] font-bold text-white flex items-center justify-center animate-bounce shadow-sm">
                    {cart.reduce((sum, i) => sum + i.cartQuantity, 0)}
                  </span>
                )}
              </button>
            )}
            {isAdmin && (
              <button
                onClick={() => { setSelectedVehicle(null); setIsModalOpen(true); }}
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

        {/* Analytics Infrastructure */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="rounded-xl bg-blue-50 p-3 text-blue-600"><Car className="h-6 w-6" /></div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Stock Available</p>
              <p className="text-2xl font-black text-slate-900">{totalStock} Units</p>
            </div>
          </div>
          <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="rounded-xl bg-green-50 p-3 text-green-600"><BarChart3 className="h-6 w-6" /></div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Inventory Value</p>
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

        {/* Main Grid Card Engine */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3 text-slate-400">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            <p className="text-sm font-semibold">Synchronizing matrix...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {vehicles.map((vehicle) => (
              <VehicleCard
                key={vehicle.id}
                vehicle={vehicle}
                isAdmin={isAdmin}
                onEdit={(v) => { setSelectedVehicle(v); setIsModalOpen(true); }}
                onDelete={handleDeleteVehicle}
                onAddToCart={handleAddToCart}
              />
            ))}
          </div>
        )}

        {/* Modals and Side Drawers */}
        <VehicleModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSave={handleSaveVehicle} vehicle={selectedVehicle} />
        
        <CartDrawer 
          isOpen={isCartOpen} 
          onClose={() => setIsCartOpen(false)} 
          cartItems={cart}
          onUpdateQty={handleUpdateCartQty}
          onRemoveItem={handleRemoveCartItem}
          onCheckout={handleCheckoutPurchase}
        />

      </div>
    </div>
  );
};

export default Dashboard;