import React from 'react';
import { Grid2X2, Users, Workflow } from 'lucide-react';

import OrderCard from './OrderCard';

const StatCard = ({ label, value, icon: Icon }) => (
  <div className="rounded-2xl border border-line bg-panel p-5 shadow-glow backdrop-blur-xl">
    <div className="flex items-start justify-between gap-4">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">{label}</p>
        <h3 className="mt-2 text-3xl font-bold text-white">{value}</h3>
      </div>
      <Icon className="text-neon-magenta" size={22} />
    </div>
  </div>
);

export default function AdminDashboard({ summary, orders, onStatusChange, onNoteAdd }) {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Total Orders" value={summary?.total_orders || 0} icon={Grid2X2} />
        <StatCard label="Users" value={summary?.total_users || 0} icon={Users} />
        <StatCard label="Processing" value={summary?.processing || 0} icon={Workflow} />
        <StatCard label="Completed" value={summary?.completed || 0} icon={Workflow} />
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        {orders.map((order) => (
          <OrderCard
            key={order.id}
            order={order}
            admin
            onStatusChange={onStatusChange}
            onNoteAdd={onNoteAdd}
          />
        ))}
        {!orders.length && (
          <div className="rounded-3xl border border-dashed border-white/10 bg-white/5 p-10 text-center text-slate-400 xl:col-span-2">
            No orders available for admin review.
          </div>
        )}
      </div>
    </div>
  );
}
