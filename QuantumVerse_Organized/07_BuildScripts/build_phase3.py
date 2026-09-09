import os

BASE = "/data/quantumverse/frontend"

files = {}

# ─── NEXT.JS MIDDLEWARE (Route Protection) ─────────────────────────────────
files["middleware.ts"] = '''
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/signup", "/about"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith(p + "/") && p !== "/")) {
    return NextResponse.next();
  }

  // Allow Next.js internals and static files
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.startsWith("/favicon") ||
    pathname.includes(".")
  ) {
    return NextResponse.next();
  }

  // Check auth token in cookie (set on client after login)
  const token = request.cookies.get("qv_token")?.value;

  if (!token && !PUBLIC_PATHS.includes(pathname)) {
    // Redirect unauthenticated users to login
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
'''

# ─── AUTH HOOK ─────────────────────────────────────────────────────────────────
files["src/hooks/useAuth.ts"] = '''
import { useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { authService } from "@/services/authService";
import toast from "react-hot-toast";

export function useAuth() {
  const { user, token, isAuthenticated, setAuth, clearAuth } = useAuthStore();
  const router = useRouter();

  const login = useCallback(
    async (email: string, password: string) => {
      const tokens = await authService.login(email, password);
      // Set cookie for middleware
      document.cookie = `qv_token=${tokens.access_token}; path=/; max-age=${60 * 60 * 24 * 7}`;
      const profile = await authService.getProfile();
      setAuth(profile as any, tokens.access_token);
      toast.success(`Welcome back, ${profile.name}!`);
      router.push("/dashboard");
    },
    [router, setAuth]
  );

  const signup = useCallback(
    async (name: string, email: string, password: string, learning_level: string) => {
      const tokens = await authService.signup(name, email, password, learning_level);
      document.cookie = `qv_token=${tokens.access_token}; path=/; max-age=${60 * 60 * 24 * 7}`;
      const profile = await authService.getProfile();
      setAuth(profile as any, tokens.access_token);
      toast.success("🚀 Welcome to QuantumVerse AI!");
      router.push("/dashboard");
    },
    [router, setAuth]
  );

  const logout = useCallback(() => {
    document.cookie = "qv_token=; path=/; max-age=0";
    clearAuth();
    router.push("/login");
    toast.success("Signed out successfully");
  }, [router, clearAuth]);

  const refreshProfile = useCallback(async () => {
    try {
      const profile = await authService.getProfile();
      if (token) setAuth(profile as any, token);
    } catch {
      // Silent fail
    }
  }, [token, setAuth]);

  return { user, token, isAuthenticated, login, signup, logout, refreshProfile };
}
'''

# ─── CIRCUIT HOOK ───────────────────────────────────────────────────────────────
files["src/hooks/useCircuit.ts"] = '''
import { useCallback } from "react";
import { useCircuitStore } from "@/stores/circuitStore";
import { simulationService } from "@/services/simulationService";
import { circuitService } from "@/services/circuitService";
import toast from "react-hot-toast";
import type { GateType } from "@/types/circuit";

export function useCircuit() {
  const store = useCircuitStore();

  const runSimulation = useCallback(async () => {
    if (store.operations.length === 0) {
      toast.error("Add some gates before simulating!");
      return;
    }
    store.setIsSimulating(true);
    store.setSimulationResult(null);
    try {
      const result = await simulationService.run(
        store.qubits,
        store.operations,
        1024
      );
      store.setSimulationResult(result);
      if (result.success) {
        toast.success("Simulation complete!");
      } else {
        toast.error(result.error ?? "Simulation failed");
      }
    } catch {
      toast.error("Simulation error — check backend connection");
    } finally {
      store.setIsSimulating(false);
    }
  }, [store]);

  const runStep = useCallback(
    async (stepIndex: number) => {
      store.setIsStepping(true);
      try {
        const result = await simulationService.step(
          store.qubits,
          store.operations,
          stepIndex
        );
        store.setStepResult(result);
        store.setCurrentStep(stepIndex);
      } catch {
        toast.error("Step execution failed");
      } finally {
        store.setIsStepping(false);
      }
    },
    [store]
  );

  const saveCircuit = useCallback(async () => {
    try {
      await circuitService.create({
        name: store.circuitName,
        qubits: store.qubits,
        classical_bits: store.classicalBits,
        circuit_data: { operations: store.operations },
      } as any);
      toast.success("Circuit saved!");
    } catch {
      toast.error("Failed to save circuit");
    }
  }, [store]);

  const maxColumn = store.operations.length > 0
    ? Math.max(...store.operations.map((op) => op.column)) + 2
    : 8;

  return { ...store, runSimulation, runStep, saveCircuit, maxColumn };
}
'''

# ─── QUANTUM LAB COMPONENTS ────────────────────────────────────────────────────
files["src/components/quantum-lab/GatePalette.tsx"] = '''
"use client";
import { motion } from "framer-motion";
import { GATE_CATALOG } from "@/lib/constants";
import type { GateType, GateInfo } from "@/types/circuit";

interface GatePaletteProps {
  onGateSelect: (gate: GateInfo) => void;
  selectedGate: GateInfo | null;
}

const CATEGORIES = [
  { id: "single",      label: "Single Qubit" },
  { id: "rotation",   label: "Rotation" },
  { id: "multi",      label: "Multi-Qubit" },
  { id: "measurement",label: "Measurement" },
];

export function GatePalette({ onGateSelect, selectedGate }: GatePaletteProps) {
  return (
    <div className="w-52 glass border-r border-quantum-blue/10 p-3 overflow-y-auto flex-shrink-0">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-widest mb-4 px-1">Gate Palette</p>
      {CATEGORIES.map((cat) => {
        const gates = GATE_CATALOG.filter((g) => g.category === cat.id);
        if (!gates.length) return null;
        return (
          <div key={cat.id} className="mb-5">
            <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-2 px-1">{cat.label}</p>
            <div className="grid grid-cols-2 gap-1.5">
              {gates.map((gate) => (
                <motion.button
                  key={gate.type}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => onGateSelect(gate)}
                  title={gate.description}
                  className={`relative flex flex-col items-center justify-center px-2 py-2.5 rounded-lg border text-xs font-bold font-mono transition-all ${
                    selectedGate?.type === gate.type
                      ? "border-quantum-blue/60 bg-quantum-blue/20 text-quantum-blue"
                      : "border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/10"
                  }`}
                  style={selectedGate?.type === gate.type ? {} : { color: gate.color }}
                >
                  <span className="text-sm" style={{ color: gate.color }}>{gate.label}</span>
                  <span className="text-[9px] text-muted-foreground mt-0.5 truncate w-full text-center">{gate.description.split("—")[0].trim()}</span>
                  {selectedGate?.type === gate.type && (
                    <div className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-quantum-blue" />
                  )}
                </motion.button>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
'''

