export default function Topbar({ title, subtitle, actions }) {
  return (
    <div className="flex flex-wrap items-start justify-between gap-4 mb-8">
      <div>
        <h1 className="font-display text-2xl md:text-3xl font-semibold text-ink">{title}</h1>
        {subtitle && <p className="text-sm text-muted mt-1.5 max-w-xl">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-3">{actions}</div>}
    </div>
  );
}
