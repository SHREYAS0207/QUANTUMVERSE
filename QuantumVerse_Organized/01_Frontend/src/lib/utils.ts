import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatXP(xp: number): string {
  if (xp >= 1000) return `${(xp / 1000).toFixed(1)}k XP`;
  return `${xp} XP`;
}

export function getLevelFromXP(xp: number, xpPerLevel = 500): number {
  return Math.floor(xp / xpPerLevel) + 1;
}

export function getXPProgress(xp: number, xpPerLevel = 500): number {
  return (xp % xpPerLevel) / xpPerLevel * 100;
}

export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return s > 0 ? `${m}m ${s}s` : `${m}m`;
}