files["src/components/quantum-lab/GateBlock.tsx"] = '''
"use client";
import { motion } from "framer-motion";
import { X } from "lucide-react";
import { GATE_CATALOG } from "@/lib/constants";
import type { GateOperation } from "@/types/circuit";

interface GateBlockProps {
  operation: GateOperation;
  onRemove: (id: string) => void;
}

export function GateBlock({ operation, onRemove }: GateBlockProps) {
  const gateInfo = GATE_CATALOG.find((g) => g.type === operation.gate);
  const color = gateInfo?.color ?? "#64748b";

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      className="relative group w-10 h-10 rounded-lg border flex items-center justify-center font-mono font-bold text-sm cursor-pointer transition-all hover:scale-110"
      style={{
        borderColor: `${color}60`,
        backgroundColor: `${color}15`,
        color,
        boxShadow: `0 0 8px ${color}30`,
      }}
    >
      {operation.gate === "MEASURE" ? "📏" : operation.gate.length <= 3 ? operation.gate : operation.gate.slice(0, 3)}
      <button
        onClick={(e) => { e.stopPropagation(); onRemove(operation.id); }}
        className="absolute -top-2 -right-2 w-4 h-4 rounded-full bg-red-500/80 text-white opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
      >
        <X className="w-2.5 h-2.5" />
      </button>
    </motion.div>
  );
}
'''

files["src/components/quantum-lab/CircuitCanvas.tsx"] = '''
"use client";
import { AnimatePresence } from "framer-motion";
import { GateBlock } from "./GateBlock";
import type { GateOperation } from "@/types/circuit";
import type { GateInfo } from "@/types/circuit";

interface CircuitCanvasProps {
  qubits: number;
  operations: GateOperation[];
  columns: number;
  selectedGate: GateInfo | null;
  onCellClick: (qubit: number, column: number) => void;
  onRemoveGate: (id: string) => void;
  currentStep: number;
  isStepping: boolean;
}

export function CircuitCanvas({
  qubits,
  operations,
  columns,
  selectedGate,
  onCellClick,
  onRemoveGate,
  currentStep,
  isStepping,
}: CircuitCanvasProps) {
  const getGateAt = (qubit: number, col: number) =>
    operations.find((op) => op.targets.includes(qubit) && op.column === col) ||
    operations.find((op) => op.controls.includes(qubit) && op.column === col);

  return (
    <div className="flex-1 overflow-auto p-6">
      <div className="min-w-max">
        {Array.from({ length: qubits }).map((_, qubit) => (
          <div key={qubit} className="flex items-center mb-4">
            {/* Qubit label */}
            <div className="w-14 flex-shrink-0 text-right pr-3">
              <span className="text-xs font-mono text-quantum-blue">q{qubit}</span>
              <span className="block text-[9px] text-muted-foreground font-mono">|0⟩</span>
            </div>

            {/* Wire + cells */}
            <div className="flex items-center">
              {Array.from({ length: columns }).map((_, col) => {
                const gate = getGateAt(qubit, col);
                const isControl = operations.some(
                  (op) => op.controls.includes(qubit) && op.column === col
                );
                const isActiveStep = isStepping && col <= currentStep;

                return (
                  <div key={col} className="relative flex items-center">
                    {/* Wire segment */}
                    <div
                      className="h-px w-12"
                      style={{
                        background: isActiveStep
                          ? "linear-gradient(90deg, #00D4FF, #06FFA5)"
                          : "rgba(0,212,255,0.2)",
                        boxShadow: isActiveStep ? "0 0 6px rgba(0,212,255,0.4)" : undefined,
                      }}
                    />

                    {/* Cell */}
                    <div
                      className="relative flex items-center justify-center w-12 h-12 cursor-pointer"
                      onClick={() => !gate && onCellClick(qubit, col)}
                    >
                      {gate ? (
                        isControl ? (
                          // Control dot
                          <div className="w-3 h-3 rounded-full bg-quantum-blue border-2 border-quantum-blue shadow-[0_0_8px_rgba(0,212,255,0.6)]" />
                        ) : (
                          <AnimatePresence>
                            <GateBlock
                              key={gate.id}
                              operation={gate}
                              onRemove={onRemoveGate}
                            />
                          </AnimatePresence>
                        )
                      ) : (
                        // Empty cell hover effect
                        <div className={`w-10 h-10 rounded-lg border border-dashed transition-all ${
                          selectedGate
                            ? "border-quantum-blue/30 hover:border-quantum-blue/70 hover:bg-quantum-blue/5"
                            : "border-transparent"
                        }`} />
                      )}
                    </div>
                  </div>
                );
              })}

              {/* End wire */}
              <div className="h-px w-8 bg-quantum-blue/20" />
              <div className="w-2 h-2 rounded-full bg-quantum-blue/40" />
            </div>
          </div>
        ))}

        {/* Column step indicators */}
        <div className="flex items-center ml-14">
          {Array.from({ length: columns }).map((_, col) => (
            <div key={col} className="flex items-center">
              <div className="w-12" />
              <div className="w-12 text-center">
                <span className={`text-[9px] font-mono ${
                  isStepping && col === currentStep ? "text-quantum-blue" : "text-muted-foreground/40"
                }`}>t{col}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
'''

