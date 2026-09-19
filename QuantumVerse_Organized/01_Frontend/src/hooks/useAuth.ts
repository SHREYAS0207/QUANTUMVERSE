import { useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { authService } from "@/services/authService";
import toast from "react-hot-toast";

export function useAuth() {
  const { user, token, isAuthenticated, setAuth, clearAuth } = useAuthStore();
  const router = useRouter();

  const login = useCallback(
    async (email: string, password: string) => {
      const tokens = await authService.login(email, password);
      // Set cookie for middleware
      document.cookie = `qv_token=${tokens.access_token}; path=/; max-age=${60 * 60 * 24 * 7}`;
      const profile = await authService.getProfile();
      setAuth(profile as any, tokens.access_token);
      toast.success(`Welcome back, ${profile.name}!`);
      router.push("/dashboard");
    },
    [router, setAuth]
  );

  const signup = useCallback(
    async (name: string, email: string, password: string, learning_level: string) => {
      const tokens = await authService.signup(name, email, password, learning_level);
      document.cookie = `qv_token=${tokens.access_token}; path=/; max-age=${60 * 60 * 24 * 7}`;
      const profile = await authService.getProfile();
      setAuth(profile as any, tokens.access_token);
      toast.success("🚀 Welcome to QuantumVerse AI!");
      router.push("/dashboard");
    },
    [router, setAuth]
  );

  const logout = useCallback(() => {
    document.cookie = "qv_token=; path=/; max-age=0";
    clearAuth();
    router.push("/login");
    toast.success("Signed out successfully");
  }, [router, clearAuth]);

  const refreshProfile = useCallback(async () => {
    try {
      const profile = await authService.getProfile();
      if (token) setAuth(profile as any, token);
    } catch {
      // Silent fail
    }
  }, [token, setAuth]);

  return { user, token, isAuthenticated, login, signup, logout, refreshProfile };
}
