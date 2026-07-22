import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  FolderKanban,
  FileBarChart,
  Bell,
  Settings,
  LogOut,
  Presentation,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import ThemeToggle from "../ui/ThemeToggle";

const NAV = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/reports", label: "Reports", icon: FileBarChart },
  { to: "/notifications", label: "Notifications", icon: Bell },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/sign-in");
  };

  return (
    <aside className="hidden lg:flex flex-col w-64 shrink-0 h-screen sticky top-0 p-4">
      <div className="glass-heavy rounded-2xl flex flex-col h-full p-4">
        <div className="flex items-center gap-2.5 px-2 py-3 mb-4">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accentblue to-accentgreen flex items-center justify-center shadow-glass-sm">
            <Presentation className="w-4.5 h-4.5 text-white" strokeWidth={2.2} />
          </div>
          <div>
            <p className="font-display font-semibold text-sm text-ink leading-tight">AI Boardroom</p>
            <p className="text-[11px] text-muted font-mono">Executive Console</p>
          </div>
        </div>

        <nav className="flex-1 flex flex-col gap-1">
          {NAV.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-accentblue/15 to-accentgreen/10 text-ink border border-accentblue/25 shadow-glass-sm"
                    : "text-muted hover:text-ink hover:bg-ink/5 border border-transparent"
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="pt-3 mt-3 border-t border-line/10 space-y-3">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs text-muted">Theme</span>
            <ThemeToggle />
          </div>

          <div className="flex items-center gap-2.5 px-2 py-2 rounded-xl hover:bg-ink/5 transition-colors">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accentblue to-accentgreen flex items-center justify-center text-white text-xs font-semibold shrink-0">
              {user?.name?.[0]?.toUpperCase() || "U"}
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-medium text-ink truncate">{user?.name}</p>
              <p className="text-[11px] text-muted truncate">{user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              aria-label="Sign out"
              className="text-muted hover:text-red-400 transition-colors shrink-0"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}
