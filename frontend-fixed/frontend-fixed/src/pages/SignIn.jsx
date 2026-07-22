import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Presentation, Mail, Lock, User, ArrowRight, Sparkles } from "lucide-react";
import Button from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import GlassCard from "../components/ui/GlassCard";
import ThemeToggle from "../components/ui/ThemeToggle";
import { useAuth } from "../context/AuthContext";
import { buildGoogleAuthUrl, buildGithubAuthUrl } from "../lib/oauth";
import { AGENT_LIST } from "../data/agents";

function GoogleIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" {...props}>
      <path fill="#4285F4" d="M23.52 12.27c0-.85-.08-1.67-.22-2.45H12v4.64h6.47a5.53 5.53 0 0 1-2.4 3.63v3h3.88c2.27-2.09 3.57-5.17 3.57-8.82Z"/>
      <path fill="#34A853" d="M12 24c3.24 0 5.95-1.07 7.94-2.91l-3.88-3c-1.08.72-2.45 1.15-4.06 1.15-3.12 0-5.77-2.11-6.71-4.94H1.28v3.1A12 12 0 0 0 12 24Z"/>
      <path fill="#FBBC05" d="M5.29 14.3A7.2 7.2 0 0 1 4.91 12c0-.8.14-1.57.38-2.3v-3.1H1.28A12 12 0 0 0 0 12c0 1.94.46 3.77 1.28 5.4l4.01-3.1Z"/>
      <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.44-3.44C17.94 1.19 15.24 0 12 0 7.31 0 3.26 2.69 1.28 6.6l4.01 3.1C6.23 6.86 8.88 4.75 12 4.75Z"/>
    </svg>
  );
}

function GithubIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" {...props}>
      <path d="M12 0C5.37 0 0 5.5 0 12.3c0 5.44 3.44 10.05 8.21 11.68.6.11.82-.27.82-.6 0-.29-.01-1.06-.02-2.08-3.34.75-4.04-1.66-4.04-1.66-.55-1.44-1.34-1.83-1.34-1.83-1.09-.77.08-.75.08-.75 1.2.09 1.84 1.28 1.84 1.28 1.07 1.87 2.81 1.33 3.5 1.02.11-.79.42-1.33.76-1.64-2.67-.31-5.47-1.36-5.47-6.03 0-1.33.46-2.42 1.22-3.28-.12-.31-.53-1.55.12-3.23 0 0 1-.33 3.3 1.25a11.2 11.2 0 0 1 6 0c2.3-1.58 3.3-1.25 3.3-1.25.65 1.68.24 2.92.12 3.23.76.86 1.22 1.95 1.22 3.28 0 4.68-2.8 5.72-5.48 6.02.43.38.81 1.13.81 2.29 0 1.65-.02 2.98-.02 3.39 0 .33.22.72.83.6C20.57 22.34 24 17.73 24 12.3 24 5.5 18.63 0 12 0Z"/>
    </svg>
  );
}

