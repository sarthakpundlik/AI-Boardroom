import clsx from "clsx";
import { Loader2 } from "lucide-react";

const variants = {
  primary:
    "bg-gradient-to-r from-accentblue to-accentgreen text-white shadow-glass-sm hover:shadow-glow hover:brightness-110 border border-transparent",
  secondary:
    "glass text-ink hover:border-accentblue/40 hover:bg-surface/80",
  ghost:
    "text-muted hover:text-ink hover:bg-ink/5 border border-transparent",
  danger:
    "bg-red-500/90 text-white hover:bg-red-500 border border-transparent",
};

const sizes = {
  sm: "text-xs px-3 py-1.5 gap-1.5",
  md: "text-sm px-4 py-2.5 gap-2",
  lg: "text-base px-6 py-3.5 gap-2.5",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  icon: Icon,
  className,
  disabled,
  ...rest
}) {
  return (
    <button
      className={clsx(
        "inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 active:scale-[0.97] disabled:opacity-50 disabled:pointer-events-none",
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : (
        Icon && <Icon className="w-4 h-4" />
      )}
      {children}
    </button>
  );
}
