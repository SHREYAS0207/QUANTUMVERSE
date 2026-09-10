"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Zap, Search, Radio, Waves, Loader2, BarChart2 } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { algorithmService } from "@/services/algorithmService";
import toast from "react-hot-toast";

type AlgId = "grover" | "teleportation" | "deutsch-jozsa" | "qft";

const ALGORITHMS = [
  {
    id: "grover" as AlgId, icon: Search, name: "Grover's Search", color: "#00D4FF",
    complexity: { classical: "O(N)", quantum: "O(√N)" },
    description: "Finds a target item in an unsorted database with quadratic speedup.",
    steps: ["Initialize equal superposition", "Apply Oracle (mark target)", "Apply Diffusion operator", "Repeat iterations", "Measure — find target!"],
  },
  {
    id: "teleportation" as AlgId, icon: Radio, name: "Quantum Teleportation", color: "#7B2FBE",
    complexity: { classical: "Impossible", quantum: "3 qubits + 2 cbits" },
    description: "Transfers a quantum state using entanglement and classical communication.",
    steps: ["Prepare qubit to teleport", "Create Bell pair", "Apply CNOT + Hadamard", "Measure sender qubits", "Apply corrections", "State teleported!"],
  },
  {
    id: "deutsch-jozsa" as AlgId, icon: Zap, name: "Deutsch-Jozsa", color: "#06FFA5",
    complexity: { classical: "O(2^(n-1)+1)", quantum: "O(1) queries" },
    description: "Determines if a function is constant or balanced in a single query.",
    steps: ["Initialize |0⟩…|0⟩|1⟩", "Apply Hadamard to all", "Apply oracle Uf", "Apply Hadamard again", "Measure — all 0s = constant"],
  },
  {
    id: "qft" as AlgId, icon: Waves, name: "Quantum Fourier Transform", color: "#f59e0b",
    complexity: { classical: "O(N log N)", quantum: "O(n²)" },
    description: "Exponentially faster Fourier transform, backbone of Shor's and phase estimation.",
    steps: ["Apply Hadamard", "Apply controlled phase rotations", "Repeat for each qubit", "Apply SWAP gates", "Output: frequency domain state"],
  },
];

const COLORS = ["#00D4FF","#7B2FBE","#06FFA5","#f59e0b","#f87171","#818cf8","#34d399","#fb923c"];

