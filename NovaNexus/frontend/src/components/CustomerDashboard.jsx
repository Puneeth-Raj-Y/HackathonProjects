import React from 'react';
import { Box, RefreshCw, Activity, ShieldCheck, Search, Clock } from 'lucide-react';
import OrderCard from './OrderCard';

const CustomerDashboard = ({ orders, stats, loading, search, setSearch, onRefresh }) => {
  const filteredOrders = orders.filter(o => 
    o.items.some(item => item.product_name.toLowerCase().includes(search.toLowerCase())) ||
    o.id.toString().includes(search)
  );

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'My Orders', value: stats.total || 0, icon: Box, color: 'text-primary' },
          { label: 'Active', value: stats.active || 0, icon: Activity, color: 'text-warning' },
          { label: 'Delivered', value: stats.completed || 0, icon: ShieldCheck, color: 'text-success' },
          { label: 'Avg Lead Time', value: '4.2 Days', icon: Clock, color: 'text-slate-400' },
        ].map((stat, i) => (
          <div key={i} className="glass-card p-6 flex items-center justify-between border-white/5 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:animate-scan opacity-20"></div>
            <div>
              <p className="text-[10px] uppercase font-bold text-slate-500 tracking-widest">{stat.label}</p>
              <h3 className="text-3xl font-black mt-1 italic">{stat.value}</h3>
            </div>
            <stat.icon className={stat.color} size={32} />
          </div>
        ))}
      </div>

      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
          <input 
            placeholder="Search my orders..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="glass-input w-full pl-10 bg-black/20"
          />
        </div>
        <button onClick={onRefresh} className="flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-primary transition-colors uppercase tracking-wider text-[10px]">
          <RefreshCw size={16} className={loading ? 'animate-spin' : ''} /> Refresh History
        </button>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 opacity-50">
          {[1,2,3].map(i => <div key={i} className="glass-card h-64 animate-pulse bg-white/5 border-white/5"></div>)}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filteredOrders.length > 0 ? (
            filteredOrders.map(order => (
              <OrderCard key={order.id} order={order} />
            ))
          ) : (
            <div className="col-span-full py-20 text-center glass-card border-dashed border-white/10 bg-transparent">
              <p className="text-slate-500 font-medium">No matching orders in your history.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CustomerDashboard;
