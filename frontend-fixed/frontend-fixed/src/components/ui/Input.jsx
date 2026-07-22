import clsx from "clsx";

export function Input({ label, error, className, id, ...rest }) {
  return (
    <label className="block">
      {label && (
        <span className="block text-xs font-medium text-muted mb-1.5 tracking-wide uppercase">
          {label}
        </span>
      )}
      <input
        id={id}
        className={clsx(
          "w-full rounded-xl glass px-4 py-3 text-sm text-ink placeholder:text-muted/70",
          "focus:outline-none focus:ring-2 focus:ring-accentblue/50 focus:border-accentblue/50",
          "transition-all duration-200",
          error && "ring-2 ring-red-500/50 border-red-500/50",
          className
        )}
        {...rest}
      />
      {error && <span className="block text-xs text-red-400 mt-1.5">{error}</span>}
    </label>
  );
}

export function Textarea({ label, error, className, ...rest }) {
  return (
    <label className="block">
      {label && (
        <span className="block text-xs font-medium text-muted mb-1.5 tracking-wide uppercase">
          {label}
        </span>
      )}
      <textarea
        className={clsx(
          "w-full rounded-xl glass px-4 py-3 text-sm text-ink placeholder:text-muted/70 resize-none",
          "focus:outline-none focus:ring-2 focus:ring-accentblue/50 focus:border-accentblue/50",
          "transition-all duration-200",
          error && "ring-2 ring-red-500/50 border-red-500/50",
          className
        )}
        {...rest}
      />
      {error && <span className="block text-xs text-red-400 mt-1.5">{error}</span>}
    </label>
  );
}

export function Select({ label, className, children, ...rest }) {
  return (
    <label className="block">
      {label && (
        <span className="block text-xs font-medium text-muted mb-1.5 tracking-wide uppercase">
          {label}
        </span>
      )}
      <select
        className={clsx(
          "w-full rounded-xl glass px-4 py-3 text-sm text-ink appearance-none cursor-pointer",
          "focus:outline-none focus:ring-2 focus:ring-accentblue/50 focus:border-accentblue/50",
          "transition-all duration-200",
          className
        )}
        {...rest}
      >
        {children}
      </select>
    </label>
  );
}
