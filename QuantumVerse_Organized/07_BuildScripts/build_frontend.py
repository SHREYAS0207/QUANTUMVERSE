import os

BASE = "/data/quantumverse/frontend"

files = {}

# package.json
files["package.json"] = '''{
  "name": "quantumverse-ai",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.3",
    "react": "^18",
    "react-dom": "^18",
    "@supabase/supabase-js": "^2.43.4",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-slider": "^1.1.2",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "@radix-ui/react-tooltip": "^1.0.7",
    "axios": "^1.7.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "framer-motion": "^11.2.10",
    "lucide-react": "^0.383.0",
    "recharts": "^2.12.7",
    "tailwind-merge": "^2.3.0",
    "tailwindcss-animate": "^1.0.7",
    "zustand": "^4.5.2",
    "react-hot-toast": "^2.4.1",
    "uuid": "^10.0.0"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "@types/uuid": "^10.0.0",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "eslint": "^8",
    "eslint-config-next": "14.2.3"
  }
}'''

# tsconfig.json
files["tsconfig.json"] = '''{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./src/*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}'''

# next.config.ts
files["next.config.ts"] = '''import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    domains: ["avatars.githubusercontent.com"],
  },
};

export default nextConfig;
'''

# tailwind.config.ts
files["tailwind.config.ts"] = '''import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        quantum: {
          blue: "#00D4FF",
          purple: "#7B2FBE",
          cyan: "#06FFA5",
          dark: "#050A1A",
          navy: "#0A1628",
          panel: "#0D1F3C",
          glow: "rgba(0, 212, 255, 0.15)",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "float": "float 3s ease-in-out infinite",
        "spin-slow": "spin 8s linear infinite",
      },
      keyframes: {
        "accordion-down": {"from": {"height": "0"}, "to": {"height": "var(--radix-accordion-content-height)"}},
        "accordion-up": {"from": {"height": "var(--radix-accordion-content-height)"}, "to": {"height": "0"}},
        "pulse-glow": {"0%, 100%": {"opacity": "1", "boxShadow": "0 0 20px rgba(0,212,255,0.3)"}, "50%": {"opacity": "0.8", "boxShadow": "0 0 40px rgba(0,212,255,0.6)"}},
        "float": {"0%, 100%": {"transform": "translateY(0)"}, "50%": {"transform": "translateY(-10px)"}},
      },
      backgroundImage: {
        "quantum-gradient": "linear-gradient(135deg, #050A1A 0%, #0A1628 50%, #0D1F3C 100%)",
        "glow-gradient": "radial-gradient(ellipse at center, rgba(0,212,255,0.1) 0%, transparent 70%)",
      },
      fontFamily: {
        mono: ["var(--font-mono)", "monospace"],
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [animate],
};

export default config;
'''

# postcss.config.js
files["postcss.config.js"] = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
'''

# .env.local.example
files[".env.local.example"] = '''NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
'''

# globals.css
files["src/app/globals.css"] = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 222 84% 5%;
    --foreground: 210 40% 96%;
    --card: 221 65% 8%;
    --card-foreground: 210 40% 96%;
    --primary: 195 100% 50%;
    --primary-foreground: 222 84% 5%;
    --secondary: 270 60% 45%;
    --secondary-foreground: 210 40% 96%;
    --muted: 217 33% 17%;
    --muted-foreground: 215 20% 65%;
    --accent: 162 100% 51%;
    --accent-foreground: 222 84% 5%;
    --border: 217 33% 17%;
    --input: 217 33% 15%;
    --ring: 195 100% 50%;
    --radius: 0.75rem;
  }
}

@layer base {
  * { @apply border-border; }
  body {
    @apply bg-background text-foreground;
    background: #050A1A;
    font-family: var(--font-sans), system-ui, sans-serif;
  }
  /* Quantum particle background */
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
      radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,212,255,0.08) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 90% 80%, rgba(123,47,190,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
  }
}

/* Quantum scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0A1628; }
::-webkit-scrollbar-thumb { background: #00D4FF44; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #00D4FF88; }

/* Glassmorphism utility */
.glass {
  background: rgba(13, 31, 60, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 212, 255, 0.1);
}

.glass-hover:hover {
  border-color: rgba(0, 212, 255, 0.3);
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.1);
  transition: all 0.3s ease;
}

/* Quantum glow effects */
.glow-blue { box-shadow: 0 0 20px rgba(0, 212, 255, 0.4); }
.glow-purple { box-shadow: 0 0 20px rgba(123, 47, 190, 0.4); }
.glow-cyan { box-shadow: 0 0 20px rgba(6, 255, 165, 0.4); }
.text-glow { text-shadow: 0 0 20px rgba(0, 212, 255, 0.6); }

/* Circuit line animation */
@keyframes circuit-flow {
  0% { stroke-dashoffset: 1000; }
  100% { stroke-dashoffset: 0; }
}
.circuit-line { animation: circuit-flow 3s linear infinite; }
'''

# Root layout
files["src/app/layout.tsx"] = '''import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "QuantumVerse AI — Learn. Build. Simulate. Understand Quantum Computing.",
  description: "AI-Powered Interactive Quantum Algorithm Learning and Simulation Platform",
  keywords: ["quantum computing", "qiskit", "quantum circuits", "AI tutor", "quantum education"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            style: { background: "#0D1F3C", color: "#e2e8f0", border: "1px solid rgba(0,212,255,0.2)" },
            success: { iconTheme: { primary: "#06FFA5", secondary: "#050A1A" } },
            error: { iconTheme: { primary: "#f87171", secondary: "#050A1A" } },
          }}
        />
      </body>
    </html>
  );
}
'''

