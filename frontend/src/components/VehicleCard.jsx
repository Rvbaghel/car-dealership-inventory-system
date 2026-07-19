import React from 'react';
import { Car, Calendar, DollarSign, Settings, Trash2 } from 'lucide-react';

const VehicleCard = ({ vehicle, onEdit, onDelete, isAdmin }) => {
  return (
    <div className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
      {/* Visual Placeholder Header */}
      <div className="relative mb-4 flex h-40 w-full items-center justify-center rounded-xl bg-slate-50 text-slate-400 group-hover:bg-blue-50/50 group-hover:text-blue-500 transition-colors">
        <Car className="h-12 w-12" />
        <span className="absolute top-3 right-3 rounded-full bg-blue-100 px-2.5 py-1 text-xs font-semibold text-blue-700">
          {vehicle.condition || 'New'}
        </span>
      </div>

      {/* Info Details */}
      <div className="space-y-3">
        <div>
          <h3 className="text-lg font-bold text-slate-900 leading-tight">
            {vehicle.make} {vehicle.model}
          </h3>
          <p className="text-sm text-slate-500 font-medium">{vehicle.type || 'Sedan'}</p>
        </div>

        <div className="grid grid-cols-2 gap-2 border-t border-b border-slate-100 py-3 text-xs text-slate-600 font-medium">
          <div className="flex items-center gap-1.5">
            <Calendar className="h-3.5 w-3.5 text-slate-400" />
            <span>Year: {vehicle.year}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Settings className="h-3.5 w-3.5 text-slate-400" />
            <span>{vehicle.transmission || 'Automatic'}</span>
          </div>
        </div>

        {/* Price & Administrative Callouts */}
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-baseline text-xl font-black text-blue-700">
            <DollarSign className="h-4 w-4 self-center -mr-0.5 text-blue-600" />
            <span>{Number(vehicle.price).toLocaleString()}</span>
          </div>

          {/* Render operational buttons exclusively if user profile is signed in as ADMIN */}
          {isAdmin && (
            <div className="flex gap-1">
              <button
                onClick={() => onEdit(vehicle)}
                className="rounded-lg p-2 text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-800 cursor-pointer"
                title="Edit Details"
              >
                <Settings className="h-4 w-4" />
              </button>
              <button
                onClick={() => onDelete(vehicle.id)}
                className="rounded-lg p-2 text-red-500 transition-colors hover:bg-red-50 hover:text-red-700 cursor-pointer"
                title="Remove Vehicle"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VehicleCard;