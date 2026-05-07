import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Clock3, Package, RefreshCw } from 'lucide-react';

import OrderCard from './OrderCard';

const StatCard = ({ label, value, icon: Icon }) => (
  <div className="rounded-2xl border border-line bg-panel p-5 shadow-glow backdrop-blur-xl">
    <div className="flex items-start justify-between gap-4">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">{label}</p>
        <h3 className="mt-2 text-3xl font-bold text-white">{value}</h3>
      </div>
      <Icon className="text-neon-cyan" size={22} />
    </div>
  </div>
);

export default function CustomerDashboard({ summary, orders, loading, onRefresh }) {
  const activeOrders = (summary?.pending || 0) + (summary?.processing || 0);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="My Orders" value={summary?.total_orders || 0} icon={Package} />
        <StatCard label="Active" value={activeOrders} icon={BarChart3} />
        <StatCard label="Delivered" value={summary?.completed || 0} icon={Clock3} />
        <button
          onClick={onRefresh}
          className="rounded-2xl border border-line bg-panel p-5 text-left shadow-glow backdrop-blur-xl transition hover:border-neon-cyan/40"
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Refresh</p>
              <h3 className="mt-2 text-2xl font-bold text-white">Sync Now</h3>
            </div>
            <RefreshCw size={22} className={loading ? 'animate-spin text-neon-cyan' : 'text-neon-cyan'} />
          </div>
        </button>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {orders.map((order) => (
          <OrderCard key={order.id} order={order} />
        ))}
        {!orders.length && (
          <div className="rounded-3xl border border-dashed border-white/10 bg-white/5 p-10 text-center text-slate-400 lg:col-span-2">
            No orders yet. Ask ForgeMind to create one from chat.
          </div>
        )}
      </div>
    </div>
  );
}
