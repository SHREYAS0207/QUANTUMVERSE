"use client";

import React, { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  Calculator,
  FlaskConical,
  Loader2,
  Send,
  Sparkles,
  Target,
  Wand2,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { qlearnService } from "@/services/qlearnService";

const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`glass rounded-2xl p-5 border border-white/5 ${className}`}>{children}</div>
);

const FEATURE_META = {
  tutor: {
    title: "AI Tutor",
    subtitle: "Guided explanations for quantum concepts, intuition, and step-by-step learning.",
    icon: Bot,
    accent: "text-quantum-blue",
    badge: "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/30",
  },
  solver: {
    title: "Problem Solver",
    subtitle: "Solve conceptual and numerical quantum questions with verification and reasoning.",
    icon: Calculator,
    accent: "text-quantum-purple",
    badge: "bg-quantum-purple/10 text-quantum-purple border border-quantum-purple/30",
  },
  explorer: {
    title: "Quantum Explorer",
    subtitle: "Explore topics, simulations, and learning resources using a guided discovery mode.",
    icon: FlaskConical,
    accent: "text-quantum-cyan",
    badge: "bg-quantum-cyan/10 text-quantum-cyan border border-quantum-cyan/30",
  },
} as const;

const MODE_OPTIONS = [
  { value: "tutor", label: "Tutor" },
  { value: "solver", label: "Solver" },
  { value: "explorer", label: "Explorer" },
] as const;

