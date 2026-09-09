"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Trophy, Clock, CheckCircle2, XCircle, ChevronRight, Zap, Target } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import api from "@/lib/api";
import toast from "react-hot-toast";

type QuizState = "list" | "active" | "result";

export default function QuizPage() {
  const [quizzes, setQuizzes] = useState<any[]>([]);
  const [quiz, setQuiz] = useState<any | null>(null);
  const [state, setState] = useState<QuizState>("list");
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any | null>(null);
  const [startTime, setStartTime] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/quiz/quizzes").then((r) => setQuizzes(r.data.quizzes)).catch(() => {});
  }, []);

  const startQuiz = async (quizId: string) => {
    try {
      const { data } = await api.get(`/quiz/quizzes/${quizId}`);
      setQuiz(data);
      setCurrentQ(0);
      setAnswers({});
      setSelectedOption(null);
      setStartTime(Date.now());
      setState("active");
    } catch { toast.error("Failed to load quiz"); }
  };

  const selectOption = (optId: string) => {
    if (selectedOption) return;
    setSelectedOption(optId);
    const q = quiz.questions[currentQ];
    setAnswers((prev) => ({ ...prev, [q.id]: optId }));
  };

  const nextQuestion = () => {
    setSelectedOption(null);
    if (currentQ < quiz.questions.length - 1) {
      setCurrentQ((p) => p + 1);
    } else {
      submitQuiz();
    }
  };

  const submitQuiz = async () => {
    setLoading(true);
    try {
      const time_taken = Math.round((Date.now() - startTime) / 1000);
      const { data } = await api.post(`/quiz/quizzes/${quiz.id}/submit`, { answers, time_taken });
      setResult(data);
      setState("result");
    } catch { toast.error("Failed to submit quiz"); }
    finally { setLoading(false); }
  };

  if (state === "result" && result) {
    const grade = result.accuracy >= 80 ? "Excellent!" : result.accuracy >= 60 ? "Good Job!" : "Keep Practicing";
    return (
      <AppShell>
        <PageHeader title="Quiz Results" />
        <div className="max-w-2xl mx-auto">
          <QuantumCard glow className="text-center mb-6">
            <div className="text-5xl mb-3">{result.accuracy >= 80 ? "🏆" : result.accuracy >= 60 ? "🌟" : "📚"}</div>
            <h2 className="text-2xl font-bold text-white mb-1">{grade}</h2>
            <p className="text-4xl font-black text-quantum-blue mt-2">{result.accuracy}%</p>
            <p className="text-muted-foreground text-sm mt-1">{result.score} / {result.total} correct</p>
            <div className="flex items-center justify-center gap-2 mt-4 text-quantum-cyan">
              <Zap className="w-4 h-4" />
              <span className="font-bold">+{result.xp_earned} XP earned</span>
            </div>
          </QuantumCard>

          <div className="space-y-3">
            {result.answers?.map((ans: any, i: number) => (
              <motion.div key={ans.question_id} initial={{ opacity: 0, x: -15 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                className={`p-4 rounded-xl border ${
                  ans.is_correct ? "border-green-500/20 bg-green-500/5" : "border-red-500/20 bg-red-500/5"
                }`}>
                <div className="flex items-start gap-3">
                  {ans.is_correct
                    ? <CheckCircle2 className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    : <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />}
                  <div>
                    <p className="text-sm text-white font-medium">Q{i + 1}</p>
                    {!ans.is_correct && (
                      <p className="text-xs text-muted-foreground mt-1">{ans.explanation}</p>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          <button onClick={() => setState("list")} className="mt-6 w-full py-3 rounded-xl border border-white/10 text-sm text-muted-foreground hover:text-white hover:border-white/20 transition-all">
            Back to Quizzes
          </button>
        </div>
      </AppShell>
    );
  }

  if (state === "active" && quiz) {
    const q = quiz.questions[currentQ];
    const progress = ((currentQ) / quiz.questions.length) * 100;
    const isCorrect = selectedOption === q.correct_answer;

    return (
      <AppShell>
        <div className="max-w-2xl mx-auto">
          {/* Progress */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-muted-foreground">Q{currentQ + 1} of {quiz.questions.length}</span>
            <span className="text-sm font-mono text-quantum-blue">{quiz.title}</span>
          </div>
          <div className="h-1.5 bg-muted rounded-full mb-6 overflow-hidden">
            <motion.div animate={{ width: `${progress}%` }} className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full" />
          </div>

          <AnimatePresence mode="wait">
            <motion.div key={currentQ} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <QuantumCard className="mb-5">
                <p className="text-white font-medium leading-relaxed">{q.question_text}</p>
              </QuantumCard>

              <div className="space-y-3 mb-6">
                {q.options.map((opt: any) => {
                  let variant = "border-white/10 hover:border-white/20";
                  if (selectedOption) {
                    if (opt.id === q.correct_answer) variant = "border-green-500/60 bg-green-500/10";
                    else if (opt.id === selectedOption && !isCorrect) variant = "border-red-500/60 bg-red-500/10";
                  } else if (selectedOption === opt.id) {
                    variant = "border-quantum-blue/60 bg-quantum-blue/10";
                  }
                  return (
                    <motion.button key={opt.id} onClick={() => selectOption(opt.id)} whileTap={{ scale: 0.99 }}
                      className={`w-full text-left p-4 rounded-xl border transition-all ${
                        selectedOption === opt.id && !selectedOption ? "border-quantum-blue/60 bg-quantum-blue/10" : variant
                      } flex items-center gap-3`}>
                      <span className="w-7 h-7 rounded-full border border-current flex items-center justify-center text-xs font-bold flex-shrink-0 text-muted-foreground">{opt.id.toUpperCase()}</span>
                      <span className="text-sm text-white">{opt.text}</span>
                      {selectedOption && opt.id === q.correct_answer && <CheckCircle2 className="w-4 h-4 text-green-400 ml-auto" />}
                      {selectedOption === opt.id && !isCorrect && opt.id !== q.correct_answer && <XCircle className="w-4 h-4 text-red-400 ml-auto" />}
                    </motion.button>
                  );
                })}
              </div>

              {selectedOption && (
                <motion.button initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  onClick={nextQuestion} disabled={loading}
                  className="w-full py-3 rounded-xl bg-quantum-blue text-quantum-dark font-bold flex items-center justify-center gap-2">
                  {currentQ < quiz.questions.length - 1 ? <><ChevronRight className="w-4 h-4" /> Next Question</> : loading ? "Submitting..." : <><Trophy className="w-4 h-4" /> Finish Quiz</>}
                </motion.button>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader title="Quiz Arena" subtitle="Test your quantum knowledge and earn XP" />
      {quizzes.length === 0 ? (
        <div className="glass rounded-xl border border-white/5 p-12 text-center">
          <Trophy className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
          <p className="text-muted-foreground">No quizzes found. Seed the database to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quizzes.map((q, i) => (
            <motion.div key={q.id} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
              className="glass rounded-xl border border-white/5 hover:border-quantum-blue/20 transition-all p-5">
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-white text-sm">{q.title}</h3>
                <span className={`text-xs px-2 py-0.5 rounded-full border ${
                  q.difficulty === "easy" ? "text-green-400 border-green-400/30 bg-green-400/5" :
                  q.difficulty === "medium" ? "text-yellow-400 border-yellow-400/30 bg-yellow-400/5" :
                  "text-red-400 border-red-400/30 bg-red-400/5"
                }`}>{q.difficulty}</span>
              </div>
              <div className="flex items-center gap-4 text-xs text-muted-foreground mb-4">
                <span className="flex items-center gap-1"><Target className="w-3 h-3" /> {q.question_count} questions</span>
                <span className="flex items-center gap-1 text-quantum-cyan"><Zap className="w-3 h-3" /> {q.xp_reward} XP</span>
              </div>
              <button onClick={() => startQuiz(q.id)}
                className="w-full py-2 rounded-lg bg-quantum-blue/10 border border-quantum-blue/20 text-quantum-blue text-sm font-medium hover:bg-quantum-blue/20 transition-all">
                Start Quiz
              </button>
            </motion.div>
          ))}
        </div>
      )}
    </AppShell>
  );
}
