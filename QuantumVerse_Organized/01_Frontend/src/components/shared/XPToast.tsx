"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Zap } from "lucide-react";

interface XPToastProps {
  xp: number;
  visible: boolean;
  show?: boolean;
  onComplete?: () => void;
}

export function XPToast({
  xp,
  visible,
  show,
  onComplete,
}: XPToastProps) {
  const isVisible = show ?? visible;

  return (
    <AnimatePresence onExitComplete={onComplete}>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 12, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -8, scale: 0.95 }}
          transition={{ duration: 0.2 }}
          className="fixed bottom-6 right-6 z-50"
        >
          <div className="flex items-center gap-3 rounded-2xl border border-cyan-400/20 bg-black/80 px-4 py-3 shadow-[0_0_30px_rgba(0,212,255,0.15)] backdrop-blur-xl">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-400/20 bg-cyan-400/[0.08]">
              <Zap className="h-4 w-4 text-cyan-300" />
            </div>

            <div>
              <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-white/40">
                Experience gained
              </p>

              <p className="text-sm font-semibold text-cyan-300">
                +{xp} XP
              </p>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}