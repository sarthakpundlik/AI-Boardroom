import { NavLink } from "react-router-dom";
import { LayoutDashboard, FolderKanban, FileBarChart, Bell, Settings } from "lucide-react";

const NAV = [
  { to: "/dashboard", label: "Home", icon: LayoutDashboard },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/reports", label: "Reports", icon: FileBarChart },
  { to: "/notifications", label: "Alerts", icon: Bell },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function MobileNav() {
  return (
    <nav className="lg:hidden fixed bottom-3 left-3 right-3 z-40">
      <div className="glass-heavy rounded-2xl flex items-center justify-around py-2 px-1 shadow-glass">
        {NAV.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex flex-col items-center gap-0.5 px-3 py-1.5 rounded-xl text-[10px] font-medium transition-colors ${
                isActive ? "text-accentblue" : "text-muted"
              }`
            }
          >
            <Icon className="w-4.5 h-4.5" />
            {label}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
