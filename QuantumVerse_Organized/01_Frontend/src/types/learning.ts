export interface LearningModule {
  id: string;
  title: string;
  description: string;
  level: number;
  icon: string;
  lesson_count: number;
}

export interface Lesson {
  id: string;
  title: string;
  order_index: number;
  xp_reward: number;
  estimated_minutes: number;
  youtube_url?: string | null;
  content?: LessonContent;
}

export interface LessonContent {
  blocks: ContentBlock[];
}

export type ContentBlock =
  | { type: "text"; content: string }
  | { type: "heading"; level: 1 | 2 | 3; content: string }
  | { type: "math"; content: string }
  | { type: "code"; language: string; content: string }
  | { type: "callout"; variant: "info" | "warning" | "tip"; content: string }
  | { type: "circuit"; circuit_data: object };

export interface ProgressData {
  completed: string[];
  in_progress: string[];
}
