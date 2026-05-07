import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LayoutDashboard, MessageSquare, Box, User, Shield, LogOut, Settings } from 'lucide-react';
import api from './services/api';
import ChatInterface from './components/ChatInterface';
import CustomerDashboard from './components/CustomerDashboard';
import AdminDashboard from './components/AdminDashboard';
import LandingPage from './pages/LandingPage';
import { Toaster, toast } from 'react-hot-toast';

function App() {
  const [user, setUser] = useState({ id: 1, role: 'customer', email: 'user@example.com' });
  const [orders, setOrders] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showLanding, setShowLanding] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const params = user.role === 'customer' ? { user_id: user.id } : {};
      const statsUrl = '/api/orders/analytics/summary';
      
      const [ordersRes, statsRes] = await Promise.all([
        api.get('/api/orders/', { params }),
        api.get(statsUrl)
      ]);
      
      setOrders(ordersRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error("Fetch Data Error:", error);
      const errorMsg = error.response?.data?.detail || error.message || "Cloud synchronization failed.";
      toast.error(`Sync Failed: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!showLanding) {
      fetchData();
    }
  }, [user, showLanding]);

  const toggleRole = () => {
    const newRole = user.role === 'customer' ? 'admin' : 'customer';
    setUser({ ...user, role: newRole });
    setActiveTab('dashboard');
    toast.success(`Switched to ${newRole.toUpperCase()} Portal`);
  };

  const handleUpdateStatus = async (orderId, newStatus) => {
    try {
      await api.patch(`/api/orders/${orderId}/status`, null, { params: { status: newStatus } });
      toast.success(`Order #${orderId} set to ${newStatus}`);
      fetchData();
    } catch (error) {
      console.error("Update Status Error:", error);
      toast.error("Failed to update status.");
    }
  };

  const handleAddQualityLog = async (orderId, note) => {
    try {
      await api.post(`/api/orders/${orderId}/quality`, null, { params: { note } });
      toast.success(`Quality log added to Order #${orderId}`);
      fetchData();
    } catch (error) {
      console.error("Add Quality Log Error:", error);
      toast.error("Failed to add quality log.");
    }
  };

  if (showLanding) {
    return (
      <>
        <Toaster position="bottom-right" />
        <LandingPage onGetStarted={() => setShowLanding(false)} />
      </>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/30">
      <Toaster position="bottom-right" />

      <nav className="border-b border-white/5 bg-[#020205]/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div 
            className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
            onClick={() => setShowLanding(true)}
          >
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center shadow-neon-blue border border-white/10">
              <Box className="text-white" size={20} />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tighter text-white uppercase italic">ForgeMind AI</h1>
              <p className="text-[9px] font-black text-primary tracking-[0.3em] uppercase -mt-1">Intelligence</p>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex bg-white/5 p-1 rounded-xl border border-white/10">
              <button 
                onClick={() => setActiveTab('dashboard')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-black uppercase tracking-wider transition-all ${activeTab === 'dashboard' ? 'bg-primary/20 text-primary shadow-neon-blue' : 'text-slate-400 hover:text-white'}`}
              >
                <LayoutDashboard size={16} /> Portal
              </button>
              {user.role === 'customer' && (
                <button 
                  onClick={() => setActiveTab('chat')}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-black uppercase tracking-wider transition-all ${activeTab === 'chat' ? 'bg-secondary/20 text-secondary shadow-neon-purple' : 'text-slate-400 hover:text-white'}`}
                >
                  <MessageSquare size={16} /> Order AI
                </button>
              )}
            </div>

            <div className="h-8 w-[1px] bg-white/10 mx-2"></div>

            <div className="flex items-center gap-4">
               <button 
                 onClick={toggleRole}
                 className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-[10px] font-black text-slate-400 hover:bg-white/10 transition-all uppercase tracking-widest"
               >
                 {user.role === 'customer' ? <Shield size={14} /> : <User size={14} />} Switch View
               </button>
               <div className="flex items-center gap-2 bg-black/50 px-3 py-1.5 rounded-full border border-white/10">
                  <div className={`w-2 h-2 rounded-full shadow-neon-blue ${user.role === 'admin' ? 'bg-secondary' : 'bg-primary'}`}></div>
                  <span className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-300">{user.role}</span>
               </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8 relative">
        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' ? (
            <motion.div
              key={user.role}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="w-full"
            >
              {user.role === 'customer' ? (
                <CustomerDashboard 
                  orders={orders} 
                  stats={{ total: orders.length, active: orders.filter(o => o.status !== 'Completed').length, completed: orders.filter(o => o.status === 'Completed').length }} 
                  loading={loading} 
                  search={search} 
                  setSearch={setSearch} 
                  onRefresh={fetchData} 
                />
              ) : (
                <AdminDashboard 
                  orders={orders} 
                  stats={stats} 
                  loading={loading} 
                  search={search} 
                  setSearch={setSearch} 
                  onUpdateStatus={handleUpdateStatus} 
                  onAddQualityLog={handleAddQualityLog}
                />
              )}
            </motion.div>
          ) : (
            <motion.div
              key="chat"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex flex-col items-center justify-center min-h-[70vh]"
            >
              <div className="mb-8 text-center max-w-xl">
                <h2 className="text-4xl font-black mb-2 uppercase italic tracking-tighter">Omni-Channel Intelligent Ordering</h2>
                <p className="text-slate-400 text-sm font-medium">Experience the power of multi-item extraction. Order anything from industrial valves to medical kits in a single breath.</p>
              </div>
              <ChatInterface onAction={fetchData} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