files["src/components/quantum-lab/SimulationPanel.tsx"] = '''
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
              <XAxis dataKey="state" tick={{ fill: "#94a3b8", fontSize: 10, fontFamily: "monospace" }} axisLine={false} tickLine={false} />
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
'''

files["src/components/quantum-lab/StepExecutor.tsx"] = '''
"use client";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, ChevronLeft, Play, RotateCcw } from "lucide-react";
import type { StepResult } from "@/types/circuit";

interface StepExecutorProps {
  maxStep: number;
  currentStep: number;
  stepResult: StepResult | null;
  isStepping: boolean;
  onStep: (step: number) => void;
  onReset: () => void;
}

export function StepExecutor({ maxStep, currentStep, stepResult, isStepping, onStep, onReset }: StepExecutorProps) {
  return (
    <div className="p-5 space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Step-by-Step</p>
        <div className="flex items-center gap-2">
          <button onClick={onReset} className="p-1.5 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors">
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0 || isStepping}
            className="p-1.5 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors disabled:opacity-40"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-xs font-mono text-muted-foreground px-2">
            {currentStep + 1} / {maxStep + 1}
          </span>
          <button
            onClick={() => onStep(Math.min(maxStep, currentStep + 1))}
            disabled={currentStep >= maxStep || isStepping}
            className="p-1.5 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors disabled:opacity-40"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-muted rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full"
          animate={{ width: `${((currentStep) / Math.max(maxStep, 1)) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>

      {/* Step result */}
      <AnimatePresence mode="wait">
        {stepResult ? (
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-3"
          >
            {/* Gate applied */}
            <div className="flex items-center gap-3 p-3 rounded-xl bg-quantum-blue/5 border border-quantum-blue/15">
              <div className="w-9 h-9 rounded-lg bg-quantum-blue/10 border border-quantum-blue/30 flex items-center justify-center font-mono font-bold text-quantum-blue text-sm">
                {stepResult.gate_applied}
              </div>
              <div>
                <p className="text-xs font-medium text-white">Gate Applied</p>
                <p className="text-[10px] text-muted-foreground">{stepResult.gate_applied} gate at step {currentStep}</p>
              </div>
            </div>

            {/* Explanation */}
            <div className="p-3 rounded-xl bg-white/3 border border-white/5">
              <p className="text-xs text-muted-foreground leading-relaxed">{stepResult.explanation}</p>
            </div>

            {/* State */}
            <div>
              <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-2">Quantum State</p>
              <div className="p-3 rounded-xl bg-quantum-dark/60 border border-quantum-blue/10 font-mono text-xs text-quantum-cyan break-all">
                {stepResult.state_description || "|0⟩"}
              </div>
            </div>

            {/* Probabilities */}
            <div>
              <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-2">Measurement Probabilities</p>
              <div className="space-y-1.5">
                {Object.entries(stepResult.probabilities)
                  .sort(([, a], [, b]) => b - a)
                  .slice(0, 6)
                  .map(([state, prob]) => (
                    <div key={state} className="flex items-center gap-2">
                      <span className="font-mono text-[10px] text-quantum-blue w-12 text-right">|{state}⟩</span>
                      <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                        <motion.div
                          animate={{ width: `${Math.round((prob as number) * 100)}%` }}
                          className="h-full bg-quantum-blue/60 rounded-full"
                        />
                      </div>
                      <span className="text-[10px] font-mono text-muted-foreground w-8">{Math.round((prob as number) * 100)}%</span>
                    </div>
                  ))}
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-6"
          >
            <Play className="w-8 h-8 text-muted-foreground/30 mx-auto mb-2" />
            <p className="text-xs text-muted-foreground">Click Next Step to execute gates one by one</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
'''

