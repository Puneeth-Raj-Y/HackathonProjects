import React from 'react';
import { Users, ClipboardList, TrendingUp, AlertTriangle, Search, Filter } from 'lucide-react';
import OrderCard from './OrderCard';

const AdminDashboard = ({ orders, stats, loading, search, setSearch, onUpdateStatus, onAddQualityLog }) => {
  const filteredOrders = orders.filter(o => 
    o.id.toString().includes(search) ||
    o.items.some(i => i.product_name.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Orders', value: stats.total_orders || 0, icon: ClipboardList, color: 'text-primary' },
          { label: 'Total Customers', value: stats.total_users || 0, icon: Users, color: 'text-secondary' },
          { label: 'Pending Review', value: stats.pending || 0, icon: AlertTriangle, color: 'text-warning' },
          { label: 'System Efficiency', value: '94%', icon: TrendingUp, color: 'text-success' },
        ].map((stat, i) => (
          <div key={i} className="glass-card p-6 border-l-4 border-l-primary/30 border-y-white/5 border-r-white/5 relative overflow-hidden">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-[10px] uppercase font-bold text-slate-500 tracking-widest">{stat.label}</p>
                <h3 className="text-3xl font-black mt-1 italic">{stat.value}</h3>
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
            className="glass-input w-full pl-10 bg-black/20"
          />
        </div>
        <div className="flex gap-2">
           <button className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-xs font-bold text-slate-400 hover:bg-white/10 transition-colors uppercase tracking-wider">
             <Filter size={14} /> All Industries
           </button>
           <button className="flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary/20 rounded-lg text-xs font-black text-primary hover:bg-primary/20 transition-colors uppercase tracking-wider shadow-neon-blue">
             Export Analytics
           </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {loading ? (
          [1,2,3,4].map(i => <div key={i} className="glass-card h-48 animate-pulse bg-white/5 border-white/5"></div>)
        ) : (
          filteredOrders.map(order => (
            <OrderCard 
              key={order.id} 
              order={order} 
              isAdmin={true} 
              onUpdateStatus={onUpdateStatus} 
              onAddQualityLog={onAddQualityLog}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
