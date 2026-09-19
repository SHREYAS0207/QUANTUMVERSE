"use client";
import { useState } from "react";
import { Wand2, Loader2 } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { api } from "@/lib/api";

interface AICircuitGeneratorProps {
  onGenerated: (circuit: any) => void;
}

const EXAMPLES = [
  "Create a Bell state circuit",
  "Build a 3-qubit GHZ state",
  "Make a superposition of all states",
  "Show me a 2-qubit QFT",
];

export function AICircuitGenerator({ onGenerated }: AICircuitGeneratorProps) {
  const [prompt,  setPrompt]  = useState("");
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState("");

  async function generate() {
    if (!prompt.trim()) return;
    setLoading(true); setError("");
    try {
      const res = await api.post("/ai-circuit/generate", { description: prompt });
      const data = res.data;
      onGenerated(data);
      setPrompt("");
    } catch (e: any) {
      setError(e.message ?? "Generation failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="glass rounded-xl border border-white/5 p-5">
      <div className="flex items-center gap-2 mb-3">
        <Wand2 className="w-4 h-4 text-quantum-blue" />
        <h3 className="text-sm font-semibold text-white">AI Circuit Generator</h3>
      </div>

      <div className="flex gap-2 mb-3">
        <input
          value={prompt} onChange={e => setPrompt(e.target.value)}
          onKeyDown={e => e.key === "Enter" && generate()}
          placeholder="Describe a circuit in plain English..."
          className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-quantum-blue/50"
        />
        <GlowButton onClick={generate} loading={loading} disabled={!prompt.trim()}>
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Wand2 className="w-4 h-4" />}
        </GlowButton>
      </div>

      {error && <p className="text-red-400 text-xs mb-3">{error}</p>}

      <div className="flex flex-wrap gap-2">
        {EXAMPLES.map(ex => (
          <button key={ex} onClick={() => setPrompt(ex)}
            className="text-xs px-2.5 py-1 rounded-full border border-white/10 text-muted-foreground hover:border-quantum-blue/30 hover:text-quantum-blue transition-colors">
            {ex}
          </button>
        ))}
      </div>
    </div>
  );
}
