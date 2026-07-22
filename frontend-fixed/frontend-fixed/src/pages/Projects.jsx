import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Plus, Clock, ChevronRight } from "lucide-react";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import PageTransition from "../components/ui/PageTransition";
import { DEMO_PROJECTS } from "../data/mock";
import { INPUT_TYPES } from "../data/agents";
import { useAuth } from "../context/AuthContext";
import { ProjectsAPI } from "../lib/api";

const STATUS_TONE = { draft: "neutral", active: "blue", completed: "green", archived: "neutral" };
const FILTERS = ["all", "draft", "active", "completed", "archived"];

function timeAgo(iso) {
  const diff = Date.now() - new Date(iso).getTime();
  const hrs = Math.round(diff / 3600000);
  if (hrs < 1) return "just now";
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.round(hrs / 24)}d ago`;
}

export default function Projects() {
  const navigate = useNavigate();
  const { demoMode } = useAuth();
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [projects, setProjects] = useState(demoMode ? DEMO_PROJECTS : []);
  const [loading, setLoading] = useState(!demoMode);

  useEffect(() => {
    if (demoMode) return;
    let cancelled = false;
    ProjectsAPI.list(1, 100)
      .then(({ data }) => {
        if (!cancelled) setProjects(data.projects);
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [demoMode]);

  const filtered = useMemo(() => {
    return projects.filter((p) => {
      const matchesFilter = filter === "all" || p.status === filter;
      const matchesQuery = p.title.toLowerCase().includes(query.toLowerCase());
      return matchesFilter && matchesQuery;
    });
  }, [projects, query, filter]);

  return (
    <PageTransition>
      <Topbar
        title="Projects"
        subtitle="Every idea, dataset, and proposal you've brought to the board."
        actions={
          <Button icon={Plus} onClick={() => navigate("/new-session")}>
            New project
          </Button>
        }
      />

      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-muted absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search projects…"
            className="w-full rounded-xl glass pl-10 pr-4 py-2.5 text-sm text-ink placeholder:text-muted/70 focus:outline-none focus:ring-2 focus:ring-accentblue/50 transition-all"
          />
        </div>
        <div className="flex gap-1.5 overflow-x-auto no-scrollbar">
          {FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`shrink-0 text-xs px-3.5 py-2 rounded-xl capitalize transition-colors ${
                filter === f ? "bg-gradient-to-r from-accentblue to-accentgreen text-white" : "glass text-muted hover:text-ink"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <GlassCard className="p-12 text-center">
          <p className="text-sm text-muted">Loading projects…</p>
        </GlassCard>
      ) : filtered.length === 0 ? (
        <GlassCard className="p-12 text-center">
          <p className="text-sm text-muted">
            {projects.length === 0 ? "No projects yet — start your first boardroom session." : "No projects match that search."}
          </p>
        </GlassCard>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((p) => (
            <GlassCard
              key={p.id}
              hover
              className="p-5 cursor-pointer flex items-center justify-between gap-4"
              onClick={() => navigate(`/projects/${p.id}`)}
            >
              <div className="min-w-0">
                <div className="flex items-center gap-2.5 mb-1.5">
                  <h4 className="text-sm font-medium text-ink truncate">{p.title}</h4>
                  <Badge tone={STATUS_TONE[p.status]} dot>{p.status}</Badge>
                </div>
                <p className="text-xs text-muted truncate max-w-xl">{p.description}</p>
                <div className="flex items-center gap-3 mt-2 text-[11px] text-muted">
                  <span>{INPUT_TYPES.find((t) => t.value === p.input_type)?.label}</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {timeAgo(p.updated_at)}</span>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-muted shrink-0" />
            </GlassCard>
          ))}
        </div>
      )}
    </PageTransition>
  );
}
