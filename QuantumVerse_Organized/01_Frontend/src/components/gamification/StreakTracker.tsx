import { Flame } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface StreakTrackerProps {
  streak: number;
  className?: string;
}

const DAY_LABELS = ["M", "T", "W", "T", "F", "S", "S"];

export function StreakTracker({ streak, className }: StreakTrackerProps) {
  const today = new Date().getDay(); // 0 = Sunday
  const activeDays = Math.min(streak, 7);

  return (
    <div className={cn("glass rounded-xl border border-white/5 p-5", className)}>
      <div className="flex items-center gap-3 mb-5">
        <motion.div
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
        >
          <Flame className={cn("w-6 h-6", streak > 0 ? "text-orange-400" : "text-muted-foreground/30")} />
        </motion.div>
        <div>
          <p className="font-bold text-white">{streak} day{streak !== 1 ? "s" : ""}</p>
          <p className="text-xs text-muted-foreground">Current streak</p>
        </div>
      </div>

      <div className="flex gap-1.5 justify-between">
        {DAY_LABELS.map((label, i) => {
          const dayIndex = (i + 1) % 7; // Mon=1...Sun=0
          const isActive = activeDays >= (7 - ((today - dayIndex + 7) % 7));
          return (
            <div key={i} className="flex flex-col items-center gap-1.5">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className={cn(
                  "w-8 h-8 rounded-lg flex items-center justify-center text-sm",
                  isActive ? "bg-orange-500/20 border border-orange-500/40" : "bg-white/5 border border-white/5"
                )}
              >
                {isActive ? <Flame className="w-4 h-4 text-orange-400" /> : <div className="w-2 h-2 rounded-full bg-white/20" />}
              </motion.div>
              <span className="text-[10px] text-muted-foreground">{label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
