import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, CheckCircle, Package } from 'lucide-react';
import api from '../services/api';

const ChatInterface = ({ onAction }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm ForgeMind Intelligence. I can help you manage orders across electronics, furniture, medical supplies, and more. How can I assist you today?",
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };
    
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await api.post('/api/chat/', {
  message: userMsg.text,
  user_id: 1
});
      
      const aiMsg = {
        id: Date.now() + 1,
        text: response.data.reply,
        sender: 'ai',
        intent: response.data.intent,
        extracted: response.data.extracted_data,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, aiMsg]);
      if (onAction && response.data.intent.includes("ORDER")) {
        onAction();
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || "Unknown connection error";
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: `System Error: Connection to intelligence core failed. [${errorMessage}]`,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="w-full max-w-3xl flex flex-col h-[70vh] glass-card shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary via-secondary to-primary animate-gradient-x"></div>
      
      {/* Header */}
      <div className="p-4 border-b border-white/5 bg-black/20 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/30 relative">
           <Bot className="text-primary" size={20} />
           <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-success rounded-full border border-black shadow-[0_0_5px_#00ff88]"></div>
        </div>
        <div>
          <h2 className="text-lg font-black uppercase italic tracking-tighter">ForgeMind Core</h2>
          <p className="text-[10px] text-primary uppercase font-bold tracking-widest flex items-center gap-1">
             <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span> Online
          </p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <AnimatePresence>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className={`flex flex-col max-w-[85%] ${msg.sender === 'user' ? 'ml-auto items-end' : 'mr-auto items-start'}`}
            >
              <div 
                className={`p-4 rounded-2xl ${
                  msg.sender === 'user' 
                    ? 'bg-primary/10 border border-primary/20 text-white rounded-br-none' 
                    : msg.isError
                      ? 'bg-error/10 border border-error/20 text-white rounded-bl-none'
                      : 'glass-card rounded-bl-none text-slate-200 shadow-lg'
                }`}
              >
                {msg.text}
              </div>

              {/* Entity extraction pill */}
              {msg.extracted && msg.extracted.order_id && (
                <div className="mt-2 flex items-center gap-2 px-3 py-1 bg-success/10 border border-success/20 rounded-full text-xs text-success">
                  <CheckCircle size={14} />
                  <span>Action Confirmed</span>
                </div>
              )}
            </motion.div>
          ))}
          {isTyping && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-2 p-4 glass-card max-w-[100px] rounded-2xl rounded-bl-none items-center justify-center h-12">
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="p-4 bg-black/20 border-t border-white/5 relative z-10">
        <div className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type e.g., 'Need 200 titanium flanges'..."
            className="w-full bg-white/5 border border-white/10 text-white px-6 py-4 rounded-xl pr-14 focus:outline-none focus:border-primary/50 focus:bg-white/10 transition-all placeholder:text-slate-500"
          />
          <button 
            type="submit"
            disabled={!input.trim() || isTyping}
            className="absolute right-2 w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30 text-primary hover:bg-primary/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <Send size={18} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