# ─── FULL QUANTUM LAB PAGE ─────────────────────────────────────────────────────────
files["src/app/quantum-lab/page.tsx"] = '''
"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  Play, Pause, RotateCcw, Save, Minus, Plus, Undo2, Redo2,
  ChevronRight, FlaskConical, Footprints, BarChart3
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { GatePalette } from "@/components/quantum-lab/GatePalette";
import { CircuitCanvas } from "@/components/quantum-lab/CircuitCanvas";
import { SimulationPanel } from "@/components/quantum-lab/SimulationPanel";
import { StepExecutor } from "@/components/quantum-lab/StepExecutor";
import { useCircuit } from "@/hooks/useCircuit";
import type { GateInfo } from "@/types/circuit";
import { cn } from "@/lib/utils";

const TEMPLATES = [
  { name: "Bell State",    ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"CNOT",targets:[1],controls:[0],column:1},{gate:"MEASURE",targets:[0,1],controls:[],column:2}], qubits: 2, cb: 2 },
  { name: "Superposition", ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"MEASURE",targets:[0],controls:[],column:1}], qubits: 1, cb: 1 },
  { name: "GHZ State",     ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"CNOT",targets:[1],controls:[0],column:1},{gate:"CNOT",targets:[2],controls:[0],column:2},{gate:"MEASURE",targets:[0,1,2],controls:[],column:3}], qubits: 3, cb: 3 },
  { name: "Phase Kickback",ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"X",targets:[1],controls:[],column:0},{gate:"CZ",targets:[1],controls:[0],column:1},{gate:"H",targets:[0],controls:[],column:2}], qubits: 2, cb: 0 },
];

type PanelMode = "results" | "steps";

export default function QuantumLabPage() {
  const [
    selectedGate, setSelectedGate
  ] = useState<GateInfo | null>(null);
  const [panelMode, setPanelMode] = useState<PanelMode>("results");
  const circuit = useCircuit();

  const handleCellClick = (qubit: number, column: number) => {
    if (!selectedGate) return;
    const controls: number[] = [];
    circuit.addGate(selectedGate.type, [qubit], controls, column);
  };

  const handleLoadTemplate = (tpl: typeof TEMPLATES[0]) => {
    circuit.clearCircuit();
    circuit.setQubits(tpl.qubits);
    circuit.setClassicalBits(tpl.cb);
    tpl.ops.forEach((op) => {
      circuit.addGate(op.gate as any, op.targets, op.controls, op.column);
    });
    circuit.setCircuitName(tpl.name);
  };

  const maxStep = Math.max(...circuit.operations.map((o) => o.column), 0);

  return (
    <AppShell>
      {/* Top toolbar */}
      <div className="flex items-center gap-3 mb-4 flex-wrap">
        {/* Circuit name */}
        <input
          value={circuit.circuitName}
          onChange={(e) => circuit.setCircuitName(e.target.value)}
          className="px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white font-medium focus:outline-none focus:border-quantum-blue/50 w-48"
        />

        {/* Qubits */}
        <div className="flex items-center gap-1.5 glass px-3 py-1.5 rounded-lg border border-white/5">
          <span className="text-xs text-muted-foreground">Qubits:</span>
          <button onClick={() => circuit.setQubits(circuit.qubits - 1)} disabled={circuit.qubits <= 1} className="w-5 h-5 rounded flex items-center justify-center hover:bg-white/10 disabled:opacity-40">
            <Minus className="w-3 h-3" />
          </button>
          <span className="text-sm font-mono text-quantum-blue w-4 text-center">{circuit.qubits}</span>
          <button onClick={() => circuit.setQubits(circuit.qubits + 1)} disabled={circuit.qubits >= 6} className="w-5 h-5 rounded flex items-center justify-center hover:bg-white/10 disabled:opacity-40">
            <Plus className="w-3 h-3" />
          </button>
        </div>

        {/* History controls */}
        <div className="flex gap-1">
          <button onClick={circuit.undo} className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors" title="Undo">
            <Undo2 className="w-4 h-4" />
          </button>
          <button onClick={circuit.redo} className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors" title="Redo">
            <Redo2 className="w-4 h-4" />
          </button>
          <button onClick={circuit.clearCircuit} className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-red-400 transition-colors" title="Clear">
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* Templates */}
        <div className="flex gap-1.5">
          {TEMPLATES.map((tpl) => (
            <button key={tpl.name} onClick={() => handleLoadTemplate(tpl)}
              className="px-3 py-1.5 rounded-lg text-xs border border-white/10 text-muted-foreground hover:border-quantum-blue/30 hover:text-white transition-all">
              {tpl.name}
            </button>
          ))}
        </div>

        <div className="ml-auto flex gap-2">
          <button onClick={circuit.saveCircuit} className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-white/10 text-xs text-muted-foreground hover:text-white hover:border-white/20 transition-all">
            <Save className="w-3.5 h-3.5" /> Save
          </button>
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={circuit.runSimulation}
            disabled={circuit.isSimulating}
            className="flex items-center gap-2 px-5 py-2 rounded-lg bg-quantum-blue text-quantum-dark font-bold text-sm hover:opacity-90 transition-opacity disabled:opacity-60"
          >
            {circuit.isSimulating ? (
              <><div className="w-3.5 h-3.5 border-2 border-quantum-dark/30 border-t-quantum-dark rounded-full animate-spin" /> Simulating...</>
            ) : (
              <><Play className="w-3.5 h-3.5" /> Run Circuit</>
            )}
          </motion.button>
        </div>
      </div>

      {/* Main layout */}
      <div className="flex gap-0 h-[calc(100vh-13rem)] rounded-xl overflow-hidden border border-white/5 glass">
        {/* Gate Palette */}
        <GatePalette selectedGate={selectedGate} onGateSelect={(g) => setSelectedGate((prev) => prev?.type === g.type ? null : g)} />

        {/* Circuit Canvas */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Canvas header */}
          <div className="px-5 py-3 border-b border-white/5 flex items-center gap-4">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <FlaskConical className="w-3.5 h-3.5" />
              <span>{circuit.operations.length} gates</span>
            </div>
            {selectedGate ? (
              <span className="text-xs text-quantum-blue">
                Click any empty cell to place <strong>{selectedGate.label}</strong> gate
              </span>
            ) : (
              <span className="text-xs text-muted-foreground">Select a gate from the palette, then click a cell</span>
            )}
          </div>

          <CircuitCanvas
            qubits={circuit.qubits}
            operations={circuit.operations}
            columns={circuit.maxColumn}
            selectedGate={selectedGate}
            onCellClick={handleCellClick}
            onRemoveGate={circuit.removeGate}
            currentStep={circuit.currentStep}
            isStepping={circuit.isStepping}
          />
        </div>

        {/* Results Panel */}
        <div className="w-72 border-l border-white/5 flex flex-col overflow-hidden">
          {/* Panel tabs */}
          <div className="flex border-b border-white/5">
            {([
              { id: "results", label: "Results",    icon: BarChart3 },
              { id: "steps",   label: "Step Mode",  icon: Footprints },
            ] as const).map((tab) => (
              <button key={tab.id} onClick={() => setPanelMode(tab.id)}
                className={cn(
                  "flex-1 flex items-center justify-center gap-1.5 py-3 text-xs transition-all border-b-2",
                  panelMode === tab.id
                    ? "border-quantum-blue text-quantum-blue"
                    : "border-transparent text-muted-foreground hover:text-white"
                )}>
                <tab.icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto">
            {panelMode === "results" ? (
              <SimulationPanel result={circuit.simulationResult} />
            ) : (
              <StepExecutor
                maxStep={maxStep}
                currentStep={circuit.currentStep}
                stepResult={circuit.stepResult}
                isStepping={circuit.isStepping}
                onStep={(step) => circuit.runStep(step)}
                onReset={() => { circuit.setCurrentStep(0); circuit.setStepResult(null); }}
              />
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
'''

# ─── AI TUTOR PAGE ─────────────────────────────────────────────────────────────────
files["src/app/ai-tutor/page.tsx"] = '''
"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Atom, Loader2, Plus } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { aiService } from "@/services/aiService";
import { useAuthStore } from "@/stores/authStore";
import toast from "react-hot-toast";

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
  "Explain Grover\'s algorithm simply",
  "What is quantum decoherence?",
];

const DIFFICULTY_LABELS = [
  { value: "beginner",     label: "Beginner",    color: "text-green-400 border-green-400/30 bg-green-400/5" },
  { value: "intermediate", label: "Intermediate", color: "text-yellow-400 border-yellow-400/30 bg-yellow-400/5" },
  { value: "advanced",     label: "Advanced",     color: "text-red-400 border-red-400/30 bg-red-400/5" },
];

export default function AITutorPage() {
  const { user } = useAuthStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [convId, setConvId] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState(user?.learning_level ?? "beginner");
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
'''