# ─── TYPES ──────────────────────────────────────────────────────────────────
files["src/types/circuit.ts"] = '''export type GateType =
  | "H" | "X" | "Y" | "Z" | "S" | "T" | "SDG" | "TDG"
  | "RX" | "RY" | "RZ"
  | "CNOT" | "CX" | "CZ" | "SWAP" | "CCX"
  | "MEASURE" | "BARRIER";

export interface GateOperation {
  id: string;
  gate: GateType;
  targets: number[];
  controls: number[];
  column: number;
  params?: { angle?: number };
}

export interface Circuit {
  id: string;
  name: string;
  description?: string;
  qubits: number;
  classical_bits: number;
  circuit_data: {
    operations: GateOperation[];
  };
  is_template: boolean;
  template_name?: string;
  created_at: string;
  updated_at: string;
}

export interface SimulationResult {
  success: boolean;
  counts: Record<string, number>;
  probabilities: Record<string, number>;
  execution_time: number;
  total_shots: number;
  error?: string;
}

export interface StepResult {
  success: boolean;
  step_index: number;
  gate_applied: string;
  state_description: string;
  state_vector: [number, number][];
  probabilities: Record<string, number>;
  explanation: string;
  error?: string;
}

export interface GateInfo {
  type: GateType;
  label: string;
  color: string;
  description: string;
  category: "single" | "rotation" | "multi" | "measurement";
  requiresControl?: boolean;
  requiresParam?: boolean;
}
'''

files["src/types/user.ts"] = '''export interface User {
  id: string;
  name: string;
  email: string;
  learning_level: "beginner" | "intermediate" | "advanced";
  xp: number;
  level: number;
  streak_days: number;
  statistics: UserStatistics;
}

export interface UserStatistics {
  total_lessons: number;
  total_circuits: number;
  total_quizzes: number;
  quiz_accuracy: number;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
  user_id: string;
  name: string;
  email: string;
  learning_level: string;
}
'''

files["src/types/learning.ts"] = '''export interface LearningModule {
  id: string;
  title: string;
  description: string;
  level: number;
  icon: string;
  lesson_count: number;
}

export interface Lesson {
  id: string;
  title: string;
  order_index: number;
  xp_reward: number;
  estimated_minutes: number;
  content?: LessonContent;
}

export interface LessonContent {
  blocks: ContentBlock[];
}

export type ContentBlock =
  | { type: "text"; content: string }
  | { type: "heading"; level: 1 | 2 | 3; content: string }
  | { type: "math"; content: string }
  | { type: "code"; language: string; content: string }
  | { type: "callout"; variant: "info" | "warning" | "tip"; content: string }
  | { type: "circuit"; circuit_data: object };

export interface ProgressData {
  completed: string[];
  in_progress: string[];
}
'''

files["src/types/quiz.ts"] = '''export interface QuizOption {
  id: string;
  text: string;
}

export interface Question {
  id: string;
  question_text: string;
  question_type: "mcq" | "true_false" | "circuit_predict" | "gate_identify";
  options: QuizOption[];
}

export interface Quiz {
  id: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  time_limit_seconds: number;
  xp_reward: number;
  questions: Question[];
}

export interface QuizResult {
  score: number;
  total: number;
  accuracy: number;
  xp_earned: number;
  answers: AnswerResult[];
}

export interface AnswerResult {
  question_id: string;
  user_answer: string;
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
}
'''

files["src/types/api.ts"] = '''export interface ApiError {
  detail: string;
  status?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export type ApiResponse<T> = T | ApiError;
'''

# ─── LIB ──────────────────────────────────────────────────────────────────────
files["src/lib/api.ts"] = '''import axios, { AxiosError } from "axios";
import toast from "react-hot-toast";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("qv_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Global error handling
api.interceptors.response.use(
  (res) => res,
  (error: AxiosError<{ detail: string }>) => {
    const message = error.response?.data?.detail || "Something went wrong";
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("qv_token");
        localStorage.removeItem("qv_user");
        window.location.href = "/login";
      }
    }
    toast.error(message);
    return Promise.reject(error);
  }
);

export default api;
'''

files["src/lib/supabase.ts"] = '''import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

export const supabase = supabaseUrl && supabaseAnonKey
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export default supabase;
'''

files["src/lib/constants.ts"] = '''import type { GateInfo } from "@/types/circuit";

export const GATE_CATALOG: GateInfo[] = [
  { type: "H",    label: "H",    color: "#00D4FF", description: "Hadamard — creates superposition",           category: "single" },
  { type: "X",    label: "X",    color: "#f87171", description: "Pauli-X — quantum NOT gate",                 category: "single" },
  { type: "Y",    label: "Y",    color: "#fb923c", description: "Pauli-Y — X + Z with phase",                 category: "single" },
  { type: "Z",    label: "Z",    color: "#a78bfa", description: "Pauli-Z — phase flip",                       category: "single" },
  { type: "S",    label: "S",    color: "#34d399", description: "S gate — 90° phase rotation",                category: "single" },
  { type: "T",    label: "T",    color: "#6ee7b7", description: "T gate — 45° phase rotation",                category: "single" },
  { type: "RX",   label: "RX",   color: "#fbbf24", description: "Rotation around X-axis",                    category: "rotation", requiresParam: true },
  { type: "RY",   label: "RY",   color: "#f59e0b", description: "Rotation around Y-axis",                    category: "rotation", requiresParam: true },
  { type: "RZ",   label: "RZ",   color: "#d97706", description: "Rotation around Z-axis",                    category: "rotation", requiresParam: true },
  { type: "CNOT", label: "CNOT", color: "#818cf8", description: "Controlled-NOT — creates entanglement",     category: "multi",   requiresControl: true },
  { type: "CZ",   label: "CZ",   color: "#6366f1", description: "Controlled-Z gate",                        category: "multi",   requiresControl: true },
  { type: "SWAP", label: "SWAP", color: "#8b5cf6", description: "Swap two qubit states",                     category: "multi" },
  { type: "CCX",  label: "CCX",  color: "#7c3aed", description: "Toffoli — controlled-controlled-NOT",       category: "multi",   requiresControl: true },
  { type: "MEASURE", label: "M", color: "#06FFA5", description: "Measure qubit — collapses superposition",   category: "measurement" },
  { type: "BARRIER", label: "|", color: "#64748b", description: "Barrier — visual separator",                category: "measurement" },
];

export const LEARNING_LEVEL_COLORS = {
  beginner:     "text-green-400 border-green-400",
  intermediate: "text-yellow-400 border-yellow-400",
  advanced:     "text-red-400 border-red-400",
};

export const XP_PER_LEVEL = 500;

export const SIDEBAR_ITEMS = [
  { href: "/dashboard",   label: "Dashboard",   icon: "LayoutDashboard" },
  { href: "/learn",       label: "Learn",        icon: "BookOpen" },
  { href: "/quantum-lab", label: "Quantum Lab",  icon: "FlaskConical" },
  { href: "/algorithms",  label: "Algorithms",   icon: "Zap" },
  { href: "/ai-tutor",    label: "AI Tutor",     icon: "Bot" },
  { href: "/quiz",        label: "Quiz Arena",   icon: "Trophy" },
  { href: "/achievements",label: "Achievements", icon: "Star" },
  { href: "/progress",    label: "Progress",     icon: "TrendingUp" },
  { href: "/profile",     label: "Profile",      icon: "User" },
  { href: "/settings",    label: "Settings",     icon: "Settings" },
];
'''

