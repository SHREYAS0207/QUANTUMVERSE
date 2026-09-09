import Link from "next/link";
import { Home, AtomIcon } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4 bg-quantum-dark">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[400px] h-[400px] rounded-full bg-quantum-blue/5 blur-3xl" />
      </div>
      <p className="text-8xl font-black text-quantum-blue/20 mb-4">404</p>
      <h1 className="text-2xl font-bold text-white mb-2">This state has collapsed</h1>
      <p className="text-muted-foreground text-sm mb-8 max-w-sm">
        Like a measured qubit, this page only exists in superposition. Try navigating back.
      </p>
      <Link href="/dashboard"
        className="flex items-center gap-2 px-6 py-3 rounded-xl bg-quantum-blue text-quantum-dark font-semibold text-sm hover:opacity-90 transition-opacity">
        <Home className="w-4 h-4" /> Back to Dashboard
      </Link>
    </div>
  );
}
