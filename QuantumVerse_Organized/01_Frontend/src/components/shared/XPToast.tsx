"use client";
import { motion, AnimatePresence } from "framer-motion";
import { Zap } from "lucide-react";

interface XPToastProps {
  xp: number;
  visible: boolean;
}

export function XPToast({ xp, visible }: XPToastProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.8 }}
          className="fixed bottom-8 right-8 z-50 flex items-center gap-2 px-5 py-3 rounded-2xl bg-quantum-blue text-quantum-dark font-bold shadow-[0_0_30px_rgba(0,212,255,0.4)]"
        >
          <Zap className="w-5 h-5" />
          <span>+{xp} XP</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