files["src/lib/utils.ts"] = '''import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatXP(xp: number): string {
  if (xp >= 1000) return `${(xp / 1000).toFixed(1)}k XP`;
  return `${xp} XP`;
}

export function getLevelFromXP(xp: number, xpPerLevel = 500): number {
  return Math.floor(xp / xpPerLevel) + 1;
}

export function getXPProgress(xp: number, xpPerLevel = 500): number {
  return (xp % xpPerLevel) / xpPerLevel * 100;
}

export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return s > 0 ? `${m}m ${s}s` : `${m}m`;
}
'''

# ─── STORES ──────────────────────────────────────────────────────────────────
files["src/stores/authStore.ts"] = '''import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/types/user";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  updateUser: (updates: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      setAuth: (user, token) => {
        localStorage.setItem("qv_token", token);
        set({ user, token, isAuthenticated: true });
      },
      clearAuth: () => {
        localStorage.removeItem("qv_token");
        localStorage.removeItem("qv_user");
        set({ user: null, token: null, isAuthenticated: false });
      },
      updateUser: (updates) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null,
        })),
    }),
    { name: "qv_auth", partialize: (state) => ({ user: state.user, token: state.token, isAuthenticated: state.isAuthenticated }) }
  )
);
'''

files["src/stores/circuitStore.ts"] = '''import { create } from "zustand";
import { v4 as uuidv4 } from "uuid";
import type { GateOperation, GateType, SimulationResult, StepResult } from "@/types/circuit";

interface CircuitState {
  qubits: number;
  classicalBits: number;
  operations: GateOperation[];
  history: GateOperation[][];
  historyIndex: number;
  simulationResult: SimulationResult | null;
  stepResult: StepResult | null;
  currentStep: number;
  isSimulating: boolean;
  isStepping: boolean;
  circuitName: string;

  setQubits: (n: number) => void;
  setClassicalBits: (n: number) => void;
  addGate: (gate: GateType, targets: number[], controls: number[], column: number, params?: object) => void;
  removeGate: (id: string) => void;
  moveGate: (id: string, newColumn: number, newTarget: number) => void;
  clearCircuit: () => void;
  undo: () => void;
  redo: () => void;
  setSimulationResult: (result: SimulationResult | null) => void;
  setStepResult: (result: StepResult | null) => void;
  setCurrentStep: (step: number) => void;
  setIsSimulating: (v: boolean) => void;
  setIsStepping: (v: boolean) => void;
  setCircuitName: (name: string) => void;
  loadCircuit: (ops: GateOperation[], qubits: number, classicalBits: number) => void;
}

export const useCircuitStore = create<CircuitState>((set, get) => ({
  qubits: 2,
  classicalBits: 2,
  operations: [],
  history: [[]],
  historyIndex: 0,
  simulationResult: null,
  stepResult: null,
  currentStep: 0,
  isSimulating: false,
  isStepping: false,
  circuitName: "My Circuit",

  setQubits: (n) => set({ qubits: Math.max(1, Math.min(6, n)) }),
  setClassicalBits: (n) => set({ classicalBits: Math.max(0, Math.min(6, n)) }),

  addGate: (gate, targets, controls, column, params) => {
    const newOp: GateOperation = { id: uuidv4(), gate, targets, controls, column, params };
    set((state) => {
      const newOps = [...state.operations, newOp];
      const newHistory = state.history.slice(0, state.historyIndex + 1);
      newHistory.push(newOps);
      return { operations: newOps, history: newHistory, historyIndex: newHistory.length - 1 };
    });
  },

  removeGate: (id) => {
    set((state) => {
      const newOps = state.operations.filter((op) => op.id !== id);
      const newHistory = state.history.slice(0, state.historyIndex + 1);
      newHistory.push(newOps);
      return { operations: newOps, history: newHistory, historyIndex: newHistory.length - 1 };
    });
  },

  moveGate: (id, newColumn, newTarget) => {
    set((state) => {
      const newOps = state.operations.map((op) =>
        op.id === id ? { ...op, column: newColumn, targets: [newTarget] } : op
      );
      return { operations: newOps };
    });
  },

  clearCircuit: () => {
    set((state) => ({
      operations: [],
      history: [[]],
      historyIndex: 0,
      simulationResult: null,
      stepResult: null,
    }));
  },

  undo: () => {
    set((state) => {
      if (state.historyIndex <= 0) return state;
      const newIndex = state.historyIndex - 1;
      return { operations: state.history[newIndex], historyIndex: newIndex };
    });
  },

  redo: () => {
    set((state) => {
      if (state.historyIndex >= state.history.length - 1) return state;
      const newIndex = state.historyIndex + 1;
      return { operations: state.history[newIndex], historyIndex: newIndex };
    });
  },

  setSimulationResult: (result) => set({ simulationResult: result }),
  setStepResult: (result) => set({ stepResult: result }),
  setCurrentStep: (step) => set({ currentStep: step }),
  setIsSimulating: (v) => set({ isSimulating: v }),
  setIsStepping: (v) => set({ isStepping: v }),
  setCircuitName: (name) => set({ circuitName: name }),
  loadCircuit: (ops, qubits, classicalBits) =>
    set({ operations: ops, qubits, classicalBits, history: [ops], historyIndex: 0 }),
}));
'''

