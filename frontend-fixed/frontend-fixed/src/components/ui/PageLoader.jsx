export default function PageLoader() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-14 h-14">
          <div className="absolute inset-0 rounded-full border-2 border-line/10" />
          <div className="absolute inset-0 rounded-full border-2 border-t-accentblue border-r-accentgreen border-b-transparent border-l-transparent animate-spin" />
        </div>
        <p className="text-sm text-muted font-mono tracking-wide">Loading the boardroom…</p>
      </div>
    </div>
  );
}
