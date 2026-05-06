import React from 'react';
import { Users, ClipboardList, TrendingUp, AlertTriangle, Search, Filter } from 'lucide-react';
import OrderCard from './OrderCard';

const AdminDashboard = ({ orders, stats, loading, search, setSearch, onUpdateStatus }) => {
  const filteredOrders = orders.filter(o => 
    o.id.toString().includes(search) ||
    o.items.some(i => i.product_name.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-8">
      {/* Admin Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Orders', value: stats.total_orders, icon: ClipboardList, color: 'text-primary' },
          { label: 'Total Customers', value: stats.total_users, icon: Users, color: 'text-secondary' },
          { label: 'Pending Review', value: stats.pending, icon: AlertTriangle, color: 'text-warning' },
          { label: 'System Efficiency', value: '94%', icon: TrendingUp, color: 'text-success' },
        ].map((stat, i) => (
          <div key={i} className="glass-card p-6 border-l-4 border-l-primary/30">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-[10px] uppercase font-bold text-slate-500 tracking-widest">{stat.label}</p>
                <h3 className="text-3xl font-black mt-1">{stat.value}</h3>
              </div>
              <stat.icon className={stat.color} size={24} />
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
          <input 
            placeholder="Global order search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="glass-input w-full pl-10"
          />
        </div>
        <div className="flex gap-2">
           <button className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-xs font-bold text-slate-400">
             <Filter size={14} /> All Industries
           </button>
           <button className="flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary/20 rounded-lg text-xs font-bold text-primary">
             Export Analytics
           </button>
        </div>
      </div>

      {/* Admin Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {loading ? (
          [1,2,3,4].map(i => <div key={i} className="glass-card h-48 animate-pulse"></div>)
        ) : (
          filteredOrders.map(order => (
            <OrderCard 
              key={order.id} 
              order={order} 
              isAdmin={true} 
              onUpdateStatus={onUpdateStatus} 
            />
          ))
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