# ─── SERVICES ─────────────────────────────────────────────────────────────────
files["src/services/authService.ts"] = '''import api from "@/lib/api";
import type { AuthTokens, User } from "@/types/user";

export const authService = {
  async signup(name: string, email: string, password: string, learning_level: string): Promise<AuthTokens> {
    const { data } = await api.post<AuthTokens>("/auth/signup", { name, email, password, learning_level });
    return data;
  },
  async login(email: string, password: string): Promise<AuthTokens> {
    const { data } = await api.post<AuthTokens>("/auth/login", { email, password });
    return data;
  },
  async getProfile(): Promise<User> {
    const { data } = await api.get<User>("/auth/profile");
    return data;
  },
  async updateProfile(updates: Partial<User>): Promise<User> {
    const { data } = await api.put<User>("/auth/profile", updates);
    return data;
  },
};
'''

files["src/services/circuitService.ts"] = '''import api from "@/lib/api";
import type { Circuit } from "@/types/circuit";

export const circuitService = {
  async list(): Promise<Circuit[]> {
    const { data } = await api.get<{ circuits: Circuit[] }>("/circuits");
    return data.circuits;
  },
  async get(id: string): Promise<Circuit> {
    const { data } = await api.get<Circuit>(`/circuits/${id}`);
    return data;
  },
  async create(payload: Partial<Circuit>): Promise<Circuit> {
    const { data } = await api.post<Circuit>("/circuits", payload);
    return data;
  },
  async update(id: string, payload: Partial<Circuit>): Promise<Circuit> {
    const { data } = await api.put<Circuit>(`/circuits/${id}`, payload);
    return data;
  },
  async delete(id: string): Promise<void> {
    await api.delete(`/circuits/${id}`);
  },
  async getTemplates(): Promise<Circuit[]> {
    const { data } = await api.get<{ templates: Circuit[] }>("/circuits/templates");
    return data.templates;
  },
};
'''

files["src/services/simulationService.ts"] = '''import api from "@/lib/api";
import type { SimulationResult, StepResult, GateOperation } from "@/types/circuit";

export const simulationService = {
  async run(qubits: number, operations: GateOperation[], shots = 1024, circuit_id?: string): Promise<SimulationResult> {
    const { data } = await api.post<SimulationResult>("/simulation/run", { qubits, operations, shots, circuit_id });
    return data;
  },
  async step(qubits: number, operations: GateOperation[], step_index: number): Promise<StepResult> {
    const { data } = await api.post<StepResult>("/simulation/step", { qubits, operations, step_index });
    return data;
  },
  async getHistory(): Promise<object[]> {
    const { data } = await api.get<{ history: object[] }>("/simulation/history");
    return data.history;
  },
};
'''

files["src/services/aiService.ts"] = '''import api from "@/lib/api";

export const aiService = {
  async createConversation(): Promise<{ id: string; title: string }> {
    const { data } = await api.post("/ai/conversations");
    return data;
  },
  async listConversations(): Promise<object[]> {
    const { data } = await api.get<{ conversations: object[] }>("/ai/conversations");
    return data.conversations;
  },
  async chat(conv_id: string, message: string, difficulty: string, context?: object): Promise<{ response: string; conversation_id: string }> {
    const { data } = await api.post(`/ai/conversations/${conv_id}/chat`, { message, difficulty, context });
    return data;
  },
  async explainCircuit(circuit_data: object, difficulty: string): Promise<object> {
    const { data } = await api.post("/ai/explain-circuit", { circuit_data, difficulty });
    return data;
  },
};
'''

files["src/services/algorithmService.ts"] = '''import api from "@/lib/api";

export const algorithmService = {
  async list(): Promise<object[]> {
    const { data } = await api.get<{ algorithms: object[] }>("/algorithms");
    return data.algorithms;
  },
  async runGrover(n_qubits: number, target: number, iterations?: number): Promise<object> {
    const { data } = await api.post("/algorithms/grover/run", { n_qubits, target, iterations });
    return data;
  },
  async runTeleportation(state: string): Promise<object> {
    const { data } = await api.post("/algorithms/teleportation/run", { state });
    return data;
  },
  async runDeutschJozsa(oracle_type: string, n_qubits: number): Promise<object> {
    const { data } = await api.post("/algorithms/deutsch-jozsa/run", { oracle_type, n_qubits });
    return data;
  },
  async runQFT(n_qubits: number, input_state: number): Promise<object> {
    const { data } = await api.post("/algorithms/qft/run", { n_qubits, input_state });
    return data;
  },
};
'''

