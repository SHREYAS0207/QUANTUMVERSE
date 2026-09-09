import api from "@/lib/api";
import type { Circuit } from "@/types/circuit";

export const circuitService = {
  async list(): Promise<Circuit[]> {
    const { data } = await api.get<{ circuits: Circuit[] }>("/circuits");
    return data.circuits;
  },
  async get(id: string): Promise<Circuit> {
    const { data } = await api.get<Circuit>(`/circuits/${id}`);
    return data;
  },
  async create(payload: Partial<Circuit>): Promise<Circuit> {
    const { data } = await api.post<Circuit>("/circuits", payload);
    return data;
  },
  async update(id: string, payload: Partial<Circuit>): Promise<Circuit> {
    const { data } = await api.put<Circuit>(`/circuits/${id}`, payload);
    return data;
  },
  async delete(id: string): Promise<void> {
    await api.delete(`/circuits/${id}`);
  },
  async getTemplates(): Promise<Circuit[]> {
    const { data } = await api.get<{ templates: Circuit[] }>("/circuits/templates");
    return data.templates;
  },
};
