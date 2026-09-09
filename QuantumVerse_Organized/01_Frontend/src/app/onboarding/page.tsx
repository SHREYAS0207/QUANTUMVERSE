"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Atom, BookOpen, BrainCircuit, FlaskConical, ArrowRight, Check } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { useAuthStore } from "@/stores/authStore";
import { api } from "@/lib/api";

const LEVELS = [
  { id: "beginner",     label: "Beginner",     desc: "New to quantum computing",       icon: "??" },
  { id: "intermediate", label: "Intermediate",  desc: "Know linear algebra & some QM",   icon: "⚡" },
  { id: "advanced",     label: "Advanced",      desc: "Research / industry background",  icon: "??" },
];

const GOALS = [
  { id: "learn_basics",    label: "Learn the basics",       icon: BookOpen      },
  { id: "build_circuits",  label: "Build quantum circuits",  icon: FlaskConical  },
  { id: "explore_ai",      label: "Explore AI + quantum",    icon: BrainCircuit  },
  { id: "research",        label: "Research & algorithms",   icon: Atom          },
];

const STEPS = ["Welcome", "Your Level", "Your Goals", "Ready!"];

export default function OnboardingPage() {
  const router   = useRouter();
  const { user } = useAuthStore();
  const [step,  setStep]  = useState(0);
  const [level, setLevel] = useState("");
  const [goals, setGoals] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);

  function toggleGoal(id: string) {
    setGoals(prev => prev.includes(id) ? prev.filter(g => g !== id) : [...prev, id]);
  }

  async function finish() {
    setSaving(true);
    try {
      await api.put("/auth/profile", { learning_level: level });
    } catch {}
    setSaving(false);
    router.push("/dashboard");
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 bg-quantum-dark">
      {/* Glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-quantum-blue/5 blur-3xl" />
      </div>

      {/* Step indicators */}
      <div className="flex gap-2 mb-10">
        {STEPS.map((s, i) => (
          <div key={s} className={`flex items-center gap-2 ${ i < STEPS.length - 1 ? "" : "" }`}>
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
              i < step  ? "bg-quantum-blue text-quantum-dark" :
              i === step ? "border-2 border-quantum-blue text-quantum-blue" :
                           "border border-white/10 text-muted-foreground"
            }`}>
              {i < step ? <Check className="w-3.5 h-3.5" /> : i + 1}
            </div>
            {i < STEPS.length - 1 && <div className={`w-10 h-px ${ i < step ? "bg-quantum-blue" : "bg-white/10" }`} />}
          </div>
        ))}
      </div>

      {/* Card */}
      <AnimatePresence mode="wait">
        <motion.div key={step}
          initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -40 }}
          transition={{ duration: 0.3 }}
          className="w-full max-w-md glass rounded-2xl border border-white/10 p-8">

          {step === 0 && (
            <div className="text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center mx-auto mb-6">
                <Atom className="w-8 h-8 text-quantum-dark" />
              </div>
              <h1 className="text-2xl font-bold text-white mb-2">Welcome to QuantumVerse{user?.name ? `, ${user.name}` : ""}!</h1>
              <p className="text-muted-foreground text-sm mb-8">Let's personalise your quantum learning journey in 60 seconds.</p>
              <GlowButton onClick={() => setStep(1)} className="w-full justify-center">
                Let's Go <ArrowRight className="w-4 h-4" />
              </GlowButton>
            </div>
          )}

          {step === 1 && (
            <div>
              <h2 className="text-xl font-bold text-white mb-1">What's your level?</h2>
              <p className="text-muted-foreground text-sm mb-6">We'll tailor explanations and content to match.</p>
              <div className="space-y-3 mb-8">
                {LEVELS.map(l => (
                  <button key={l.id} onClick={() => setLevel(l.id)}
                    className={`w-full text-left p-4 rounded-xl border transition-all ${
                      level === l.id
                        ? "border-quantum-blue bg-quantum-blue/10 text-white"
                        : "border-white/5 bg-white/2 text-muted-foreground hover:border-white/20"
                    }`}>
                    <span className="text-xl mr-3">{l.icon}</span>
                    <span className="font-medium">{l.label}</span>
                    <span className="text-xs block pl-8 mt-0.5 opacity-70">{l.desc}</span>
                  </button>
                ))}
              </div>
              <GlowButton onClick={() => setStep(2)} disabled={!level} className="w-full justify-center">
                Continue <ArrowRight className="w-4 h-4" />
              </GlowButton>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-xl font-bold text-white mb-1">What are your goals?</h2>
              <p className="text-muted-foreground text-sm mb-6">Pick all that apply. We'll highlight the most relevant content.</p>
              <div className="grid grid-cols-2 gap-3 mb-8">
                {GOALS.map(g => {
                  const active = goals.includes(g.id);
                  return (
                    <button key={g.id} onClick={() => toggleGoal(g.id)}
                      className={`p-4 rounded-xl border transition-all flex flex-col items-center gap-2 ${
                        active ? "border-quantum-blue bg-quantum-blue/10" : "border-white/5 hover:border-white/20"
                      }`}>
                      <g.icon className={`w-5 h-5 ${ active ? "text-quantum-blue" : "text-muted-foreground" }`} />
                      <span className={`text-xs font-medium text-center ${ active ? "text-white" : "text-muted-foreground" }`}>
                        {g.label}
                      </span>
                    </button>
                  );
                })}
              </div>
              <GlowButton onClick={() => setStep(3)} disabled={goals.length === 0} className="w-full justify-center">
                Continue <ArrowRight className="w-4 h-4" />
              </GlowButton>
            </div>
          )}

          {step === 3 && (
            <div className="text-center">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-2xl font-bold text-white mb-2">You're all set!</h2>
              <p className="text-muted-foreground text-sm mb-2">
                Level: <span className="text-quantum-blue font-medium capitalize">{level}</span>
              </p>
              <p className="text-muted-foreground text-sm mb-8">
                {goals.length} goal{goals.length > 1 ? "s" : ""} selected
              </p>
              <GlowButton onClick={finish} loading={saving} className="w-full justify-center">
                Enter QuantumVerse 🚀
              </GlowButton>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
