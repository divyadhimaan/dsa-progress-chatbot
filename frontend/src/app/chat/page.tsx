/* eslint-disable @typescript-eslint/no-explicit-any */

'use client';

import { useState, useEffect } from 'react';
import { useSnackbar } from 'notistack';
import { Send } from 'lucide-react';
import axios from 'axios';
import Image from 'next/image';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import { UserCircle, MessageSquarePlus } from 'lucide-react';
import { HTMLAttributes } from "react";

import { getOrCreateSessionId } from "@/utils/session";

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5001';

const suggestions = [
  "Explain how to solve Two Sum",
  "What are the key patterns for SDE interviews?",
  "Help me understand dynamic programming",
  "Suggest problems to practice today"
];

const models = [
  { label: "LLaMA 3.3 (70B) [Default]", value: "llama-3.3-70b-versatile" },
  { label: "LLaMA 3.1 (8B)", value: "llama-3.1-8b-instant" },
];

const levels = [
  { label: "SDE-1 (Entry Level)", value: "SDE1", description: "Fundamentals & Easy-Medium problems" },
  { label: "SDE-2 (Mid Level)", value: "SDE2", description: "Advanced DSA & Medium-Hard problems" },
  { label: "SDE-3 (Senior Level)", value: "SDE3", description: "Expert algorithms & System Design" },
];


