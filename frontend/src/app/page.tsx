'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import Image from 'next/image';

const levels = [
  {
    label: "SDE-1",
    subtitle: "Entry Level",
    value: "SDE1",
    description: "Fundamentals & Easy-Medium problems",
    details: "Perfect for fresh graduates and early-career engineers. Focus on basic data structures, algorithms, and problem-solving patterns.",
    icon: "🌱",
    accent: "from-emerald-500/20 to-teal-500/10",
    border: "border-emerald-500/50",
    glow: "shadow-emerald-500/20",
  },
  {
    label: "SDE-2",
    subtitle: "Mid Level",
    value: "SDE2",
    description: "Advanced DSA & Medium-Hard problems",
    details: "For experienced engineers (2-5 years). Master advanced algorithms, optimization techniques, and system design basics.",
    icon: "🚀",
    accent: "from-blue-500/20 to-violet-500/10",
    border: "border-blue-500/50",
    glow: "shadow-blue-500/20",
  },
  {
    label: "SDE-3",
    subtitle: "Senior Level",
    value: "SDE3",
    description: "Expert algorithms & System Design",
    details: "For senior engineers and tech leads. Deep dive into distributed systems, scalability, and production-ready solutions.",
    icon: "⭐",
    accent: "from-amber-500/20 to-orange-500/10",
    border: "border-amber-500/50",
    glow: "shadow-amber-500/20",
  },
];

const features = [
  {
    icon: "🧠",
    title: "AI-Powered Coaching",
    desc: "Personalized guidance from a state-of-the-art LLM that adapts to your pace.",
  },
  {
    icon: "💡",
    title: "Smart Problem Selection",
    desc: "Get problems matched to your skill level with targeted explanations.",
  },
  {
    icon: "📈",
    title: "Track Progress",
    desc: "Session memory persists your conversations so you can pick up where you left off.",
  },
];

export default function StartPage() {
  const router = useRouter();
  const [selectedLevel, setSelectedLevel] = useState<string>("SDE1");

  const handleStart = () => {
    sessionStorage.setItem("sde_level", selectedLevel);
    router.push('/chat');
  };

  const selected = levels.find(l => l.value === selectedLevel)!;

  return (
    <div className="min-h-screen bg-[#080808] text-white overflow-x-hidden">
      {/* Ambient glow blobs */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full bg-violet-600/10 blur-3xl" />
        <div className="absolute top-1/2 -right-60 w-[500px] h-[500px] rounded-full bg-blue-600/8 blur-3xl" />
        <div className="absolute bottom-0 left-1/3 w-[400px] h-[400px] rounded-full bg-emerald-600/6 blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative border-b border-white/[0.06]">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
          <Image src="/logo-light.png" alt="Logo" width={30} height={30} className="object-contain" />
          <span className="text-base font-semibold tracking-tight">Interview Coach</span>
        </div>
      </header>

      {/* Hero */}
      <main className="relative max-w-5xl mx-auto px-6 pt-24 pb-16">
        <div className="text-center mb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/[0.03] text-xs text-white/50 mb-8 font-medium tracking-wide">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            AI Interview Coach · Now with RAG-powered search
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight leading-[1.08]">
            Ready to ace your
            <br />
            <span
              className="bg-gradient-to-r from-violet-400 via-blue-400 to-emerald-400 bg-clip-text text-transparent"
              style={{ WebkitBackgroundClip: 'text' }}
            >
              interview?
            </span>
          </h1>
          <p className="text-lg text-white/50 max-w-xl mx-auto leading-relaxed">
            Your AI-powered coach adapts to your level — personalized guidance,
            curated problems, and expert tips tailored just for you.
          </p>
        </div>

        {/* Level Selection */}
        <div className="mb-14">
          <p className="text-xs font-semibold text-white/30 uppercase tracking-widest mb-5 text-center">
            Choose your level
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {levels.map((level) => {
              const isSelected = selectedLevel === level.value;
              return (
                <button
                  key={level.value}
                  onClick={() => setSelectedLevel(level.value)}
                  className={`group relative p-7 rounded-2xl border text-left transition-all duration-200 ${
                    isSelected
                      ? `bg-gradient-to-br ${level.accent} ${level.border} shadow-xl ${level.glow}`
                      : 'border-white/[0.08] bg-white/[0.02] hover:border-white/[0.14] hover:bg-white/[0.04]'
                  }`}
                >
                  {/* Selected ring */}
                  {isSelected && (
                    <div className={`absolute inset-0 rounded-2xl border ${level.border} opacity-60 pointer-events-none`} />
                  )}

                  <div className="text-3xl mb-4">{level.icon}</div>

                  <div className="mb-3">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-bold">{level.label}</h3>
                      {isSelected && (
                        <div className="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0">
                          <svg className="w-3 h-3 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                      )}
                    </div>
                    <p className="text-xs text-white/40 mt-0.5">{level.subtitle}</p>
                  </div>

                  <p className="text-sm text-white/65 mb-2 leading-relaxed font-medium">{level.description}</p>
                  <p className="text-xs text-white/35 leading-relaxed">{level.details}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mb-24">
          <button
            onClick={handleStart}
            className="group relative inline-flex items-center gap-2.5 px-8 py-4 bg-white text-black rounded-full font-semibold text-sm transition-all duration-200 hover:bg-white/90 hover:gap-3.5 hover:shadow-lg hover:shadow-white/10"
          >
            <span>Start with {selected.label}</span>
            <svg
              className="w-4 h-4 transition-transform group-hover:translate-x-0.5"
              fill="none" viewBox="0 0 24 24" stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <p className="text-xs text-white/30 mt-4">
            You can change levels any time inside the chat
          </p>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12 border-t border-white/[0.06]">
          {features.map((f) => (
            <div key={f.title} className="flex flex-col items-center text-center gap-3 p-6 rounded-2xl bg-white/[0.02] border border-white/[0.05]">
              <div className="text-3xl">{f.icon}</div>
              <h3 className="font-semibold text-sm">{f.title}</h3>
              <p className="text-xs text-white/45 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </main>

      <footer className="relative border-t border-white/[0.06]">
        <div className="max-w-7xl mx-auto px-6 py-5 text-center text-xs text-white/25">
          © 2025 · Divya Dhiman
        </div>
      </footer>
    </div>
  );
}