# ─── LAYOUT COMPONENTS ─────────────────────────────────────────────────────
files["src/components/layout/Sidebar.tsx"] = '''"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { useAuthStore } from "@/stores/authStore";
import { cn, getXPProgress } from "@/lib/utils";
import {
  LayoutDashboard, BookOpen, FlaskConical, Zap, Bot, Trophy, Star, TrendingUp, User, Settings, LogOut, Atom
} from "lucide-react";

const ICON_MAP: Record<string, React.ElementType> = {
  LayoutDashboard, BookOpen, FlaskConical, Zap, Bot, Trophy, Star, TrendingUp, User, Settings,
};

const NAV_ITEMS = [
  { href: "/dashboard",    label: "Dashboard",    icon: "LayoutDashboard" },
  { href: "/learn",        label: "Learn",         icon: "BookOpen" },
  { href: "/quantum-lab",  label: "Quantum Lab",   icon: "FlaskConical" },
  { href: "/algorithms",   label: "Algorithms",    icon: "Zap" },
  { href: "/ai-tutor",     label: "AI Tutor",      icon: "Bot" },
  { href: "/quiz",         label: "Quiz Arena",    icon: "Trophy" },
  { href: "/achievements", label: "Achievements",  icon: "Star" },
  { href: "/progress",     label: "Progress",      icon: "TrendingUp" },
  { href: "/profile",      label: "Profile",       icon: "User" },
  { href: "/settings",     label: "Settings",      icon: "Settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, clearAuth } = useAuthStore();
  const xpProgress = getXPProgress(user?.xp ?? 0);

  return (
    <aside className="fixed left-0 top-0 h-full w-64 glass border-r border-quantum-blue/10 flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 border-b border-quantum-blue/10">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-quantum-blue/10 border border-quantum-blue/30 flex items-center justify-center">
            <Atom className="w-5 h-5 text-quantum-blue" />
          </div>
          <div>
            <p className="font-bold text-sm text-white tracking-wide">QuantumVerse</p>
            <p className="text-[10px] text-quantum-blue/70 font-mono">AI Platform</p>
          </div>
        </Link>
      </div>

      {/* XP Bar */}
      {user && (
        <div className="px-4 py-3 border-b border-quantum-blue/10">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-muted-foreground">Level {user.level}</span>
            <span className="text-quantum-blue font-mono">{user.xp} XP</span>
          </div>
          <div className="h-1.5 bg-muted rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${xpProgress}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
        </div>
      )}

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-0.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = ICON_MAP[item.icon];
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                whileHover={{ x: 4 }}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200",
                  isActive
                    ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20"
                    : "text-muted-foreground hover:text-white hover:bg-white/5"
                )}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="ml-auto w-1.5 h-1.5 rounded-full bg-quantum-blue"
                  />
                )}
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* User footer */}
      <div className="p-4 border-t border-quantum-blue/10">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center text-xs font-bold text-white">
            {user?.name?.[0]?.toUpperCase() ?? "Q"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">{user?.name ?? "Quantum Explorer"}</p>
            <p className="text-xs text-muted-foreground capitalize">{user?.learning_level ?? "beginner"}</p>
          </div>
        </div>
        <button
          onClick={clearAuth}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-muted-foreground hover:text-red-400 hover:bg-red-400/5 transition-all"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
'''

files["src/components/layout/AppShell.tsx"] = '''"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { Sidebar } from "./Sidebar";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1 min-h-screen relative z-10">
        <div className="p-8">{children}</div>
      </main>
    </div>
  );
}
'''

# ─── SHARED COMPONENTS ─────────────────────────────────────────────────────
files["src/components/shared/QuantumCard.tsx"] = '''"use client";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface QuantumCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
  onClick?: () => void;
}

export function QuantumCard({ children, className, hover = false, glow = false, onClick }: QuantumCardProps) {
  return (
    <motion.div
      whileHover={hover ? { scale: 1.01, y: -2 } : undefined}
      onClick={onClick}
      className={cn(
        "glass rounded-xl p-5 transition-all duration-300",
        hover && "cursor-pointer glass-hover",
        glow && "border-quantum-blue/30 shadow-[0_0_20px_rgba(0,212,255,0.1)]",
        className
      )}
    >
      {children}
    </motion.div>
  );
}
'''

files["src/components/shared/StatCard.tsx"] = '''import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  color?: string;
  trend?: string;
}

export function StatCard({ label, value, icon: Icon, color = "text-quantum-blue", trend }: StatCardProps) {
  return (
    <div className="glass rounded-xl p-5 border border-white/5 hover:border-quantum-blue/20 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center", `bg-[color:${color}]/10`)}>
          <Icon className={cn("w-5 h-5", color)} />
        </div>
        {trend && <span className="text-xs text-green-400 bg-green-400/10 px-2 py-0.5 rounded-full">{trend}</span>}
      </div>
      <p className="text-2xl font-bold text-white mt-1">{value}</p>
      <p className="text-xs text-muted-foreground mt-0.5">{label}</p>
    </div>
  );
}
'''

files["src/components/shared/PageHeader.tsx"] = '''interface PageHeaderProps {
  title: string;
  subtitle?: string;
  children?: React.ReactNode;
}

export function PageHeader({ title, subtitle, children }: PageHeaderProps) {
  return (
    <div className="flex items-start justify-between mb-8">
      <div>
        <h1 className="text-2xl font-bold text-white">{title}</h1>
        {subtitle && <p className="text-muted-foreground text-sm mt-1">{subtitle}</p>}
      </div>
      {children && <div className="flex items-center gap-3">{children}</div>}
    </div>
  );
}
'''

files["src/components/shared/LoadingSpinner.tsx"] = '''import { cn } from "@/lib/utils";

export function LoadingSpinner({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center justify-center", className)}>
      <div className="w-8 h-8 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
    </div>
  );
}

export function FullPageLoader() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <div className="w-12 h-12 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
      <p className="text-muted-foreground text-sm">Initializing quantum systems...</p>
    </div>
  );
}
'''

