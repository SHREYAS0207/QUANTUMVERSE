
import axios, { AxiosError } from "axios";
import toast from "react-hot-toast";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("qv_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Convert API error details into a safe, readable string
function getErrorMessage(error: AxiosError): string {
  const data = error.response?.data as
    | { detail?: unknown; message?: unknown }
    | undefined;

  const detail = data?.detail;

  // Standard FastAPI string error
  if (typeof detail === "string") {
    return detail;
  }

  // FastAPI/Pydantic validation errors
  if (Array.isArray(detail)) {
    const messages = detail
      .map((item: unknown) => {
        if (
          typeof item === "object" &&
          item !== null &&
          "msg" in item &&
          typeof item.msg === "string"
        ) {
          return item.msg;
        }
        return null;
      })
      .filter((msg): msg is string => msg !== null);

    if (messages.length > 0) {
      return messages.join(", ");
    }
  }

  // Other APIs may return { message: "..." }
  if (typeof data?.message === "string") {
    return data.message;
  }

  if (!error.response) {
    return "Unable to connect to the server. Please try again.";
  }

  return "Something went wrong. Please try again.";
}

// Global error handling
api.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    const message = getErrorMessage(error);

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

