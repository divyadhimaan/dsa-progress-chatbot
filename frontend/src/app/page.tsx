'use client';

import { useRouter } from 'next/navigation';

export default function StartPage() {
  const router = useRouter();

  const handleStart = () => {
    router.push('/chat');
  };

  return (
    <main className="min-h-screen flex flex-col justify-center items-center bg-black from-slate-900 to-slate-700 text-white text-center p-6">
      <h1 className="text-4xl font-bold mb-4">Welcome to D-Bot</h1>
      <p className="text-lg max-w-xl mb-8">
      Your smart DSA prep buddy — track, revise, and stay ready to crack the toughest interviews.
      </p>
      <button
        onClick={handleStart}
        className="bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 p-4 text-left rounded-lg text-sm"
      >
        Start Chatting 
      </button>
    </main>
  );
}
