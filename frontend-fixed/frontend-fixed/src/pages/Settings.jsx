import { Sun, Moon, Shield, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Topbar from "../components/layout/Topbar";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import { Input } from "../components/ui/Input";
import PageTransition from "../components/ui/PageTransition";
import { useTheme } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";

export default function Settings() {
  const { theme, setTheme } = useTheme();
  const { user, logout, demoMode } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/sign-in");
  };

  return (
    <PageTransition>
      <Topbar title="Settings" subtitle="Your account, appearance, and connected sign-in providers." />

      <div className="grid lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <h3 className="font-display font-semibold text-ink mb-4">Profile</h3>
          <div className="flex items-center gap-4 mb-5">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-accentblue to-accentgreen flex items-center justify-center text-white font-display font-semibold text-lg">
              {user?.name?.[0]?.toUpperCase() || "U"}
            </div>
            <div>
              <p className="text-sm font-medium text-ink">{user?.name}</p>
              <p className="text-xs text-muted">{user?.email}</p>
              {demoMode && <Badge tone="warm" className="mt-1.5">Demo account</Badge>}
            </div>
          </div>
          <div className="grid sm:grid-cols-2 gap-4">
            <Input label="Full name" defaultValue={user?.name} disabled={demoMode} />
            <Input label="Email" defaultValue={user?.email} disabled={demoMode} />
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <h3 className="font-display font-semibold text-ink mb-4">Appearance</h3>
          <p className="text-xs text-muted mb-4">Choose how the boardroom console looks.</p>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => setTheme("light")}
              className={`flex flex-col items-center gap-2 p-4 rounded-xl border transition-all ${
                theme === "light" ? "border-accentblue/40 bg-accentblue/5" : "glass border-transparent"
              }`}
            >
              <Sun className="w-5 h-5 text-accentblue" />
              <span className="text-xs font-medium text-ink">Light</span>
            </button>
            <button
              onClick={() => setTheme("dark")}
              className={`flex flex-col items-center gap-2 p-4 rounded-xl border transition-all ${
                theme === "dark" ? "border-accentwarm/40 bg-accentwarm/5" : "glass border-transparent"
              }`}
            >
              <Moon className="w-5 h-5 text-accentwarm" />
              <span className="text-xs font-medium text-ink">Dark</span>
            </button>
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <h3 className="font-display font-semibold text-ink mb-4">Connected sign-in</h3>
          <div className="flex flex-col gap-2.5">
            <div className="flex items-center justify-between p-3 rounded-xl glass">
              <span className="text-sm text-ink">Google</span>
              <Badge tone={user?.oauth_provider === "google" ? "green" : "neutral"}>
                {user?.oauth_provider === "google" ? "Connected" : "Not connected"}
              </Badge>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl glass">
              <span className="text-sm text-ink">GitHub</span>
              <Badge tone={user?.oauth_provider === "github" ? "green" : "neutral"}>
                {user?.oauth_provider === "github" ? "Connected" : "Not connected"}
              </Badge>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <h3 className="font-display font-semibold text-ink mb-4 flex items-center gap-2">
            <Shield className="w-4 h-4 text-accentblue" /> Security
          </h3>
          <p className="text-xs text-muted mb-4">Sign out of AI Boardroom on this device.</p>
          <Button variant="danger" icon={LogOut} onClick={handleLogout}>
            Sign out
          </Button>
        </GlassCard>
      </div>
    </PageTransition>
  );
}
