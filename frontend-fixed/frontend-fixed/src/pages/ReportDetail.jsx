import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  Download,
  ChevronDown,
  Crown,
  ShieldAlert,
  Scale,
  FileText,
  FileType,
  Presentation as PresentationIcon,
} from "lucide-react";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import PageTransition from "../components/ui/PageTransition";
import { DEMO_REPORT } from "../data/mock";
import { AGENTS } from "../data/agents";
import { useAuth } from "../context/AuthContext";
import { ReportsAPI, resolveMediaUrl } from "../lib/api";

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

const EXPORTS = [
  { format: "pdf", label: "PDF", icon: FileText },
  { format: "docx", label: "Word", icon: FileType },
  { format: "ppt", label: "Slides", icon: PresentationIcon },
];

function ConfidenceBar({ value, color }) {
  return (
    <div className="w-full h-1.5 rounded-full bg-ink/5 overflow-hidden">
      <div
        className="h-full rounded-full transition-all duration-700"
        style={{ width: `${value}%`, backgroundColor: color }}
      />
    </div>
  );
}

function AgentFindingRow({ finding }) {
  const [open, setOpen] = useState(false);
  const agent = AGENTS[finding.agent];
  return (
    <div className="rounded-xl glass overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center gap-3 p-4 text-left"
      >
        <span
          className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-display font-semibold text-white shrink-0"
          style={{ background: `linear-gradient(135deg, ${agent.color}, ${agent.color}99)` }}
        >
          {agent.label.slice(0, 2).toUpperCase()}
        </span>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-ink">{agent.title}</p>
          <p className="text-xs text-muted truncate">{finding.summary}</p>
        </div>
        <div className="hidden sm:flex flex-col items-end w-24 shrink-0 gap-1">
          <span className="text-[10px] font-mono text-muted">{finding.confidence_score}% confidence</span>
          <ConfidenceBar value={finding.confidence_score} color={agent.color} />
        </div>
        <ChevronDown className={`w-4 h-4 text-muted shrink-0 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="px-4 pb-4"
          >
            <p className="text-xs text-muted leading-relaxed border-t border-line/10 pt-3">{agent.description}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function ReportDetail() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { demoMode } = useAuth();

  const [report, setReport] = useState(demoMode ? DEMO_REPORT : null);
  const [loading, setLoading] = useState(!demoMode);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    if (demoMode) return;
    let cancelled = false;
    ReportsAPI.get(id)
      .then(({ data }) => {
        if (!cancelled) setReport(data);
      })
      .catch(() => {
        if (!cancelled) setNotFound(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [demoMode, id]);

  if (loading) {
    return (
      <PageTransition>
        <GlassCard className="p-12 text-center">
          <p className="text-sm text-muted">Loading report…</p>
        </GlassCard>
      </PageTransition>
    );
  }

  if (notFound || !report) {
    return (
      <PageTransition>
        <GlassCard className="p-12 text-center">
          <p className="text-sm text-muted">This report couldn't be found.</p>
          <Button className="mt-4" onClick={() => navigate("/reports")}>Back to reports</Button>
        </GlassCard>
      </PageTransition>
    );
  }

  const content = report.full_content;

  return (
    <PageTransition>
      <button
        onClick={() => navigate("/reports")}
        className="flex items-center gap-1.5 text-xs text-muted hover:text-ink mb-6 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to reports
      </button>

      <div className="flex items-start justify-between gap-4 flex-wrap mb-8">
        <div className="max-w-2xl">
          <Badge tone={OUTCOME_TONE[content.decision_outcome]} dot className="mb-3">
            {OUTCOME_LABEL[content.decision_outcome]}
          </Badge>
          <h1 className="font-display text-2xl md:text-3xl font-semibold text-ink">{report.title}</h1>
          <p className="text-sm text-muted mt-2">Generated {new Date(report.created_at).toLocaleString()}</p>
        </div>
        <div className="flex gap-2 shrink-0">
          {EXPORTS.map(({ format, label, icon: Icon }) => {
            const available = format === "pdf" && (demoMode || report.pdf_url);
            return (
              <Button
                key={format}
                variant="secondary"
                size="sm"
                icon={Icon}
                disabled={!available}
                title={format !== "pdf" ? "Coming soon" : !available ? "PDF not ready yet" : undefined}
                onClick={() => {
                  if (format === "pdf" && report.pdf_url) {
                    window.open(resolveMediaUrl(report.pdf_url), "_blank");
                  }
                }}
              >
                {label}
              </Button>
            );
          })}
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 flex flex-col gap-6">
          <GlassCard heavy className="p-6">
            <h3 className="font-display font-semibold text-ink mb-3 flex items-center gap-2">
              <Crown className="w-4 h-4 text-[#FFD700]" /> Executive summary
            </h3>
            <p className="text-sm text-ink/90 leading-relaxed">{content.executive_summary}</p>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="font-display font-semibold text-ink mb-4">Key decisions</h3>
            <ul className="flex flex-col gap-3">
              {content.key_decisions.map((d, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-ink/90">
                  <span className="w-5 h-5 rounded-full bg-gradient-to-br from-accentblue to-accentgreen text-white text-[10px] font-semibold flex items-center justify-center shrink-0 mt-0.5">
                    {i + 1}
                  </span>
                  {d}
                </li>
              ))}
            </ul>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="font-display font-semibold text-ink mb-3 flex items-center gap-2">
              <Scale className="w-4 h-4 text-accentblue" /> Strategic plan
            </h3>
            <p className="text-sm text-muted leading-relaxed">{content.strategic_plan}</p>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="font-display font-semibold text-ink mb-3 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-accentwarm" /> Dissenting opinions, resolved
            </h3>
            <p className="text-sm text-muted leading-relaxed">{content.dissenting_opinions_resolved}</p>
          </GlassCard>
        </div>

        <div>
          <h3 className="font-display font-semibold text-ink mb-4 text-sm">Department findings</h3>
          <div className="flex flex-col gap-2.5">
            {content.agent_findings.map((f) => (
              <AgentFindingRow key={f.agent} finding={f} />
            ))}
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
