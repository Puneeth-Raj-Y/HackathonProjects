import React, { useState, useEffect } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { Box, Zap, Shield, BarChart3, ChevronRight, Globe, Cpu, Terminal, Activity, Lock } from 'lucide-react';

const Particle = ({ i }) => {
  const size = Math.random() * 3 + 1;
  return (
    <motion.div
      className="absolute bg-primary/20 rounded-full blur-[1px]"
      initial={{ 
        x: Math.random() * window.innerWidth, 
        y: Math.random() * window.innerHeight,
        opacity: 0 
      }}
      animate={{
        y: [null, Math.random() * -100 - 50],
        opacity: [0, 0.8, 0],
        scale: [0, 1.5, 0],
      }}
      transition={{
        duration: Math.random() * 10 + 10,
        repeat: Infinity,
        delay: Math.random() * 20,
      }}
      style={{ width: size, height: size }}
    />
  );
};

const FeatureCard = ({ icon: Icon, title, desc, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 30 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.8, delay }}
    whileHover={{ scale: 1.02, rotateY: 5 }}
    className="relative group p-8 glass-card border-white/5 hover:border-primary/30 transition-all overflow-hidden"
  >
    <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:bg-primary/20 transition-all"></div>
    <div className="relative z-10">
      <div className="w-14 h-14 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-2xl flex items-center justify-center mb-6 border border-white/10 group-hover:shadow-neon-blue transition-all">
        <Icon className="text-primary" size={28} />
      </div>
      <h3 className="text-2xl font-black mb-4 tracking-tighter uppercase italic">{title}</h3>
      <p className="text-slate-400 text-sm leading-relaxed font-medium">{desc}</p>
    </div>
  </motion.div>
);

