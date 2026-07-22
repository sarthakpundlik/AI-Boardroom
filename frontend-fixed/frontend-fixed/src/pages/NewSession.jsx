import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Sparkles, ArrowRight, Upload } from "lucide-react";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import { Input, Textarea } from "../components/ui/Input";
import PageTransition from "../components/ui/PageTransition";
import { INPUT_TYPES, AGENTS, agentsForInputType } from "../data/agents";
import { useAuth } from "../context/AuthContext";
import { ProjectsAPI, SessionsAPI } from "../lib/api";

export default function NewSession() {
  const navigate = useNavigate();
  const location = useLocation();
  const { demoMode } = useAuth();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [inputType, setInputType] = useState(location.state?.inputType || "startup_idea");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const activeAgents = agentsForInputType(inputType);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) return;
    setError("");
    setSubmitting(true);

    if (demoMode) {
      // Demo mode never touches the backend — just simulate the flow.
      setTimeout(() => {
        navigate("/session/demo", { state: { title, description, inputType, agents: activeAgents } });
      }, 500);
      return;
    }

    try {
      const { data: project } = await ProjectsAPI.create({
        title: title.trim(),
        description: description.trim(),
        input_type: inputType,
      });
      const { data: session } = await SessionsAPI.create(project.id);
      navigate(`/session/${session.id}`, {
        state: {
          title: project.title,
          projectId: project.id,
          agents: session.agents_selected?.length ? session.agents_selected : activeAgents,
        },
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Couldn't convene the board. Please try again.");
      setSubmitting(false);
    }
  };

  return (
    <PageTransition>
      <Topbar
        title="Convene the board"
        subtitle="Describe what you want reviewed. The board dynamically activates the right department heads."
      />

      <div className="grid lg:grid-cols-3 gap-6">
        <form onSubmit={handleSubmit} className="lg:col-span-2 flex flex-col gap-5">
          <GlassCard className="p-6">
            <Input
              label="Project title"
              placeholder="e.g. Modular vertical-farming kits for urban restaurants"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </GlassCard>

          <GlassCard className="p-6">
            <Textarea
              label="Describe your idea, dataset, or proposal"
              placeholder="Give the board as much context as you can — the problem, the audience, numbers you already have, and what decision you need from them."
              rows={8}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
            <button
              type="button"
              className="mt-3 flex items-center gap-2 text-xs text-muted hover:text-accentblue transition-colors"
            >
              <Upload className="w-3.5 h-3.5" /> Attach a file (.pdf, .docx, .csv, .xlsx) — up to 50MB
            </button>
          </GlassCard>

          <GlassCard className="p-6">
            <p className="text-xs font-medium text-muted mb-3 tracking-wide uppercase">What kind of input is this?</p>
            <div className="grid sm:grid-cols-2 gap-2">
              {INPUT_TYPES.map((t) => (
                <button
                  type="button"
                  key={t.value}
                  onClick={() => setInputType(t.value)}
                  className={`text-left text-sm px-4 py-3 rounded-xl border transition-all duration-200 ${
                    inputType === t.value
                      ? "bg-gradient-to-r from-accentblue/15 to-accentgreen/10 border-accentblue/40 text-ink"
                      : "glass border-transparent text-muted hover:text-ink"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </GlassCard>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <Button type="submit" size="lg" icon={ArrowRight} loading={submitting} className="self-start">
            Convene the board
          </Button>
        </form>

        {/* Live preview of which agents will activate */}
        <GlassCard heavy className="p-6 h-fit lg:sticky lg:top-10">
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="w-4 h-4 text-accentblue" />
            <h3 className="font-display font-semibold text-ink text-sm">Board will convene</h3>
          </div>
          <p className="text-xs text-muted mb-5">
            Based on <span className="text-ink">{INPUT_TYPES.find((t) => t.value === inputType)?.label}</span>, these
            department heads will run — plus the CEO for final synthesis.
          </p>
          <div className="flex flex-col gap-2.5">
            {["CEO", ...activeAgents].map((key) => {
              const a = AGENTS[key];
              return (
                <div key={key} className="flex items-center gap-3 p-2.5 rounded-xl glass">
                  <span
                    className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-display font-semibold text-white shrink-0"
                    style={{ background: `linear-gradient(135deg, ${a.color}, ${a.color}99)` }}
                  >
                    {a.label.slice(0, 2).toUpperCase()}
                  </span>
                  <div className="min-w-0">
                    <p className="text-xs font-medium text-ink truncate">{a.title}</p>
                    <p className="text-[11px] text-muted truncate">{a.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </GlassCard>
      </div>
    </PageTransition>
  );
}
