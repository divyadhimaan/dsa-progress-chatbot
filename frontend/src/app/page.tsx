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
    icon: "🌱"
  },
  {
    label: "SDE-2",
    subtitle: "Mid Level",
    value: "SDE2",
    description: "Advanced DSA & Medium-Hard problems",
    details: "For experienced engineers (2-5 years). Master advanced algorithms, optimization techniques, and system design basics.",
    icon: "🚀"
  },
  {
    label: "SDE-3",
    subtitle: "Senior Level",
    value: "SDE3",
    description: "Expert algorithms & System Design",
    details: "For senior engineers and tech leads. Deep dive into distributed systems, scalability, and production-ready solutions.",
    icon: "⭐"
  },
];

export default function StartPage() {
  const router = useRouter();
  const [selectedLevel, setSelectedLevel] = useState<string>("SDE1");

  const handleStart = () => {
    sessionStorage.setItem("sde_level", selectedLevel);
    router.push('/chat');
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
          <Image
            src="/logo-light.png"
            alt="Logo"
            width={32}
            height={32}
            className="object-contain"
          />
          <span className="text-lg font-medium">DSA Coach</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-6 py-20">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <h1 className="text-5xl md:text-6xl font-semibold mb-6 tracking-tight">
            Ready to Ace Your
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Interview?
            </span>
          </h1>
          <p className="text-lg text-white/60 max-w-2xl mx-auto leading-relaxed">
            Your AI-powered interview coach adapts to your level. Get personalized guidance,
            practice problems, and expert tips tailored just for you.
          </p>
        </div>

        {/* Level Selection */}
        <div className="mb-16">
          <h2 className="text-sm font-medium text-white/40 uppercase tracking-wider mb-6 text-center">
            Choose Your Level
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {levels.map((level) => (
              <button
                key={level.value}
                onClick={() => setSelectedLevel(level.value)}
                className={`group relative p-8 rounded-2xl border transition-all duration-200 text-left ${selectedLevel === level.value
                  ? 'border-white/20 bg-white/5'
                  : 'border-white/10 bg-white/[0.02] hover:border-white/15 hover:bg-white/[0.03]'
                  }`}
              >
                {/* Icon */}
                <div className="text-4xl mb-4">{level.icon}</div>

                {/* Title */}
                <div className="mb-4">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="text-xl font-semibold">{level.label}</h3>
                    {selectedLevel === level.value && (
                      <div className="w-5 h-5 rounded-full bg-white flex items-center justify-center">
                        <svg className="w-3 h-3 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <p className="text-sm text-white/40">{level.subtitle}</p>
                </div>

                {/* Description */}
                <p className="text-sm text-white/60 mb-3 leading-relaxed">{level.description}</p>
                <p className="text-xs text-white/40 leading-relaxed">{level.details}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Start Button */}
        <div className="text-center mb-20">
          <button
            onClick={handleStart}
            className="group inline-flex items-center gap-2 px-8 py-4 bg-white text-black rounded-full font-medium transition-all duration-200 hover:gap-3"
          >
            <span>Start Your Prep Journey</span>
            <svg className="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <p className="text-sm text-white/40 mt-4">
            Selected: <span className="text-white/80 font-medium">
              {levels.find(l => l.value === selectedLevel)?.label}
            </span>
          </p>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-12 border-t border-white/10">
          <div className="text-center">
            <div className="text-3xl mb-3">🧠</div>
            <h3 className="font-medium mb-2">AI-Powered Coaching</h3>
            <p className="text-sm text-white/60 leading-relaxed">Personalized guidance from LLaMA 3.3 70B model</p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-3">💡</div>
            <h3 className="font-medium mb-2">Smart Problem Selection</h3>
            <p className="text-sm text-white/60 leading-relaxed">Get problems matched to your skill level</p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-3">📈</div>
            <h3 className="font-medium mb-2">Track Progress</h3>
            <p className="text-sm text-white/60 leading-relaxed">Save conversations and monitor your growth</p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-6 text-center text-sm text-white/40">
          © 2025 / Divya Dhiman
        </div>
      </footer>
    </div>
  );
}