const LandingPage = ({ onGetStarted }) => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const { scrollYProgress } = useScroll();
  const yRange = useTransform(scrollYProgress, [0, 1], [0, -200]);

  useEffect(() => {
    const handleMouseMove = (e) => setMousePos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="min-h-screen bg-[#020205] text-white overflow-hidden selection:bg-primary/30">
      {/* HUD Overlays */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none z-50 border-[1px] border-white/5 m-4 rounded-3xl">
        <div className="absolute top-10 left-10 flex gap-4 opacity-30">
          <Activity size={14} className="animate-pulse text-primary" />
          <span className="text-[10px] font-black uppercase tracking-[0.3em]">System: Active</span>
        </div>
        <div className="absolute bottom-10 right-10 flex gap-4 opacity-30">
          <Terminal size={14} className="text-secondary" />
          <span className="text-[10px] font-black uppercase tracking-[0.3em]">V2.0.4-ForgeMind</span>
        </div>
      </div>

      {/* Interactive Background */}
      <div className="fixed inset-0 pointer-events-none">
        {[...Array(40)].map((_, i) => <Particle key={i} i={i} />)}
        <div 
          className="absolute w-[800px] h-[800px] bg-primary/5 rounded-full blur-[150px] transition-all duration-300 ease-out"
          style={{ left: mousePos.x - 400, top: mousePos.y - 400 }}
        />
      </div>

      {/* Navigation Branding */}
      <nav className="fixed top-0 w-full px-10 py-8 flex justify-between items-center z-[100]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center shadow-neon-blue">
            <Box className="text-white" size={20} />
          </div>
          <span className="text-xl font-black tracking-tighter uppercase italic">ForgeMind AI</span>
        </div>
        <button 
          onClick={onGetStarted}
          className="px-6 py-2 bg-white/5 border border-white/10 rounded-full text-xs font-black uppercase tracking-widest hover:bg-white/10 transition-all"
        >
          Access Portal
        </button>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-40 pb-20 px-10 max-w-7xl mx-auto flex flex-col items-center text-center min-h-screen">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1 }}
          className="relative mb-12"
        >
          <div className="absolute inset-0 bg-primary/20 blur-[100px] rounded-full animate-pulse"></div>
          <h1 className="text-[100px] md:text-[180px] font-black leading-[0.8] tracking-tighter uppercase italic select-none">
            Forge<br/>
            <span className="bg-gradient-to-r from-primary via-secondary to-primary bg-[length:200%_auto] bg-clip-text text-transparent animate-gradient-x">Mind AI</span>
          </h1>
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="text-slate-400 text-lg md:text-2xl max-w-3xl mb-12 font-medium tracking-tight"
        >
          Orchestrating Global Commerce through Hybrid Intelligence. 
          The ultimate multi-item order engine for the next generation of industry.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="flex flex-col md:flex-row gap-6 mb-20"
        >
          <button 
            onClick={onGetStarted}
            className="group relative px-10 py-5 bg-primary text-black font-black rounded-2xl hover:scale-105 transition-all shadow-neon-blue uppercase tracking-tighter overflow-hidden"
          >
            <div className="absolute inset-0 bg-white/20 -translate-x-full group-hover:translate-x-full transition-transform duration-700 ease-in-out"></div>
            <span className="flex items-center gap-2">Initiate Launch <ChevronRight size={20} /></span>
          </button>
          <button className="px-10 py-5 glass-card border-white/10 rounded-2xl font-black uppercase tracking-tighter hover:bg-white/10 transition-all flex items-center gap-2">
            <Lock size={18} className="text-secondary" /> Request Beta Access
          </button>
        </motion.div>

        {/* Floating Dashboard Preview */}
        <motion.div 
          style={{ y: yRange }}
          className="relative w-full max-w-5xl group"
        >
          <div className="absolute -inset-1 bg-gradient-to-r from-primary/50 to-secondary/50 rounded-[32px] blur opacity-25 group-hover:opacity-100 transition duration-1000"></div>
          <div className="relative glass-card p-2 rounded-[32px] border-white/10 overflow-hidden shadow-2xl shadow-primary/10">
             <img 
               src="/futuristic_ai_dashboard_preview_1778090194767.png" 
               alt="ForgeMind Dashboard Preview" 
               className="w-full h-auto rounded-[24px] brightness-90 group-hover:brightness-110 transition-all duration-700"
             />
             {/* HUD Scan Effect */}
             <div className="absolute top-0 left-0 w-full h-[2px] bg-primary shadow-neon-blue animate-scan"></div>
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="relative z-10 max-w-7xl mx-auto px-10 py-32 grid grid-cols-1 md:grid-cols-3 gap-10">
        <FeatureCard 
          icon={Cpu} 
          title="Hybrid NLP" 
          desc="Proprietary engine combining spaCy NER with semantic logic to extract complex multi-item hierarchies."
          delay={0.2}
        />
        <FeatureCard 
          icon={Globe} 
          title="Universal Scale" 
          desc="Native support for 50+ industries from aerospace manufacturing to global medical logistics."
          delay={0.4}
        />
        <FeatureCard 
          icon={Shield} 
          title="Dual Governance" 
          desc="Advanced role separation ensuring immutable tracking for both administrative nodes and customer portals."
          delay={0.6}
        />
      </section>

      {/* Tech Stack Horizontal Scroll */}
      <div className="py-20 border-y border-white/5 bg-white/[0.01]">
        <div className="flex items-center justify-center gap-20 opacity-30 grayscale hover:grayscale-0 transition-all cursor-default">
           {['FAST API', 'REACT VITE', 'SQLITE 3', 'SPACY NLP', 'FRAMER MOTION'].map((tech, i) => (
             <span key={i} className="text-2xl font-black tracking-[0.5em] italic whitespace-nowrap">{tech}</span>
           ))}
        </div>
      </div>

      <footer className="py-20 text-center relative">
        <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent pointer-events-none"></div>
        <p className="text-slate-600 text-xs font-black uppercase tracking-[0.6em] italic mb-4">ForgeMind Intelligence Platform</p>
        <div className="flex justify-center gap-8 text-slate-500 font-bold text-[10px] uppercase tracking-widest">
           <a href="#" className="hover:text-primary transition-colors">Privacy Protocal</a>
           <a href="#" className="hover:text-primary transition-colors">Security Manifest</a>
           <a href="#" className="hover:text-primary transition-colors">System Status</a>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
