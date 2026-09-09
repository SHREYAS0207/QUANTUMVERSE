"use client";
import { motion, AnimatePresence } from "framer-motion";
import { Star, X } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";

interface LevelUpModalProps {
  visible: boolean;
  newLevel: number;
  onClose: () => void;
}

export function LevelUpModal({ visible, newLevel, onClose }: LevelUpModalProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <motion.div className="relative glass border border-quantum-blue/30 rounded-2xl p-10 max-w-sm w-full mx-4 text-center overflow-hidden"
            initial={{ scale: 0.7, y: 40 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.7, y: 40 }}
            transition={{ type: "spring", stiffness: 300, damping: 24 }}>

            {/* Background glow */}
            <div className="absolute inset-0 bg-quantum-blue/5 rounded-2xl" />

            {/* Stars animation */}
            {[...Array(6)].map((_, i) => (
              <motion.div key={i}
                className="absolute text-yellow-400"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: [0, 1, 0], scale: [0, 1, 0], x: Math.cos(i * 60 * Math.PI / 180) * 80, y: Math.sin(i * 60 * Math.PI / 180) * 80 }}
                transition={{ delay: 0.3 + i * 0.1, duration: 1.2 }}
                style={{ left: "50%", top: "40%" }}
              >
                <Star className="w-5 h-5 fill-current" />
              </motion.div>
            ))}

            <button onClick={onClose} className="absolute top-4 right-4 text-muted-foreground hover:text-white">
              <X className="w-4 h-4" />
            </button>

            {/* Badge */}
            <motion.div
              className="w-24 h-24 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center mx-auto mb-6 shadow-[0_0_40px_rgba(0,212,255,0.4)]"
              initial={{ rotate: -180, scale: 0 }}
              animate={{ rotate: 0, scale: 1 }}
              transition={{ type: "spring", stiffness: 200, damping: 15 }}
            >
              <span className="text-4xl font-black text-quantum-dark">{newLevel}</span>
            </motion.div>

            <h2 className="text-2xl font-bold text-white mb-2">Level Up!</h2>
            <p className="text-muted-foreground mb-2">You've reached</p>
            <p className="text-quantum-blue font-bold text-lg mb-6">Level {newLevel}</p>

            <GlowButton onClick={onClose} className="w-full justify-center">
              Keep Learning!
            </GlowButton>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
