"use client";

import { cn } from "@/lib/utils";

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  description?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  children?: React.ReactNode;
  eyebrow?: string;
  className?: string;
}

export function PageHeader({
  title,
  subtitle,
  description,
  icon,
  action,
  children,
  eyebrow,
  className,
}: PageHeaderProps) {
  const supportingText = subtitle ?? description;

  return (
    <header
      className={cn(
        "relative mb-8 overflow-hidden rounded-2xl border border-white/[0.08]",
        "bg-white/[0.025] px-5 py-6 backdrop-blur-xl",
        "shadow-[0_16px_50px_rgba(0,0,0,0.18)]",
        "sm:px-7 sm:py-7",
        className
      )}
    >
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -left-20 -top-20 h-48 w-48 rounded-full bg-cyan-400/[0.08] blur-3xl"
      />

      <div
        aria-hidden="true"
        className="pointer-events-none absolute -bottom-24 right-0 h-40 w-40 rounded-full bg-violet-500/[0.06] blur-3xl"
      />

      <div
        aria-hidden="true"
        className="absolute left-0 top-0 h-px w-32 bg-gradient-to-r from-cyan-400/60 to-transparent"
      />

      <div className="relative flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex min-w-0 items-start gap-4">
          {icon && (
            <div
              className={cn(
                "flex h-11 w-11 shrink-0 items-center justify-center rounded-xl",
                "border border-cyan-400/15 bg-cyan-400/[0.07]",
                "text-cyan-300",
                "shadow-[0_0_24px_rgba(0,212,255,0.06)]"
              )}
            >
              {icon}
            </div>
          )}

          <div className="min-w-0">
            {eyebrow && (
              <p className="qv-label mb-2 text-cyan-400/70">
                {eyebrow}
              </p>
            )}

            <h1 className="text-2xl font-semibold tracking-tight text-white sm:text-3xl">
              {title}
            </h1>

            {supportingText && (
              <p className="mt-2 max-w-2xl text-sm leading-6 text-white/45 sm:text-[15px]">
                {supportingText}
              </p>
            )}
          </div>
        </div>

        {(action || children) && (
          <div className="shrink-0">
            {action ?? children}
          </div>
        )}
      </div>
    </header>
  );
}