'use client';

import { useState, useEffect } from 'react';
import { Send } from 'lucide-react';
import axios from 'axios';
import Image from 'next/image';
import Link from 'next/link';
// import ReactMarkdown from 'react-markdown';
import { UserCircle, MessageSquarePlus } from 'lucide-react';
// import { HTMLAttributes } from "react";


const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5001';


const suggestions = [
  "What is the plan for today?",
  "What should I revise next?",
  "How much have I done?",
  "Clear my progress."
];

const models = [
  { label: "LLaMA 3 (8B) [Default]", value: "llama3-8b-8192" },
  { label: "LLaMA 3 (70B)", value: "llama3-70b-8192" },
];


export default function Home() {
  const [chat, setChat] = useState<{ sender: "user" | "bot"; text: string }[]>([]);
  const [input, setInput] = useState('');
  const [selectedModel, setSelectedModel] = useState(models[0].value);


  const handleNewChat = async () => {
    const confirmed = confirm("Start a new chat? This will clear the current session.");
    if (!confirmed) return;

    setChat([]);
    setInput('');
    try {
      await axios.post(`${baseUrl}/api/clear`);
      console.log("✅ Memory cleared");
    } catch (err) {
      console.error("❌ Failed to clear memory:", err);
    }
  };


  useEffect(() => {
    const loadMemory = async () => {
      try {
        const res = await axios.get(`${baseUrl}/api/memory`);
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
  }, []);

  const sendMessage = async (msg?: string) => {
    const message = msg || input.trim();
    if (!message) return;

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
        model: selectedModel
      });
      console.log(res.data);
      const reply = res.data.reply || "❌ No response";
      setChat(prev => [
        ...prev.slice(0, -1),
        { sender: "bot", text: reply }
      ]);
    } catch {
      setChat(prev => [
        ...prev.slice(0, -1),
        { sender: "bot", text: "❌ Server error" }
      ]);
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
          <span className="text-white font-semibold text-lg">D-Bot</span>
        </div>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="bg-zinc-800 text-white p-2 rounded-md border border-zinc-700 text-sm"
        >
          {models.map((m) => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
        <div className="flex items-center gap-5">
          <button onClick={handleNewChat} title="New Chat">
            <MessageSquarePlus className="text-white w-8 h-8 hover:text-blue-400 transition" />
          </button>
          <UserCircle className="text-white w-8 h-8 cursor-pointer" />
        </div>

      </div>
      <main className="max-w-3xl mx-auto flex-1 px-4 pt-15 overflow-y-auto">

        {chat.length === 0 && (
          <div className="flex flex-col items-center justify-center flex-1 text-center gap-4">

            <h1 className="text-3xl font-bold mb-2">Hello there!</h1>
            <p className="text-gray-400 mb-6">How can I help you today?</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(s)}
                  className="bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 p-4 text-left rounded-lg text-sm"
                >
                  {s}
                </button>
              ))}
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
                className={`p-3 rounded-2xl max-w-[75%] min-w-[160px] break-words whitespace-pre-wrap ${message.sender === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-zinc-800 text-white rounded-bl-none"
                  }`}
              >
                {/* <ReactMarkdown
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
                > */}
                  {message.text}
                {/* </ReactMarkdown> */}
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
            className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
