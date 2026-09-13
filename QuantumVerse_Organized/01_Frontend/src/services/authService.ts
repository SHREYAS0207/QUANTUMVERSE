import type { AuthTokens, User } from "@/types/user";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/v1";
const USERS_KEY = "qv_mock_users";
const SESSION_KEY = "qv_mock_session";

interface StoredUser extends User {
  password?: string;
}

const buildUser = (
  id: string,
  name: string,
  email: string,
  password: string,
  learning_level: string
): StoredUser => ({
  id,
  name,
  email,
  password,
  learning_level: learning_level as User["learning_level"],
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

const readUsers = (): StoredUser[] => {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(USERS_KEY);
    return raw ? (JSON.parse(raw) as StoredUser[]) : [];
  } catch {
    return [];
  }
};

const writeUsers = (users: StoredUser[]) => {
  if (typeof window !== "undefined") {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
  }
};

const writeSession = (user: User, token: string) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("qv_user", JSON.stringify(user));
    localStorage.setItem("qv_token", token);
    localStorage.setItem(SESSION_KEY, JSON.stringify({ user, token }));
  }
};

const readSession = () => {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

const clearStoredSession = () => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("qv_token");
    localStorage.removeItem("qv_user");
    localStorage.removeItem(SESSION_KEY);
    document.cookie = "qv_token=; path=/; max-age=0";
  }
};

const normalizeUser = (data: Partial<User> & { user_id?: string; id?: string }): User => ({
  id: data.id ?? data.user_id ?? "local-user",
  name: data.name ?? "Quantum Explorer",
  email: data.email ?? "",
  learning_level: (data.learning_level as User["learning_level"]) ?? "beginner",
  xp: data.xp ?? 0,
  level: data.level ?? 1,
  streak_days: data.streak_days ?? 0,
  statistics: {
    total_lessons: data.statistics?.total_lessons ?? 0,
    total_circuits: data.statistics?.total_circuits ?? 0,
    total_quizzes: data.statistics?.total_quizzes ?? 0,
    quiz_accuracy: data.statistics?.quiz_accuracy ?? 0,
  },
});

export const authService = {
  async signup(name: string, email: string, password: string, learning_level: string): Promise<AuthTokens> {
    const response = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, learning_level }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Signup failed");
    }

    const data = await response.json();
    const user = normalizeUser({
      id: data.user_id,
      name: data.name,
      email: data.email,
      learning_level: data.learning_level,
    });

    writeSession(user, data.access_token);
    return {
      access_token: data.access_token,
      token_type: data.token_type || "bearer",
      user_id: data.user_id,
      name: data.name,
      email: data.email,
      learning_level: data.learning_level,
    };
  },

  async login(email: string, password: string): Promise<AuthTokens> {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Invalid email or password");
    }

    const data = await response.json();
    const user = normalizeUser({
      id: data.user_id,
      name: data.name,
      email: data.email,
      learning_level: data.learning_level,
    });

    writeSession(user, data.access_token);
    return {
      access_token: data.access_token,
      token_type: data.token_type || "bearer",
      user_id: data.user_id,
      name: data.name,
      email: data.email,
      learning_level: data.learning_level,
    };
  },

  async getProfile(): Promise<User> {
    const token = typeof window !== "undefined" ? localStorage.getItem("qv_token") : null;

    if (token) {
      try {
        const response = await fetch(`${API_BASE}/auth/profile`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
          const profile = await response.json();
          const user = normalizeUser(profile);
          writeSession(user, token);
          return user;
        }

        if (response.status === 401) {
          clearStoredSession();
          throw new Error("Your session expired. Please sign in again.");
        }
      } catch {
        if (typeof window !== "undefined" && !localStorage.getItem("qv_token")) {
          throw new Error("Your session expired. Please sign in again.");
        }
      }
    }

    const session = readSession();
    if (session?.user) {
      return session.user as User;
    }

    throw new Error("No active session found");
  },

  async updateProfile(updates: Partial<User>): Promise<User> {
    const token = typeof window !== "undefined" ? localStorage.getItem("qv_token") : null;
    if (!token) throw new Error("No active session found");

    const response = await fetch(`${API_BASE}/auth/profile`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        ...(updates.name !== undefined ? { name: updates.name } : {}),
        ...(updates.learning_level !== undefined ? { learning_level: updates.learning_level } : {}),
      }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Unable to update profile");
    }

    const user = normalizeUser(await response.json());
    writeSession(user, token);
    return user;
  },
};
