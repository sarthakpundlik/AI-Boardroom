import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Presentation, FileBarChart, Play, Clock } from "lucide-react";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import PageTransition from "../components/ui/PageTransition";
import { DEMO_PROJECTS, DEMO_SESSIONS, DEMO_REPORT } from "../data/mock";
import { INPUT_TYPES, AGENTS } from "../data/agents";
import { useAuth } from "../context/AuthContext";
import { ProjectsAPI, SessionsAPI, ReportsAPI } from "../lib/api";

const STATUS_TONE = { draft: "neutral", active: "blue", completed: "green", archived: "neutral" };

export default function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { demoMode } = useAuth();

  const [project, setProject] = useState(demoMode ? DEMO_PROJECTS.find((p) => p.id === id) || DEMO_PROJECTS[0] : null);
  const [session, setSession] = useState(demoMode ? DEMO_SESSIONS[project?.id] : null);
  const [reportId, setReportId] = useState(demoMode && project?.status === "completed" ? DEMO_REPORT.id : null);
  const [loading, setLoading] = useState(!demoMode);

  useEffect(() => {
    if (demoMode) return;
    let cancelled = false;

    (async () => {
      try {
        const [{ data: proj }, { data: sessionData }, { data: reportData }] = await Promise.all([
          ProjectsAPI.get(id),
          SessionsAPI.listForProject(id, 1, 1),
          ReportsAPI.listForProject(id),
        ]);
        if (cancelled) return;
        setProject(proj);
        setSession(sessionData.sessions?.[0] || null);
        setReportId(reportData.reports?.[0]?.id || null);
      } catch {
        // Best effort — show what we have.
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [demoMode, id]);

  if (loading || !project) {
    return (
      <PageTransition>
        <GlassCard className="p-12 text-center">
          <p className="text-sm text-muted">Loading project…</p>
        </GlassCard>
      </PageTransition>
    );
  }

  const sessionInProgress = session && session.status !== "completed" && session.status !== "failed";

  return (
    <PageTransition>
      <button
        onClick={() => navigate("/projects")}
        className="flex items-center gap-1.5 text-xs text-muted hover:text-ink mb-6 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to projects
      </button>

      <div className="flex items-start justify-between gap-4 flex-wrap mb-6">
        <div className="max-w-2xl">
          <div className="flex items-center gap-2.5 mb-2">
            <Badge tone={STATUS_TONE[project.status]} dot>{project.status.replace("_", " ")}</Badge>
            <Badge tone="neutral">{INPUT_TYPES.find((t) => t.value === project.input_type)?.label}</Badge>
          </div>
          <h1 className="font-display text-2xl font-semibold text-ink">{project.title}</h1>
          <p className="text-sm text-muted mt-2 leading-relaxed">{project.description}</p>
        </div>
        <div className="flex gap-2.5 shrink-0">
          {sessionInProgress && (
            <Button icon={Play} onClick={() => navigate(`/session/${session.id}`)}>
              Open live session
            </Button>
          )}
          {reportId && (
            <Button icon={FileBarChart} onClick={() => navigate(`/reports/${reportId}`)}>
              View report
            </Button>
          )}
          {!session && (
            <Button icon={Play} onClick={() => navigate("/new-session")}>
              Convene the board
            </Button>
          )}
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <GlassCard className="p-6 lg:col-span-2">
          <h3 className="font-display font-semibold text-ink mb-4 flex items-center gap-2">
            <Presentation className="w-4 h-4 text-accentblue" /> Session history
          </h3>
          {session ? (
            <div className="flex items-center justify-between p-4 rounded-xl glass">
              <div>
                <p className="text-sm text-ink font-medium">Session {session.id}</p>
                <p className="text-xs text-muted mt-1 flex items-center gap-1.5">
                  <Clock className="w-3 h-3" />
                  {session.started_at ? `Started ${new Date(session.started_at).toLocaleString()}` : "Not started yet"}
                </p>
              </div>
              <Badge tone={session.status === "completed" ? "green" : "blue"} dot>
                {session.status.replace("_", " ")}
              </Badge>
            </div>
          ) : (
            <p className="text-sm text-muted">No session has been run for this project yet.</p>
          )}
        </GlassCard>

        <GlassCard className="p-6">
          <h3 className="font-display font-semibold text-ink mb-4">Board composition</h3>
          <div className="flex flex-col gap-2">
            {(session?.agents_selected || []).map((key) => {
              const a = AGENTS[key];
              if (!a) return null;
              return (
                <div key={key} className="flex items-center gap-2.5 text-sm">
                  <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: a.color }} />
                  <span className="text-ink">{a.title}</span>
                </div>
              );
            })}
            {!session?.agents_selected?.length && <p className="text-xs text-muted">Agents are selected once a session starts.</p>}
          </div>
        </GlassCard>
      </div>
    </PageTransition>
  );
}
