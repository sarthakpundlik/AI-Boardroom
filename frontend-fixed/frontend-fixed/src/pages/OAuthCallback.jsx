import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { AlertTriangle } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import GlassCard from "../components/ui/GlassCard";
import Button from "../components/ui/Button";

export default function OAuthCallback() {
  const { provider } = useParams(); // "google" | "github"
  const [params] = useSearchParams();
  const { handleOAuthCallback } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const ran = useRef(false);

  useEffect(() => {
    if (ran.current) return;
    ran.current = true;

    const code = params.get("code");
    const state = params.get("state");
    const oauthError = params.get("error");

    if (oauthError) {
      setError(`${provider} declined the request: ${oauthError}`);
      return;
    }
    if (!code) {
      setError("No authorization code was returned by the provider.");
      return;
    }

    handleOAuthCallback(provider, code, state)
      .then(() => navigate("/dashboard", { replace: true }))
      .catch((err) => {
        setError(err.response?.data?.detail || "Couldn't complete sign-in with this provider.");
      });
  }, [provider, params, handleOAuthCallback, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="mesh-bg" />
      <GlassCard heavy className="max-w-sm w-full p-8 text-center">
        {error ? (
          <>
            <div className="w-12 h-12 rounded-full bg-red-500/10 flex items-center justify-center mx-auto mb-4">
              <AlertTriangle className="w-6 h-6 text-red-400" />
            </div>
            <h2 className="font-display font-semibold text-ink mb-2">Sign-in didn't complete</h2>
            <p className="text-xs text-muted leading-relaxed mb-6">{error}</p>
            <Button className="w-full" onClick={() => navigate("/sign-in")}>
              Back to sign in
            </Button>
          </>
        ) : (
          <>
            <div className="relative w-12 h-12 mx-auto mb-4">
              <div className="absolute inset-0 rounded-full border-2 border-line/10" />
              <div className="absolute inset-0 rounded-full border-2 border-t-accentblue border-r-accentgreen border-b-transparent border-l-transparent animate-spin" />
            </div>
            <p className="text-sm text-muted">Finishing sign-in with {provider}…</p>
          </>
        )}
      </GlassCard>
    </div>
  );
}
