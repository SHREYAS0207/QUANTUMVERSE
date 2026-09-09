"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck, Play } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { PageHeader } from "@/components/shared/PageHeader";
import { GlowButton } from "@/components/shared/GlowButton";
import { api } from "@/lib/api";

const CODES = [
  { id: "bit_flip",   label: "Bit Flip Code",   desc: "3-qubit code for X errors",     qubits: 3 },
  { id: "phase_flip", label: "Phase Flip Code",  desc: "3-qubit code for Z errors",     qubits: 3 },
  { id: "noisy",      label: "Noisy Simulation", desc: "Run circuit with noise model",   qubits: 2 },
];

const TOOLTIP_STYLE = {
  contentStyle: { background: "#0d0d1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 },
  itemStyle: { color: "#00d4ff" },
};

export default function ErrorCorrectionPage() {
  const [selected, setSelected] = useState("bit_flip");
  const [errorQubit, setErrorQubit] = useState(0);
  const [applyError, setApplyError] = useState(true);
  const [result, setResult]   = useState<any>(null);
  const [running, setRunning] = useState(false);

  async function run() {
    setRunning(true);
    try {
      let res;
      if (selected === "bit_flip") {
        res = await api.post("/error-correction/bit-flip",   { error_qubit: errorQubit, apply_error: applyError });
      } else if (selected === "phase_flip") {
        res = await api.post("/error-correction/phase-flip", { apply_error: applyError });
      } else {
        res = await api.post("/error-correction/noisy",      { qubits: 2, operations: [{gate:"H",targets:[0],controls:[],column:0},{gate:"CNOT",targets:[1],controls:[0],column:1}], error_rate: 0.05 });
      }
      setResult(res.data);
    } finally {
      setRunning(false);
    }
  }

  const chartData = result ? Object.entries(result.probabilities).map(([k, v]) => ({ state: `|${k}⟩`, prob: Math.round((v as number) * 100) })) : [];

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <PageHeader icon={<ShieldCheck className="w-6 h-6 text-quantum-blue" />}
        title="Error Correction" subtitle="Understand how quantum computers protect against noise" />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {CODES.map(c => (
          <button key={c.id} onClick={() => setSelected(c.id)}
            className={`p-4 rounded-xl border text-left transition-all ${
              selected === c.id ? "border-quantum-blue bg-quantum-blue/10" : "border-white/5 hover:border-white/20 glass"
            }`}>
            <p className={`font-semibold text-sm mb-1 ${ selected === c.id ? "text-quantum-blue" : "text-white" }`}>{c.label}</p>
            <p className="text-xs text-muted-foreground">{c.desc}</p>
          </button>
        ))}
      </div>

      <div className="glass rounded-xl border border-white/5 p-6 mb-6">
        <h3 className="text-sm font-semibold text-white mb-4">Configuration</h3>
        {selected === "bit_flip" && (
          <div className="flex gap-6 flex-wrap">
            <div>
              <label className="text-xs text-muted-foreground mb-2 block">Error qubit</label>
              <div className="flex gap-2">
                {[0,1,2].map(q => (
                  <button key={q} onClick={() => setErrorQubit(q)}
                    className={`w-10 h-10 rounded-lg font-bold text-sm transition-all ${ errorQubit === q ? "bg-quantum-blue text-quantum-dark" : "bg-white/5 text-muted-foreground hover:bg-white/10" }`}>
                    q{q}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-2 block">Apply error?</label>
              <button onClick={() => setApplyError(p => !p)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${ applyError ? "bg-red-500/20 text-red-400 border border-red-500/30" : "bg-white/5 text-muted-foreground" }`}>
                {applyError ? "Error ON" : "Error OFF"}
              </button>
            </div>
          </div>
        )}
        <GlowButton onClick={run} loading={running} className="mt-5">
          <Play className="w-4 h-4" /> Run Simulation
        </GlowButton>
      </div>

      {result && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl border border-white/5 p-6">
          <p className="text-xs text-muted-foreground mb-4">{result.description}</p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData}>
              <XAxis dataKey="state" tick={{ fontSize: 11, fill: "#6b6b80" }} />
              <YAxis unit="%" tick={{ fontSize: 11, fill: "#6b6b80" }} />
              <Tooltip {...TOOLTIP_STYLE} formatter={(v: any) => [`${v}%`, "Probability"]} />
              <Bar dataKey="prob" fill="#00d4ff" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      )}
    </div>
  );
}
