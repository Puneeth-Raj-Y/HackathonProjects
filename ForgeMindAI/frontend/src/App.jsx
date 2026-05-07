import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Shield, Sparkles, LayoutDashboard, MessageSquareText, RotateCw } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';

import api from './services/api';
import AdminDashboard from './components/AdminDashboard';
import ChatInterface from './components/ChatInterface';
import CustomerDashboard from './components/CustomerDashboard';
import LandingPage from './pages/LandingPage';

export default function App() {
  const [started, setStarted] = useState(false);
  const [role, setRole] = useState('customer');
  const [view, setView] = useState('dashboard');
  const [summary, setSummary] = useState(null);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [syncError, setSyncError] = useState('');
  const [refreshNonce, setRefreshNonce] = useState(0);

  const loadData = useCallback(async () => {
    setLoading(true);
    setSyncError('');
    try {
      const summaryResponse = await api.get('/api/dashboard/overview', {
        params: { user_id: 1, role },
      });
      const ordersResponse = await api.get('/api/dashboard/orders', {
        params: { user_id: 1, role },
      });

      setSummary(summaryResponse.data);
      setOrders(ordersResponse.data.orders || []);
    } catch (error) {
      const detail = error.response?.data?.detail || error.message || 'Cloud synchronization failed.';
      setSyncError(detail);
      toast.error(detail);
    } finally {
      setLoading(false);
    }
  }, [role]);

  useEffect(() => {
    if (started) {
      loadData();
    }
  }, [started, loadData, refreshNonce]);

  const activeCount = useMemo(() => (summary?.pending || 0) + (summary?.processing || 0), [summary]);

  const handleChatCreated = () => {
    setRefreshNonce((value) => value + 1);
  };

  const updateStatus = async (orderId, status) => {
    try {
      await api.patch(`/api/admin/orders/${orderId}/status`, { status });
      toast.success('Order status updated');
      setRefreshNonce((value) => value + 1);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Status update failed');
    }
  };

  const addNote = async (orderId, note) => {
    try {
      await api.post(`/api/admin/orders/${orderId}/quality`, { note });
      toast.success('Quality note added');
      setRefreshNonce((value) => value + 1);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Note update failed');
    }
  };

  if (!started) {
    return (
      <>
        <Toaster position="bottom-right" />
        <LandingPage onStart={() => setStarted(true)} />
      </>
    );
  }

  return (
    <div className="min-h-screen bg-[#050816] text-white">
      <Toaster position="bottom-right" />
      <div className="absolute inset-0 -z-10 bg-grid-faint bg-[length:48px_48px] opacity-20" />
      <div className="absolute left-0 top-0 -z-10 h-80 w-80 rounded-full bg-neon-cyan/20 blur-3xl" />
      <div className="absolute bottom-0 right-0 -z-10 h-80 w-80 rounded-full bg-neon-magenta/20 blur-3xl" />

      <header className="sticky top-0 z-20 border-b border-white/5 bg-[#050816]/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <button className="flex items-center gap-3" onClick={() => setStarted(false)}>
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-neon-cyan to-neon-magenta text-slate-950 shadow-glow">
              <Sparkles size={18} />
            </div>
            <div className="text-left">
              <p className="text-xs uppercase tracking-[0.35em] text-slate-400">ForgeMind AI</p>
              <h1 className="text-lg font-semibold">Workflow Console</h1>
            </div>
          </button>

          <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 p-1">
            <button
              className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-medium ${view === 'dashboard' ? 'bg-neon-cyan/15 text-neon-cyan' : 'text-slate-400'}`}
              onClick={() => setView('dashboard')}
            >
              <LayoutDashboard size={16} /> Dashboard
            </button>
            <button
              className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-medium ${view === 'chat' ? 'bg-neon-cyan/15 text-neon-cyan' : 'text-slate-400'}`}
              onClick={() => setView('chat')}
            >
              <MessageSquareText size={16} /> Chat
            </button>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setRole((current) => (current === 'customer' ? 'admin' : 'customer'))}
              className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200"
            >
              <Shield size={16} /> {role}
            </button>
            <button
              onClick={() => setRefreshNonce((value) => value + 1)}
              className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-neon-cyan to-neon-magenta px-4 py-2 text-sm font-semibold text-slate-950"
            >
              <RotateCw size={16} className={loading ? 'animate-spin' : ''} /> Refresh
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">
        {syncError ? (
          <div className="mb-6 rounded-2xl border border-neon-red/20 bg-neon-red/10 px-4 py-3 text-sm text-rose-200">
            {syncError}
          </div>
        ) : null}

        <AnimatePresence mode="wait">
          {view === 'chat' ? (
            <motion.div key="chat" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <ChatInterface onOrdersCreated={handleChatCreated} />
            </motion.div>
          ) : (
            <motion.div key="dashboard" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-6">
              {role === 'admin' ? (
                <AdminDashboard summary={summary} orders={orders} onStatusChange={updateStatus} onNoteAdd={addNote} />
              ) : (
                <CustomerDashboard summary={summary} orders={orders} loading={loading} onRefresh={() => setRefreshNonce((value) => value + 1)} />
              )}
              <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
                Total orders: {summary?.total_orders || 0} | Active: {activeCount} | Completed: {summary?.completed || 0}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