# ─── LEARN PAGE ───────────────────────────────────────────────────────────────────
files["src/app/learn/page.tsx"] = '''
"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, CheckCircle2, Lock, ChevronRight, Clock, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import api from "@/lib/api";
import type { LearningModule } from "@/types/learning";

const LEVEL_COLORS = ["from-blue-500 to-cyan-500", "from-purple-500 to-pink-500", "from-green-500 to-emerald-500", "from-orange-500 to-yellow-500"];
const LEVEL_ICONS = ["atom", "cpu", "link", "zap"];

export default function LearnPage() {
  const [modules, setModules] = useState<LearningModule[]>([]);
  const [progress, setProgress] = useState<{ completed: string[] }>({ completed: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/learning/modules").then((r) => r.data.modules),
      api.get("/learning/progress").then((r) => r.data).catch(() => ({ completed: [] })),
    ]).then(([mods, prog]) => {
      setModules(mods);
      setProgress(prog);
    }).finally(() => setLoading(false));
  }, []);

  const getModuleProgress = (module: LearningModule) => {
    if (!module.lesson_count) return 0;
    return 0; // Will be computed per lesson in detail view
  };

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader title="Learning Path" subtitle="Master quantum computing step by step" />

      {/* Level progression */}
      <div className="flex items-center gap-2 mb-8 overflow-x-auto pb-2">
        {["Fundamentals", "Quantum Gates", "Multi-Qubit", "Algorithms"].map((lvl, i) => (
          <div key={lvl} className="flex items-center gap-2 flex-shrink-0">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium bg-gradient-to-r ${LEVEL_COLORS[i]} text-white`}>
              <span>Level {i + 1}</span>
              <span className="opacity-80">{lvl}</span>
            </div>
            {i < 3 && <ChevronRight className="w-4 h-4 text-muted-foreground" />}
          </div>
        ))}
      </div>

      {/* Modules grid */}
      {modules.length === 0 ? (
        <div className="glass rounded-xl border border-white/5 p-12 text-center">
          <BookOpen className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
          <p className="text-muted-foreground">No modules found. Make sure the backend is running and seeded.</p>
          <p className="text-xs text-muted-foreground/60 mt-2">Run: <code className="font-mono bg-white/5 px-2 py-0.5 rounded">python -m app.database.seed</code></p>
        </div>
      ) : (
        <div className="space-y-6">
          {[1, 2, 3, 4].map((level) => {
            const levelModules = modules.filter((m) => m.level === level);
            if (!levelModules.length) return null;
            return (
              <div key={level}>
                <div className="flex items-center gap-3 mb-4">
                  <div className={`h-px flex-1 bg-gradient-to-r ${LEVEL_COLORS[level - 1]} opacity-30`} />
                  <span className={`text-xs font-semibold uppercase tracking-widest bg-gradient-to-r ${LEVEL_COLORS[level - 1]} bg-clip-text text-transparent`}>
                    Level {level}
                  </span>
                  <div className={`h-px flex-1 bg-gradient-to-l ${LEVEL_COLORS[level - 1]} opacity-30`} />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {levelModules.map((mod, i) => (
                    <motion.div
                      key={mod.id}
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="glass rounded-xl border border-white/5 hover:border-quantum-blue/20 transition-all hover:-translate-y-1 p-5 cursor-pointer group"
                    >
                      <div className={`h-1 rounded-full bg-gradient-to-r ${LEVEL_COLORS[level - 1]} mb-4`} />
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold text-white text-sm group-hover:text-quantum-blue transition-colors">{mod.title}</h3>
                          <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{mod.description}</p>
                        </div>
                        <ChevronRight className="w-4 h-4 text-muted-foreground/40 group-hover:text-quantum-blue transition-colors flex-shrink-0 ml-2" />
                      </div>
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <BookOpen className="w-3 h-3" /> {mod.lesson_count} lessons
                        </span>
                        <span className="flex items-center gap-1">
                          <Zap className="w-3 h-3 text-yellow-400" />
                          {mod.lesson_count * 50} XP
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </AppShell>
  );
}
'''

# ─── ALGORITHMS PAGE ────────────────────────────────────────────────────────────
files["src/app/algorithms/page.tsx"] = '''
"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Zap, Search, Radio, Waves, Loader2, BarChart2 } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { algorithmService } from "@/services/algorithmService";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import toast from "react-hot-toast";

type AlgId = "grover" | "teleportation" | "deutsch-jozsa" | "qft";

const ALGORITHMS = [
  {
    id: "grover" as AlgId, icon: Search, name: "Grover\'s Search", color: "#00D4FF",
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
    description: "Exponentially faster Fourier transform, backbone of Shor\'s and phase estimation.",
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
        .map(([state, prob]) => ({ state: `|${state}⟩`, probability: Math.round(prob * 100) }))
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
                      <p className="text-sm font-medium text-white">Measurement Distribution</p>
                    </div>
                    <div className="h-48">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData}>
                          <XAxis dataKey="state" tick={{ fill: "#94a3b8", fontSize: 10, fontFamily: "monospace" }} axisLine={false} tickLine={false} />
                          <YAxis hide />
                          <Tooltip contentStyle={{ background: "#0D1F3C", border: "1px solid rgba(0,212,255,0.2)", borderRadius: "8px", color: "#e2e8f0", fontSize: "11px" }} />
                          <Bar dataKey="probability" radius={[4, 4, 0, 0]}>
                            {chartData.map((_, i) => <Cell key={i} fill={i === 0 ? alg.color : COLORS[i % COLORS.length]} fillOpacity={0.85} />)}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
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
'''

