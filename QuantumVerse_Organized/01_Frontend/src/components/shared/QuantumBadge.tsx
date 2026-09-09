import { cn } from "@/lib/utils";

type BadgeVariant = "blue" | "purple" | "cyan" | "green" | "yellow" | "red" | "gray";

const COLORS: Record<BadgeVariant, string> = {
  blue:   "text-blue-400   border-blue-400/30   bg-blue-400/5",
  purple: "text-purple-400 border-purple-400/30 bg-purple-400/5",
  cyan:   "text-cyan-400   border-cyan-400/30   bg-cyan-400/5",
  green:  "text-green-400  border-green-400/30  bg-green-400/5",
  yellow: "text-yellow-400 border-yellow-400/30 bg-yellow-400/5",
  red:    "text-red-400    border-red-400/30    bg-red-400/5",
  gray:   "text-gray-400   border-gray-400/30   bg-gray-400/5",
};

interface QuantumBadgeProps {
  label: string;
  variant?: BadgeVariant;
  className?: string;
}

export function QuantumBadge({ label, variant = "blue", className }: QuantumBadgeProps) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${COLORS[variant]} ${className ?? ""}`}>
      {label}
    </span>
  );
}
