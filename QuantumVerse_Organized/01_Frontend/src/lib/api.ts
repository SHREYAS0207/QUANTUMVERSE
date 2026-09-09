import axios, { AxiosError } from "axios";
import toast from "react-hot-toast";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("qv_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Global error handling
api.interceptors.response.use(
  (res) => res,
  (error: AxiosError<{ detail: string }>) => {
    const message = error.response?.data?.detail || "Something went wrong";
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("qv_token");
        localStorage.removeItem("qv_user");
        window.location.href = "/login";
      }
    }
    toast.error(message);
    return Promise.reject(error);
  }
);

export default api;
