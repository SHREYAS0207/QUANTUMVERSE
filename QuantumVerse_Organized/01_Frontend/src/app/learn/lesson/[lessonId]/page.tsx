"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import {
  ArrowLeft,
  CheckCircle2,
  Code2,
  Info,
  Lightbulb,
  PlayCircle,
  TriangleAlert,
  Zap,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { QuantumCard } from "@/components/shared/QuantumCard";
import api from "@/lib/api";
import toast from "react-hot-toast";
import type {
  ContentBlock,
  Lesson,
  LessonContent,
} from "@/types/learning";

function ContentRenderer({
  content,
}: {
  content?: LessonContent;
}) {
  if (!content?.blocks?.length) {
    return (
      <QuantumCard>
        <div className="py-10 text-center">
          <PlayCircle className="w-10 h-10 text-muted-foreground/30 mx-auto mb-3" />

          <p className="text-sm text-muted-foreground">
            Lecture content for this lesson is being prepared.
          </p>
        </div>
      </QuantumCard>
    );
  }

  return (
    <div className="space-y-4">
      {content.blocks.map(
        (block: ContentBlock, index) => {
          if (block.type === "heading") {
            const Tag =
              block.level === 1
                ? "h2"
                : block.level === 2
                ? "h3"
                : "h4";

            return (
              <Tag
                key={index}
                className="text-white font-bold text-xl mt-7 first:mt-0"
              >
                {block.content}
              </Tag>
            );
          }

          if (block.type === "text") {
            return (
              <p
                key={index}
                className="text-sm md:text-base text-muted-foreground leading-8"
              >
                {block.content}
              </p>
            );
          }

          if (block.type === "math") {
            return (
              <div
                key={index}
                className="rounded-xl border border-quantum-blue/15 bg-quantum-blue/5 px-5 py-4 font-mono text-sm text-quantum-cyan overflow-x-auto"
              >
                {block.content}
              </div>
            );
          }

          if (block.type === "code") {
            return (
              <div
                key={index}
                className="rounded-xl overflow-hidden border border-white/10"
              >
                <div className="px-4 py-2 bg-white/5 text-xs text-muted-foreground flex items-center gap-2">
                  <Code2 className="w-3.5 h-3.5" />
                  {block.language}
                </div>

                <pre className="p-4 bg-black/30 overflow-x-auto text-xs text-white/80">
                  <code>{block.content}</code>
                </pre>
              </div>
            );
          }

          if (block.type === "callout") {
            const Icon =
              block.variant === "warning"
                ? TriangleAlert
                : block.variant === "tip"
                ? Lightbulb
                : Info;

            return (
              <div
                key={index}
                className="rounded-xl border border-quantum-blue/20 bg-quantum-blue/5 p-4 flex gap-3"
              >
                <Icon className="w-4 h-4 flex-shrink-0 mt-0.5 text-quantum-cyan" />

                <p className="text-sm leading-6 text-blue-100">
                  {block.content}
                </p>
              </div>
            );
          }

          if (block.type === "circuit") {
            return (
              <div
                key={index}
                className="rounded-xl border border-purple-500/20 bg-purple-500/5 p-4 text-sm text-muted-foreground"
              >
                Circuit visualization data is available for this lesson.
              </div>
            );
          }

          return null;
        }
      )}
    </div>
  );
}
function YouTubeVideo({ url }: { url?: string | null }) {
  if (!url) return null;

  function getYouTubeId(value: string) {
    try {
      const parsed = new URL(value);

      if (parsed.hostname.includes("youtu.be")) {
        return parsed.pathname.slice(1);
      }

      if (parsed.hostname.includes("youtube.com")) {
        return (
          parsed.searchParams.get("v") ||
          parsed.pathname.split("/").pop() ||
          ""
        );
      }
    } catch {
      return "";
    }

    return "";
  }

  const videoId = getYouTubeId(url);

  if (!videoId) return null;

  return (
    <QuantumCard className="mt-6 overflow-hidden">
      <div className="mb-4">
        <div className="flex items-center gap-2">
          <PlayCircle className="w-5 h-5 text-quantum-cyan" />
          <h2 className="text-lg font-bold text-white">
            Watch the Lecture
          </h2>
        </div>

        <p className="text-sm text-muted-foreground mt-1">
          Reinforce the concepts covered in this lesson.
        </p>
      </div>

      <div className="relative w-full aspect-video rounded-xl overflow-hidden bg-black border border-white/10">
        <iframe
          src={`https://www.youtube.com/embed/${videoId}`}
          title="QuantumVerse lesson video"
          className="absolute inset-0 w-full h-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
        />
      </div>

      <div className="mt-4">
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-quantum-cyan hover:underline"
        >
          Watch directly on YouTube →
        </a>
      </div>
    </QuantumCard>
  );
}
export default function LessonPage() {
  const params = useParams<{ lessonId: string }>();
  const searchParams = useSearchParams();

  const level = searchParams.get("level") || "1";

  const [lesson, setLesson] = useState<Lesson | null>(
    null
  );

  const [loading, setLoading] = useState(true);
  const [completed, setCompleted] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api
      .get(`/learning/lessons/${params.lessonId}`)
      .then((r) => setLesson(r.data))
      .catch(() => toast.error("Failed to load lecture"))
      .finally(() => setLoading(false));
  }, [params.lessonId]);

  async function markComplete() {
    if (!lesson || completed) return;

    setSaving(true);

    try {
      const { data } = await api.post(
        `/learning/lessons/${lesson.id}/complete`
      );

      setCompleted(true);

      toast.success(
        `Lesson complete · +${data.xp_earned} XP`
      );
    } catch {
      toast.error("Could not mark the lesson complete");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
        </div>
      </AppShell>
    );
  }

  if (!lesson) {
    return (
      <AppShell>
        <div className="text-center py-20 text-muted-foreground">
          Lecture not found.
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex items-center justify-between gap-3">
          <Link
            href={`/learn/level/${level}`}
            className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Level {level}
          </Link>

          {completed && (
            <span className="inline-flex items-center gap-2 text-xs text-green-400">
              <CheckCircle2 className="w-4 h-4" />
              Completed
            </span>
          )}
        </div>

        <div className="glass rounded-2xl border border-white/5 overflow-hidden mb-6">
          <div className="h-1.5 bg-gradient-to-r from-quantum-blue to-quantum-cyan" />

          <div className="p-6 md:p-8">
            <p className="text-xs uppercase tracking-widest text-muted-foreground">
              Lecture
            </p>

            <h1 className="text-3xl font-bold text-white mt-2">
              {lesson.title}
            </h1>

            <div className="flex flex-wrap items-center gap-4 mt-4 text-xs text-muted-foreground">
              <span>{lesson.estimated_minutes} minutes</span>

              <span className="flex items-center gap-1 text-yellow-400">
                <Zap className="w-3 h-3" />
                {lesson.xp_reward} XP
              </span>
            </div>
          </div>
        </div>

        <ContentRenderer content={lesson.content} />
        <YouTubeVideo url={lesson.youtube_url} />
        <div className="mt-8 flex flex-col sm:flex-row gap-3">
          <button
            onClick={markComplete}
            disabled={completed || saving}
            className="flex-1 inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-quantum-blue text-quantum-dark font-bold disabled:opacity-50"
          >
            <CheckCircle2 className="w-4 h-4" />

            {saving
              ? "Saving..."
              : completed
              ? "Lesson Completed"
              : "Mark Lesson Complete"}
          </button>

          <Link
            href="/quiz"
            className="flex-1 inline-flex items-center justify-center gap-2 py-3 rounded-xl border border-white/10 text-white font-medium hover:border-white/20 transition-colors"
          >
            <Zap className="w-4 h-4" />
            Go to Level Quiz
          </Link>
        </div>
      </div>
    </AppShell>
  );
}
