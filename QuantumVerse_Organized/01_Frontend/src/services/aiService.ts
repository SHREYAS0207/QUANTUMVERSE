import api from "@/lib/api";

export const aiService = {
  async createConversation(): Promise<{ id: string; title: string }> {
    const { data } = await api.post("/ai/conversations");
    return data;
  },
  async listConversations(): Promise<object[]> {
    const { data } = await api.get<{ conversations: object[] }>("/ai/conversations");
    return data.conversations;
  },
  async chat(conv_id: string, message: string, difficulty: string, context?: object): Promise<{ response: string; conversation_id: string }> {
    const { data } = await api.post(`/ai/conversations/${conv_id}/chat`, { message, difficulty, context });
    return data;
  },
  async explainCircuit(circuit_data: object, difficulty: string): Promise<object> {
    const { data } = await api.post("/ai/explain-circuit", { circuit_data, difficulty });
    return data;
  },
};
