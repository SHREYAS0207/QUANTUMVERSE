"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Trophy, Zap, Medal } from "lucide-react";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";

const MOCK_LEADERS = [
  { rank: 1,  name: "QuantumNova",    xp: 12450, level: 25, streak: 34, avatar: "QN" },
  { rank: 2,  name: "SchrodingerCat", xp: 11200, level: 23, streak: 21, avatar: "SC" },
  { rank: 3,  name: "WaveFunction",   xp:  9800, level: 20, streak: 15, avatar: "WF" },
  { rank: 4,  name: "QubitHero",      xp:  8400, level: 17, streak: 12, avatar: "QH" },
  { rank: 5,  name: "EntangleMaster", xp:  7100, level: 15, streak:  9, avatar: "EM" },
  { rank: 6,  name: "SuperpositionX", xp:  6200, level: 13, streak:  7, avatar: "SX" },
  { rank: 7,  name: "TeleportAce",    xp:  5400, level: 11, streak:  5, avatar: "TA" },
  { rank: 8,  name: "PhaseShifter",   xp:  4100, level:  9, streak:  3, avatar: "PS" },
  { rank: 9,  name: "OracleSeeker",   xp:  2800, level:  6, streak:  2, avatar: "OS" },
  { rank: 10, name: "You",            xp:  1200, level:  3, streak:  1, avatar: "ME", isMe: true },
];

const RANK_STYLES: Record<number, { icon: React.ReactNode; color: string }> = {
  1: { icon: <Trophy className="w-5 h-5 text-yellow-400 fill-yellow-400" />, color: "border-yellow-500/30 bg-yellow-500/5" },
  2: { icon: <Medal  className="w-5 h-5 text-gray-300 fill-gray-300" />,   color: "border-gray-400/30  bg-gray-400/5"  },
  3: { icon: <Medal  className="w-5 h-5 text-amber-600 fill-amber-600" />, color: "border-amber-600/30 bg-amber-600/5" },
};

const TABS = ["All Time", "This Week", "This Month"] as const;

export default function LeaderboardPage() {
  const [tab, setTab] = useState<typeof TABS[number]>("All Time");

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <PageHeader
        icon={<Trophy className="w-6 h-6 text-yellow-400" />}
        title="Leaderboard"
        subtitle="Top quantum learners this period"
      />

      {/* Tabs */}
      <div className="flex gap-1 mb-6 p-1 glass rounded-xl border border-white/5">
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
              tab === t ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20" : "text-muted-foreground hover:text-white"
            }`}>
            {t}
          </button>
        ))}
      </div>

      {/* Top 3 podium */}
      <div className="flex items-end justify-center gap-4 mb-8">
        {[MOCK_LEADERS[1], MOCK_LEADERS[0], MOCK_LEADERS[2]].map((leader, i) => {
          const heights = ["h-24", "h-32", "h-20"];
          return (
            <motion.div key={leader.rank} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
              transition={{ delay: i * 0.15 }} className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center text-quantum-dark font-bold">
                {leader.avatar}
              </div>
              <p className="text-xs text-white font-medium">{leader.name}</p>
              <p className="text-xs text-quantum-blue">{leader.xp.toLocaleString()} XP</p>
              <div className={`w-20 ${heights[i]} rounded-t-xl flex items-center justify-center ${
                i === 1 ? "bg-yellow-500/20 border border-yellow-500/30" :
                i === 0 ? "bg-gray-400/10 border border-gray-400/20" :
                           "bg-amber-700/10 border border-amber-700/20"
              }`}>
                <span className="text-2xl font-black text-muted-foreground/60">{leader.rank}</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Full list */}
      <div className="space-y-2">
        {MOCK_LEADERS.map((leader, idx) => {
          const rankStyle = RANK_STYLES[leader.rank];
          return (
            <motion.div key={leader.rank}
              initial={{ x: -20, opacity: 0 }} animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.3 + idx * 0.04 }}
              className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
                (leader as any).isMe
                  ? "border-quantum-blue/30 bg-quantum-blue/5"
                  : rankStyle ? rankStyle.color : "border-white/5 bg-white/2 hover:bg-white/5"
              }`}
            >
              <div className="w-8 text-center">
                {rankStyle ? rankStyle.icon : <span className="text-sm text-muted-foreground font-bold">{leader.rank}</span>}
              </div>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-quantum-blue/30 to-quantum-purple/30 flex items-center justify-center text-sm font-bold text-white">
                {leader.avatar}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="text-sm font-medium text-white">{leader.name}</p>
                  {(leader as any).isMe && <span className="text-xs text-quantum-blue font-medium">(you)</span>}
                </div>
                <p className="text-xs text-muted-foreground">Level {leader.level} · {leader.streak}d streak</p>
              </div>
              <div className="flex items-center gap-1 text-quantum-blue font-bold text-sm">
                <Zap className="w-3.5 h-3.5" />
                {leader.xp.toLocaleString()}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
