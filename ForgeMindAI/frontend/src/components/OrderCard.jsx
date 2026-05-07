import React from 'react';
import { motion } from 'framer-motion';
import { Clock3, Package, ShieldCheck } from 'lucide-react';

const statusStyles = {
  Pending: 'border-neon-amber/40 bg-neon-amber/10 text-neon-amber',
  Processing: 'border-neon-cyan/40 bg-neon-cyan/10 text-neon-cyan',
  Completed: 'border-neon-lime/40 bg-neon-lime/10 text-neon-lime',
};

export default function OrderCard({ order, admin = false, onStatusChange, onNoteAdd }) {
  const latestItemCount = order.items?.length || 0;

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-line bg-panel p-5 shadow-glow backdrop-blur-xl"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-slate-400">Order</p>
          <h3 className="mt-1 text-2xl font-bold text-white">#{order.id}</h3>
        </div>
        <span className={`rounded-full border px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.25em] ${statusStyles[order.status] || statusStyles.Pending}`}>
          {order.status}
        </span>
      </div>

      <div className="mt-5 space-y-3">
        {order.items?.map((item) => (
          <div key={item.id} className="flex items-center justify-between rounded-xl border border-white/5 bg-white/5 px-3 py-2">
            <div className="flex items-center gap-3">
              <Package size={16} className="text-neon-cyan" />
              <div>
                <p className="font-medium text-slate-100">{item.product_name}</p>
                <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{item.category} • {item.specification}</p>
              </div>
            </div>
            <div className="text-right text-sm font-semibold text-white">x{item.quantity}</div>
          </div>
        ))}
      </div>

      <div className="mt-5 flex items-center gap-2 text-sm text-slate-300">
        <Clock3 size={15} className="text-neon-cyan" />
        Deadline: {order.deadline || 'TBD'}
      </div>

      <div className="mt-4 rounded-xl border border-white/5 bg-black/20 p-3 text-sm text-slate-400">
        {latestItemCount} item{latestItemCount === 1 ? '' : 's'} linked to this order.
      </div>

      {admin && (
        <div className="mt-4 space-y-3 border-t border-white/5 pt-4">
          <select
            value={order.status}
            onChange={(event) => onStatusChange?.(order.id, event.target.value)}
            className="w-full rounded-xl border border-white/10 bg-[#070d1c] px-3 py-2 text-sm text-white outline-none"
          >
            <option value="Pending">Pending</option>
            <option value="Processing">Processing</option>
            <option value="Completed">Completed</option>
          </select>
          <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-[#070d1c] px-3 py-2">
            <ShieldCheck size={16} className="text-neon-lime" />
            <input
              placeholder="Add quality note and press Enter"
              className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
              onKeyDown={(event) => {
                if (event.key === 'Enter' && event.currentTarget.value.trim()) {
                  onNoteAdd?.(order.id, event.currentTarget.value.trim());
                  event.currentTarget.value = '';
                }
              }}
            />
          </div>
        </div>
      )}
    </motion.article>
  );
}
