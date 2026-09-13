"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { motion } from "framer-motion";
import type { SimulationResult } from "@/types/circuit";

interface SimulationPanelProps {
  result: SimulationResult | null;
}

const COLORS = ["#00D4FF", "#7B2FBE", "#06FFA5", "#f59e0b", "#f87171", "#818cf8", "#34d399", "#fb923c"];

export function SimulationPanel({ result }: SimulationPanelProps) {
  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <div className="w-16 h-16 rounded-2xl bg-quantum-blue/5 border border-quantum-blue/10 flex items-center justify-center mb-4">
          <span className="text-2xl">🔬</span>
        </div>
        <p className="text-sm text-muted-foreground">Run the circuit to see simulation results</p>
        <p className="text-xs text-muted-foreground/60 mt-1">Results will show measurement probabilities</p>
      </div>
    );
  }

  if (!result.success) {
    return (
      <div className="p-6">
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20">
          <p className="text-sm text-red-400 font-medium">Simulation Error</p>
          <p className="text-xs text-red-400/70 mt-1">{result.error}</p>
        </div>
      </div>
    );
  }

  const chartData = Object.entries(result.probabilities)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([state, prob]) => ({
      state: `|${state}⟩`,
      probability: Math.round(prob * 100),
      count: result.counts[state] ?? 0,
    }));

  return (
    <div className="p-5 space-y-5">
      {/* Summary */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Shots",    value: result.total_shots.toLocaleString() },
          { label: "States",   value: Object.keys(result.counts).length },
          { label: "Time",     value: `${result.execution_time}ms` },
        ].map((s) => (
          <div key={s.label} className="glass rounded-lg p-3 text-center border border-white/5">
            <p className="text-lg font-bold text-white font-mono">{s.value}</p>
            <p className="text-[10px] text-muted-foreground">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Histogram */}
      <div>
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Probability Distribution</p>
        <div className="h-44">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
              <XAxis dataKey="state" tick={{ fill: "#94a3b8", fontSize: 10, fontFamily: "Times New Roman" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#64748b", fontSize: 9 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: "#0D1F3C", border: "1px solid rgba(0,212,255,0.2)", borderRadius: "8px", color: "#e2e8f0", fontSize: "11px" }}
                formatter={(val: number, name: string, props: any) => [
                  `${val}% (${props.payload.count} counts)`, "Probability"
                ]}
              />
              <Bar dataKey="probability" radius={[4, 4, 0, 0]}>
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} fillOpacity={0.85} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* State breakdown */}
      <div>
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">State Breakdown</p>
        <div className="space-y-2">
          {chartData.map((d, i) => (
            <motion.div
              key={d.state}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center gap-3"
            >
              <span className="font-mono text-xs w-16 text-right" style={{ color: COLORS[i % COLORS.length] }}>{d.state}</span>
              <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${d.probability}%` }}
                  transition={{ duration: 0.8, ease: "easeOut", delay: i * 0.05 }}
                  className="h-full rounded-full"
                  style={{ backgroundColor: COLORS[i % COLORS.length] }}
                />
              </div>
              <span className="text-xs font-mono text-muted-foreground w-10 text-right">{d.probability}%</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
