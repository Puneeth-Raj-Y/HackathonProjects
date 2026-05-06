import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { OrderService } from '../services/api';

const ChatInterface = ({ onAction }) => {
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Welcome to ForgeMind AI. I'm your professional manufacturing assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setIsLoading(true);

    try {
      const response = await OrderService.sendMessage(userMsg);
      const { reply, intent } = response.data;
      
      setMessages(prev => [...prev, { role: 'bot', text: reply }]);
      
      // Notify dashboard to refresh if an order was created/updated
      if (['CREATE_ORDER', 'UPDATE_STATUS', 'ADD_QUALITY_LOG'].includes(intent)) {
        onAction?.();
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', text: "Connection error. Please ensure the backend is running." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-card flex flex-col h-[600px] w-full max-w-2xl mx-auto overflow-hidden">
      <div className="p-4 border-b border-white/10 flex items-center gap-3 bg-white/5">
        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary">
          <Bot size={20} />
        </div>
        <div>
          <h3 className="font-bold text-sm">ForgeMind Intelligence</h3>
          <span className="text-[10px] text-success flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></span> Online
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${
              msg.role === 'user' 
                ? 'bg-primary/10 border border-primary/20 text-slate-100' 
                : 'bg-white/5 border border-white/10 text-slate-300'
            }`}>
              {msg.text}
            </div>
          </motion.div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white/5 p-3 rounded-2xl">
              <Loader2 className="animate-spin text-primary" size={18} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="p-4 bg-white/5 border-t border-white/10 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type e.g., 'Need 200 titanium flanges'..."
          className="glass-input flex-1 text-sm py-3"
        />
        <button type="submit" className="btn-primary p-3 rounded-xl flex items-center justify-center">
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