# ─── QUIZ PAGE ──────────────────────────────────────────────────────────────────────
files["src/app/quiz/page.tsx"] = '''
"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Trophy, Clock, CheckCircle2, XCircle, ChevronRight, Zap, Target } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import api from "@/lib/api";
import toast from "react-hot-toast";

type QuizState = "list" | "active" | "result";

export default function QuizPage() {
  const [quizzes, setQuizzes] = useState<any[]>([]);
  const [quiz, setQuiz] = useState<any | null>(null);
  const [state, setState] = useState<QuizState>("list");
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any | null>(null);
  const [startTime, setStartTime] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/quiz/quizzes").then((r) => setQuizzes(r.data.quizzes)).catch(() => {});
  }, []);

  const startQuiz = async (quizId: string) => {
    try {
      const { data } = await api.get(`/quiz/quizzes/${quizId}`);
      setQuiz(data);
      setCurrentQ(0);
      setAnswers({});
      setSelectedOption(null);
      setStartTime(Date.now());
      setState("active");
    } catch { toast.error("Failed to load quiz"); }
  };

  const selectOption = (optId: string) => {
    if (selectedOption) return;
    setSelectedOption(optId);
    const q = quiz.questions[currentQ];
    setAnswers((prev) => ({ ...prev, [q.id]: optId }));
  };

  const nextQuestion = () => {
    setSelectedOption(null);
    if (currentQ < quiz.questions.length - 1) {
      setCurrentQ((p) => p + 1);
    } else {
      submitQuiz();
    }
  };

  const submitQuiz = async () => {
    setLoading(true);
    try {
      const time_taken = Math.round((Date.now() - startTime) / 1000);
      const { data } = await api.post(`/quiz/quizzes/${quiz.id}/submit`, { answers, time_taken });
      setResult(data);
      setState("result");
    } catch { toast.error("Failed to submit quiz"); }
    finally { setLoading(false); }
  };

  if (state === "result" && result) {
    const grade = result.accuracy >= 80 ? "Excellent!" : result.accuracy >= 60 ? "Good Job!" : "Keep Practicing";
    return (
      <AppShell>
        <PageHeader title="Quiz Results" />
        <div className="max-w-2xl mx-auto">
          <QuantumCard glow className="text-center mb-6">
            <div className="text-5xl mb-3">{result.accuracy >= 80 ? "🏆" : result.accuracy >= 60 ? "🌟" : "📚"}</div>
            <h2 className="text-2xl font-bold text-white mb-1">{grade}</h2>
            <p className="text-4xl font-black text-quantum-blue mt-2">{result.accuracy}%</p>
            <p className="text-muted-foreground text-sm mt-1">{result.score} / {result.total} correct</p>
            <div className="flex items-center justify-center gap-2 mt-4 text-quantum-cyan">
              <Zap className="w-4 h-4" />
              <span className="font-bold">+{result.xp_earned} XP earned</span>
            </div>
          </QuantumCard>

          <div className="space-y-3">
            {result.answers?.map((ans: any, i: number) => (
              <motion.div key={ans.question_id} initial={{ opacity: 0, x: -15 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                className={`p-4 rounded-xl border ${
                  ans.is_correct ? "border-green-500/20 bg-green-500/5" : "border-red-500/20 bg-red-500/5"
                }`}>
                <div className="flex items-start gap-3">
                  {ans.is_correct
                    ? <CheckCircle2 className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    : <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />}
                  <div>
                    <p className="text-sm text-white font-medium">Q{i + 1}</p>
                    {!ans.is_correct && (
                      <p className="text-xs text-muted-foreground mt-1">{ans.explanation}</p>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          <button onClick={() => setState("list")} className="mt-6 w-full py-3 rounded-xl border border-white/10 text-sm text-muted-foreground hover:text-white hover:border-white/20 transition-all">
            Back to Quizzes
          </button>
        </div>
      </AppShell>
    );
  }

  if (state === "active" && quiz) {
    const q = quiz.questions[currentQ];
    const progress = ((currentQ) / quiz.questions.length) * 100;
    const isCorrect = selectedOption === q.correct_answer;

    return (
      <AppShell>
        <div className="max-w-2xl mx-auto">
          {/* Progress */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-muted-foreground">Q{currentQ + 1} of {quiz.questions.length}</span>
            <span className="text-sm font-mono text-quantum-blue">{quiz.title}</span>
          </div>
          <div className="h-1.5 bg-muted rounded-full mb-6 overflow-hidden">
            <motion.div animate={{ width: `${progress}%` }} className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full" />
          </div>

          <AnimatePresence mode="wait">
            <motion.div key={currentQ} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <QuantumCard className="mb-5">
                <p className="text-white font-medium leading-relaxed">{q.question_text}</p>
              </QuantumCard>

              <div className="space-y-3 mb-6">
                {q.options.map((opt: any) => {
                  let variant = "border-white/10 hover:border-white/20";
                  if (selectedOption) {
                    if (opt.id === q.correct_answer) variant = "border-green-500/60 bg-green-500/10";
                    else if (opt.id === selectedOption && !isCorrect) variant = "border-red-500/60 bg-red-500/10";
                  } else if (selectedOption === opt.id) {
                    variant = "border-quantum-blue/60 bg-quantum-blue/10";
                  }
                  return (
                    <motion.button key={opt.id} onClick={() => selectOption(opt.id)} whileTap={{ scale: 0.99 }}
                      className={`w-full text-left p-4 rounded-xl border transition-all ${
                        selectedOption === opt.id && !selectedOption ? "border-quantum-blue/60 bg-quantum-blue/10" : variant
                      } flex items-center gap-3`}>
                      <span className="w-7 h-7 rounded-full border border-current flex items-center justify-center text-xs font-bold flex-shrink-0 text-muted-foreground">{opt.id.toUpperCase()}</span>
                      <span className="text-sm text-white">{opt.text}</span>
                      {selectedOption && opt.id === q.correct_answer && <CheckCircle2 className="w-4 h-4 text-green-400 ml-auto" />}
                      {selectedOption === opt.id && !isCorrect && opt.id !== q.correct_answer && <XCircle className="w-4 h-4 text-red-400 ml-auto" />}
                    </motion.button>
                  );
                })}
              </div>

              {selectedOption && (
                <motion.button initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  onClick={nextQuestion} disabled={loading}
                  className="w-full py-3 rounded-xl bg-quantum-blue text-quantum-dark font-bold flex items-center justify-center gap-2">
                  {currentQ < quiz.questions.length - 1 ? <><ChevronRight className="w-4 h-4" /> Next Question</> : loading ? "Submitting..." : <><Trophy className="w-4 h-4" /> Finish Quiz</>}
                </motion.button>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader title="Quiz Arena" subtitle="Test your quantum knowledge and earn XP" />
      {quizzes.length === 0 ? (
        <div className="glass rounded-xl border border-white/5 p-12 text-center">
          <Trophy className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
          <p className="text-muted-foreground">No quizzes found. Seed the database to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quizzes.map((q, i) => (
            <motion.div key={q.id} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
              className="glass rounded-xl border border-white/5 hover:border-quantum-blue/20 transition-all p-5">
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-white text-sm">{q.title}</h3>
                <span className={`text-xs px-2 py-0.5 rounded-full border ${
                  q.difficulty === "easy" ? "text-green-400 border-green-400/30 bg-green-400/5" :
                  q.difficulty === "medium" ? "text-yellow-400 border-yellow-400/30 bg-yellow-400/5" :
                  "text-red-400 border-red-400/30 bg-red-400/5"
                }`}>{q.difficulty}</span>
              </div>
              <div className="flex items-center gap-4 text-xs text-muted-foreground mb-4">
                <span className="flex items-center gap-1"><Target className="w-3 h-3" /> {q.question_count} questions</span>
                <span className="flex items-center gap-1 text-quantum-cyan"><Zap className="w-3 h-3" /> {q.xp_reward} XP</span>
              </div>
              <button onClick={() => startQuiz(q.id)}
                className="w-full py-2 rounded-lg bg-quantum-blue/10 border border-quantum-blue/20 text-quantum-blue text-sm font-medium hover:bg-quantum-blue/20 transition-all">
                Start Quiz
              </button>
            </motion.div>
          ))}
        </div>
      )}
    </AppShell>
  );
}
'''

