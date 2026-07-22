import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bell, CheckCheck } from "lucide-react";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import PageTransition from "../components/ui/PageTransition";
import { DEMO_NOTIFICATIONS } from "../data/mock";
import { useAuth } from "../context/AuthContext";
import { NotificationsAPI } from "../lib/api";

function timeAgo(iso) {
  const diff = Date.now() - new Date(iso).getTime();
  const hrs = Math.round(diff / 3600000);
  if (hrs < 1) return "just now";
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.round(hrs / 24)}d ago`;
}

export default function Notifications() {
  const navigate = useNavigate();
  const { demoMode } = useAuth();
  const [items, setItems] = useState(demoMode ? DEMO_NOTIFICATIONS : []);
  const [loading, setLoading] = useState(!demoMode);
  const unreadCount = items.filter((n) => !n.is_read).length;

  useEffect(() => {
    if (demoMode) return;
    let cancelled = false;
    NotificationsAPI.list(1, 50)
      .then(({ data }) => {
        if (!cancelled) setItems(data.notifications);
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [demoMode]);

  const markOneRead = (n) => {
    if (n.is_read) return;
    setItems((prev) => prev.map((x) => (x.id === n.id ? { ...x, is_read: true } : x)));
    if (!demoMode) NotificationsAPI.markRead(n.id).catch(() => {});
  };

  const markAllRead = () => {
    setItems((prev) => prev.map((n) => ({ ...n, is_read: true })));
    if (!demoMode) NotificationsAPI.markAllRead().catch(() => {});
  };

  const goToNotification = (n) => {
    markOneRead(n);
    if (n.type === "session_completed" && n.reference_id) navigate(`/reports/${n.reference_id}`);
  };

  return (
    <PageTransition>
      <Topbar
        title="Notifications"
        subtitle={loading ? "Loading…" : unreadCount ? `${unreadCount} unread` : "You're all caught up."}
        actions={
          unreadCount > 0 && (
            <Button variant="secondary" icon={CheckCheck} onClick={markAllRead}>
              Mark all read
            </Button>
          )
        }
      />

      <div className="flex flex-col gap-2.5">
        {!loading && items.length === 0 && (
          <GlassCard className="p-10 text-center">
            <p className="text-sm text-muted">No notifications yet.</p>
          </GlassCard>
        )}

        {items.map((n) => (
          <GlassCard
            key={n.id}
            className={`p-4 flex items-start gap-3.5 cursor-pointer transition-colors ${!n.is_read ? "border-accentblue/25" : ""}`}
            onClick={() => goToNotification(n)}
          >
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${!n.is_read ? "bg-accentblue/12 text-accentblue" : "bg-ink/5 text-muted"}`}>
              <Bell className="w-4 h-4" />
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <p className={`text-sm ${!n.is_read ? "text-ink font-medium" : "text-muted"}`}>{n.title}</p>
                {!n.is_read && <span className="w-1.5 h-1.5 rounded-full bg-accentblue shrink-0" />}
              </div>
              <p className="text-xs text-muted mt-0.5">{n.message}</p>
            </div>
            <span className="text-[11px] text-muted shrink-0 font-mono">{timeAgo(n.created_at)}</span>
          </GlassCard>
        ))}
      </div>
    </PageTransition>
  );
}
