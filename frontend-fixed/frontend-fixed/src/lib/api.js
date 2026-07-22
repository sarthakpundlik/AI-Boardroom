import axios from "axios";

// Base URL of the FastAPI backend. Override via .env -> VITE_API_URL.
// Matches backend/app/core/config.py: API_V1_PREFIX = "/api/v1"
export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
export const WS_BASE = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";
// The bare backend origin (no /api/v1 suffix) — static files like generated
// report PDFs are served from here (see main.py's /media StaticFiles mount).
export const SERVER_ORIGIN = API_BASE.replace(/\/api\/v1\/?$/, "");

/** Turns a relative pdf_url (e.g. "/media/reports/...") into an absolute URL. */
export function resolveMediaUrl(path) {
  if (!path) return null;
  if (/^https?:\/\//.test(path)) return path;
  return `${SERVER_ORIGIN}${path.startsWith("/") ? "" : "/"}${path}`;
}

const TOKEN_KEY = "ab_access_token";
const REFRESH_KEY = "ab_refresh_token";

export const tokenStore = {
  get access() {
    return localStorage.getItem(TOKEN_KEY);
  },
  get refresh() {
    return localStorage.getItem(REFRESH_KEY);
  },
  set(access, refresh) {
    if (access) localStorage.setItem(TOKEN_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

export const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const t = tokenStore.access;
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

let refreshing = null;

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry && tokenStore.refresh) {
      original._retry = true;
      try {
        if (!refreshing) {
          refreshing = axios
            .post(`${API_BASE}/auth/refresh`, { refresh_token: tokenStore.refresh })
            .then((r) => {
              tokenStore.set(r.data.access_token, r.data.refresh_token);
              return r.data.access_token;
            })
            .finally(() => {
              refreshing = null;
            });
        }
        const newToken = await refreshing;
        original.headers.Authorization = `Bearer ${newToken}`;
        return api(original);
      } catch (e) {
        tokenStore.clear();
        window.location.href = "/sign-in";
        return Promise.reject(e);
      }
    }
    return Promise.reject(error);
  }
);

// ---- Auth (backend/app/auth/router.py) ----
export const AuthAPI = {
  register: (data) => api.post("/auth/register", data),
  login: (data) => api.post("/auth/login", data),
  logout: (refresh_token) => api.post("/auth/logout", { refresh_token }),
  googleCallback: (code, state) => api.post("/auth/google/callback", { code, state }),
  githubCallback: (code, state) => api.post("/auth/github/callback", { code, state }),
  microsoftCallback: (code, state) => api.post("/auth/microsoft/callback", { code, state }),
  requestPasswordReset: (email) => api.post("/auth/password-reset-request", { email }),
  confirmPasswordReset: (token, new_password) =>
    api.post("/auth/password-reset-confirm", { token, new_password }),
};

// ---- Users (backend/app/users/router.py) ----
export const UsersAPI = {
  me: () => api.get("/users/me"),
  updateMe: (data) => api.patch("/users/me", data),
  changePassword: (data) => api.post("/users/me/change-password", data),
};

// ---- Projects (backend/app/projects/router.py) ----
export const ProjectsAPI = {
  list: (page = 1, per_page = 20) => api.get("/projects", { params: { page, per_page } }),
  create: (data) => api.post("/projects", data),
  get: (id) => api.get(`/projects/${id}`),
  update: (id, data) => api.patch(`/projects/${id}`, data),
  remove: (id) => api.delete(`/projects/${id}`),
};

// ---- Sessions (backend/app/sessions/router.py) ----
export const SessionsAPI = {
  create: (project_id) => api.post("/sessions", { project_id }),
  listForProject: (project_id, page = 1, per_page = 20) =>
    api.get(`/sessions/project/${project_id}`, { params: { page, per_page } }),
  get: (id) => api.get(`/sessions/${id}`),
  remove: (id) => api.delete(`/sessions/${id}`),
};

// ---- Reports (backend/app/reports/router.py) ----
export const ReportsAPI = {
  list: (page = 1, per_page = 20) => api.get("/reports", { params: { page, per_page } }),
  listForProject: (project_id) => api.get(`/reports/project/${project_id}`),
  get: (id) => api.get(`/reports/${id}`),
};

// ---- Notifications (backend/app/notifications/router.py) ----
export const NotificationsAPI = {
  list: (page = 1, per_page = 20) => api.get("/notifications", { params: { page, per_page } }),
  markRead: (id) => api.patch(`/notifications/${id}/read`),
  markAllRead: () => api.post("/notifications/read-all"),
};

// ---- Health (backend/app/api/v1/health.py) ----
export const HealthAPI = {
  check: () => api.get("/health"),
};
