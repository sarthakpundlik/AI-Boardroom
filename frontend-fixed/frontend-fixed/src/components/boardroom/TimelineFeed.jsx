import { motion, AnimatePresence } from "framer-motion";
import { Play, CheckCircle2, ArrowRightCircle, Crown, PartyPopper, AlertTriangle } from "lucide-react";
import { AGENTS } from "../../data/agents";

const ICONS = {
  agent_started: Play,
  agent_finished: CheckCircle2,
  round_advanced: ArrowRightCircle,
  ceo_started: Crown,
  session_completed: PartyPopper,
  error: AlertTriangle,
};

function describe(evt) {
  const agent = evt.payload?.agent ? AGENTS[evt.payload.agent] : null;
  switch (evt.type) {
    case "agent_started":
      return `${agent?.title || evt.payload?.agent} started analyzing`;
    case "agent_finished":
      return `${agent?.title || evt.payload?.agent} finished — summary ready`;
    case "round_advanced":
      return `Advanced to round ${evt.payload?.round ?? evt.payload?.current_round ?? ""}`;
    case "ceo_started":
      return "CEO began final synthesis";
    case "session_completed":
      return "Session complete — board report generated";
    case "error":
      return evt.payload?.message || "An error occurred";
    default:
      return evt.type;
  }
}

export default function TimelineFeed({ events }) {
  if (!events.length) {
    return (
      <div className="text-sm text-muted text-center py-10 font-mono">
        Waiting for the room to convene…
      </div>
    );
  }

  return (
    <div className="flex flex-col-reverse gap-2 max-h-96 overflow-y-auto pr-1">
      <AnimatePresence initial={false}>
        {[...events].reverse().map((evt, i) => {
          const Icon = ICONS[evt.type] || Play;
          const agent = evt.payload?.agent ? AGENTS[evt.payload.agent] : null;
          const isError = evt.type === "error";
          return (
            <motion.div
              key={`${evt.ts}-${i}`}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.25 }}
              className="flex items-start gap-3 px-3 py-2.5 rounded-xl glass"
            >
              <div
                className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
                style={{
                  backgroundColor: isError ? "#EF444422" : agent ? `${agent.color}22` : "rgb(var(--accent-blue) / 0.12)",
                  color: isError ? "#EF4444" : agent?.color || "rgb(var(--accent-blue))",
                }}
              >
                <Icon className="w-3.5 h-3.5" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-xs text-ink leading-snug">{describe(evt)}</p>
                <p className="text-[10px] text-muted font-mono mt-0.5">
                  {new Date(evt.ts).toLocaleTimeString()}
                </p>
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
