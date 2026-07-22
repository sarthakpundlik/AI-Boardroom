import { useNavigate } from "react-router-dom";
import { Compass } from "lucide-react";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";

export default function NotFound() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="mesh-bg" />
      <GlassCard heavy className="max-w-sm w-full p-8 text-center">
        <div className="w-12 h-12 rounded-full bg-accentblue/10 flex items-center justify-center mx-auto mb-4">
          <Compass className="w-6 h-6 text-accentblue" />
        </div>
        <h2 className="font-display font-semibold text-ink mb-2">This room is empty</h2>
        <p className="text-xs text-muted leading-relaxed mb-6">The page you're looking for doesn't exist, or has moved.</p>
        <Button className="w-full" onClick={() => navigate("/dashboard")}>
          Back to dashboard
        </Button>
      </GlassCard>
    </div>
  );
}
