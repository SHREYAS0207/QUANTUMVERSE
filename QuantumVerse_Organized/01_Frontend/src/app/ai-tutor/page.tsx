"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Atom, Loader2, Plus } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { aiService } from "@/services/aiService";
import { useAuthStore } from "@/stores/authStore";
import toast from "react-hot-toast";
import { QLearnShell } from "@/components/qlearn/QLearnShell";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const SUGGESTED = [
  "What is quantum superposition?",
  "Explain the Hadamard gate",
  "How does quantum entanglement work?",
  "What is a Bell state?",
  "Explain Grover's algorithm simply",
  "What is quantum decoherence?",
];

const DIFFICULTY_LABELS: Array<{
  value: "beginner" | "intermediate" | "advanced";
  label: string;
  color: string;
}> = [
  { value: "beginner",     label: "Beginner",    color: "text-green-400 border-green-400/30 bg-green-400/5" },
  { value: "intermediate", label: "Intermediate", color: "text-yellow-400 border-yellow-400/30 bg-yellow-400/5" },
  { value: "advanced",     label: "Advanced",     color: "text-red-400 border-red-400/30 bg-red-400/5" },
];

export default function AITutorPage() {
  return <QLearnShell feature="tutor" />;

  const { user } = useAuthStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [convId, setConvId] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<"beginner" | "intermediate" | "advanced">(
    user?.learning_level ?? "beginner"
  );
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const startNewConversation = async () => {
    try {
      const conv = await aiService.createConversation();
      setConvId(conv.id);
      setMessages([]);
    } catch {
      toast.error("Failed to start conversation");
    }
  };

  const sendMessage = async (text?: string) => {
    const content = text ?? input.trim();
    if (!content) return;
    setInput("");

    let currentConvId = convId;
    if (!currentConvId) {
      try {
        const conv = await aiService.createConversation();
        currentConvId = conv.id;
        setConvId(conv.id);
      } catch {
        toast.error("Failed to start conversation");
        return;
      }
    }

    const userMsg: Message = { role: "user", content, timestamp: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await aiService.chat(currentConvId, content, difficulty);
      const aiMsg: Message = { role: "assistant", content: res.response, timestamp: new Date() };
      setMessages((prev) => [...prev, aiMsg]);
    } catch {
      toast.error("QubitAI failed to respond");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="flex flex-col h-[calc(100vh-6rem)] max-h-[900px]">
        <PageHeader title="QubitAI Tutor" subtitle="AI quantum computing expert, adapts to your level">
          <div className="flex gap-1.5">
            {DIFFICULTY_LABELS.map((d) => (
              <button key={d.value} onClick={() => setDifficulty(d.value)}
                className={`px-3 py-1.5 rounded-lg border text-xs font-medium transition-all ${
                  difficulty === d.value ? d.color : "border-white/10 text-muted-foreground hover:border-white/20"
                }`}>
                {d.label}
              </button>
            ))}
          </div>
          <button onClick={startNewConversation}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-white/10 text-xs text-muted-foreground hover:text-white hover:border-white/20 transition-all">
            <Plus className="w-3.5 h-3.5" /> New Chat
          </button>
        </PageHeader>

        <div className="flex-1 glass rounded-xl border border-white/5 flex flex-col overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-2xl bg-quantum-blue/10 border border-quantum-blue/20 flex items-center justify-center mx-auto mb-4 animate-pulse-glow">
                  <Atom className="w-8 h-8 text-quantum-blue" />
                </div>
                <h2 className="text-lg font-bold text-white mb-2">QubitAI</h2>
                <p className="text-sm text-muted-foreground mb-8">Expert quantum computing tutor — ask me anything!</p>
                <div className="grid grid-cols-2 gap-2 max-w-lg mx-auto">
                  {SUGGESTED.map((q) => (
                    <button key={q} onClick={() => sendMessage(q)}
                      className="text-left px-4 py-3 rounded-xl border border-white/10 text-xs text-muted-foreground hover:text-white hover:border-quantum-blue/30 hover:bg-quantum-blue/5 transition-all">
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <AnimatePresence>
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-3 ${
                    msg.role === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    msg.role === "assistant"
                      ? "bg-quantum-blue/10 border border-quantum-blue/30"
                      : "bg-white/10 border border-white/20"
                  }`}>
                    {msg.role === "assistant"
                      ? <Atom className="w-4 h-4 text-quantum-blue" />
                      : <User className="w-4 h-4 text-muted-foreground" />}
                  </div>
                  <div className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-quantum-blue/10 border border-quantum-blue/20 text-white rounded-tr-sm"
                      : "bg-white/5 border border-white/10 text-muted-foreground rounded-tl-sm"
                  }`}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    <p className="text-[10px] text-muted-foreground/50 mt-1.5">
                      {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-quantum-blue/10 border border-quantum-blue/30 flex items-center justify-center">
                  <Atom className="w-4 h-4 text-quantum-blue" />
                </div>
                <div className="px-4 py-3 rounded-2xl rounded-tl-sm bg-white/5 border border-white/10">
                  <div className="flex items-center gap-1">
                    {[0, 1, 2].map((i) => (
                      <motion.div key={i} animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.2, delay: i * 0.2 }}
                        className="w-1.5 h-1.5 rounded-full bg-quantum-blue" />
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-white/5">
            <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }} className="flex gap-3">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={`Ask QubitAI about quantum computing... (${difficulty} level)`}
                className="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-sm text-white placeholder-muted-foreground focus:outline-none focus:border-quantum-blue/40 transition-colors"
                disabled={loading}
              />
              <button type="submit" disabled={loading || !input.trim()}
                className="w-11 h-11 rounded-xl bg-quantum-blue text-quantum-dark flex items-center justify-center hover:opacity-90 disabled:opacity-50 transition-opacity">
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
