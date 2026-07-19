import React from 'react';
import { X, Trash2, ShoppingBag, Plus, Minus, CreditCard } from 'lucide-react';

const CartDrawer = ({ isOpen, onClose, cartItems, onUpdateQty, onRemoveItem, onCheckout }) => {
  if (!isOpen) return null;

  const totalCost = cartItems.reduce((sum, item) => sum + item.price * item.cartQuantity, 0);

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-xs animate-fade-in">
      <div className="h-full w-full max-w-md bg-white p-6 shadow-2xl flex flex-col animate-slide-left">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
          <div className="flex items-center gap-2">
            <ShoppingBag className="h-5 w-5 text-blue-700" />
            <h2 className="text-lg font-bold text-slate-900">Your Checkout Cart</h2>
          </div>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 cursor-pointer">
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Item List Container */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-1">
          {cartItems.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-slate-400 space-y-2">
              <ShoppingBag className="h-10 w-10 text-slate-300 animate-pulse" />
              <p className="text-sm font-semibold">Your cart is completely empty</p>
            </div>
          ) : (
            cartItems.map((item) => (
              <div key={item.id} className="flex items-center justify-between p-3 border border-slate-100 rounded-xl bg-slate-50/50">
                <div className="flex-1 min-w-0 pr-3">
                  <h4 className="font-bold text-sm text-slate-900 truncate">{item.make} {item.model}</h4>
                  <p className="text-xs font-semibold text-blue-600">${Number(item.price).toLocaleString()}</p>
                </div>

                {/* Counter controls */}
                <div className="flex items-center gap-2 mr-3 bg-white border border-slate-200 rounded-lg p-1">
                  <button onClick={() => onUpdateQty(item.id, item.cartQuantity - 1)} className="p-1 hover:bg-slate-50 rounded text-slate-500 cursor-pointer">
                    <Minus className="h-3 w-3" />
                  </button>
                  <span className="text-xs font-bold px-1 w-4 text-center">{item.cartQuantity}</span>
                  <button onClick={() => onUpdateQty(item.id, item.cartQuantity + 1)} className="p-1 hover:bg-slate-50 rounded text-slate-500 cursor-pointer">
                    <Plus className="h-3 w-3" />
                  </button>
                </div>

                <button onClick={() => onRemoveItem(item.id)} className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg cursor-pointer">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Footer Billing Actions */}
        {cartItems.length > 0 && (
          <div className="border-t border-slate-100 pt-4 mt-4 space-y-4">
            <div className="flex items-center justify-between text-slate-900">
              <span className="text-sm font-medium text-slate-500">Order Summary:</span>
              <span className="text-xl font-black text-blue-700">${totalCost.toLocaleString()}</span>
            </div>
            <button 
              onClick={onCheckout}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-sm font-bold text-white transition-all hover:bg-emerald-700 shadow-md cursor-pointer"
            >
              <CreditCard className="h-4 w-4" />
              <span>Confirm Purchase</span>
            </button>
          </div>
        )}

      </div>
    </div>
  );
};

export default CartDrawer;