const envBase = (import.meta.env.VITE_API_BASE_URL || "").trim();
const fallbackBase =
  typeof window !== "undefined" ? `${window.location.origin}/api` : "/api";

export const API_BASE_URL = envBase || fallbackBase;
