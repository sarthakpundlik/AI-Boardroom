import { useEffect, useRef, useState, useCallback } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { FileBarChart, Radio, CheckCircle2 } from "lucide-react";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import PageTransition from "../components/ui/PageTransition";
import BoardroomTable from "../components/boardroom/BoardroomTable";
import RoundTracker from "../components/boardroom/RoundTracker";
import TimelineFeed from "../components/boardroom/TimelineFeed";
import { AGENTS } from "../data/agents";
import { DEMO_REPORT } from "../data/mock";
import { useBoardroomSocket } from "../lib/ws";
import { SessionsAPI, ReportsAPI } from "../lib/api";

// Derives the SESSION_STAGES value ("round_1", "synthesis", ...) that the
// RoundTracker expects, from the live event stream.
function deriveStage(events, round) {
  if (!events.length) return "preprocessing";
  const last = events[events.length - 1];
  if (last.type === "session_completed") return "completed";
  if (last.type === "ceo_started" || events.some((e) => e.type === "ceo_started")) return "synthesis";
  return `round_${round}`;
}

/** Plays a scripted event sequence with realistic pacing, for demo mode. */
function useScriptedPlayback(agentKeys, onEvent, active) {
  const timeoutsRef = useRef([]);

  useEffect(() => {
    if (!active) return;
    const timeouts = timeoutsRef.current;
    let t = 400;

    const schedule = (fn, delay) => {
      t += delay;
      timeouts.push(setTimeout(fn, t));
    };

    [1, 2, 3].forEach((round) => {
      if (round > 1) {
        schedule(() => onEvent({ type: "round_advanced", payload: { round } }), 500);
      }
      agentKeys.forEach((agent) => {
        schedule(() => onEvent({ type: "agent_started", payload: { agent, round } }), 450);
        schedule(() => onEvent({ type: "agent_finished", payload: { agent, round } }), 950);
      });
    });
    schedule(() => onEvent({ type: "ceo_started", payload: {} }), 700);
    schedule(() => onEvent({ type: "session_completed", payload: {} }), 1600);

    return () => {
      timeouts.forEach(clearTimeout);
      timeoutsRef.current = [];
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [active]);
}

const DEFAULT_AGENTS = ["CFO", "CTO", "CMO", "COO", "CISO", "CHRO", "CCO", "CDO"];

export default function Session() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isDemo = sessionId === "demo" || !sessionId;

  const [agentKeys, setAgentKeys] = useState(location.state?.agents || DEFAULT_AGENTS);
  const [projectTitle, setProjectTitle] = useState(location.state?.title || "Live boardroom session");
  const [projectId, setProjectId] = useState(location.state?.projectId || null);
  const [resolvedReportId, setResolvedReportId] = useState(null);

  // Demo-mode local event state (mirrors useBoardroomSocket's shape exactly).
  const [demoEvents, setDemoEvents] = useState([]);
  const [demoAgentStatus, setDemoAgentStatus] = useState({});
  const [demoRound, setDemoRound] = useState(1);

  const applyDemoEvent = useCallback((evt) => {
    setDemoEvents((prev) => [...prev, { ...evt, ts: Date.now() }]);
    setDemoAgentStatus((prev) => {
      const next = { ...prev };
      if (evt.type === "agent_started") next[evt.payload.agent] = "thinking";
      if (evt.type === "agent_finished") next[evt.payload.agent] = "done";
      if (evt.type === "ceo_started") next.CEO = "thinking";
      if (evt.type === "session_completed") next.CEO = "done";
      if (evt.type === "round_advanced") {
        setDemoRound(evt.payload.round);
        return {};
      }
      return next;
    });
  }, []);

  useScriptedPlayback(agentKeys, applyDemoEvent, isDemo);

  // Real mode: on a direct load / refresh (no router state), fetch the
  // session so we know which agents ran and which project it belongs to.
  useEffect(() => {
    if (isDemo || location.state?.agents) return;
    let cancelled = false;
    SessionsAPI.get(sessionId)
      .then(({ data }) => {
        if (cancelled) return;
        if (data.agents_selected?.length) setAgentKeys(data.agents_selected);
        setProjectId(data.project_id);
        if (data.status === "completed") {
          // Session already finished before we connected — find its report directly.
          ReportsAPI.listForProject(data.project_id).then(({ data: reportData }) => {
            const match = reportData.reports.find((r) => r.session_id === sessionId);
            if (match) setResolvedReportId(match.id);
          });
        }
      })
      .catch(() => {
        // Best effort — fall back to defaults if the session can't be fetched.
      });
    return () => {
      cancelled = true;
    };
  }, [isDemo, sessionId, location.state]);

  // Real mode: live WebSocket, matching backend/app/websocket/events.py.
  const live = useBoardroomSocket(sessionId, { enabled: !isDemo });

  const events = isDemo ? demoEvents : live.events;
  const agentStatus = isDemo ? demoAgentStatus : live.agentStatus;
  const round = isDemo ? demoRound : live.round;
  const stage = deriveStage(events, round);
  const isComplete = stage === "completed";
  const reportId = isDemo ? DEMO_REPORT.id : live.reportId || resolvedReportId;

  const finishedAgents = agentKeys.filter((k) => agentStatus[k] === "done");

  const goToReport = () => {
    if (reportId) navigate(`/reports/${reportId}`);
  };

  return (
    <PageTransition>
      <Topbar
        title={projectTitle}
        subtitle={isDemo ? "Simulated session — connect the API to see this run live." : "Live session"}
        actions={
          isComplete && (
            <Button icon={FileBarChart} onClick={goToReport} disabled={!reportId}>
              View board report
            </Button>
          )
        }
      />

      {!isDemo && live.error && (
        <GlassCard className="p-4 mb-6 border border-red-500/30">
          <p className="text-sm text-red-500">{live.error}</p>
        </GlassCard>
      )}

      <GlassCard className="p-5 mb-6">
        <RoundTracker currentStage={stage} />
      </GlassCard>

      <div className="grid lg:grid-cols-5 gap-6">
        {/* The boardroom table — signature visual */}
        <GlassCard heavy className="lg:col-span-3 p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-display font-semibold text-ink text-sm">The boardroom</h3>
            <span className="flex items-center gap-1.5 text-[11px] font-mono text-muted">
              {isComplete ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5 text-accentgreen" /> synthesis complete
                </>
              ) : (
                <>
                  <Radio className="w-3.5 h-3.5 text-accentblue animate-pulse" /> round {round} of 3
                </>
              )}
            </span>
          </div>
          <BoardroomTable activeAgentKeys={["CEO", ...agentKeys]} agentStatus={agentStatus} />

          {/* Findings as they land */}
          <div className="mt-4 flex flex-col gap-2">
            <AnimatePresence>
              {finishedAgents.map((key) => {
                const a = AGENTS[key];
                if (!a) return null;
                return (
                  <motion.div
                    key={key}
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="flex items-center gap-2.5 px-3 py-2 rounded-lg glass text-xs"
                  >
                    <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: a.color }} />
                    <span className="text-ink font-medium">{a.title}</span>
                    <span className="text-muted">submitted analysis</span>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        </GlassCard>

        {/* Live timeline */}
        <GlassCard className="lg:col-span-2 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-semibold text-ink text-sm">Session activity</h3>
            <Badge tone={isComplete ? "green" : "blue"} dot>{isComplete ? "complete" : "streaming"}</Badge>
          </div>
          <TimelineFeed events={events} />
        </GlassCard>
      </div>

      {isComplete && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="mt-6">
          <GlassCard heavy className="p-6 flex items-center justify-between gap-4 flex-wrap">
            <div>
              <h3 className="font-display font-semibold text-ink">The board has reached a decision</h3>
              <p className="text-xs text-muted mt-1">The CEO agent has synthesized every department's findings into a final report.</p>
            </div>
            <Button icon={FileBarChart} onClick={goToReport} disabled={!reportId}>
              Read the report
            </Button>
          </GlassCard>
        </motion.div>
      )}
    </PageTransition>
  );
}
