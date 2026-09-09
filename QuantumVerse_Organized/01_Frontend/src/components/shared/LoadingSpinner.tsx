import { cn } from "@/lib/utils";

export function LoadingSpinner({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center justify-center", className)}>
      <div className="w-8 h-8 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
    </div>
  );
}

export function FullPageLoader() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <div className="w-12 h-12 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
      <p className="text-muted-foreground text-sm">Initializing quantum systems...</p>
    </div>
  );
}