# ─── FULL PROFILE PAGE ────────────────────────────────────────────────────────────
files["src/app/profile/page.tsx"] = '''
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
'''

# ─── ACHIEVEMENTS PAGE ───────────────────────────────────────────────────────────
files["src/app/achievements/page.tsx"] = '''
"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Star, Lock, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import api from "@/lib/api";

const BADGE_COLORS: Record<string, string> = {
  blue: "from-blue-500 to-cyan-500",
  purple: "from-purple-500 to-pink-500",
  cyan: "from-cyan-500 to-emerald-500",
  gold: "from-yellow-400 to-orange-400",
  green: "from-green-500 to-emerald-400",
  orange: "from-orange-500 to-yellow-500",
  pink: "from-pink-500 to-rose-500",
};

export default function AchievementsPage() {
  const [achievements, setAchievements] = useState<any[]>([]);
  const [unlocked, setUnlocked] = useState<string[]>([]);

  useEffect(() => {
    Promise.all([
      api.get("/achievements").then((r) => r.data.achievements),
      api.get("/achievements/user").then((r) => r.data.unlocked.map((u: any) => u.achievement_id)).catch(() => []),
    ]).then(([achs, unlockedIds]) => {
      setAchievements(achs);
      setUnlocked(unlockedIds);
    });
  }, []);

  const unlockedCount = achievements.filter((a) => unlocked.includes(a.id)).length;

  return (
    <AppShell>
      <PageHeader title="Achievements" subtitle={`${unlockedCount} / ${achievements.length} unlocked`} />

      <div className="mb-6 glass rounded-xl border border-white/5 p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-muted-foreground">Overall Progress</span>
          <span className="text-sm font-mono text-quantum-blue">{unlockedCount}/{achievements.length}</span>
        </div>
        <div className="h-2 bg-muted rounded-full overflow-hidden">
          <motion.div
            animate={{ width: achievements.length ? `${(unlockedCount / achievements.length) * 100}%` : "0%" }}
            className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {achievements.map((ach, i) => {
          const isUnlocked = unlocked.includes(ach.id);
          const gradient = BADGE_COLORS[ach.badge_color] ?? "from-slate-500 to-slate-600";
          return (
            <motion.div key={ach.id} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.05 }}
              className={`glass rounded-xl border p-5 text-center transition-all ${
                isUnlocked ? "border-quantum-blue/20 hover:border-quantum-blue/40" : "border-white/5 opacity-60"
              }`}>
              <div className={`w-16 h-16 rounded-2xl mx-auto mb-3 flex items-center justify-center bg-gradient-to-br ${gradient} ${
                isUnlocked ? "shadow-lg" : "grayscale opacity-50"
              }`}>
                {isUnlocked
                  ? <Star className="w-8 h-8 text-white" />
                  : <Lock className="w-8 h-8 text-white/60" />}
              </div>
              <h3 className="text-sm font-bold text-white mb-1">{ach.name}</h3>
              <p className="text-xs text-muted-foreground line-clamp-2 mb-2">{ach.description}</p>
              <div className="flex items-center justify-center gap-1 text-xs text-quantum-cyan">
                <Zap className="w-3 h-3" />
                <span>{ach.xp_reward} XP</span>
              </div>
              {isUnlocked && (
                <span className="mt-2 inline-block text-[10px] text-green-400 bg-green-400/10 border border-green-400/20 px-2 py-0.5 rounded-full">Unlocked ✓</span>
              )}
            </motion.div>
          );
        })}
      </div>
    </AppShell>
  );
}
'''

