import { Check } from "lucide-react";
import { SESSION_STAGES } from "../../data/agents";

export default function RoundTracker({ currentStage = "pending" }) {
  const currentIdx = SESSION_STAGES.findIndex((s) => s.value === currentStage);

  return (
    <div className="flex items-center overflow-x-auto no-scrollbar pb-1">
      {SESSION_STAGES.map((stage, i) => {
        const done = i < currentIdx;
        const active = i === currentIdx;
        return (
          <div key={stage.value} className="flex items-center shrink-0">
            <div className="flex flex-col items-center gap-1.5 min-w-[92px]">
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center text-[11px] font-semibold transition-all duration-300 ${
                  done
                    ? "bg-accentgreen text-white"
                    : active
                    ? "bg-gradient-to-br from-accentblue to-accentgreen text-white shadow-glow"
                    : "glass text-muted"
                }`}
              >
                {done ? <Check className="w-3.5 h-3.5" strokeWidth={3} /> : i + 1}
              </div>
              <span
                className={`text-[10px] text-center leading-tight ${
                  active ? "text-ink font-medium" : "text-muted"
                }`}
              >
                {stage.label}
              </span>
            </div>
            {i < SESSION_STAGES.length - 1 && (
              <div
                className={`h-[2px] w-8 mb-5 transition-colors duration-500 ${
                  done ? "bg-accentgreen" : "bg-line/15"
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
