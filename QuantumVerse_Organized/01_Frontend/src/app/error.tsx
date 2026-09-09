"use client";
import { useEffect } from "react";
import { RefreshCw } from "lucide-react";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => { console.error(error); }, [error]);
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
      <p className="text-6xl mb-4">⚠️</p>
      <h2 className="text-xl font-bold text-white mb-2">Something went wrong</h2>
      <p className="text-muted-foreground text-sm mb-6 max-w-sm">{error.message || "An unexpected error occurred."}</p>
      <button onClick={reset}
        className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-quantum-blue text-quantum-dark font-semibold text-sm">
        <RefreshCw className="w-4 h-4" /> Try Again
      </button>
    </div>
  );
}
