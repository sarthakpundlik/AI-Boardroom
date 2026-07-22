// IMPORTANT INTEGRATION NOTE (see README "Backend integration notes"):
// backend/app/core/config.py currently sets GOOGLE_REDIRECT_URI /
// MICROSOFT_REDIRECT_URI to the *backend's own* URL
// (http://localhost:8000/api/v1/auth/google/callback), but the router
// (auth/router.py) implements the callback as a POST endpoint that expects
// the frontend to already have the `code` and forward it as JSON. Those two
// things are incompatible with a single redirect_uri: the redirect_uri used
// when opening the provider's consent screen MUST be the URI Google/GitHub
// redirects back to (a page that can read `?code=` from the URL) — which
// has to be a FRONTEND route, not the backend API route.
//
// This file builds the authorize URL using frontend-owned callback routes
// and the code is then POSTed to the backend from AuthContext. Set the
// matching env vars documented in .env.example, and set the SAME redirect
// URI in the Google/GitHub OAuth app config and in the backend's
// GOOGLE_REDIRECT_URI setting.

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";
const GITHUB_CLIENT_ID = import.meta.env.VITE_GITHUB_CLIENT_ID || "";

export function googleRedirectUri() {
  return `${window.location.origin}/auth/callback/google`;
}

export function githubRedirectUri() {
  return `${window.location.origin}/auth/callback/github`;
}

export function buildGoogleAuthUrl() {
  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: googleRedirectUri(),
    response_type: "code",
    scope: "openid email profile",
    access_type: "offline",
    prompt: "consent",
    state: crypto.randomUUID(),
  });
  return `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
}

// GitHub sign-in: the backend repo only implements Google + Microsoft OAuth
// today (see app/auth/oauth.py). This button is wired end-to-end on the
// frontend and ready to go the moment a matching
// `/auth/github/callback` route + `exchange_github_code` /
// `get_github_user_info` pair is added on the backend, mirroring the
// existing Google implementation. See README for the ~20-line addition.
export function buildGithubAuthUrl() {
  const params = new URLSearchParams({
    client_id: GITHUB_CLIENT_ID,
    redirect_uri: githubRedirectUri(),
    scope: "read:user user:email",
    state: crypto.randomUUID(),
  });
  return `https://github.com/login/oauth/authorize?${params.toString()}`;
}