export function QLearnShell({ feature = "tutor" }: { feature?: "tutor" | "solver" | "explorer" | "all" }) {
  const initialFeature = feature === "all" ? "tutor" : feature;
  const [activeFeature, setActiveFeature] = useState<(typeof MODE_OPTIONS)[number]["value"]>(initialFeature);
  const meta = FEATURE_META[activeFeature];
  const Icon = meta.icon;

  const [topic, setTopic] = useState("Quantum Teleportation");
  const [question, setQuestion] = useState(
    activeFeature === "tutor"
      ? "Explain the difference between superposition and entanglement in a beginner-friendly way."
      : activeFeature === "solver"
        ? "Apply the Hadamard gate to |0> and explain the measurement probabilities."
        : "Explore how Bell states enable quantum teleportation and what makes them special."
  );
  const [answer, setAnswer] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [difficulty, setDifficulty] = useState<"beginner" | "intermediate" | "advanced">("beginner");

  const context = useMemo(
    () => ({ currentTopic: topic, currentLesson: activeFeature, difficulty }),
    [topic, activeFeature, difficulty]
  );

  async function run() {
    if (!question.trim()) return;

    setLoading(true);
    try {
      const result =
        activeFeature === "tutor"
          ? await qlearnService.chat({
              message: question.trim(),
              mode: "step_by_step",
              context,
            })
          : activeFeature === "solver"
            ? await qlearnService.solve({ question: question.trim(), context })
            : await qlearnService.explore({ query: question.trim(), context });

      setAnswer(result);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          title={feature === "all" ? "AI & Tutor" : meta.title}
          subtitle={feature === "all"
            ? "Unified AI assistance for tutoring, problem solving, and guided exploration."
            : meta.subtitle}
          icon={
            <div className="w-11 h-11 rounded-xl border border-quantum-blue/20 bg-quantum-blue/10 flex items-center justify-center">
              <Icon className={`w-5 h-5 ${meta.accent}`} />
            </div>
          }
        >
          <div className="flex flex-wrap items-center gap-2">
            {feature === "all" && MODE_OPTIONS.map((option) => (
              <button
                key={option.value}
                onClick={() => setActiveFeature(option.value)}
                className={`rounded-full border px-3 py-1.5 text-[11px] font-medium transition-all ${
                  activeFeature === option.value
                    ? "border-quantum-blue/40 bg-quantum-blue/10 text-quantum-blue"
                    : "border-white/10 text-muted-foreground hover:border-white/20 hover:text-white"
                }`}
              >
                {option.label}
              </button>
            ))}
            <span className={`inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-medium ${meta.badge}`}>
              <Sparkles className="w-3.5 h-3.5" />
              {feature === "all" ? "AI & Tutor Active" : "QLearn Active"}
            </span>
          </div>
        </PageHeader>

        <div className="grid gap-6 xl:grid-cols-[260px_minmax(0,1fr)_300px]">
          <Card className="h-fit">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-4 h-4 text-quantum-blue" />
              <h2 className="text-sm font-semibold uppercase tracking-[0.22em] text-muted-foreground">Context</h2>
            </div>

            <label className="block text-xs uppercase tracking-[0.18em] text-muted-foreground mb-2">Topic</label>
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2.5 text-sm text-white placeholder:text-muted-foreground/70 focus:border-quantum-blue/40 focus:outline-none"
            />

            <div className="mt-5 space-y-2 text-sm text-muted-foreground">
              <div className="rounded-xl bg-white/5 border border-white/10 p-3">Lesson: <span className="text-white">Auto-linked</span></div>
              <div className="rounded-xl bg-white/5 border border-white/10 p-3">Simulation: <span className="text-white">Shared context</span></div>
              <div className="rounded-xl bg-white/5 border border-white/10 p-3">Circuit: <span className="text-white">Solver-ready</span></div>
            </div>

            <div className="mt-5 pt-4 border-t border-white/10">
              <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground mb-3">Difficulty</p>
              <div className="flex flex-wrap gap-2">
                {(["beginner", "intermediate", "advanced"] as const).map((level) => (
                  <button
                    key={level}
                    onClick={() => setDifficulty(level)}
                    className={`rounded-full border px-2.5 py-1.5 text-[11px] capitalize transition-all ${
                      difficulty === level
                        ? "border-quantum-blue/40 bg-quantum-blue/10 text-quantum-blue"
                        : "border-white/10 text-muted-foreground hover:border-white/20 hover:text-white"
                    }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>
          </Card>

          <Card className="overflow-hidden">
            <div className="flex items-center justify-between gap-3 mb-4">
              <div className="flex items-center gap-2">
                <Wand2 className="w-4 h-4 text-quantum-cyan" />
                <h2 className="text-sm font-semibold uppercase tracking-[0.22em] text-muted-foreground">Prompt</h2>
              </div>
              <span className="text-[10px] uppercase tracking-[0.2em] text-quantum-blue">{activeFeature}</span>
            </div>

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={activeFeature === "explorer" ? "Describe a quantum concept to explore..." : "Ask a question about quantum theory or computation..."}
              className="h-36 w-full rounded-xl border border-white/10 bg-black/30 p-3 text-sm text-white placeholder:text-muted-foreground/70 focus:border-quantum-blue/40 focus:outline-none"
            />

            <div className="mt-5 flex items-center justify-between gap-3">
              <span className="text-xs text-muted-foreground">Context-aware reasoning enabled</span>
              <button
                onClick={run}
                disabled={loading || !question.trim()}
                className="inline-flex items-center gap-2 rounded-xl bg-quantum-blue px-4 py-2.5 text-sm font-semibold text-quantum-dark disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                {loading ? "Processing..." : "Run"}
              </button>
            </div>

            <div className="mt-6 space-y-4">
              <AnimatePresence mode="wait">
                {!answer ? (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -8 }}
                    className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-5 text-sm text-muted-foreground"
                  >
                    Results will appear here with explanation, verification, and guided next steps.
                  </motion.div>
                ) : (
                  <motion.div
                    key="response"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="rounded-2xl border border-quantum-blue/20 bg-[#07121e] p-4"
                  >
                    <div className="mb-3 flex items-center gap-2 text-[10px] uppercase tracking-[0.2em] text-quantum-blue">
                      <Sparkles className="w-3.5 h-3.5" />
                      Response
                    </div>

                    <div className="space-y-3 text-sm leading-relaxed text-slate-200">
                      {activeFeature === "tutor" && (
                        <>
                          <p>{answer?.response ?? "No response generated yet."}</p>
                          {answer?.suggestedActions?.length ? (
                            <div className="flex flex-wrap gap-2 pt-2">
                              {answer.suggestedActions.map((item: any, idx: number) => (
                                <button
                                  key={idx}
                                  onClick={() => setQuestion(item.action || item.label)}
                                  className="rounded-full border border-quantum-blue/20 bg-quantum-blue/5 px-3 py-1.5 text-xs text-quantum-blue hover:border-quantum-blue/40"
                                >
                                  {item.label}
                                </button>
                              ))}
                            </div>
                          ) : null}
                        </>
                      )}

                      {activeFeature === "solver" && (
                        <>
                          <p>{answer?.finalAnswer ?? answer?.explanation ?? "No computed result generated yet."}</p>
                          {answer?.verification && (
                            <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-3 text-emerald-300 text-xs">
                              {answer.verification.status}: {answer.verification.message}
                            </div>
                          )}
                        </>
                      )}

                      {activeFeature === "explorer" && (
                        <>
                          <p>{answer?.summary ?? answer?.result ?? answer?.message ?? "No exploration result yet."}</p>
                          {answer?.suggestedActions?.length ? (
                            <ul className="space-y-2 pt-2 text-xs text-slate-300">
                              {answer.suggestedActions.map((item: any, idx: number) => (
                                <li key={idx} className="rounded-lg border border-white/10 bg-white/5 p-2">
                                  {item.label}
                                </li>
                              ))}
                            </ul>
                          ) : null}
                        </>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </Card>

          <Card className="h-fit">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-4 h-4 text-quantum-purple" />
              <h2 className="text-sm font-semibold uppercase tracking-[0.22em] text-muted-foreground">Overview</h2>
            </div>

            <div className="space-y-3 text-sm text-muted-foreground">
              <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                <span className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Current topic</span>
                <p className="mt-2 text-white">{topic}</p>
              </div>
              <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                <span className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Mode</span>
                <p className="mt-2 text-white capitalize">{feature}</p>
              </div>
              <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                <span className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Difficulty</span>
                <p className="mt-2 text-white capitalize">{difficulty}</p>
              </div>
            </div>

            <div className="mt-5 border-t border-white/10 pt-4">
              <p className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground mb-3">Suggested topics</p>
              <div className="space-y-2 text-xs text-muted-foreground">
                {[
                  "Superposition",
                  "Hadamard gate",
                  "Quantum entanglement",
                  "Bell states",
                  "Grover's algorithm",
                ].map((item) => (
                  <button
                    key={item}
                    onClick={() => setTopic(item)}
                    className="block w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-left hover:border-quantum-blue/30 hover:text-white"
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
