import { AGENTS } from "../../data/agents";
import AgentNode from "./AgentNode";

/**
 * Renders the active agent roster seated around an oval "table" — the
 * literal visual metaphor of an AI Boardroom. CEO sits at the head; every
 * other selected agent is distributed evenly around the ellipse. Connector
 * lines pulse toward the center table while an agent is "thinking".
 */
export default function BoardroomTable({ activeAgentKeys, agentStatus = {} }) {
  const seatKeys = activeAgentKeys.filter((k) => k !== "CEO");
  const cx = 50;
  const cy = 54;
  const rx = 40;
  const ry = 30;

  const seats = seatKeys.map((key, i) => {
    // Distribute around the bottom ~300 degrees of the ellipse, leaving the
    // top clear for the CEO so the "head of the table" reads clearly.
    const startDeg = -80;
    const endDeg = 260;
    const t = seatKeys.length === 1 ? 0.5 : i / (seatKeys.length - 1);
    const deg = startDeg + t * (endDeg - startDeg);
    const rad = (deg * Math.PI) / 180;
    const x = cx + rx * Math.cos(rad);
    const y = cy + ry * Math.sin(rad);
    return { key, x, y };
  });

  return (
    <div className="relative w-full aspect-[16/10] select-none">
      <svg viewBox="0 0 100 100" className="absolute inset-0 w-full h-full" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="tableGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="rgb(var(--accent-blue))" stopOpacity="0.16" />
            <stop offset="100%" stopColor="rgb(var(--accent-green))" stopOpacity="0.16" />
          </linearGradient>
        </defs>
        {/* Table surface */}
        <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="url(#tableGrad)" stroke="rgb(var(--line) / 0.15)" strokeWidth="0.4" />

        {/* Connector lines: each seat to the CEO's head-seat */}
        {seats.map(({ key, x, y }) => {
          const status = agentStatus[key] || "idle";
          const active = status === "thinking";
          const done = status === "done";
          return (
            <line
              key={key}
              x1={cx}
              y1={cy - ry - 6}
              x2={x}
              y2={y}
              stroke={active ? AGENTS[key]?.color : done ? "rgb(var(--accent-green))" : "rgb(var(--line) / 0.12)"}
              strokeWidth={active ? 0.6 : 0.3}
              strokeDasharray={active ? "2 1.5" : "0"}
              opacity={active ? 0.9 : done ? 0.5 : 0.4}
            >
              {active && (
                <animate attributeName="stroke-dashoffset" from="10" to="0" dur="0.6s" repeatCount="indefinite" />
              )}
            </line>
          );
        })}
      </svg>

      {/* CEO — head of the table */}
      <AgentNode
        agent={AGENTS.CEO}
        status={agentStatus.CEO || "idle"}
        size="lg"
        style={{ left: `${cx}%`, top: `${cy - ry - 6}%` }}
      />

      {/* Specialist agents around the table */}
      {seats.map(({ key, x, y }) => (
        <AgentNode key={key} agent={AGENTS[key]} status={agentStatus[key] || "idle"} style={{ left: `${x}%`, top: `${y}%` }} />
      ))}
    </div>
  );
}
