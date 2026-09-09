import { cn } from "@/lib/utils";
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
