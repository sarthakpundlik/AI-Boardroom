import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FolderKanban,
  Presentation,
  FileBarChart,
  Gauge,
  Plus,
  ArrowUpRight,
  Clock,
  ChevronRight,
} from "lucide-react";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import PageTransition from "../components/ui/PageTransition";
import { useAuth } from "../context/AuthContext";
import { DEMO_PROJECTS, DEMO_SESSIONS, DEMO_STATS } from "../data/mock";
import { INPUT_TYPES, SESSION_STAGES } from "../data/agents";
import { ProjectsAPI, SessionsAPI } from "../lib/api";

const STATUS_TONE = {
  draft: "neutral",
  active: "blue",
  completed: "green",
  archived: "neutral",
  round_1: "blue",
  round_2: "blue",
  round_3: "warm",
};

function timeAgo(iso) {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.round(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.round(hrs / 24)}d ago`;
}

function StatCard({ icon: Icon, label, value, hint, tone }) {
  return (
    <GlassCard className="p-5" hover>
      <div className="flex items-start justify-between">
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center"
          style={{ backgroundColor: `rgb(var(--${tone}) / 0.12)`, color: `rgb(var(--${tone}))` }}
        >
          <Icon className="w-5 h-5" />
        </div>
        <ArrowUpRight className="w-4 h-4 text-muted" />
      </div>
      <p className="font-display text-3xl font-semibold text-ink mt-4">{value}</p>
      <p className="text-xs text-muted mt-1">{label}</p>
      {hint && <p className="text-[11px] text-muted/80 mt-2 font-mono">{hint}</p>}
    </GlassCard>
  );
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, demoMode } = useAuth();

  const [projects, setProjects] = useState(demoMode ? DEMO_PROJECTS : []);
  const [totalProjects, setTotalProjects] = useState(demoMode ? DEMO_PROJECTS.length : 0);
  const [inProgress, setInProgress] = useState(demoMode ? Object.values(DEMO_SESSIONS).find((s) => s.status !== "completed") : null);
  const [loading, setLoading] = useState(!demoMode);

  useEffect(() => {
    if (demoMode) return;
    let cancelled = false;

    (async () => {
      try {
        const { data } = await ProjectsAPI.list(1, 6);
        if (cancelled) return;
        setProjects(data.projects);
        setTotalProjects(data.total);

        // Check the most recently updated project for a running session —
        // there's no aggregate "sessions in progress" endpoint, so we only
        // look at the single freshest project to avoid N+1 fetches.
        const freshest = data.projects[0];
        if (freshest) {
          const { data: sessionData } = await SessionsAPI.listForProject(freshest.id, 1, 1);
          const latest = sessionData.sessions?.[0];
          if (latest && latest.status !== "completed" && latest.status !== "failed" && !cancelled) {
            setInProgress({ ...latest, projectTitle: freshest.title });
          }
        }
      } catch {
        // Best effort — dashboard just shows empty state if this fails.
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [demoMode]);

  const inProgressProject = demoMode
    ? inProgress && DEMO_PROJECTS.find((p) => p.id === inProgress.project_id)
    : inProgress && { title: inProgress.projectTitle };
  const stageIdx = inProgress ? SESSION_STAGES.findIndex((s) => s.value === inProgress.status) : -1;

  const activeCount = useMemo(() => projects.filter((p) => p.status === "active").length, [projects]);
  const completedCount = useMemo(() => projects.filter((p) => p.status === "completed").length, [projects]);
  const recentCount = useMemo(
    () => projects.filter((p) => Date.now() - new Date(p.updated_at).getTime() < 7 * 24 * 60 * 60 * 1000).length,
    [projects]
  );

  const firstName = user?.name?.split(" ")[0] || "there";

  return (
    <PageTransition>
      <Topbar
        title={`Welcome back, ${firstName}`}
        subtitle="Here's what your boardroom has been working on."
        actions={
          <Button icon={Plus} onClick={() => navigate("/new-session")}>
            New boardroom session
          </Button>
        }
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {demoMode ? (
          <>
            <StatCard icon={FolderKanban} label="Active projects" value={DEMO_STATS.activeProjects} tone="accent-blue" hint="2 awaiting input" />
            <StatCard icon={Presentation} label="Sessions run" value={DEMO_STATS.sessionsRun} tone="accent-green" hint="1 in progress" />
            <StatCard icon={FileBarChart} label="Reports generated" value={DEMO_STATS.reportsGenerated} tone="accent-warm" hint="1 exported this week" />
            <StatCard icon={Gauge} label="Avg. board confidence" value={`${DEMO_STATS.avgConfidence}%`} tone="accent-blue" hint="across all agents" />
          </>
        ) : (
          <>
            <StatCard icon={FolderKanban} label="Total projects" value={totalProjects} tone="accent-blue" />
            <StatCard icon={Presentation} label="Active projects" value={activeCount} tone="accent-green" />
            <StatCard icon={FileBarChart} label="Completed" value={completedCount} tone="accent-warm" />
            <StatCard icon={Gauge} label="Updated this week" value={recentCount} tone="accent-blue" />
          </>
        )}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* In-progress session */}
        <GlassCard heavy className="lg:col-span-2 p-6">
          <div className="flex items-center justify-between mb-1">
            <h3 className="font-display font-semibold text-ink">Live session</h3>
            {inProgress && (
              <span className="flex items-center gap-1.5 text-[11px] text-accentgreen font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-accentgreen animate-pulse" />
                In progress
              </span>
            )}
          </div>
          {inProgress ? (
            <>
              <p className="text-sm text-muted mb-5">{inProgressProject?.title}</p>
              <div className="flex items-center gap-2 mb-6 overflow-x-auto no-scrollbar pb-1">
                {SESSION_STAGES.map((s, i) => (
                  <span
                    key={s.value}
                    className={`shrink-0 text-[10px] px-2.5 py-1 rounded-full border ${
                      i < stageIdx
                        ? "bg-accentgreen/15 text-accentgreen border-accentgreen/30"
                        : i === stageIdx
                        ? "bg-gradient-to-r from-accentblue to-accentgreen text-white border-transparent"
                        : "glass text-muted"
                    }`}
                  >
                    {s.label}
                  </span>
                ))}
              </div>
              <Button
                variant="secondary"
                icon={ChevronRight}
                onClick={() => navigate(`/session/${inProgress.id}`)}
              >
                Open live boardroom
              </Button>
            </>
          ) : (
            <div className="text-center py-10">
              <p className="text-sm text-muted mb-4">
                {loading ? "Loading…" : "No session is running right now."}
              </p>
              {!loading && (
                <Button icon={Plus} onClick={() => navigate("/new-session")}>
                  Start a boardroom session
                </Button>
              )}
            </div>
          )}
        </GlassCard>

        {/* Quick start by input type */}
        <GlassCard className="p-6">
          <h3 className="font-display font-semibold text-ink mb-1">Quick start</h3>
          <p className="text-xs text-muted mb-4">Jump straight into a session type.</p>
          <div className="flex flex-col gap-1.5">
            {INPUT_TYPES.slice(0, 5).map((t) => (
              <button
                key={t.value}
                onClick={() => navigate("/new-session", { state: { inputType: t.value } })}
                className="flex items-center justify-between text-left px-3 py-2.5 rounded-xl text-sm text-ink hover:bg-ink/5 transition-colors group"
              >
                {t.label}
                <ChevronRight className="w-4 h-4 text-muted group-hover:translate-x-0.5 transition-transform" />
              </button>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Recent projects */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-semibold text-ink">Recent projects</h3>
          <button onClick={() => navigate("/projects")} className="text-xs text-accentblue font-medium hover:underline">
            View all
          </button>
        </div>
        {!loading && projects.length === 0 ? (
          <GlassCard className="p-8 text-center">
            <p className="text-sm text-muted">No projects yet — start your first boardroom session.</p>
          </GlassCard>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {projects.map((p) => (
              <GlassCard
                key={p.id}
                hover
                className="p-5 cursor-pointer"
                onClick={() => navigate(`/projects/${p.id}`)}
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h4 className="text-sm font-medium text-ink leading-snug">{p.title}</h4>
                  <Badge tone={STATUS_TONE[p.status]} dot>
                    {p.status.replace("_", " ")}
                  </Badge>
                </div>
                <p className="text-xs text-muted leading-relaxed line-clamp-2 mb-4">{p.description}</p>
                <div className="flex items-center justify-between text-[11px] text-muted">
                  <span>{INPUT_TYPES.find((t) => t.value === p.input_type)?.label}</span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" /> {timeAgo(p.updated_at)}
                  </span>
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </div>
    </PageTransition>
  );
}
