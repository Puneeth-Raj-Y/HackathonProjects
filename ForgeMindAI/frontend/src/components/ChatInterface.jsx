import React, { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, SendHorizonal, Sparkles, User } from 'lucide-react';
import toast from 'react-hot-toast';

import api from '../services/api';

export default function ChatInterface({ onOrdersCreated }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'ForgeMind online. Send a request like: Need 100 bolts, 50 laptops, 20 medical kits.',
    },
  ]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const canSend = useMemo(() => message.trim().length > 0 && !loading, [message, loading]);

  const sendMessage = async (event) => {
    event.preventDefault();
    if (!message.trim() || loading) return;

    const outgoing = message.trim();
    setMessage('');
    setMessages((current) => [...current, { id: Date.now(), role: 'user', content: outgoing }]);
    setLoading(true);

    try {
      const response = await api.post('/api/chat', { message: outgoing, user_id: 1 });
      const data = response.data;

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.reply,
          metadata: data,
        },
      ]);

      if (data.created_orders?.length) {
        onOrdersCreated?.(data.created_orders);
        toast.success(`Created ${data.created_orders.length} order${data.created_orders.length === 1 ? '' : 's'}`);
      }
    } catch (error) {
      const detail = error.response?.data?.detail || error.message || 'Network error';
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: `System Error: Connection to intelligence core failed. [${detail}]`,
          error: true,
        },
      ]);
      toast.error('Chat request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full min-h-[72vh] flex-col rounded-3xl border border-line bg-panel shadow-glow backdrop-blur-xl">
      <div className="flex items-center justify-between border-b border-white/5 px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-2xl bg-neon-cyan/10 text-neon-cyan">
            <Bot size={20} />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-slate-400">Intelligence Core</p>
            <h2 className="text-lg font-semibold text-white">Conversational Ordering</h2>
          </div>
        </div>
        <Sparkles className="text-neon-cyan" size={20} />
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto px-5 py-5">
        <AnimatePresence initial={false}>
          {messages.map((entry) => (
            <motion.div
              key={entry.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className={`flex ${entry.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-6 ${entry.role === 'user' ? 'bg-neon-cyan/15 text-white' : entry.error ? 'bg-neon-red/10 text-rose-200' : 'bg-white/5 text-slate-100'} border border-white/5`}>
                <div className="mb-2 flex items-center gap-2 text-[10px] uppercase tracking-[0.3em] text-slate-400">
                  {entry.role === 'user' ? <User size={12} /> : <Bot size={12} />}
                  {entry.role === 'user' ? 'You' : 'ForgeMind'}
                </div>
                {entry.content}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <form onSubmit={sendMessage} className="border-t border-white/5 p-4">
        <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-[#071122] px-4 py-3">
          <input
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Try: Need 100 bolts, 50 laptops, 20 medical kits"
            className="flex-1 bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
          />
          <button
            type="submit"
            disabled={!canSend}
            className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-neon-cyan to-neon-magenta px-4 py-2 text-sm font-semibold text-slate-950 transition disabled:cursor-not-allowed disabled:opacity-50"
          >
            <SendHorizonal size={16} />
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
