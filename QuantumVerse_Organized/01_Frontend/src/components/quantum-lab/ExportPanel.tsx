"use client";
import { useState } from "react";
import { Download, Copy, Check } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { api } from "@/lib/api";

type Format = "qasm" | "python" | "json";

interface ExportPanelProps {
  qubits: number;
  classicalBits: number;
  operations: any[];
}

export function ExportPanel({ qubits, classicalBits, operations }: ExportPanelProps) {
  const [format, setFormat] = useState<Format>("python");
  const [code, setCode]     = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied]   = useState(false);

  async function generate() {
    setLoading(true);
    try {
      const res = await api.post("/export/circuit", { qubits, classical_bits: classicalBits, operations, format });
      setCode(String(res.data ?? ""));
    } finally {
      setLoading(false);
    }
  }

  function copy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function download() {
    const ext = format === "python" ? "py" : format === "json" ? "json" : "qasm";
    const blob = new Blob([code], { type: "text/plain" });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href = url; a.download = `circuit.${ext}`;
    a.click(); URL.revokeObjectURL(url);
  }

  return (
    <div className="glass rounded-xl border border-white/5 p-5">
      <h3 className="text-sm font-semibold text-white mb-4">Export Circuit</h3>

      <div className="flex gap-1 p-1 bg-white/5 rounded-lg mb-4">
        {(["python", "qasm", "json"] as Format[]).map(f => (
          <button key={f} onClick={() => setFormat(f)}
            className={`flex-1 py-1.5 rounded-md text-xs font-medium transition-all ${
              format === f ? "bg-quantum-blue/15 text-quantum-blue" : "text-muted-foreground hover:text-white"
            }`}>
            {f.toUpperCase()}
          </button>
        ))}
      </div>

      <GlowButton onClick={generate} loading={loading} className="w-full justify-center mb-4">
        Generate Code
      </GlowButton>

      {code && (
        <>
          <div className="relative">
            <pre className="p-4 bg-[#0d0d1a] border border-white/10 rounded-xl text-xs text-green-400 overflow-auto max-h-48 font-mono">{code}</pre>
            <button onClick={copy} className="absolute top-2 right-2 p-1.5 bg-white/5 hover:bg-white/10 rounded-md transition">
              {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5 text-muted-foreground" />}
            </button>
          </div>
          <GlowButton variant="secondary" onClick={download} className="w-full justify-center mt-3">
            <Download className="w-4 h-4" /> Download
          </GlowButton>
        </>
      )}
    </div>
  );
}
