import React from 'react';
import { Car, Tag, Boxes, DollarSign, Edit, Trash2, ShoppingCart } from 'lucide-react';

const VehicleCard = ({ vehicle, onEdit, onDelete, isAdmin, onAddToCart }) => {
  return (
    <div className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
      
      {/* Visual Header */}
      <div className="relative mb-4 flex h-40 w-full items-center justify-center rounded-xl bg-slate-50 text-slate-400 group-hover:bg-blue-50/50 group-hover:text-blue-500 transition-colors">
        <Car className="h-12 w-12" />
        <span className={`absolute top-3 right-3 rounded-full px-2.5 py-1 text-xs font-semibold shadow-sm ${
          vehicle.quantity > 0 
            ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' 
            : 'bg-rose-100 text-rose-800 border border-rose-200'
        }`}>
          {vehicle.quantity > 0 ? `${vehicle.quantity} In Stock` : 'Out of Stock'}
        </span>
      </div>

      {/* Specifications */}
      <div className="space-y-3">
        <div>
          <h3 className="text-lg font-bold text-slate-900 leading-tight">
            {vehicle.make} {vehicle.model}
          </h3>
        </div>

        <div className="grid grid-cols-2 gap-2 border-t border-b border-slate-100 py-3 text-xs text-slate-600 font-medium">
          <div className="flex items-center gap-1.5">
            <Tag className="h-3.5 w-3.5 text-slate-400" />
            <span className="truncate">Class: {vehicle.category}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Boxes className="h-3.5 w-3.5 text-slate-400" />
            <span>Qty: {vehicle.quantity}</span>
          </div>
        </div>

        {/* Dynamic Action Buttons Based on Role */}
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-baseline text-xl font-black text-blue-700">
            <DollarSign className="h-4 w-4 self-center -mr-0.5 text-blue-600" />
            <span>{Number(vehicle.price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
          </div>

          {isAdmin ? (
            <div className="flex gap-1">
              <button
                onClick={() => onEdit(vehicle)}
                className="rounded-lg p-2 text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-800 cursor-pointer"
              >
                <Edit className="h-4 w-4" />
              </button>
              <button
                onClick={() => onDelete(vehicle.id)}
                className="rounded-lg p-2 text-red-500 transition-colors hover:bg-red-50 hover:text-red-700 cursor-pointer"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => onAddToCart(vehicle)}
              disabled={vehicle.quantity <= 0}
              className="flex items-center gap-1.5 rounded-xl bg-blue-700 px-3 py-2 text-xs font-bold text-white transition-all hover:bg-blue-800 disabled:bg-slate-200 disabled:text-slate-400 shadow-sm cursor-pointer"
            >
              <ShoppingCart className="h-3.5 w-3.5" />
              <span>Buy Car</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default VehicleCard;