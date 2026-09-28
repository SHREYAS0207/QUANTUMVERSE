import api from "@/lib/api";

const ENDPOINT = process.env.NEXT_PUBLIC_AI_TUTOR_API || "/api/v1/tutor";

class AiTutorService {
  private model: any = null;

  async initializeModel() {
    try {
      const { data } = await api.get(`${ENDPOINT}/model`);
      this.model = data;
      return this.model;
    } catch {
      // fallback: mark model as locally initialized
      this.model = { status: "local", initialized: true };
      return this.model;
    }
  }

  async trainModel(dataset: any[]) {
    const { data } = await api.post(`${ENDPOINT}/train`, { dataset });
    return data;
  }

  async askQuestion(question: string, context: object | null = null) {
    const { data } = await api.post(`${ENDPOINT}/ask`, { question, context });
    return data;
  }

  async generateQuiz(topic: string, difficulty = "medium", count = 10) {
    const { data } = await api.post(`${ENDPOINT}/quiz`, { topic, difficulty, count });
    return data;
  }

  getModel() {
    return this.model;
  }

  isInitialized() {
    return this.model !== null;
  }
}

export const aiTutorService = new AiTutorService();
