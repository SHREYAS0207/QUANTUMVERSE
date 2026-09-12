"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { motion } from "framer-motion";
import {
  BarChart3,
  CheckCircle2,
  Clock3,
  Hash,
  Activity,
  AlertTriangle,
} from "lucide-react";
import type { SimulationResult } from "@/types/circuit";

interface SimulationPanelProps {
  result: SimulationResult | null;
}

const COLORS = [
  "#22d3ee",
  "#a78bfa",
  "#34d399",
  "#fbbf24",
  "#fb7185",
  "#818cf8",
  "#2dd4bf",
  "#fb923c",
];

export function SimulationPanel({
  result,
}: SimulationPanelProps) {
  /* Empty state */
  if (!result) {
    return (
      <div className="flex h-full flex-col items-center justify-center px-6 py-10 text-center">
        <div className="relative mb-5">
          <div className="absolute inset-0 rounded-2xl bg-cyan-400/10 blur-xl" />

          <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.04]">
            <Activity className="h-7 w-7 text-cyan-300/70" />
          </div>
        </div>

        <p className="text-sm font-semibold text-white/70">
          No simulation results
        </p>

        <p className="mt-1 max-w-[210px] text-[10px] leading-relaxed text-white/30">
          Run your circuit to observe measurement probabilities and quantum
          state statistics.
        </p>

        <div className="mt-5 flex items-center gap-2 rounded-lg border border-white/5 bg-white/[0.02] px-3 py-2">
          <BarChart3 className="h-3 w-3 text-cyan-300/40" />

          <span className="text-[9px] uppercase tracking-[0.12em] text-white/25">
            Awaiting execution
          </span>
        </div>
      </div>
    );
  }

  /* Error state */
  if (!result.success) {
    return (
      <div className="p-5">
        <div className="rounded-2xl border border-red-400/20 bg-red-400/[0.05] p-4">
          <div className="mb-3 flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-red-400/10">
              <AlertTriangle className="h-3.5 w-3.5 text-red-300" />
            </div>

            <div>
              <p className="text-xs font-semibold text-red-300">
                Simulation Error
              </p>

              <p className="text-[9px] text-red-300/40">
                Execution could not be completed
              </p>
            </div>
          </div>

          <div className="rounded-lg border border-red-400/10 bg-black/20 p-3">
            <p className="break-words text-[10px] leading-relaxed text-red-200/70">
              {result.error || "An unknown simulation error occurred."}
            </p>
          </div>
        </div>
      </div>
    );
  }

  const chartData = Object.entries(result.probabilities)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([state, prob]) => ({
      state: `|${state}⟩`,
      probability: Math.round(prob * 100),
      exactProbability: prob,
      count: result.counts[state] ?? 0,
    }));

  const dominantState = chartData.reduce(
    (highest, current) =>
      current.probability > highest.probability
        ? current
        : highest,
    chartData[0]
  );

  return (
    <div className="space-y-5 p-5">
      {/* Success header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg border border-emerald-400/15 bg-emerald-400/[0.06]">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-300" />
            </div>

            <div>
              <p className="text-xs font-semibold text-white/80">
                Simulation Complete
              </p>

              <p className="text-[9px] text-white/25">
                Measurement analysis
              </p>
            </div>
          </div>
        </div>

        <span className="rounded-full border border-emerald-400/15 bg-emerald-400/[0.05] px-2 py-1 text-[8px] font-semibold uppercase tracking-[0.12em] text-emerald-300/70">
          Success
        </span>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-3 gap-2">
        <SummaryCard
          icon={Hash}
          label="Shots"
          value={result.total_shots.toLocaleString()}
        />

        <SummaryCard
          icon={BarChart3}
          label="States"
          value={Object.keys(result.counts).length.toString()}
        />

        <SummaryCard
          icon={Clock3}
          label="Time"
          value={`${result.execution_time}ms`}
        />
      </div>

      {/* Dominant state */}
      {dominantState && (
        <div className="relative overflow-hidden rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.025] p-4">
          <div className="absolute -right-8 -top-8 h-24 w-24 rounded-full bg-cyan-400/10 blur-2xl" />

          <div className="relative">
            <div className="mb-2 flex items-center gap-2">
              <Activity className="h-3 w-3 text-cyan-300/60" />

              <span className="text-[9px] font-semibold uppercase tracking-[0.16em] text-white/30">
                Dominant State
              </span>
            </div>

            <div className="flex items-end justify-between">
              <span className="font-mono text-2xl font-bold text-cyan-300">
                {dominantState.state}
              </span>

              <span className="font-mono text-sm text-white/60">
                {dominantState.probability}%
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Probability distribution */}
      <section>
        <div className="mb-3 flex items-center justify-between">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-white/50">
              Probability Distribution
            </p>

            <p className="mt-0.5 text-[9px] text-white/20">
              Measured output across computational basis states
            </p>
          </div>
        </div>

        <div className="h-48 rounded-xl border border-white/5 bg-black/20 p-2">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart
              data={chartData}
              margin={{
                top: 10,
                right: 5,
                bottom: 5,
                left: -20,
              }}
            >
              <XAxis
                dataKey="state"
                tick={{
                  fill: "#64748b",
                  fontSize: 9,
                  fontFamily: "monospace",
                }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                domain={[0, 100]}
                tick={{
                  fill: "#475569",
                  fontSize: 8,
                }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(value) => `${value}%`}
              />

              <Tooltip
                cursor={{
                  fill: "rgba(255,255,255,0.025)",
                }}
                contentStyle={{
                  background: "#050505",
                  border: "1px solid rgba(34,211,238,0.18)",
                  borderRadius: "10px",
                  color: "#e2e8f0",
                  fontSize: "10px",
                  boxShadow:
                    "0 15px 40px rgba(0,0,0,0.5)",
                }}
                formatter={(
                  value: number,
                  _name: string,
                  props: any
                ) => [
                  `${value}% · ${props.payload.count} counts`,
                  "Probability",
                ]}
              />

              <Bar
                dataKey="probability"
                radius={[5, 5, 1, 1]}
              >
                {chartData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      COLORS[index % COLORS.length]
                    }
                    fillOpacity={0.85}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* State breakdown */}
      <section>
        <div className="mb-3">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-white/50">
            State Breakdown
          </p>

          <p className="mt-0.5 text-[9px] text-white/20">
            Probability and observed measurement counts
          </p>
        </div>

        <div className="space-y-2">
          {chartData.map((item, index) => {
            const color =
              COLORS[index % COLORS.length];

            return (
              <motion.div
                key={item.state}
                initial={{
                  opacity: 0,
                  x: -8,
                }}
                animate={{
                  opacity: 1,
                  x: 0,
                }}
                transition={{
                  delay: index * 0.04,
                }}
                className="rounded-xl border border-white/5 bg-white/[0.015] p-2.5 transition-colors hover:border-white/10 hover:bg-white/[0.025]"
              >
                <div className="mb-2 flex items-center justify-between">
                  <span
                    className="font-mono text-xs font-semibold"
                    style={{ color }}
                  >
                    {item.state}
                  </span>

                  <div className="flex items-center gap-2">
                    <span className="font-mono text-[9px] text-white/25">
                      {item.count} counts
                    </span>

                    <span
                      className="font-mono text-[10px] font-semibold"
                      style={{ color }}
                    >
                      {item.probability}%
                    </span>
                  </div>
                </div>

                <div className="h-1.5 overflow-hidden rounded-full bg-white/5">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{
                      width: `${item.probability}%`,
                    }}
                    transition={{
                      duration: 0.7,
                      ease: "easeOut",
                      delay: index * 0.04,
                    }}
                    className="h-full rounded-full"
                    style={{
                      backgroundColor: color,
                      boxShadow: `0 0 8px ${color}55`,
                    }}
                  />
                </div>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Footer information */}
      <div className="border-t border-white/5 pt-3">
        <div className="flex items-center justify-between text-[8px] uppercase tracking-[0.12em] text-white/20">
          <span>QuantumVerse Simulator</span>
          <span>{chartData.length} basis states</span>
        </div>
      </div>
    </div>
  );
}

function SummaryCard({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Hash;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-white/5 bg-white/[0.02] p-3">
      <div className="mb-2 flex items-center gap-1.5">
        <Icon className="h-3 w-3 text-cyan-300/50" />

        <span className="text-[8px] uppercase tracking-[0.12em] text-white/25">
          {label}
        </span>
      </div>

      <p className="font-mono text-sm font-bold text-white/80">
        {value}
      </p>
    </div>
  );
}