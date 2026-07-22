import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileBarChart, ChevronRight, Clock } from "lucide-react";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Badge from "../components/ui/Badge";
import PageTransition from "../components/ui/PageTransition";
import { DEMO_REPORT } from "../data/mock";
import { useAuth } from "../context/AuthContext";
import { ReportsAPI } from "../lib/api";

const OUTCOME_TONE = {
  go: "green",
  go_with_modifications: "blue",
  needs_further_research: "warm",
  not_recommended: "red",
};
const OUTCOME_LABEL = {
  go: "Go",
  go_with_modifications: "Go, with modifications",
  needs_further_research: "Needs further research",
  not_recommended: "Not recommended",
};

export default function Reports() {
  const navigate = useNavigate();
  const { demoMode } = useAuth();
  const [reports, setReports] = useState(demoMode ? [DEMO_REPORT] : []);
  const [loading, setLoading] = useState(!demoMode);

  useEffect(() => {
    if (demoMode) return;
    let cancelled = false;
    ReportsAPI.list(1, 50)
      .then(({ data }) => {
        if (!cancelled) setReports(data.reports);
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [demoMode]);

  return (
    <PageTransition>
      <Topbar title="Reports" subtitle="Final board decisions, synthesized by the CEO agent from every department's findings." />

      <div className="flex flex-col gap-3">
        {loading && (
          <GlassCard className="p-10 text-center">
            <p className="text-sm text-muted">Loading reports…</p>
          </GlassCard>
        )}

        {!loading &&
          reports.map((report) => (
            <GlassCard
              key={report.id}
              hover
              className="p-5 cursor-pointer flex items-center justify-between gap-4 flex-wrap"
              onClick={() => navigate(`/reports/${report.id}`)}
            >
              <div className="flex items-start gap-4 min-w-0">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accentblue to-accentgreen flex items-center justify-center shrink-0">
                  <FileBarChart className="w-5 h-5 text-white" />
                </div>
                <div className="min-w-0">
                  <h4 className="text-sm font-medium text-ink truncate">{report.title}</h4>
                  <p className="text-xs text-muted mt-1 line-clamp-1 max-w-lg">{report.summary}</p>
                  <span className="text-[11px] text-muted mt-2 flex items-center gap-1">
                    <Clock className="w-3 h-3" /> {new Date(report.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <Badge tone={OUTCOME_TONE[report.full_content.decision_outcome]} dot>
                  {OUTCOME_LABEL[report.full_content.decision_outcome]}
                </Badge>
                <ChevronRight className="w-4 h-4 text-muted" />
              </div>
            </GlassCard>
          ))}

        {!loading && reports.length === 0 && (
          <GlassCard className="p-10 text-center">
            <p className="text-sm text-muted">Reports from sessions still in progress will appear here once the board reaches synthesis.</p>
          </GlassCard>
        )}
      </div>
    </PageTransition>
  );
}
