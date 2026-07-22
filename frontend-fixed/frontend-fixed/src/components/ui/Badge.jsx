import clsx from "clsx";

const tones = {
  neutral: "bg-ink/5 text-muted border-line/10",
  blue: "bg-accentblue/10 text-accentblue border-accentblue/25",
  green: "bg-accentgreen/10 text-accentgreen border-accentgreen/25",
  warm: "bg-accentwarm/10 text-accentwarm border-accentwarm/25",
  red: "bg-red-500/10 text-red-400 border-red-500/25",
};

export default function Badge({ children, tone = "neutral", className, dot = false }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1.5 text-[11px] font-medium px-2.5 py-1 rounded-full border tracking-wide uppercase",
        tones[tone],
        className
      )}
    >
      {dot && <span className={clsx("w-1.5 h-1.5 rounded-full", tone === "neutral" ? "bg-muted" : "bg-current")} />}
      {children}
    </span>
  );
}
