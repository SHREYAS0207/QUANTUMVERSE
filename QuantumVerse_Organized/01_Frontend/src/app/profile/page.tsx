"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { User, Mail, Zap, BookOpen, FlaskConical, Trophy, Flame, Save, Loader2 } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { useAuthStore } from "@/stores/authStore";
import { authService } from "@/services/authService";
import { formatXP, getXPProgress } from "@/lib/utils";
import toast from "react-hot-toast";

const LEVELS = ["beginner", "intermediate", "advanced"] as const;

export default function ProfilePage() {
  const { user, setAuth, token } = useAuthStore();
  const [name, setName] = useState(user?.name ?? "");
  const [level, setLevel] = useState(user?.learning_level ?? "beginner");
  const [saving, setSaving] = useState(false);

  const xpProgress = getXPProgress(user?.xp ?? 0);

  const handleSave = async () => {
    setSaving(true);
    try {
      const updated = await authService.updateProfile({ name, learning_level: level } as any);
      if (token) setAuth(updated as any, token);
      toast.success("Profile updated!");
    } catch { toast.error("Failed to update profile"); }
    finally { setSaving(false); }
  };

  return (
    <AppShell>
      <PageHeader title="Profile" subtitle="Manage your account and preferences" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Avatar + stats */}
        <div className="space-y-4">
          <QuantumCard className="text-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center text-3xl font-black text-white mx-auto mb-4">
              {user?.name?.[0]?.toUpperCase() ?? "Q"}
            </div>
            <h2 className="text-lg font-bold text-white">{user?.name}</h2>
            <p className="text-sm text-muted-foreground">{user?.email}</p>
            <span className={`mt-2 inline-block px-3 py-1 rounded-full text-xs border capitalize ${
              level === "beginner" ? "text-green-400 border-green-400/30 bg-green-400/5" :
              level === "intermediate" ? "text-yellow-400 border-yellow-400/30 bg-yellow-400/5" :
              "text-red-400 border-red-400/30 bg-red-400/5"
            }`}>{user?.learning_level}</span>

            {/* XP bar */}
            <div className="mt-5">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-muted-foreground">Level {user?.level}</span>
                <span className="text-quantum-blue font-mono">{formatXP(user?.xp ?? 0)}</span>
              </div>
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <motion.div
                  animate={{ width: `${xpProgress}%` }}
                  className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full"
                />
              </div>
              <p className="text-xs text-muted-foreground mt-1 text-right">{Math.round(xpProgress)}% to Level {(user?.level ?? 1) + 1}</p>
            </div>
          </QuantumCard>

          {/* Stats */}
          <QuantumCard>
            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Statistics</p>
            <div className="space-y-3">
              {[
                { icon: BookOpen, label: "Lessons Completed",  value: user?.statistics?.total_lessons ?? 0,   color: "text-blue-400" },
                { icon: FlaskConical, label: "Circuits Built",  value: user?.statistics?.total_circuits ?? 0,  color: "text-purple-400" },
                { icon: Trophy, label: "Quizzes Taken",        value: user?.statistics?.total_quizzes ?? 0,   color: "text-yellow-400" },
                { icon: Zap,   label: "Quiz Accuracy",         value: `${user?.statistics?.quiz_accuracy ?? 0}%`, color: "text-green-400" },
                { icon: Flame, label: "Day Streak",            value: user?.streak_days ?? 0,                  color: "text-orange-400" },
              ].map((s) => (
                <div key={s.label} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <s.icon className={`w-4 h-4 ${s.color}`} />
                    <span className="text-xs text-muted-foreground">{s.label}</span>
                  </div>
                  <span className="text-sm font-bold text-white">{s.value}</span>
                </div>
              ))}
            </div>
          </QuantumCard>
        </div>

        {/* Right: Edit form */}
        <div className="lg:col-span-2">
          <QuantumCard>
            <h3 className="text-sm font-semibold text-white mb-5">Edit Profile</h3>
            <div className="space-y-5">
              <div>
                <label className="block text-xs text-muted-foreground mb-2">Display Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                  <input type="text" value={name} onChange={(e) => setName(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-sm text-white focus:outline-none focus:border-quantum-blue/50 transition-colors" />
                </div>
              </div>

              <div>
                <label className="block text-xs text-muted-foreground mb-2">Email</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                  <input type="email" value={user?.email} disabled
                    className="w-full pl-10 pr-4 py-3 rounded-xl bg-white/3 border border-white/5 text-sm text-muted-foreground cursor-not-allowed" />
                </div>
              </div>

              <div>
                <label className="block text-xs text-muted-foreground mb-3">Learning Level</label>
                <div className="grid grid-cols-3 gap-3">
                  {LEVELS.map((lv) => (
                    <button key={lv} onClick={() => setLevel(lv)}
                      className={`py-3 rounded-xl border text-sm font-medium capitalize transition-all ${
                        level === lv
                          ? lv === "beginner" ? "border-green-500/50 bg-green-500/10 text-green-400"
                          : lv === "intermediate" ? "border-yellow-500/50 bg-yellow-500/10 text-yellow-400"
                          : "border-red-500/50 bg-red-500/10 text-red-400"
                          : "border-white/10 text-muted-foreground hover:border-white/20"
                      }`}>{lv}</button>
                  ))}
                </div>
              </div>

              <button onClick={handleSave} disabled={saving}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-quantum-blue text-quantum-dark font-bold text-sm hover:opacity-90 transition-opacity disabled:opacity-60">
                {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                {saving ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </QuantumCard>
        </div>
      </div>
    </AppShell>
  );
}
