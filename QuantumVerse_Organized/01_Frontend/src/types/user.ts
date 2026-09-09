export interface User {
  id: string;
  name: string;
  email: string;
  learning_level: "beginner" | "intermediate" | "advanced";
  xp: number;
  level: number;
  streak_days: number;
  statistics: UserStatistics;
}

export interface UserStatistics {
  total_lessons: number;
  total_circuits: number;
  total_quizzes: number;
  quiz_accuracy: number;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
  user_id: string;
  name: string;
  email: string;
  learning_level: string;
}
