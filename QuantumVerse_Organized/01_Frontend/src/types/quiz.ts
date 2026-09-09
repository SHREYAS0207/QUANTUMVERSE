export interface QuizOption {
  id: string;
  text: string;
}

export interface Question {
  id: string;
  question_text: string;
  question_type: "mcq" | "true_false" | "circuit_predict" | "gate_identify";
  options: QuizOption[];
}

export interface Quiz {
  id: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  time_limit_seconds: number;
  xp_reward: number;
  questions: Question[];
}

export interface QuizResult {
  score: number;
  total: number;
  accuracy: number;
  xp_earned: number;
  answers: AnswerResult[];
}

export interface AnswerResult {
  question_id: string;
  user_answer: string;
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
}
