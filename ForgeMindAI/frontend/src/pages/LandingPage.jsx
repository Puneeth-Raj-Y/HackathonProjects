import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Bot, Sparkles, Workflow } from 'lucide-react';

export default function LandingPage({ onStart }) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#050816] text-white">
      <div className="absolute inset-0 bg-grid-faint bg-[length:48px_48px] opacity-20" />
      <div className="absolute left-[-10%] top-[-10%] h-96 w-96 rounded-full bg-neon-cyan/20 blur-3xl" />
      <div className="absolute bottom-[-10%] right-[-10%] h-[28rem] w-[28rem] rounded-full bg-neon-magenta/20 blur-3xl" />

      <div className="relative mx-auto flex min-h-screen max-w-7xl items-center px-6 py-16">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-neon-cyan/30 bg-neon-cyan/10 px-4 py-2 text-xs uppercase tracking-[0.35em] text-neon-cyan">
              <Sparkles size={14} /> ForgeMind AI
            </div>
            <div className="space-y-4">
              <h1 className="max-w-2xl text-5xl font-bold leading-tight md:text-7xl" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Enterprise workflow intelligence built for live operations.
              </h1>
              <p className="max-w-xl text-lg leading-8 text-slate-300">
                Conversational ordering, real-time dashboard synchronization, and role-based operations in one production-ready platform.
              </p>
            </div>
            <div className="flex flex-wrap gap-4">
              <button
                onClick={onStart}
                className="inline-flex items-center gap-3 rounded-2xl bg-gradient-to-r from-neon-cyan to-neon-magenta px-6 py-4 text-sm font-bold uppercase tracking-[0.25em] text-slate-950 transition hover:scale-[1.02]"
              >
                Launch Console <ArrowRight size={16} />
              </button>
              <div className="inline-flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-6 py-4 text-sm text-slate-200">
                <Bot size={16} className="text-neon-cyan" />
                NLP order orchestration
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            className="rounded-[2rem] border border-line bg-panel p-6 shadow-glow backdrop-blur-xl"
          >
            <div className="space-y-4 rounded-[1.5rem] border border-white/5 bg-black/20 p-6">
              <div className="flex items-center justify-between text-sm text-slate-400">
                <span>Live workflow</span>
                <Workflow className="text-neon-cyan" size={16} />
              </div>
              <div className="space-y-3">
                {['Need 100 bolts', '50 laptops', '20 medical kits'].map((line, index) => (
                  <div key={line} className="rounded-2xl border border-white/5 bg-white/5 px-4 py-3 text-slate-200" style={{ animationDelay: `${index * 120}ms` }}>
                    {line}
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
