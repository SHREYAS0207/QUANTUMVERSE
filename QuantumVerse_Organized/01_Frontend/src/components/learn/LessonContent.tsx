"use client";

import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { Check, Copy } from "lucide-react";

interface LessonContentProps {
  content?: string;
}

function CopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard access can be unavailable in restricted browser contexts.
    }
  }

  return (
    <button
      type="button"
      onClick={copy}
      aria-label={copied ? "Code copied" : "Copy code"}
      title={copied ? "Copied" : "Copy code"}
      className={[
        "absolute right-3 top-3 z-10 inline-flex h-8 w-8 items-center justify-center",
        "rounded-lg border border-white/[0.08] bg-black/40",
        "text-white/40 backdrop-blur-md",
        "transition-all duration-200",
        "hover:border-cyan-400/20 hover:bg-cyan-400/[0.08] hover:text-cyan-300",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400/50",
      ].join(" ")}
    >
      {copied ? (
        <Check className="h-3.5 w-3.5 text-emerald-300" />
      ) : (
        <Copy className="h-3.5 w-3.5" />
      )}
    </button>
  );
}

export function LessonContent({ content }: LessonContentProps) {
  return (
    <article className="qv-lesson-content max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || "");
            const code = String(children).replace(/\n$/, "");

            if (!inline && match) {
              return (
                <div className="group relative my-7 overflow-hidden rounded-2xl border border-white/[0.08] bg-[#07090d] shadow-[0_16px_50px_rgba(0,0,0,0.3)]">
                  <div
                    aria-hidden="true"
                    className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-400/30 to-transparent"
                  />

                  <div className="flex h-10 items-center justify-between border-b border-white/[0.06] bg-white/[0.025] px-4">
                    <div className="flex items-center gap-2">
                      <span className="flex gap-1.5" aria-hidden="true">
                        <span className="h-2 w-2 rounded-full bg-red-400/60" />
                        <span className="h-2 w-2 rounded-full bg-amber-400/60" />
                        <span className="h-2 w-2 rounded-full bg-emerald-400/60" />
                      </span>

                      <span className="ml-2 font-mono text-[10px] font-medium uppercase tracking-[0.12em] text-white/30">
                        {match[1]}
                      </span>
                    </div>

                    <span className="font-mono text-[9px] uppercase tracking-[0.12em] text-white/15">
                      quantumverse
                    </span>
                  </div>

                  <SyntaxHighlighter
                    style={vscDarkPlus as any}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                    customStyle={{
                      margin: 0,
                      padding: "1.25rem",
                      paddingTop: "1.15rem",
                      background: "transparent",
                      fontSize: "0.8rem",
                      lineHeight: "1.75",
                    }}
                    codeTagProps={{
                      style: {
                        fontFamily:
                          "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
                      },
                    }}
                  >
                    {code}
                  </SyntaxHighlighter>

                  <CopyButton code={code} />
                </div>
              );
            }

            return (
              <code
                className={[
                  "rounded-md border border-cyan-400/10",
                  "bg-cyan-400/[0.06] px-1.5 py-0.5",
                  "font-mono text-[0.88em] text-cyan-300",
                ].join(" ")}
                {...props}
              >
                {children}
              </code>
            );
          },

          h1: ({ children }) => (
            <h1 className="mb-7 mt-0 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
              <span className="bg-gradient-to-r from-white via-white to-cyan-200 bg-clip-text text-transparent">
                {children}
              </span>
            </h1>
          ),

          h2: ({ children }) => (
            <div className="mt-10 mb-5">
              <h2 className="flex items-center gap-3 text-xl font-semibold tracking-tight text-white sm:text-2xl">
                <span
                  aria-hidden="true"
                  className="h-5 w-1 rounded-full bg-cyan-400 shadow-[0_0_14px_rgba(0,212,255,0.35)]"
                />
                {children}
              </h2>
              <div
                aria-hidden="true"
                className="mt-3 h-px bg-gradient-to-r from-cyan-400/15 via-white/[0.06] to-transparent"
              />
            </div>
          ),

          h3: ({ children }) => (
            <h3 className="mb-3 mt-7 text-lg font-semibold tracking-tight text-white/90">
              <span className="text-cyan-400/60">/</span>{" "}
              {children}
            </h3>
          ),

          p: ({ children }) => (
            <p className="mb-5 text-[15px] leading-7 text-white/55 sm:text-base">
              {children}
            </p>
          ),

          ul: ({ children }) => (
            <ul className="mb-6 space-y-2.5 pl-1">{children}</ul>
          ),

          ol: ({ children }) => (
            <ol className="mb-6 space-y-3 pl-6 text-white/55 marker:font-semibold marker:text-cyan-400">
              {children}
            </ol>
          ),

          li: ({ children }) => (
            <li className="flex gap-3 text-[15px] leading-7 text-white/55 sm:text-base">
              <span
                aria-hidden="true"
                className="mt-[0.72rem] h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(0,212,255,0.45)]"
              />
              <span className="min-w-0">{children}</span>
            </li>
          ),

          blockquote: ({ children }) => (
            <blockquote className="relative my-7 overflow-hidden rounded-xl border border-cyan-400/10 bg-cyan-400/[0.045] px-5 py-4 text-white/55 not-italic">
              <div
                aria-hidden="true"
                className="absolute bottom-0 left-0 top-0 w-0.5 bg-gradient-to-b from-cyan-300 via-cyan-400 to-violet-400"
              />
              <div className="text-[15px] leading-7 [&>p]:mb-0">
                {children}
              </div>
            </blockquote>
          ),

          strong: ({ children }) => (
            <strong className="font-semibold text-white">{children}</strong>
          ),

          em: ({ children }) => (
            <em className="text-cyan-100/70">{children}</em>
          ),

          a: ({ children, href }) => (
            <a
              href={href}
              target="_blank"
              rel="noreferrer"
              className="font-medium text-cyan-300 underline decoration-cyan-400/30 underline-offset-4 transition-colors hover:text-cyan-200 hover:decoration-cyan-400/70"
            >
              {children}
            </a>
          ),

          hr: () => (
            <div className="my-9 h-px bg-gradient-to-r from-transparent via-white/[0.09] to-transparent" />
          ),

          table: ({ children }) => (
            <div className="my-7 overflow-x-auto rounded-2xl border border-white/[0.08] bg-white/[0.015]">
              <table className="w-full min-w-[520px] border-collapse">
                {children}
              </table>
            </div>
          ),

          thead: ({ children }) => (
            <thead className="bg-white/[0.035]">{children}</thead>
          ),

          th: ({ children }) => (
            <th className="border-b border-white/[0.08] px-4 py-3.5 text-left text-[10px] font-semibold uppercase tracking-[0.1em] text-cyan-300/70">
              {children}
            </th>
          ),

          td: ({ children }) => (
            <td className="border-b border-white/[0.05] px-4 py-3.5 text-sm leading-6 text-white/50">
              {children}
            </td>
          ),

          tr: ({ children }) => (
            <tr className="transition-colors hover:bg-white/[0.025]">
              {children}
            </tr>
          ),

          del: ({ children }) => (
            <del className="text-white/30">{children}</del>
          ),
        }}
      >
        {content ?? ""}
      </ReactMarkdown>
    </article>
  );
}