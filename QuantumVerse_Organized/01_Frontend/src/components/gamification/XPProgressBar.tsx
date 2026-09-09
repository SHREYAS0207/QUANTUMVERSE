import { motion } from "framer-motion";

interface XPProgressBarProps {
  xp: number;
  level: number;
  animated?: boolean;
}

const XP_PER_LEVEL = 500;

export function XPProgressBar({ xp, level, animated = true }: XPProgressBarProps) {
  const xpInLevel   = xp % XP_PER_LEVEL;
  const xpNeeded    = XP_PER_LEVEL;
  const percent     = Math.min((xpInLevel / xpNeeded) * 100, 100);

  return (
    <div className="w-full">
      <div className="flex justify-between text-xs text-muted-foreground mb-1.5">
        <span>Level {level}</span>
        <span>{xpInLevel} / {xpNeeded} XP</span>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-quantum-blue to-quantum-purple"
          initial={animated ? { width: 0 } : { width: `${percent}%` }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
        />
      </div>
      <div className="text-right text-[10px] text-muted-foreground/60 mt-1">
        {Math.round(xpNeeded - xpInLevel)} XP to Level {level + 1}
      </div>
    </div>
  );
}
