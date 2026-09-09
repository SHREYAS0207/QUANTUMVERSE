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