export default function AlgorithmsPage() {
  const [selected, setSelected] = useState<AlgId>("grover");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  // Grover params
  const [groverN, setGroverN] = useState(3);
  const [groverTarget, setGroverTarget] = useState(5);
  // DJ params
  const [djOracle, setDjOracle] = useState("balanced");
  // QFT params
  const [qftN, setQftN] = useState(3);
  const [qftInput, setQftInput] = useState(0);
  // Teleport params
  const [teleState, setTeleState] = useState("plus");

  const alg = ALGORITHMS.find((a) => a.id === selected)!;

  const runAlgorithm = async () => {
    setLoading(true);
    setResult(null);
    try {
      let res;
      if (selected === "grover") res = await algorithmService.runGrover(groverN, groverTarget);
      else if (selected === "teleportation") res = await algorithmService.runTeleportation(teleState);
      else if (selected === "deutsch-jozsa") res = await algorithmService.runDeutschJozsa(djOracle, 3);
      else if (selected === "qft") res = await algorithmService.runQFT(qftN, qftInput);
      setResult(res);
      toast.success("Algorithm executed!");
    } catch { toast.error("Execution failed"); }
    finally { setLoading(false); }
  };

  const chartData = result?.probabilities
  ? Object.entries(result.probabilities as Record<string, number>)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 8)
      .map(([state, probability]) => ({
        state: `|${state}⟩`,
        probability: Number((probability * 100).toFixed(2)),
      }))
  : [];

  return (
    <AppShell>
      <PageHeader title="Quantum Algorithm Explorer" subtitle="Understand and run famous quantum algorithms interactively" />

      {/* Algorithm selector */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {ALGORITHMS.map((alg) => (
          <motion.button key={alg.id} onClick={() => { setSelected(alg.id); setResult(null); }}
            whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className={`p-4 rounded-xl border text-left transition-all ${
              selected === alg.id
                ? "border-opacity-60 bg-opacity-10"
                : "border-white/10 hover:border-white/20"
            }`}
            style={selected === alg.id ? { borderColor: `${alg.color}60`, backgroundColor: `${alg.color}10` } : {}}>
            <alg.icon className="w-5 h-5 mb-2" style={{ color: alg.color }} />
            <p className="text-sm font-semibold text-white">{alg.name}</p>
            <p className="text-xs text-muted-foreground mt-1 font-mono">{alg.complexity.quantum}</p>
          </motion.button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Left: Description + Controls */}
        <div className="space-y-4">
          <QuantumCard>
            <div className="h-1 rounded-full mb-4" style={{ background: `linear-gradient(90deg, ${alg.color}, transparent)` }} />
            <h2 className="text-base font-bold text-white mb-2">{alg.name}</h2>
            <p className="text-sm text-muted-foreground mb-4">{alg.description}</p>

            {/* Complexity */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <div className="p-2 rounded-lg bg-red-500/5 border border-red-500/15 text-center">
                <p className="text-xs text-muted-foreground">Classical</p>
                <p className="font-mono text-xs text-red-400 font-bold">{alg.complexity.classical}</p>
              </div>
              <div className="p-2 rounded-lg border text-center" style={{ backgroundColor: `${alg.color}08`, borderColor: `${alg.color}25` }}>
                <p className="text-xs text-muted-foreground">Quantum</p>
                <p className="font-mono text-xs font-bold" style={{ color: alg.color }}>{alg.complexity.quantum}</p>
              </div>
            </div>

            {/* Steps */}
            <div className="space-y-1.5">
              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Steps</p>
              {alg.steps.map((step, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-xs font-mono mt-0.5" style={{ color: alg.color }}>{i + 1}.</span>
                  <span className="text-xs text-muted-foreground">{step}</span>
                </div>
              ))}
            </div>
          </QuantumCard>

          {/* Parameters */}
          <QuantumCard>
            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Parameters</p>
            {selected === "grover" && (
              <div className="space-y-3">
                <div>
                  <label className="text-xs text-muted-foreground">Qubits (search space = 2^n)</label>
                  <input type="number" min={2} max={5} value={groverN} onChange={(e) => setGroverN(+e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white focus:outline-none focus:border-quantum-blue/50" />
                </div>
                <div>
                  <label className="text-xs text-muted-foreground">Target item (0 to {2**groverN - 1})</label>
                  <input type="number" min={0} max={2**groverN - 1} value={groverTarget} onChange={(e) => setGroverTarget(+e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white focus:outline-none focus:border-quantum-blue/50" />
                </div>
              </div>
            )}
            {selected === "teleportation" && (
              <div>
                <label className="text-xs text-muted-foreground">State to teleport</label>
                <select value={teleState} onChange={(e) => setTeleState(e.target.value)}
                  className="w-full mt-1 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white focus:outline-none">
                  <option value="zero">|0⟩ (zero)</option>
                  <option value="one">|1⟩ (one)</option>
                  <option value="plus">|+⟩ (plus = superposition)</option>
                  <option value="minus">|-⟩ (minus)</option>
                </select>
              </div>
            )}
            {selected === "deutsch-jozsa" && (
              <div>
                <label className="text-xs text-muted-foreground">Oracle type</label>
                <select value={djOracle} onChange={(e) => setDjOracle(e.target.value)}
                  className="w-full mt-1 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white focus:outline-none">
                  <option value="constant_zero">Constant (f=0)</option>
                  <option value="constant_one">Constant (f=1)</option>
                  <option value="balanced">Balanced</option>
                </select>
              </div>
            )}
            {selected === "qft" && (
              <div className="space-y-3">
                <div>
                  <label className="text-xs text-muted-foreground">Qubits</label>
                  <input type="number" min={1} max={6} value={qftN} onChange={(e) => setQftN(+e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white focus:outline-none focus:border-quantum-blue/50" />
                </div>
                <div>
                  <label className="text-xs text-muted-foreground">Input state |n⟩</label>
                  <input type="number" min={0} value={qftInput} onChange={(e) => setQftInput(+e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white focus:outline-none focus:border-quantum-blue/50" />
                </div>
              </div>
            )}

            <button onClick={runAlgorithm} disabled={loading}
              className="w-full mt-4 py-2.5 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all disabled:opacity-60"
              style={{ background: `linear-gradient(135deg, ${alg.color}, ${alg.color}99)`, color: "#050A1A" }}>
              {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Running...</> : <><Zap className="w-4 h-4" /> Run Algorithm</>}
            </button>
          </QuantumCard>
        </div>

        {/* Right: Results */}
        <div className="lg:col-span-2">
          <AnimatePresence mode="wait">
            {result ? (
              <motion.div key="result" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
                {/* Success/Conclusion */}
                {result.result && (
                  <QuantumCard glow>
                    <p className="text-xs text-muted-foreground mb-1">Algorithm Conclusion</p>
                    <p className="text-xl font-bold capitalize" style={{ color: alg.color }}>
                      Function is <strong>{result.result}</strong>
                    </p>
                    {result.is_correct !== undefined && (
                      <p className="text-xs mt-1 text-green-400">Result matches oracle type ✓</p>
                    )}
                  </QuantumCard>
                )}

                {result.target_probability !== undefined && (
                  <QuantumCard glow>
                    <p className="text-xs text-muted-foreground mb-1">Target Found</p>
                    <p className="text-xl font-bold text-quantum-blue">|{result.target}⟩</p>
                    <p className="text-2xl font-black mt-1" style={{ color: alg.color }}>
                      {Math.round(result.target_probability * 100)}%
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">probability after {result.iterations_used} iterations</p>
                    <div className="grid grid-cols-2 gap-2 mt-3 text-center">
                      <div className="p-2 rounded-lg bg-red-500/5 border border-red-500/10">
                        <p className="text-xs text-muted-foreground">Classical</p>
                        <p className="text-xs font-mono text-red-400">{result.classical_complexity}</p>
                      </div>
                      <div className="p-2 rounded-lg" style={{ backgroundColor: `${alg.color}08`, border: `1px solid ${alg.color}25` }}>
                        <p className="text-xs text-muted-foreground">Quantum</p>
                        <p className="text-xs font-mono" style={{ color: alg.color }}>{result.quantum_complexity}</p>
                      </div>
                    </div>
                  </QuantumCard>
                )}

                {/* Histogram */}
                {chartData.length > 0 && (
                  <QuantumCard>
                    <div className="flex items-center gap-2 mb-4">
                      <BarChart2 className="w-4 h-4 text-muted-foreground" />
                      <p className="text-sm font-medium text-white">
                        Measurement Distribution
                      </p>
                    </div>

                    <div className="space-y-3">
                      {chartData.map((item, index) => (
                        <div
                          key={item.state}
                          className="grid grid-cols-[70px_1fr_55px] items-center gap-3"
                        >
                          <span className="text-xs font-mono text-muted-foreground">
                            {item.state}
                          </span>

                          <div className="h-5 rounded bg-white/5 overflow-hidden">
                            <div
                              className="h-full rounded transition-all duration-500"
                              style={{
                                width: `${Math.max(item.probability, 1)}%`,
                                backgroundColor:
                                  index === 0 ? alg.color : `${alg.color}99`,
                              }}
                            />
                          </div>

                          <span
                            className="text-xs font-mono text-right"
                            style={{ color: alg.color }}
                          >
                            {item.probability}%
                          </span>
                        </div>
                      ))}
                    </div>
                  </QuantumCard>
                )}

                {/* Teleportation steps */}
                {result.steps && (
                  <QuantumCard>
                    <p className="text-sm font-medium text-white mb-3">Teleportation Steps</p>
                    <div className="space-y-2">
                      {result.steps.map((step: any, i: number) => (
                        <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                          className="flex items-center gap-3">
                          <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white" style={{ background: alg.color }}>{step.step}</div>
                          <p className="text-xs text-muted-foreground">{step.description}</p>
                        </motion.div>
                      ))}
                    </div>
                  </QuantumCard>
                )}
              </motion.div>
            ) : (
              <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className="glass rounded-xl border border-white/5 flex flex-col items-center justify-center h-80">
                <alg.icon className="w-16 h-16 mb-4 opacity-10" style={{ color: alg.color }} />
                <p className="text-muted-foreground text-sm">Configure parameters and run the algorithm</p>
                <p className="text-xs text-muted-foreground/60 mt-1">Results will appear here</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </AppShell>
  );
}
