"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { Sidebar } from "./Sidebar";

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
    <div className="relative min-h-screen bg-black text-white">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(ellipse_at_top,rgba(0,255,240,0.08),transparent_30%),radial-gradient(ellipse_at_bottom_right,rgba(191,0,255,0.10),transparent_35%)]" />
      <Sidebar />
      <main className="ml-64 flex-1 min-h-screen relative z-10">
        <div className="p-8">{children}</div>
      </main>
    </div>
  );
}
