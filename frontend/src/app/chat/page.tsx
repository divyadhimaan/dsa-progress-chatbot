/* eslint-disable @typescript-eslint/no-explicit-any */

'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useSnackbar } from 'notistack';
import { Send, MessageSquarePlus, UserCircle, Copy, Check } from 'lucide-react';
import axios from 'axios';
import Image from 'next/image';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import { getOrCreateSessionId } from "@/utils/session";

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5001';

/**
 * Qwen3 emits one leading <think>…</think> block before the answer.
 * Strip only that opening block — leave any <think> used inline untouched.
 */
const stripThinkTags = (text: string): string => {
  const trimmed = text.trimStart();
  if (trimmed.startsWith('<think>')) {
    const closeIdx = trimmed.indexOf('</think>');
    if (closeIdx !== -1) return trimmed.slice(closeIdx + '</think>'.length).trim();
    return '';
  }
  return text;
};

const suggestions = [
  { icon: "🔢", text: "Explain how to solve Two Sum" },
  { icon: "🗂️", text: "What are the key patterns for SDE interviews?" },
  { icon: "💡", text: "Help me understand dynamic programming" },
  { icon: "📋", text: "Suggest problems to practice today" },
];

const levels = [
  { label: "SDE-1", value: "SDE1" },
  { label: "SDE-2", value: "SDE2" },
  { label: "SDE-3", value: "SDE3" },
];

// ── Typing indicator ──────────────────────────────────────────────────────────
function TypingDots() {
  return (
    <div className="flex items-center gap-1 px-1 py-0.5">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-white/40 animate-bounce"
          style={{ animationDelay: `${i * 0.15}s`, animationDuration: '0.9s' }}
        />
      ))}
    </div>
  );
}

// ── Copy button for code blocks ───────────────────────────────────────────────
function CopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={handleCopy}
      title="Copy code"
      className="absolute top-2 right-2 p-1.5 rounded-md bg-white/5 hover:bg-white/10 text-white/40 hover:text-white/80 transition-all"
    >
      {copied ? <Check size={13} /> : <Copy size={13} />}
    </button>
  );
}