# ─── APP PAGES ─────────────────────────────────────────────────────────────────
files["src/app/page.tsx"] = '''"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Atom, Zap, Bot, Trophy, FlaskConical, BookOpen, GitBranch, Cpu } from "lucide-react";

const FEATURES = [
  { icon: FlaskConical, title: "Drag-Drop Circuit Builder",     desc: "Build quantum circuits visually — no coding required." },
  { icon: Zap,          title: "Real-Time Qiskit Simulation",   desc: "Powered by IBM Qiskit Aer for accurate quantum results." },
  { icon: Bot,          title: "QubitAI Tutor",                  desc: "AI assistant that adapts explanations to your level." },
  { icon: BookOpen,     title: "Interactive Learning Paths",     desc: "From fundamentals to advanced algorithms, step by step." },
  { icon: GitBranch,    title: "Step-by-Step Execution",         desc: "Watch quantum state evolve gate by gate in real time." },
  { icon: Trophy,       title: "Gamified Progress",              desc: "Earn XP, badges, and track your quantum journey." },
];

const ALGORITHMS = [
  { name: "Grover\'s Search",   complexity: "O(√N)", color: "from-blue-500 to-cyan-500" },
  { name: "Quantum Teleportation", complexity: "3 qubits",  color: "from-purple-500 to-pink-500" },
  { name: "Deutsch-Jozsa",      complexity: "O(1) queries", color: "from-green-500 to-emerald-500" },
  { name: "Quantum Fourier Transform", complexity: "O(n²)",    color: "from-orange-500 to-yellow-500" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen text-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-quantum-blue/10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Atom className="w-7 h-7 text-quantum-blue" />
            <span className="font-bold text-lg tracking-tight">QuantumVerse AI</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-sm text-muted-foreground hover:text-white transition-colors px-4 py-2">
              Sign In
            </Link>
            <Link href="/signup" className="text-sm px-4 py-2 rounded-lg bg-quantum-blue text-quantum-dark font-semibold hover:opacity-90 transition-opacity">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-40 pb-24 px-6 text-center relative overflow-hidden">
        <div className="absolute inset-0 bg-glow-gradient pointer-events-none" />
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-quantum-blue/30 bg-quantum-blue/5 text-quantum-blue text-sm font-mono mb-8">
            <span className="w-2 h-2 rounded-full bg-quantum-blue animate-pulse" />
            QuantumVerse AI
          </span>
          <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-6">
            Learn Quantum Computing
            <br />
            <span className="bg-gradient-to-r from-quantum-blue via-quantum-purple to-quantum-cyan bg-clip-text text-transparent">
              by Experimenting
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Build quantum circuits visually, simulate with real Qiskit backend, learn from AI,
            and master quantum algorithms — no physics PhD required.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Link href="/signup">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
                className="flex items-center gap-2 px-8 py-4 rounded-xl bg-quantum-blue text-quantum-dark font-bold text-lg hover:opacity-90 transition-all glow-blue">
                Start Learning <ArrowRight className="w-5 h-5" />
              </motion.button>
            </Link>
            <Link href="/quantum-lab">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
                className="flex items-center gap-2 px-8 py-4 rounded-xl border border-quantum-blue/30 text-white font-semibold text-lg hover:bg-quantum-blue/10 transition-all">
                <FlaskConical className="w-5 h-5" /> Explore Simulator
              </motion.button>
            </Link>
          </div>
        </motion.div>

        {/* Animated circuit preview */}
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4, duration: 0.8 }}
          className="mt-20 max-w-4xl mx-auto">
          <div className="glass rounded-2xl border border-quantum-blue/20 p-8 glow-blue">
            <div className="font-mono text-sm text-left space-y-4">
              {["|q0⟩", "|q1⟩", "|q2⟩"].map((q, i) => (
                <div key={q} className="flex items-center gap-3">
                  <span className="text-quantum-blue w-10">{q}</span>
                  <div className="flex-1 h-px bg-quantum-blue/20 relative">
                    {i === 0 && <div className="absolute left-[15%] -top-4 w-8 h-8 rounded-lg bg-cyan-500/20 border border-cyan-500/50 flex items-center justify-center text-xs text-cyan-400">H</div>}
                    {i === 0 && <div className="absolute left-[45%] -top-1 w-3 h-3 rounded-full bg-blue-400 border-2 border-blue-400" />}
                    {i === 1 && <div className="absolute left-[45%] -top-4 w-8 h-8 rounded-lg bg-purple-500/20 border border-purple-500/50 flex items-center justify-center text-xs text-purple-400">⊕</div>}
                    {i === 2 && <div className="absolute left-[70%] -top-4 w-8 h-8 rounded-lg bg-green-500/20 border border-green-500/50 flex items-center justify-center text-xs text-green-400">M</div>}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 flex items-center justify-between text-xs text-muted-foreground">
              <span>Bell State Circuit</span>
              <span className="text-quantum-cyan font-mono">|00⟩ → ½(|00⟩ + |11⟩)</span>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Everything You Need to Master Quantum Computing</h2>
          <p className="text-muted-foreground text-lg">One platform. Complete learning ecosystem.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((f, i) => (
            <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }} viewport={{ once: true }}
              className="glass rounded-xl p-6 border border-white/5 hover:border-quantum-blue/20 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-quantum-blue/10 border border-quantum-blue/20 flex items-center justify-center mb-4">
                <f.icon className="w-6 h-6 text-quantum-blue" />
              </div>
              <h3 className="font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Algorithms */}
      <section className="py-24 px-6 bg-quantum-navy/30">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4">Quantum Algorithm Explorer</h2>
          <p className="text-muted-foreground mb-12">Understand landmark quantum algorithms interactively.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {ALGORITHMS.map((alg, i) => (
              <motion.div key={alg.name} initial={{ opacity: 0, scale: 0.9 }} whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }} viewport={{ once: true }}
                className="glass rounded-xl p-6 border border-white/5 hover:border-white/20 transition-all">
                <div className={`h-1 rounded-full bg-gradient-to-r ${alg.color} mb-4`} />
                <h3 className="font-semibold text-white mb-2 text-sm">{alg.name}</h3>
                <span className="font-mono text-xs text-muted-foreground">{alg.complexity}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { val: "4", label: "Learning Levels" },
            { val: "25+", label: "Lessons" },
            { val: "15+", label: "Quantum Gates" },
            { val: "4", label: "Famous Algorithms" },
          ].map((s) => (
            <div key={s.label}>
              <p className="text-4xl font-black text-quantum-blue">{s.val}</p>
              <p className="text-sm text-muted-foreground mt-1">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6 text-center">
        <div className="max-w-2xl mx-auto glass rounded-2xl border border-quantum-blue/20 p-12">
          <Atom className="w-12 h-12 text-quantum-blue mx-auto mb-6 animate-spin-slow" />
          <h2 className="text-3xl font-bold mb-4">Ready to Enter the Quantum Realm?</h2>
          <p className="text-muted-foreground mb-8">Join the future of computing education. Free for SIH demo.</p>
          <Link href="/signup">
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
              className="px-10 py-4 rounded-xl bg-gradient-to-r from-quantum-blue to-quantum-purple text-white font-bold text-lg hover:opacity-90 transition-opacity">
              Start for Free
            </motion.button>
          </Link>
        </div>
      </section>

      <footer className="py-8 px-6 border-t border-white/5 text-center text-sm text-muted-foreground">
        <p>© 2024 QuantumVerse AI</p>
        <p className="mt-1 font-mono text-xs text-quantum-blue/50">Learn. Build. Simulate. Understand Quantum Computing.</p>
      </footer>
    </div>
  );
}
'''

