import axios from "axios";
import { useAuthStore } from "../stores/authStore";

function normalizeApiBaseURL(url?: string) {
  if (!url) return "/api";
  // If caller already provided /api, keep it. Otherwise append /api.
  return url.endsWith("/api") ? url : `${url.replace(/\/+$/, "")}/api`;
}

const api = axios.create({
  baseURL: normalizeApiBaseURL(import.meta.env.VITE_API_URL),
});


api.interceptors.request.use((config) => {
  // Ensure we always send requests under /api even if a caller passes an absolute-like path.
  if (config.url?.startsWith("/auth/")) {
    config.url = config.url.replace(/^\/auth\//, "/auth/");
  }

  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
