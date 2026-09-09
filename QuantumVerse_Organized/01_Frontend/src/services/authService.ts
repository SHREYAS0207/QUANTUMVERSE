import type { AuthTokens, User } from "@/types/user";

const USERS_KEY = "qv_mock_users";
const SESSION_KEY = "qv_mock_session";

interface StoredUser extends User {
  password: string;
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

export const authService = {
  async signup(name: string, email: string, password: string, learning_level: string): Promise<AuthTokens> {
    const users = readUsers();
    if (users.some((user) => user.email.toLowerCase() === email.toLowerCase())) {
      throw new Error("Email already registered");
    }

    const newUser = buildUser(
      crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}`,
      name,
      email,
      password,
      learning_level
    );

    users.push(newUser);
    writeUsers(users);

    const token = `mock_token_${Date.now()}`;
    writeSession(newUser, token);

    return {
      access_token: token,
      token_type: "bearer",
      user_id: newUser.id,
      name: newUser.name,
      email: newUser.email,
      learning_level: newUser.learning_level,
    };
  },

  async login(email: string, password: string): Promise<AuthTokens> {
    const users = readUsers();
    const user = users.find((entry) => entry.email.toLowerCase() === email.toLowerCase());

    if (!user || user.password !== password) {
      throw new Error("Invalid email or password");
    }

    const token = `mock_token_${Date.now()}`;
    writeSession(user, token);

    return {
      access_token: token,
      token_type: "bearer",
      user_id: user.id,
      name: user.name,
      email: user.email,
      learning_level: user.learning_level,
    };
  },

  async getProfile(): Promise<User> {
    const session = readSession();
    if (!session?.user) {
      throw new Error("No active session found");
    }

    return session.user as User;
  },

  async updateProfile(updates: Partial<User>): Promise<User> {
    const session = readSession();
    if (!session?.user) {
      throw new Error("No active session found");
    }

    const users = readUsers();
    const userIndex = users.findIndex((entry) => entry.email.toLowerCase() === session.user.email.toLowerCase());

    if (userIndex >= 0) {
      const updatedUser = {
        ...users[userIndex],
        ...updates,
        statistics: {
          ...users[userIndex].statistics,
          ...(updates.statistics ?? {}),
        },
      };

      users[userIndex] = updatedUser;
      writeUsers(users);
      writeSession(updatedUser, session.token);
      return updatedUser;
    }

    return session.user as User;
  },
};