export default function SignIn() {
  const navigate = useNavigate();
  const { login, register, enterDemoMode } = useAuth();
  const [mode, setMode] = useState("login"); // login | register
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "login") {
        await login(form.email, form.password);
      } else {
        await register(form.name, form.email, form.password);
      }
      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Couldn't reach the AI Boardroom API. Try demo mode below to preview the console."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDemo = () => {
    enterDemoMode();
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex">
      <div className="mesh-bg" />

      {/* Left — brand / narrative panel */}
      <div className="hidden lg:flex flex-col justify-between w-1/2 p-12 relative overflow-hidden">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accentblue to-accentgreen flex items-center justify-center shadow-glass-sm">
            <Presentation className="w-4.5 h-4.5 text-white" strokeWidth={2.2} />
          </div>
          <span className="font-display font-semibold text-ink">AI Boardroom</span>
        </div>

        <div className="max-w-md">
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="font-display text-4xl xl:text-5xl font-semibold leading-[1.08] text-ink"
          >
            Pitch your idea.
            <br />
            <span className="text-gradient">Let the C-suite argue it out.</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-muted mt-5 text-sm leading-relaxed"
          >
            Every submission convenes a full board — Strategy, Finance, Technology,
            Customer, Risk and a Devil's Advocate — who debate across three rounds
            before the CEO agent synthesizes a final decision.
          </motion.p>
        </div>

        {/* Mini boardroom preview */}
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <GlassCard className="p-5">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-mono text-muted">live_session.preview</span>
              <span className="flex items-center gap-1.5 text-[11px] text-accentgreen">
                <span className="w-1.5 h-1.5 rounded-full bg-accentgreen animate-pulse" /> Round 2 of 3
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {AGENT_LIST.map((a) => (
                <span
                  key={a.key}
                  className="flex items-center gap-1.5 text-[11px] px-2.5 py-1.5 rounded-lg glass"
                >
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: a.color }} />
                  {a.label}
                </span>
              ))}
            </div>
          </GlassCard>
        </motion.div>
      </div>

      {/* Right — auth form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-10 relative">
        <div className="absolute top-6 right-6">
          <ThemeToggle />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-sm"
        >
          <GlassCard heavy className="p-8">
            <div className="lg:hidden flex items-center gap-2.5 mb-8">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accentblue to-accentgreen flex items-center justify-center">
                <Presentation className="w-4.5 h-4.5 text-white" />
              </div>
              <span className="font-display font-semibold text-ink">AI Boardroom</span>
            </div>

            <h2 className="font-display text-xl font-semibold text-ink">
              {mode === "login" ? "Welcome back" : "Create your account"}
            </h2>
            <p className="text-sm text-muted mt-1 mb-6">
              {mode === "login" ? "Sign in to open your boardroom." : "Set up access to your boardroom."}
            </p>

            <div className="space-y-3 mb-6">
              <button
                type="button"
                onClick={() => (window.location.href = buildGoogleAuthUrl())}
                className="w-full flex items-center justify-center gap-3 glass rounded-xl py-2.5 text-sm font-medium text-ink hover:border-accentblue/40 hover:bg-surface/80 transition-all duration-200"
              >
                <GoogleIcon /> Continue with Google
              </button>
              <button
                type="button"
                onClick={() => (window.location.href = buildGithubAuthUrl())}
                className="w-full flex items-center justify-center gap-3 glass rounded-xl py-2.5 text-sm font-medium text-ink hover:border-accentblue/40 hover:bg-surface/80 transition-all duration-200"
              >
                <GithubIcon /> Continue with GitHub
              </button>
            </div>

            <div className="flex items-center gap-3 mb-6">
              <div className="h-px flex-1 bg-line/12" />
              <span className="text-[11px] text-muted uppercase tracking-wide">or with email</span>
              <div className="h-px flex-1 bg-line/12" />
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === "register" && (
                <Input
                  label="Full name"
                  placeholder="Sarthak Pundlik"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  required
                />
              )}
              <Input
                label="Email"
                type="email"
                placeholder="you@company.com"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
              <Input
                label="Password"
                type="password"
                placeholder="••••••••"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                minLength={8}
                required
              />

              {error && (
                <p className="text-xs text-red-400 bg-red-500/10 border border-red-500/25 rounded-lg px-3 py-2">
                  {error}
                </p>
              )}

              <Button type="submit" className="w-full" loading={loading} icon={ArrowRight}>
                {mode === "login" ? "Sign in" : "Create account"}
              </Button>
            </form>

            <button
              onClick={handleDemo}
              className="w-full flex items-center justify-center gap-2 text-xs text-muted hover:text-accentblue mt-5 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5" /> Explore with demo data — no backend required
            </button>

            <p className="text-center text-xs text-muted mt-6">
              {mode === "login" ? "New to AI Boardroom?" : "Already have an account?"}{" "}
              <button
                onClick={() => setMode(mode === "login" ? "register" : "login")}
                className="text-accentblue font-medium hover:underline"
              >
                {mode === "login" ? "Create an account" : "Sign in"}
              </button>
            </p>
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
}
