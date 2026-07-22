import { useState } from "react";
import { Check, Loader2 } from "lucide-react";

export default function AgentNode({ agent, status = "idle", style, size = "md" }) {
  const [hovered, setHovered] = useState(false);
  const dims = size === "lg" ? "w-16 h-16 text-base" : "w-12 h-12 text-sm";

  return (
    <div
      className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-1.5 z-10"
      style={style}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div
        className={`relative ${dims} rounded-full flex items-center justify-center font-display font-semibold text-white transition-all duration-500`}
        style={{
          background: `linear-gradient(135deg, ${agent.color}, ${agent.color}99)`,
          boxShadow:
            status === "thinking"
              ? `0 0 0 3px ${agent.color}33, 0 0 24px -2px ${agent.color}88`
              : status === "done"
              ? `0 0 0 2px ${agent.color}55`
              : "0 0 0 1px rgba(120,120,130,0.15)",
          opacity: status === "idle" ? 0.55 : 1,
        }}
      >
        {status === "thinking" && (
          <span
            className="absolute inset-0 rounded-full animate-ping"
            style={{ backgroundColor: `${agent.color}44` }}
          />
        )}
        {agent.label.slice(0, 2).toUpperCase()}
        {status === "done" && (
          <span className="absolute -bottom-0.5 -right-0.5 w-4.5 h-4.5 rounded-full bg-accentgreen flex items-center justify-center border-2 border-base">
            <Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
          </span>
        )}
        {status === "thinking" && (
          <span className="absolute -bottom-0.5 -right-0.5 w-4.5 h-4.5 rounded-full bg-surface flex items-center justify-center border-2 border-base">
            <Loader2 className="w-2.5 h-2.5 animate-spin" style={{ color: agent.color }} />
          </span>
        )}
      </div>
      <span className="text-[10px] font-medium text-muted whitespace-nowrap">{agent.label}</span>

      {hovered && (
        <div className="absolute top-full mt-2 w-56 glass-heavy rounded-xl p-3 shadow-glass z-30 pointer-events-none">
          <p className="text-xs font-semibold text-ink mb-0.5">{agent.title}</p>
          <p className="text-[11px] text-muted leading-relaxed">{agent.description}</p>
        </div>
      )}
    </div>
  );
}
