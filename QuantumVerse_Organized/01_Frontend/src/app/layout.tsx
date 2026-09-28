import type { Metadata } from "next";
import { JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "QuantumVerse AI — Learn. Build. Simulate. Understand Quantum Computing.",
  description: "AI-Powered Interactive Quantum Algorithm Learning and Simulation Platform",
  keywords: ["quantum computing", "qiskit", "quantum circuits", "AI tutor", "quantum education"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${jetbrainsMono.variable}`}>
      <body>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            style: { background: "#0D1F3C", color: "#e2e8f0", border: "1px solid rgba(0,212,255,0.2)" },
            success: { iconTheme: { primary: "#06FFA5", secondary: "#050A1A" } },
            error: { iconTheme: { primary: "#f87171", secondary: "#050A1A" } },
          }}
        />
      </body>
    </html>
  );
}
