import api from "@/lib/api";
import type { AuthTokens, User } from "@/types/user";

interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  name: string;
  email: string;
  learning_level: string;
}

const mapUser = (data: AuthResponse): User => ({
  id: data.user_id,
  name: data.name,
  email: data.email,
  learning_level: data.learning_level as User["learning_level"],
  xp: 0,
  level: 1,
  streak_days: 0,
  statistics: {
    total_lessons: 0,
    total_circuits: 0,
    total_quizzes: 0,
    quiz_accuracy: 0,
  },
});

const saveToken = (token: string) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("qv_token", token);
    document.cookie = `qv_token=${token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
  }
};

const clearToken = () => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("qv_token");
    localStorage.removeItem("qv_user");
    document.cookie = "qv_token=; path=/; max-age=0; SameSite=Lax";
  }
};

export const authService = {
  async signup(
    name: string,
    email: string,
    password: string,
    learning_level: string
  ): Promise<AuthTokens> {
    const { data } = await api.post<AuthResponse>("/auth/signup", {
      name,
      email,
      password,
      learning_level,
    });

    const user = mapUser(data);
    saveToken(data.access_token);

    return {
      access_token: data.access_token,
      token_type: data.token_type,
      user_id: data.user_id,
      name: data.name,
      email: data.email,
      learning_level: data.learning_level,
    };
  },

  async login(email: string, password: string): Promise<AuthTokens> {
    const { data } = await api.post<AuthResponse>("/auth/login", {
      email,
      password,
    });

    saveToken(data.access_token);

    return {
      access_token: data.access_token,
      token_type: data.token_type,
      user_id: data.user_id,
      name: data.name,
      email: data.email,
      learning_level: data.learning_level,
    };
  },

  async getProfile(): Promise<User> {
    const { data } = await api.get<User>("/auth/profile");

    if (typeof window !== "undefined") {
      localStorage.setItem("qv_user", JSON.stringify(data));
    }

    return data;
  },

  async updateProfile(updates: Partial<User>): Promise<User> {
    const { data } = await api.put<User>("/auth/profile", updates);

    if (typeof window !== "undefined") {
      localStorage.setItem("qv_user", JSON.stringify(data));
    }

    return data;
  },

  logout(): void {
    clearToken();
  },
};