export default function Home() {
  const [chat, setChat] = useState<{ sender: "user" | "bot"; text: string }[]>([]);
  const [input, setInput] = useState('');
  const [selectedModel, setSelectedModel] = useState(models[0].value);
  const [selectedLevel, setSelectedLevel] = useState(levels[0].value);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const { enqueueSnackbar } = useSnackbar();


  const handleNewChat = async () => {
    const confirmed = confirm("Start a new chat? This will clear the current session.");
    if (!confirmed) return;

    setChat([]);
    setInput('');

    const newSessionId = getOrCreateSessionId();
    sessionStorage.setItem("session_id", newSessionId);
    setSessionId(newSessionId);

    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    try {
      await axios.post(`${baseUrl}/api/clear?session_id=${sessionId}`);
      console.log("✅ Memory cleared");
    } catch (err) {
      console.error("❌ Failed to clear memory:", err);
    }
  };


  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedSession = sessionStorage.getItem("session_id");
      if (storedSession) {
        setSessionId(storedSession);
      }

      // Load the selected level from landing page
      const storedLevel = sessionStorage.getItem("sde_level");
      if (storedLevel) {
        setSelectedLevel(storedLevel);
      }
    }
  }, []);


  useEffect(() => {
    if (!sessionId) return;

    const loadMemory = async () => {
      try {
        const res = await axios.get(`${baseUrl}/api/memory`, {
          params: { session_id: sessionId }
        });
        const restoredChat = res.data.map((log: any) => ([
          { sender: "user", text: log.user_input },
          { sender: "bot", text: log.response }
        ])).flat();
        setChat(restoredChat);
      } catch (err) {
        console.error("❌ Failed to load memory:", err);
      }
    };

    loadMemory();
  }, [sessionId]);

  const sendMessage = async (msg?: string) => {
    const message = msg || input.trim();
    if (!message) return;

    //first time chat
    let currentSessionId = sessionId;
    if (!currentSessionId) {
      currentSessionId = crypto.randomUUID();
      sessionStorage.setItem("session_id", currentSessionId);
      setSessionId(currentSessionId);
    }

    console.log("Sending message:", message);

    setChat(prev => [
      ...prev,
      { sender: "user", text: message },
      { sender: "bot", text: "..." }
    ]);
    setInput('');

    try {
      const res = await axios.post(`${baseUrl}/api/message`, {
        message,
        session_id: sessionId,
        model: selectedModel,
        level: selectedLevel
      });


      const data = res.data.reply;

      const reply = data.message || "❌ No response";
      if (data.status === "error" && data.snackbar) {
        enqueueSnackbar(data.snackbar, { variant: "error" });
      }

      setChat(prev => [
        ...prev.slice(0, -1),
        { sender: "bot", text: reply }
      ]);
    } catch (err) {
      console.error("Server error:", err);
      // Replace the "..." placeholder with error text
      setChat(prev => [
        ...prev.slice(0, -1),
        { sender: "bot", text: "❌ Server error" }
      ]);
      enqueueSnackbar("Something went wrong while sending your message.", { variant: "error" });
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col justify-between">
      {/* <main className="max-w-3xl mx-auto flex-1 flex flex-col items-center justify-center px-4"> */}
      <div className="sticky top-0 z-10 w-full px-4 py-3 bg-black/50 backdrop-blur-lg flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Link href="/">
            <Image
              src="/logo-light.png"
              alt="Logo"
              width={32}
              height={32}
              className="object-contain"
            />
          </Link>
          {/* <span className="text-white font-semibold text-lg">bot</span> */}
        </div>
        <div className="flex items-center gap-3">
          <select
            value={selectedLevel}
            onChange={(e) => {
              setSelectedLevel(e.target.value);
              sessionStorage.setItem("sde_level", e.target.value);
            }}
            className="bg-zinc-800 text-white p-2 rounded-md border border-zinc-700 text-sm"
            title="Select your interview level"
          >
            {levels.map((l) => (
              <option key={l.value} value={l.value}>{l.label}</option>
            ))}
          </select>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="bg-zinc-800 text-white p-2 rounded-md border border-zinc-700 text-sm"
          >
            {models.map((m) => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-5">
          <button onClick={handleNewChat} title="New Chat">
            <MessageSquarePlus className="text-white w-8 h-8 hover:text-blue-400 transition" />
          </button>
          <UserCircle className="text-white w-8 h-8 cursor-pointer" />
        </div>

      </div>
      <main className="max-w-3xl mx-auto flex-1 px-4 pt-15 overflow-y-auto">

        {chat.length === 0 && (
          <div className="flex flex-col items-center justify-center flex-1 text-center gap-6 py-8">

            <h1 className="text-4xl font-bold mb-2">Ready to ace your DSA interviews? 🚀</h1>
            <p className="text-gray-400 mb-4">I'm your personal interview coach. Choose your level to get started!</p>

            {/* Level Selection Cards */}
            <div className="w-full mb-8">
              <h2 className="text-xl font-semibold mb-4 text-left">Select Your Interview Level</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {levels.map((level) => (
                  <button
                    key={level.value}
                    onClick={() => {
                      setSelectedLevel(level.value);
                      sessionStorage.setItem("sde_level", level.value);
                    }}
                    className={`p-6 rounded-xl border-2 transition-all text-left ${selectedLevel === level.value
                      ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20'
                      : 'border-zinc-700 bg-zinc-900 hover:border-zinc-600 hover:bg-zinc-800'
                      }`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-bold">{level.label}</h3>
                      {selectedLevel === level.value && (
                        <span className="text-blue-500 text-xl">✓</span>
                      )}
                    </div>
                    <p className="text-sm text-gray-400">{level.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Suggestions */}
            <div className="w-full">
              <h2 className="text-xl font-semibold mb-4 text-left">Quick Start Questions</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(s)}
                    className="bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 p-4 text-left rounded-lg text-sm transition-all hover:border-zinc-600"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          </div>

        )}
        <div className="w-full max-w-3xl flex flex-col gap-4 p-4 bg-black min-h-screen text-white">
          {chat.map((message, idx) => (
            <div
              key={idx}
              className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`p-3 rounded-2xl w-fit min-w-[250px] max-w-[75%] break-words whitespace-pre-wrap bg-blue-600 text-white rounded-br-none ${message.sender === "user"
                  ? "bg-zinc-500 text-white rounded-br-none"
                  : "bg-zinc-800 text-white rounded-bl-none"
                  }`}
              >
                <ReactMarkdown
                  components={{
                    a: (props: HTMLAttributes<HTMLAnchorElement>) => (
                      <a
                        {...props}
                        className="text-blue-400 underline hover:text-blue-300"
                        target="_blank"
                        rel="noopener noreferrer"
                      />
                    ),
                  }}
                >
                  {message.text}
                </ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      </main>

      <div className="sticky bottom-0 bg-black p-4 border-t border-zinc-700">
        <div className="max-w-3xl mx-auto flex items-center gap-2">
          {/* <button className="text-zinc-400">
            <Paperclip size={20} />
          </button> */}
          <input
            type="text"
            className="flex-1 bg-zinc-800 text-white p-3 rounded-lg outline-none"
            placeholder="Send a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button
            onClick={() => sendMessage()}
            className="bg-zinc-500 hover:bg-blue-700 text-white p-3 rounded-lg"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