files["src/app/login/page.tsx"] = '''"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Atom, Eye, EyeOff, Loader2 } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";
import { authService } from "@/services/authService";
import toast from "react-hot-toast";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const tokens = await authService.login(email, password);
      const user = await authService.getProfile();
      setAuth(user as any, tokens.access_token);
      toast.success("Welcome back!");
      router.push("/dashboard");
    } catch {
      // toast handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-quantum-blue/10 border border-quantum-blue/30 flex items-center justify-center mx-auto mb-4">
            <Atom className="w-8 h-8 text-quantum-blue" />
          </div>
          <h1 className="text-2xl font-bold text-white">Welcome Back</h1>
          <p className="text-muted-foreground mt-1 text-sm">Sign in to continue your quantum journey</p>
        </div>
        <div className="glass rounded-2xl border border-white/10 p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm text-muted-foreground mb-2">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-muted-foreground focus:outline-none focus:border-quantum-blue/50 transition-colors"
                placeholder="you@example.com" />
            </div>
            <div>
              <label className="block text-sm text-muted-foreground mb-2">Password</label>
              <div className="relative">
                <input type={showPass ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} required
                  className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-muted-foreground focus:outline-none focus:border-quantum-blue/50 transition-colors pr-12"
                  placeholder="••••••••" />
                <button type="button" onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-3.5 text-muted-foreground hover:text-white">
                  {showPass ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-3 rounded-xl bg-quantum-blue text-quantum-dark font-bold hover:opacity-90 transition-opacity disabled:opacity-60 flex items-center justify-center gap-2">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Signing In...</> : "Sign In"}
            </button>
          </form>
          <p className="text-center text-sm text-muted-foreground mt-6">
            No account? <Link href="/signup" className="text-quantum-blue hover:underline">Sign up for free</Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
'''

files["src/app/signup/page.tsx"] = '''"use client";
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
'''

# App route layouts
files["src/app/dashboard/page.tsx"] = '''"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Zap, BookOpen, FlaskConical, Trophy, Flame, TrendingUp, ArrowRight } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { useAuthStore } from "@/stores/authStore";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Link from "next/link";
import { cn } from "@/lib/utils";

const MOCK_ACTIVITY = [
  { day: "Mon", minutes: 30 }, { day: "Tue", minutes: 45 }, { day: "Wed", minutes: 20 },
  { day: "Thu", minutes: 60 }, { day: "Fri", minutes: 35 }, { day: "Sat", minutes: 50 }, { day: "Sun", minutes: 0 },
];

export default function DashboardPage() {
  const { user } = useAuthStore();

  const stats = [
    { label: "Total XP",       value: user?.xp ?? 0,                      icon: Zap,        color: "text-yellow-400" },
    { label: "Lessons Done",   value: user?.statistics?.total_lessons ?? 0, icon: BookOpen,   color: "text-blue-400" },
    { label: "Circuits Built", value: user?.statistics?.total_circuits ?? 0, icon: FlaskConical, color: "text-purple-400" },
    { label: "Quiz Accuracy",  value: `${user?.statistics?.quiz_accuracy ?? 0}%`, icon: Trophy, color: "text-green-400" },
  ];

  return (
    <AppShell>
      <PageHeader
        title={`Welcome back, ${user?.name?.split(" ")[0] ?? "Explorer"}! 👋`}
        subtitle="Continue your quantum computing journey"
      >
        <Link href="/quantum-lab">
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-quantum-blue text-quantum-dark font-semibold text-sm hover:opacity-90 transition-opacity">
            Open Lab <ArrowRight className="w-4 h-4" />
          </button>
        </Link>
      </PageHeader>

      {/* Streak banner */}
      {(user?.streak_days ?? 0) > 0 && (
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
          className="mb-6 flex items-center gap-3 px-5 py-3 rounded-xl bg-orange-500/10 border border-orange-500/20">
          <Flame className="w-5 h-5 text-orange-400" />
          <span className="text-sm text-orange-300">
            🔥 <strong>{user?.streak_days} day</strong> learning streak — keep it up!
          </span>
        </motion.div>
      )}

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            className="glass rounded-xl p-5 border border-white/5">
            <s.icon className={cn("w-6 h-6 mb-3", s.color)} />
            <p className="text-2xl font-bold text-white">{s.value}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{s.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Activity Chart */}
        <QuantumCard className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-white">Weekly Activity</h2>
            <TrendingUp className="w-4 h-4 text-quantum-blue" />
          </div>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={MOCK_ACTIVITY}>
              <XAxis dataKey="day" tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip contentStyle={{ background: "#0D1F3C", border: "1px solid rgba(0,212,255,0.2)", borderRadius: "8px", color: "#e2e8f0" }} />
              <Bar dataKey="minutes" fill="#00D4FF" radius={[4, 4, 0, 0]} opacity={0.8} />
            </BarChart>
          </ResponsiveContainer>
        </QuantumCard>

        {/* Quick Actions */}
        <QuantumCard>
          <h2 className="text-sm font-semibold text-white mb-4">Quick Actions</h2>
          <div className="space-y-2">
            {[
              { href: "/learn",        label: "Continue Learning",  icon: BookOpen,    color: "text-blue-400" },
              { href: "/quantum-lab",  label: "Build a Circuit",    icon: FlaskConical, color: "text-purple-400" },
              { href: "/ai-tutor",     label: "Ask QubitAI",        icon: Zap,          color: "text-cyan-400" },
              { href: "/quiz",         label: "Take a Quiz",         icon: Trophy,       color: "text-green-400" },
            ].map((action) => (
              <Link key={action.href} href={action.href}>
                <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors cursor-pointer">
                  <action.icon className={cn("w-4 h-4", action.color)} />
                  <span className="text-sm text-muted-foreground hover:text-white transition-colors">{action.label}</span>
                  <ArrowRight className="w-3 h-3 ml-auto text-muted-foreground" />
                </div>
              </Link>
            ))}
          </div>
        </QuantumCard>
      </div>
    </AppShell>
  );
}
'''

