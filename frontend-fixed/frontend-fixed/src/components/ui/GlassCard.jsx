import clsx from "clsx";

export default function GlassCard({ children, className, heavy = false, hover = false, as: Tag = "div", ...rest }) {
  return (
    <Tag
      className={clsx(
        heavy ? "glass-heavy" : "glass",
        "rounded-2xl shadow-glass-sm transition-all duration-300",
        hover && "hover:shadow-glass hover:-translate-y-0.5 hover:border-accentblue/30",
        className
      )}
      {...rest}
    >
      {children}
    </Tag>
  );
}
