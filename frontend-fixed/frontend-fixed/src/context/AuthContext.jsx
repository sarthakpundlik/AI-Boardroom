import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { AuthAPI, UsersAPI, tokenStore } from "../lib/api";

const AuthContext = createContext(null);

const DEMO_USER = {
  id: "demo-user",
  name: "Sarthak Pundlik",
  email: "founder@aiboardroom.dev",
  role: "user",
  is_active: true,
  oauth_provider: "google",
  avatar_url: null,
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [demoMode, setDemoMode] = useState(false);

  const loadMe = useCallback(async () => {
    if (!tokenStore.access) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const res = await UsersAPI.me();
      setUser(res.data);
    } catch {
      tokenStore.clear();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMe();
  }, [loadMe]);

  const login = useCallback(async (email, password) => {
    const res = await AuthAPI.login({ email, password });
    tokenStore.set(res.data.access_token, res.data.refresh_token);
    await loadMe();
  }, [loadMe]);

  const register = useCallback(async (name, email, password) => {
    await AuthAPI.register({ name, email, password });
    await login(email, password);
  }, [login]);

  const handleOAuthCallback = useCallback(async (provider, code, state) => {
    let res;
    if (provider === "google") {
      res = await AuthAPI.googleCallback(code, state);
    } else if (provider === "github") {
      res = await AuthAPI.githubCallback(code, state);
    } else {
      res = await AuthAPI.microsoftCallback(code, state);
    }
    tokenStore.set(res.data.access_token, res.data.refresh_token);
    await loadMe();
  }, [loadMe]);

  const enterDemoMode = useCallback(() => {
    setDemoMode(true);
    setUser(DEMO_USER);
    setLoading(false);
  }, []);

  const logout = useCallback(async () => {
    try {
      if (tokenStore.refresh && !demoMode) await AuthAPI.logout(tokenStore.refresh);
    } catch {
      // Best-effort — clear local state regardless.
    }
    tokenStore.clear();
    setUser(null);
    setDemoMode(false);
  }, [demoMode]);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        demoMode,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        handleOAuthCallback,
        enterDemoMode,
        refresh: loadMe,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
