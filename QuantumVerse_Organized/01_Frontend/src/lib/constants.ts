import type { GateInfo } from "@/types/circuit";

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
  { href: "/progress",    label: "Progress",     icon: "TrendingUp" },
  { href: "/profile",     label: "Profile",      icon: "User" },
  { href: "/settings",    label: "Settings",     icon: "Settings" },
];
