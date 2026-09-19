"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Atom, Loader2 } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";
import { authService } from "@/services/authService";
import toast from "react-hot-toast";

const LEVELS = [
  { value: "beginner",     label: "Beginner",     desc: "New to quantum computing" },
  { value: "intermediate", label: "Intermediate",  desc: "Know basics of linear algebra" },
  { value: "advanced",     label: "Advanced",      desc: "Comfortable with quantum formalism" },
];

export default function SignupPage() {
  const [form, setForm] = useState({ name: "", email: "", password: "", learning_level: "beginner" });
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const tokens = await authService.signup(form.name, form.email, form.password, form.learning_level);
      const user = await authService.getProfile();
      setAuth(user as any, tokens.access_token);
      toast.success("Welcome to QuantumVerse AI! 🚀");
      router.push("/dashboard");
    } catch {
      // handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-lg">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-quantum-blue/10 border border-quantum-blue/30 flex items-center justify-center mx-auto mb-4">
            <Atom className="w-8 h-8 text-quantum-blue" />
          </div>
          <h1 className="text-2xl font-bold text-white">Start Your Quantum Journey</h1>
          <p className="text-muted-foreground mt-1 text-sm">Create your free account</p>
        </div>
        <div className="glass rounded-2xl border border-white/10 p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm text-muted-foreground mb-2">Full Name</label>
              <input type="text" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} required
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-quantum-blue/50 transition-colors"
                placeholder="Your name" />
            </div>
            <div>
              <label className="block text-sm text-muted-foreground mb-2">Email</label>
              <input type="email" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} required
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-quantum-blue/50 transition-colors"
                placeholder="you@example.com" />
            </div>
            <div>
              <label className="block text-sm text-muted-foreground mb-2">Password</label>
              <input type="password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} required minLength={8}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-quantum-blue/50 transition-colors"
                placeholder="Min 8 characters" />
            </div>
            <div>
              <label className="block text-sm text-muted-foreground mb-3">Learning Level</label>
              <div className="space-y-2">
                {LEVELS.map((lv) => (
                  <label key={lv.value} className={`flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-all ${
                    form.learning_level === lv.value
                      ? "border-quantum-blue/50 bg-quantum-blue/10"
                      : "border-white/10 hover:border-white/20"
                  }`}>
                    <input type="radio" name="level" value={lv.value} checked={form.learning_level === lv.value}
                      onChange={(e) => setForm({...form, learning_level: e.target.value})} className="sr-only" />
                    <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                      form.learning_level === lv.value ? "border-quantum-blue" : "border-white/30"
                    }`}>
                      {form.learning_level === lv.value && <div className="w-2 h-2 rounded-full bg-quantum-blue" />}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-white">{lv.label}</p>
                      <p className="text-xs text-muted-foreground">{lv.desc}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-quantum-blue to-quantum-purple text-white font-bold hover:opacity-90 transition-opacity disabled:opacity-60 flex items-center justify-center gap-2">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Creating Account...</> : "Create Account"}
            </button>
          </form>
          <p className="text-center text-sm text-muted-foreground mt-6">
            Already have an account? <Link href="/login" className="text-quantum-blue hover:underline">Sign in</Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