# Placeholder pages for remaining routes
for page_info in [
    ("learn",        "Learn",        "Explore learning modules and lessons"),
    ("quantum-lab",  "Quantum Lab",  "Build and simulate quantum circuits"),
    ("algorithms",   "Algorithms",   "Explore famous quantum algorithms"),
    ("ai-tutor",     "AI Tutor",     "Chat with QubitAI quantum tutor"),
    ("quiz",         "Quiz Arena",   "Test your quantum knowledge"),
    ("achievements", "Achievements", "Your earned badges and milestones"),
    ("progress",     "Progress",     "Track your learning analytics"),
    ("profile",      "Profile",      "Manage your account and preferences"),
    ("settings",     "Settings",     "Customize your QuantumVerse experience"),
]:
    slug, title, subtitle = page_info
    files[f"src/app/{slug}/page.tsx"] = f'''"use client";
import {{ AppShell }} from "@/components/layout/AppShell";
import {{ PageHeader }} from "@/components/shared/PageHeader";

export default function {title.replace(" ", "")}Page() {{
  return (
    <AppShell>
      <PageHeader title="{title}" subtitle="{subtitle}" />
      <div className="glass rounded-xl border border-white/5 p-12 text-center">
        <p className="text-muted-foreground">🚧 {title} module — full implementation in Phase 3+</p>
      </div>
    </AppShell>
  );
}}
'''

# ─── README ──────────────────────────────────────────────────────────────────────
files["../README.md"] = '''# QuantumVerse AI

> **Learn. Build. Simulate. Understand Quantum Computing.**

AI-Powered Interactive Quantum Algorithm Learning and Simulation Platform

---

## Problem Statement
Quantum computing education is fragmented, mathematically dense, and lacks interactive tools for beginners.

## Solution
QuantumVerse AI provides:
- **Visual drag-and-drop circuit builder** (no coding required)
- **Real Qiskit Aer simulation** engine
- **Step-by-step quantum state visualization**
- **AI Tutor (QubitAI)** adapting explanations to your level
- **4 famous algorithm explorers** (Grover, Teleportation, Deutsch-Jozsa, QFT)
- **Gamified XP + badge system**

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Framer Motion |
| Backend | FastAPI (Python 3.11), SQLAlchemy, Pydantic v2 |
| Quantum Engine | Qiskit 1.x + Qiskit Aer |
| AI Tutor | OpenRouter API (abstraction layer) |
| Database | PostgreSQL via Supabase |
| Auth | JWT (custom) or Supabase Auth |
| Deployment | Vercel (FE) + Render/Railway (BE) |

---

## Quick Start

### Prerequisites
- Node.js 18+, Python 3.11+, PostgreSQL (or Supabase)

### 1. Clone and setup
```bash
git clone <repo>
cd quantumverse
```

### 2. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in your values

# Create DB tables + seed data
python -m app.database.seed

# Run server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local  # fill in your values
npm run dev
```

### 4. Docker (all-in-one)
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
docker-compose up --build
```

Visit: http://localhost:3000

---

## API Documentation
After running backend, visit: http://localhost:8000/docs (FastAPI Swagger UI)

---

## Deployment

**Frontend → Vercel**
```bash
cd frontend && vercel deploy
```

**Backend → Render**
- Connect GitHub repo, select `backend/` root
- Set env vars from `backend/.env.example`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Database → Supabase**
- Create project at supabase.com
- Copy connection string to `DATABASE_URL`
- Run: `python -m app.database.seed`

---

## Project Structure
```
quantumverse/
├── frontend/         # Next.js 14 app
├── backend/          # FastAPI + Qiskit
├── docker-compose.yml
└── README.md
```

---

## Development Phases
- [x] Phase 1 — Architecture
- [x] Phase 2 — Project scaffold + DB models + Core API
- [ ] Phase 3 — Auth flow complete
- [ ] Phase 4 — Design system + Layout
- [ ] Phase 5 — Dashboard
- [ ] Phase 6 — Learning modules
- [ ] Phase 7 — Quantum Lab UI
- [ ] Phase 8 — Qiskit simulation
- [ ] Phase 9 — Step-by-step execution
- [ ] Phase 10 — Algorithm Explorer
- [ ] Phase 11 — AI Tutor
- [ ] Phase 12 — Quiz Arena
- [ ] Phase 13 — Gamification
- [ ] Phase 14 — Analytics
- [ ] Phase 15 — Deployment

---

*QuantumVerse AI Team*
'''

# Write all files
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.lstrip('\n'))
    print(f"  wrote: {rel_path}")

print(f"\nTotal frontend files written: {len(files)}")
