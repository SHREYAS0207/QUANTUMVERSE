"use client";
import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { Copy, Check } from "lucide-react";
import { useState } from "react";

interface LessonContentProps {
  content?: string;
}

function CopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);
  function copy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }
  return (
    <button onClick={copy}
      className="absolute top-3 right-3 p-1.5 rounded-md bg-white/5 hover:bg-white/10 text-muted-foreground hover:text-white transition-colors">
      {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
    </button>
  );
}

export function LessonContent({ content }: LessonContentProps) {
  return (
    <article className="prose prose-invert prose-quantum max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || "");
            const code = String(children).replace(/\n$/, "");
            if (!inline && match) {
              return (
                <div className="relative group my-5">
                  <div className="absolute top-0 left-0 px-3 py-1 text-xs text-muted-foreground font-mono bg-white/5 rounded-tl-lg rounded-br-lg">
                    {match[1]}
                  </div>
                  <SyntaxHighlighter
                    style={vscDarkPlus as any}
                    language={match[1]}
                    PreTag="div"
                    className="!rounded-xl !bg-[#0d0d1a] !border !border-white/10 !pt-8"
                    {...props}
                  >
                    {code}
                  </SyntaxHighlighter>
                  <CopyButton code={code} />
                </div>
              );
            }
            return (
              <code className="px-1.5 py-0.5 rounded bg-white/10 text-quantum-blue font-mono text-sm" {...props}>
                {children}
              </code>
            );
          },
          h1: ({ children }) => <h1 className="text-3xl font-bold text-white mb-6 mt-0">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-semibold text-white/90 mb-4 mt-8 pb-2 border-b border-white/10">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-semibold text-white/80 mb-3 mt-6">{children}</h3>,
          p:  ({ children }) => <p className="text-muted-foreground leading-relaxed mb-4">{children}</p>,
          ul: ({ children }) => <ul className="space-y-1 mb-4 pl-4">{children}</ul>,
          ol: ({ children }) => <ol className="space-y-1 mb-4 pl-4 list-decimal">{children}</ol>,
          li: ({ children }) => <li className="text-muted-foreground flex gap-2"><span className="text-quantum-blue mt-1">›</span><span>{children}</span></li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-quantum-blue pl-4 py-1 my-4 bg-quantum-blue/5 rounded-r-lg text-muted-foreground italic">
              {children}
            </blockquote>
          ),
          strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
          table: ({ children }) => (
            <div className="overflow-x-auto my-6">
              <table className="w-full border-collapse border border-white/10 rounded-lg overflow-hidden">{children}</table>
            </div>
          ),
          th: ({ children }) => <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase bg-white/5 border-b border-white/10">{children}</th>,
          td: ({ children }) => <td className="px-4 py-3 text-sm text-muted-foreground border-b border-white/5">{children}</td>,
        }}
      >
        {content ?? ""}
      </ReactMarkdown>
    </article>
  );
}