// ── Main component ────────────────────────────────────────────────────────────
export default function ChatPage() {
  const [chat, setChat] = useState<{ sender: "user" | "bot"; text: string }[]>([]);
  const [input, setInput] = useState('');
  const [selectedLevel, setSelectedLevel] = useState(levels[0].value);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { enqueueSnackbar } = useSnackbar();

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  // Restore session on mount
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const storedSession = sessionStorage.getItem("session_id");
    if (storedSession) setSessionId(storedSession);
    const storedLevel = sessionStorage.getItem("sde_level");
    if (storedLevel) setSelectedLevel(storedLevel);
  }, []);

  // Load memory when session is known
  useEffect(() => {
    if (!sessionId) return;
    const loadMemory = async () => {
      try {
        const res = await axios.get(`${baseUrl}/api/memory`, { params: { session_id: sessionId } });
        const restoredChat = res.data.flatMap((log: any) => ([
          { sender: "user", text: log.user_input },
          { sender: "bot", text: log.response },
        ]));
        setChat(restoredChat);
      } catch (err) {
        console.error("❌ Failed to load memory:", err);
      }
    };
    loadMemory();
  }, [sessionId]);

  const handleNewChat = async () => {
    const confirmed = confirm("Start a new chat? This will clear the current session.");
    if (!confirmed) return;

    setChat([]);
    setInput('');

    const newSessionId = getOrCreateSessionId();
    sessionStorage.setItem("session_id", newSessionId);
    setSessionId(newSessionId);

    try {
      await axios.post(`${baseUrl}/api/clear?session_id=${sessionId}`);
    } catch (err) {
      console.error("❌ Failed to clear memory:", err);
    }
    inputRef.current?.focus();
  };

  const sendMessage = useCallback(async (msg?: string) => {
    const message = (msg ?? input).trim();
    if (!message || isLoading) return;

    let currentSessionId = sessionId;
    if (!currentSessionId) {
      currentSessionId = crypto.randomUUID();
      sessionStorage.setItem("session_id", currentSessionId);
      setSessionId(currentSessionId);
    }

    setChat(prev => [...prev, { sender: "user", text: message }, { sender: "bot", text: "" }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.post(`${baseUrl}/api/message`, {
        message,
        session_id: currentSessionId,
        level: selectedLevel,
      });

      const data = res.data.reply;
      const reply = data.message || "❌ No response";
      if (data.status === "error" && data.snackbar) {
        enqueueSnackbar(data.snackbar, { variant: "error" });
      }

      setChat(prev => [...prev.slice(0, -1), { sender: "bot", text: reply }]);
    } catch {
      setChat(prev => [...prev.slice(0, -1), { sender: "bot", text: "❌ Server error. Please try again." }]);
      enqueueSnackbar("Something went wrong while sending your message.", { variant: "error" });
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, sessionId, selectedLevel, enqueueSnackbar]);

  return (
    <div className="h-screen bg-[#080808] text-white flex flex-col overflow-hidden">

      {/* ── Header ─────────────────────────────────────────────── */}
      <header className="shrink-0 z-10 border-b border-white/[0.06] bg-[#080808]/80 backdrop-blur-xl">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center gap-3">
          {/* Logo */}
          <Link href="/" className="shrink-0">
            <Image src="/logo-light.png" alt="Logo" width={28} height={28} className="object-contain" />
          </Link>

          {/* Level picker */}
          <div className="flex-1 flex justify-center">
            <div className="flex items-center gap-1 bg-white/[0.04] border border-white/[0.08] rounded-full p-1">
              {levels.map((l) => (
                <button
                  key={l.value}
                  onClick={() => {
                    setSelectedLevel(l.value);
                    sessionStorage.setItem("sde_level", l.value);
                  }}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all duration-150 ${
                    selectedLevel === l.value
                      ? 'bg-white text-black'
                      : 'text-white/50 hover:text-white/80'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={handleNewChat}
              title="New Chat"
              className="p-1.5 rounded-lg text-white/40 hover:text-white hover:bg-white/[0.06] transition-all"
            >
              <MessageSquarePlus size={19} />
            </button>
            <div className="p-1.5 rounded-lg text-white/40 hover:text-white hover:bg-white/[0.06] transition-all cursor-pointer">
              <UserCircle size={19} />
            </div>
          </div>
        </div>
      </header>

      {/* ── Chat area ───────────────────────────────────────────── */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-6">

          {/* Empty state */}
          {chat.length === 0 && (
            <div className="flex flex-col items-center justify-center gap-8 py-16 text-center">
              <div>
                <div className="text-5xl mb-4">🧑‍💻</div>
                <h1 className="text-3xl font-bold tracking-tight mb-2">
                  Ready to ace your DSA interviews?
                </h1>
                <p className="text-white/45 text-sm leading-relaxed max-w-sm mx-auto">
                  Your AI coach is here. Pick a quick-start question or type your own below.
                </p>
              </div>

              <div className="w-full max-w-lg grid grid-cols-1 sm:grid-cols-2 gap-3">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(s.text)}
                    className="flex items-start gap-3 p-4 bg-white/[0.03] hover:bg-white/[0.06] border border-white/[0.07] hover:border-white/[0.14] rounded-xl text-left text-sm transition-all duration-150"
                  >
                    <span className="text-lg leading-none">{s.icon}</span>
                    <span className="text-white/70 leading-snug">{s.text}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="flex flex-col gap-5">
            {chat.map((message, idx) => {
              const isUser = message.sender === "user";
              const isLastBot = !isUser && idx === chat.length - 1 && isLoading;

              return (
                <div key={idx} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>

                  {/* Bot avatar */}
                  {!isUser && (
                    <div className="shrink-0 w-7 h-7 rounded-full bg-gradient-to-br from-violet-500 to-blue-500 flex items-center justify-center mt-0.5">
                      <span className="text-xs">🤖</span>
                    </div>
                  )}

                  <div
                    className={`relative rounded-2xl px-4 py-3 text-sm leading-relaxed break-words ${
                      isUser
                        ? 'max-w-[75%] bg-white text-black rounded-tr-sm font-medium'
                        : 'max-w-[88%] bg-[#141414] border border-white/[0.07] text-white/90 rounded-tl-sm'
                    }`}
                  >
                    {isLastBot && message.text === "" ? (
                      <TypingDots />
                    ) : isUser ? (
                      <p className="whitespace-pre-wrap">{message.text}</p>
                    ) : (
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          p: ({ children }) => (
                            <p className="mb-2 last:mb-0 whitespace-pre-wrap leading-relaxed">{children}</p>
                          ),
                          h1: ({ children }) => <h1 className="text-xl font-bold mt-4 mb-2">{children}</h1>,
                          h2: ({ children }) => <h2 className="text-lg font-semibold mt-3 mb-1.5">{children}</h2>,
                          h3: ({ children }) => <h3 className="text-base font-semibold mt-2 mb-1">{children}</h3>,
                          code: ({ className, children, ...props }) => {
                            const isBlock = className?.startsWith('language-');
                            return isBlock ? (
                              <code className={`${className} block`} {...props}>{children}</code>
                            ) : (
                              <code
                                className="bg-white/[0.07] text-emerald-300 px-1.5 py-0.5 rounded text-xs font-mono"
                                {...props}
                              >
                                {children}
                              </code>
                            );
                          },
                          pre: ({ children }) => {
                            const codeText = (children as any)?.props?.children ?? '';
                            return (
                              <div className="relative group my-3">
                                <pre className="bg-[#0d0d0d] border border-white/[0.08] rounded-xl p-4 overflow-x-auto text-xs font-mono text-zinc-100 leading-relaxed">
                                  {children}
                                </pre>
                                <CopyButton code={String(codeText).trimEnd()} />
                              </div>
                            );
                          },
                          table: ({ children }) => (
                            <div className="overflow-x-auto my-3">
                              <table className="min-w-full border-collapse text-sm">{children}</table>
                            </div>
                          ),
                          thead: ({ children }) => <thead className="bg-white/[0.05]">{children}</thead>,
                          tbody: ({ children }) => <tbody className="divide-y divide-white/[0.05]">{children}</tbody>,
                          tr: ({ children }) => <tr className="hover:bg-white/[0.03] transition-colors">{children}</tr>,
                          th: ({ children }) => (
                            <th className="px-3 py-2 text-left font-semibold text-white/70 whitespace-nowrap text-xs">{children}</th>
                          ),
                          td: ({ children }) => (
                            <td className="px-3 py-2 text-white/60 align-top text-sm">{children}</td>
                          ),
                          ul: ({ children }) => <ul className="list-disc list-inside space-y-1 my-2 pl-2">{children}</ul>,
                          ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 my-2 pl-2">{children}</ol>,
                          li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                          blockquote: ({ children }) => (
                            <blockquote className="border-l-4 border-blue-500/60 pl-3 my-2 text-white/50 italic">{children}</blockquote>
                          ),
                          a: ({ href, children }) => (
                            <a href={href} className="text-blue-400 underline hover:text-blue-300 transition-colors" target="_blank" rel="noopener noreferrer">
                              {children}
                            </a>
                          ),
                          hr: () => <hr className="border-white/10 my-4" />,
                          strong: ({ children }) => <strong className="font-semibold text-white">{children}</strong>,
                          em: ({ children }) => <em className="italic text-white/70">{children}</em>,
                        }}
                      >
                        {stripThinkTags(message.text)}
                      </ReactMarkdown>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Scroll anchor */}
          <div ref={bottomRef} className="h-4" />
        </div>
      </main>

      {/* ── Input bar ───────────────────────────────────────────── */}
      <div className="shrink-0 border-t border-white/[0.06] bg-[#080808]/90 backdrop-blur-xl px-4 py-4">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-2 bg-[#141414] border border-white/[0.08] rounded-2xl px-4 py-3 focus-within:border-white/20 transition-colors duration-150">
            <input
              ref={inputRef}
              type="text"
              className="flex-1 bg-transparent text-white text-sm placeholder:text-white/25 outline-none resize-none leading-relaxed"
              placeholder="Ask anything about DSA…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              disabled={isLoading}
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || isLoading}
              className={`shrink-0 p-2 rounded-xl transition-all duration-150 ${
                input.trim() && !isLoading
                  ? 'bg-white text-black hover:bg-white/90'
                  : 'bg-white/[0.05] text-white/20 cursor-not-allowed'
              }`}
            >
              <Send size={16} />
            </button>
          </div>
          <p className="text-center text-[11px] text-white/20 mt-2">
            Press <kbd className="font-mono text-white/30">Enter</kbd> to send
          </p>
        </div>
      </div>
    </div>
  );
}
