import React from 'react';
import { motion } from 'framer-motion';
import { Package, Clock, ShieldCheck, AlertCircle, ShoppingBag, Layers } from 'lucide-react';

const OrderCard = ({ order, isAdmin = false, onUpdateStatus, onAddQualityLog }) => {
  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'completed': return 'text-success border-success/30 bg-success/10';
      case 'processing': return 'text-warning border-warning/30 bg-warning/10';
      default: return 'text-primary border-primary/30 bg-primary/10';
    }
  };

  const latestLog = order.quality_logs?.[order.quality_logs.length - 1];

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-5 hover:bg-white/10 transition-all group relative overflow-hidden flex flex-col h-full border-white/5"
    >
      <div className="absolute top-0 right-0 w-24 h-24 bg-primary/5 rounded-full -mr-12 -mt-12 blur-2xl group-hover:bg-primary/10 transition-all"></div>
      
      <div className="flex justify-between items-start mb-4 relative z-10">
        <div>
          <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Order ID</span>
          <h4 className="text-xl font-black text-white italic">#{order.id}</h4>
        </div>
        <div className="flex flex-col items-end gap-2">
          <span className={`text-[10px] px-2 py-1 rounded-full border uppercase font-bold tracking-tighter ${getStatusColor(order.status)}`}>
            {order.status}
          </span>
          {isAdmin && (
            <select 
              className="bg-black/50 border border-white/10 rounded px-1 py-0.5 text-[10px] text-slate-400 focus:outline-none"
              onChange={(e) => onUpdateStatus?.(order.id, e.target.value)}
              value={order.status}
            >
              <option value="Pending">Set Pending</option>
              <option value="Processing">Set Processing</option>
              <option value="Completed">Set Completed</option>
            </select>
          )}
        </div>
      </div>

      <div className="flex-1 space-y-4 relative z-10">
        <div className="space-y-2">
          {order.items?.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between bg-white/5 p-2 rounded-lg border border-white/5">
              <div className="flex items-center gap-3">
                <Package className="text-primary/70" size={16} />
                <div>
                  <p className="text-xs font-semibold text-slate-200">{item.product_name}</p>
                  <p className="text-[10px] text-slate-500 uppercase">{item.category} • {item.specification}</p>
                </div>
              </div>
              <span className="text-xs font-black text-primary">×{item.quantity}</span>
            </div>
          ))}
        </div>

        <div className="flex items-center gap-3 px-1">
          <Clock className="text-slate-400" size={16} />
          <div>
            <p className="text-[10px] text-slate-500 uppercase">Deadline</p>
            <p className="text-xs font-medium text-slate-200">{order.deadline}</p>
          </div>
        </div>

        {latestLog ? (
          <div className="mt-2 p-3 bg-success/5 rounded-lg border border-success/10">
            <div className="flex items-center gap-2 mb-1">
              <ShieldCheck className="text-success" size={12} />
              <span className="text-[9px] font-bold text-success uppercase tracking-widest">Quality Update</span>
            </div>
            <p className="text-[11px] text-slate-300 italic">"{latestLog.note}"</p>
          </div>
        ) : (
          <div className="mt-2 p-3 bg-white/5 rounded-lg border border-white/5 flex items-center gap-2">
            <AlertCircle className="text-slate-500" size={12} />
            <span className="text-[9px] text-slate-500 font-bold uppercase italic">No quality reports pending</span>
          </div>
        )}

        {isAdmin && (
          <div className="mt-4 pt-4 border-t border-white/5 flex gap-2 relative z-20">
            <input 
              type="text" 
              placeholder="Add quality log..."
              className="glass-input flex-1 text-[10px] py-1 px-2"
              id={`quality-input-${order.id}`}
              onKeyDown={(e) => {
                if(e.key === 'Enter' && e.target.value) {
                  onAddQualityLog?.(order.id, e.target.value);
                  e.target.value = '';
                }
              }}
            />
            <button 
              className="px-2 py-1 bg-success/20 text-success text-[10px] font-bold rounded border border-success/30 hover:bg-success/30 transition-all uppercase tracking-widest"
              onClick={() => {
                const input = document.getElementById(`quality-input-${order.id}`);
                if (input && input.value) {
                  onAddQualityLog?.(order.id, input.value);
                  input.value = '';
                }
              }}
            >
              Log
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default OrderCard;
