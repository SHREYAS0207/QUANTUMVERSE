"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { Sidebar } from "./Sidebar";
import AtomBackground from "@/components/qlearn-ui/AtomBackground";
import QlearnNavbar from "@/components/qlearn-ui/QlearnNavbar";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  return (
    <div className="qv-shell relative min-h-screen bg-[#030507] text-white">
      <AtomBackground />

      <div className="pointer-events-none fixed inset-0 z-[1] bg-[radial-gradient(ellipse_at_top,rgba(0,255,240,0.055),transparent_34%),radial-gradient(ellipse_at_bottom_right,rgba(170,90,255,0.07),transparent_38%)]" />
      <div className="pointer-events-none fixed left-0 right-0 top-16 z-[2] h-px bg-gradient-to-r from-transparent via-cyan-300/20 to-transparent" />

      <div className="relative z-10">
        <Sidebar />
        <QlearnNavbar />

        <main className="ml-64 min-h-screen flex-1 relative">
          <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-cyan-300/[0.025] to-transparent" />
          <div className="relative p-5 sm:p-6 lg:p-8">{children}</div>
        </main>
      </div>
    </div>
  );
}
