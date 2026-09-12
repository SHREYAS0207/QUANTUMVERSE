"use client";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { Atom, Moon, Bell, Shield, ExternalLink } from "lucide-react";

const SECTIONS: Array<{
  title: string;
  icon: typeof Moon;
  items: Array<{
    label: string;
    description: string;
    type: "static" | "toggle" | "button" | "button-danger";
    value?: string;
    default?: boolean;
  }>;
}> = [
  {
    title: "Appearance",
    icon: Moon,
    items: [
      { label: "Theme", description: "Dark quantum mode", value: "Dark (Default)", type: "static" },
      { label: "Animations", description: "Reduce motion for accessibility", type: "toggle", default: true },
    ],
  },
  {
    title: "Notifications",
    icon: Bell,
    items: [
      { label: "Daily Reminder", description: "Get reminded to continue learning", type: "toggle", default: true },
    ],
  },
  {
    title: "Privacy & Security",
    icon: Shield,
    items: [
      { label: "Change Password", description: "Update your account password", type: "button" },
      { label: "Delete Account", description: "Permanently remove your account", type: "button-danger" },
    ],
  },
];

export default function SettingsPage() {
  return (
    <AppShell>
      <PageHeader title="Settings" subtitle="Customize your QuantumVerse experience" />
      <div className="max-w-2xl space-y-5">
        {SECTIONS.map((section) => (
          <QuantumCard key={section.title}>
            <div className="flex items-center gap-2 mb-4">
              <section.icon className="w-4 h-4 text-quantum-blue" />
              <h3 className="text-sm font-semibold text-white">{section.title}</h3>
            </div>
            <div className="space-y-4">
              {section.items.map((item) => (
                <div key={item.label} className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-white">{item.label}</p>
                    <p className="text-xs text-muted-foreground">{item.description}</p>
                  </div>
                  {item.type === "toggle" && (
                    <div className="w-10 h-5 rounded-full bg-quantum-blue/20 border border-quantum-blue/30 relative cursor-pointer">
                      <div className="absolute right-0.5 top-0.5 w-4 h-4 rounded-full bg-quantum-blue transition-all" />
                    </div>
                  )}
                  {item.type === "static" && (
                    <span className="text-xs text-muted-foreground border border-white/10 px-2 py-1 rounded-lg">{item.value}</span>
                  )}
                  {item.type === "button" && (
                    <button className="text-xs px-3 py-1.5 rounded-lg border border-white/10 text-muted-foreground hover:text-white hover:border-white/20 transition-all">
                      Update
                    </button>
                  )}
                  {item.type === "button-danger" && (
                    <button className="text-xs px-3 py-1.5 rounded-lg border border-red-500/20 text-red-400 hover:bg-red-500/10 transition-all">
                      Delete
                    </button>
                  )}
                </div>
              ))}
            </div>
          </QuantumCard>
        ))}

        {/* About */}
        <QuantumCard>
          <div className="flex items-center gap-3">
            <Atom className="w-8 h-8 text-quantum-blue" />
            <div>
              <p className="text-sm font-bold text-white">QuantumVerse AI</p>
              <p className="text-xs text-muted-foreground">v1.0.0</p>
            </div>
            <a href="/" className="ml-auto text-muted-foreground hover:text-white transition-colors">
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </QuantumCard>
      </div>
    </AppShell>
  );
}