# ─── PROGRESS PAGE ─────────────────────────────────────────────────────────────
files["src/app/progress/page.tsx"] = '''
"use client";
import { useAuthStore } from "@/stores/authStore";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { BookOpen, FlaskConical, Trophy, Zap, Clock, TrendingUp } from "lucide-react";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from "recharts";

const WEEKLY_DATA = [
  { day: "Mon", minutes: 30 }, { day: "Tue", minutes: 45 }, { day: "Wed", minutes: 20 },
  { day: "Thu", minutes: 60 }, { day: "Fri", minutes: 35 }, { day: "Sat", minutes: 50 }, { day: "Sun", minutes: 10 },
];

export default function ProgressPage() {
  const { user } = useAuthStore();

  const radarData = [
    { topic: "Fundamentals", score: 80 },
    { topic: "Gates",         score: 60 },
    { topic: "Multi-Qubit",  score: 40 },
    { topic: "Algorithms",   score: 20 },
    { topic: "Quiz",          score: user?.statistics?.quiz_accuracy ?? 0 },
  ];

  return (
    <AppShell>
      <PageHeader title="Learning Progress" subtitle="Your quantum mastery journey" />

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[
          { icon: BookOpen,    label: "Lessons Done",  value: user?.statistics?.total_lessons ?? 0, color: "text-blue-400" },
          { icon: FlaskConical,label: "Circuits Built", value: user?.statistics?.total_circuits ?? 0, color: "text-purple-400" },
          { icon: Trophy,      label: "Quizzes",        value: user?.statistics?.total_quizzes ?? 0,  color: "text-yellow-400" },
          { icon: Zap,         label: "Total XP",       value: user?.xp ?? 0,                          color: "text-cyan-400" },
        ].map((s) => (
          <QuantumCard key={s.label}>
            <s.icon className={`w-5 h-5 mb-2 ${s.color}`} />
            <p className="text-xl font-bold text-white">{s.value}</p>
            <p className="text-xs text-muted-foreground">{s.label}</p>
          </QuantumCard>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Weekly chart */}
        <QuantumCard>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-4 h-4 text-quantum-blue" />
            <p className="text-sm font-medium text-white">Weekly Activity (minutes)</p>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={WEEKLY_DATA}>
                <XAxis dataKey="day" tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis hide />
                <Tooltip contentStyle={{ background: "#0D1F3C", border: "1px solid rgba(0,212,255,0.2)", borderRadius: "8px", color: "#e2e8f0", fontSize: "11px" }} />
                <Bar dataKey="minutes" radius={[4,4,0,0]}>
                  {WEEKLY_DATA.map((_, i) => <Cell key={i} fill={i === 3 ? "#00D4FF" : "#00D4FF55"} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </QuantumCard>

        {/* Skill Radar */}
        <QuantumCard>
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-4 h-4 text-quantum-purple" />
            <p className="text-sm font-medium text-white">Skill Radar</p>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.05)" />
                <PolarAngleAxis dataKey="topic" tick={{ fill: "#64748b", fontSize: 10 }} />
                <Radar dataKey="score" fill="rgba(0,212,255,0.2)" stroke="#00D4FF" strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </QuantumCard>
      </div>
    </AppShell>
  );
}
'''

# ─── SETTINGS PAGE ─────────────────────────────────────────────────────────────────
files["src/app/settings/page.tsx"] = '''
"use client";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { Atom, Moon, Bell, Shield, ExternalLink } from "lucide-react";

const SECTIONS = [
  {
    title: "Appearance",
    icon: Moon,
    items: [
      { label: "Theme", description: "Dark quantum mode", value: "Dark (Default)", type: "static" },
      { label: "Animations", description: "Reduce motion for accessibility", type: "toggle", default: true },
    ],
  },
  {
    title: "Notifications",
    icon: Bell,
    items: [
      { label: "Daily Reminder", description: "Get reminded to continue learning", type: "toggle", default: true },
      { label: "Achievement Alerts", description: "Notify when you earn a badge", type: "toggle", default: true },
    ],
  },
  {
    title: "Privacy & Security",
    icon: Shield,
    items: [
      { label: "Change Password", description: "Update your account password", type: "button" },
      { label: "Delete Account", description: "Permanently remove your account", type: "button-danger" },
    ],
  },
];

export default function SettingsPage() {
  return (
    <AppShell>
      <PageHeader title="Settings" subtitle="Customize your QuantumVerse experience" />
      <div className="max-w-2xl space-y-5">
        {SECTIONS.map((section) => (
          <QuantumCard key={section.title}>
            <div className="flex items-center gap-2 mb-4">
              <section.icon className="w-4 h-4 text-quantum-blue" />
              <h3 className="text-sm font-semibold text-white">{section.title}</h3>
            </div>
            <div className="space-y-4">
              {section.items.map((item) => (
                <div key={item.label} className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-white">{item.label}</p>
                    <p className="text-xs text-muted-foreground">{item.description}</p>
                  </div>
                  {item.type === "toggle" && (
                    <div className="w-10 h-5 rounded-full bg-quantum-blue/20 border border-quantum-blue/30 relative cursor-pointer">
                      <div className="absolute right-0.5 top-0.5 w-4 h-4 rounded-full bg-quantum-blue transition-all" />
                    </div>
                  )}
                  {item.type === "static" && (
                    <span className="text-xs text-muted-foreground border border-white/10 px-2 py-1 rounded-lg">{item.value}</span>
                  )}
                  {item.type === "button" && (
                    <button className="text-xs px-3 py-1.5 rounded-lg border border-white/10 text-muted-foreground hover:text-white hover:border-white/20 transition-all">
                      Update
                    </button>
                  )}
                  {item.type === "button-danger" && (
                    <button className="text-xs px-3 py-1.5 rounded-lg border border-red-500/20 text-red-400 hover:bg-red-500/10 transition-all">
                      Delete
                    </button>
                  )}
                </div>
              ))}
            </div>
          </QuantumCard>
        ))}

        {/* About */}
        <QuantumCard>
          <div className="flex items-center gap-3">
            <Atom className="w-8 h-8 text-quantum-blue" />
            <div>
              <p className="text-sm font-bold text-white">QuantumVerse AI</p>
              <p className="text-xs text-muted-foreground">v1.0.0</p>
            </div>
            <a href="/" className="ml-auto text-muted-foreground hover:text-white transition-colors">
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </QuantumCard>
      </div>
    </AppShell>
  );
}
'''

# Write all files
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.lstrip('\n'))
    print(f"  wrote: {rel_path}")

print(f"\nTotal Phase 3 files written: {len(files)}")
