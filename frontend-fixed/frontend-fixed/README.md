# AI Boardroom — Frontend

A production-styled React frontend for [AI-Boardroom](https://github.com/sarthakpundlik/AI-Boardroom): submit a business idea, dataset, or proposal, and watch a full "board" of AI department heads (CEO + 8 C-suite agents) debate it across three rounds before the CEO agent synthesizes a final decision.

Built to match the FastAPI backend's actual data contracts (Pydantic schemas, WebSocket event types, session state machine) field-for-field — see **Backend integration notes** below.

## Stack

- **React 19 + Vite** — no framework lock-in, fast HMR
- **Tailwind CSS** — design tokens driven entirely by CSS custom properties (see `src/index.css`) so light/dark theming is a single class toggle
- **Framer Motion** — page transitions, streaming timeline entries, findings reveal
- **React Router 7** — client-side routing + protected routes
- **Axios** — API client with automatic access-token refresh
- **lucide-react** — icon set
- **clsx** — conditional class composition

## Getting started

```bash
npm install
cp .env.example .env   # fill in your backend URL + OAuth client IDs
npm run dev
```

Open `http://localhost:5173`. Click **"Explore with demo data"** on the sign-in screen to preview the entire app — dashboard, live boardroom session, and report — with realistic fixture data and no backend running at all. This is the fastest way to see the design.

## Design system

- **Glassmorphism**: `.glass` / `.glass-heavy` utility classes (`backdrop-filter: blur + saturate`) layered over an ambient blurred-mesh background (`.mesh-bg`), used consistently for every panel, card, input, and nav surface.
- **Typography**: Space Grotesk (display/headings, bold and geometric) + Inter (body) + JetBrains Mono (timestamps, session IDs, technical labels).
- **Theming**: `ThemeContext` toggles a `.dark` class on `<html>`; every color is a CSS variable, so no component branches on theme.
  - **Light**: white / black / grey base, with deep navy + forest green as the accent pair.
  - **Dark**: black / white / grey base, with light orange, light blue, and light green as the accent trio.
- **Signature element — the Boardroom Table** (`src/components/boardroom/BoardroomTable.jsx`): an SVG oval table with the CEO seated at the head and every active department agent distributed around it. Pulsing dashed connector lines animate from an agent to the CEO while that agent is "thinking," and settle to a solid green tick when it finishes — this is the literal, live visualization of "AI Boardroom" the brief asked for, driven directly by WebSocket events.

## Project structure

```
src/
  components/
    boardroom/   BoardroomTable, AgentNode, RoundTracker, TimelineFeed — the live session visualization
    layout/      AppShell, Sidebar, Topbar, MobileNav
    ui/          GlassCard, Button, Badge, Input/Textarea/Select, ThemeToggle, PageLoader, PageTransition
    ProtectedRoute.jsx
  context/       ThemeContext, AuthContext (handles real auth + a local-only demo mode)
  data/
    agents.js    Mirrors backend/app/core/constants.py — AgentName, AGENT_COLORS, AGENT_SELECTION_MATRIX, SessionStatus
    mock.js      Demo-mode fixtures only, shaped exactly like the real API responses
  lib/
    api.js       Axios instance + typed endpoint groups (Auth/Users/Projects/Sessions/Reports/Notifications), token refresh interceptor
    oauth.js     Google + GitHub authorize-URL builders (see note below)
    ws.js        useBoardroomSocket() — WebSocket hook matching app/websocket/events.py exactly, with auto-reconnect
  pages/         SignIn, OAuthCallback, Dashboard, Projects, ProjectDetail, NewSession, Session, Reports, ReportDetail, Notifications, Settings, NotFound
```

## Backend integration notes

A few things worth knowing before wiring this up to `AI-Boardroom/backend`:

1. **GitHub sign-in isn't implemented on the backend yet.** `backend/app/core/constants.py` only defines `OAuthProvider.GOOGLE` and `OAuthProvider.MICROSOFT`, and `backend/app/auth/oauth.py` / `auth/router.py` only implement Google + Microsoft token exchange. The GitHub button is fully wired on the frontend (`buildGithubAuthUrl()` in `src/lib/oauth.js`, plus `/auth/callback/github` route) and will work the moment you add, mirroring the existing Google implementation:
   - `get_github_user_info(access_token)` and `exchange_github_code(code)` in `auth/oauth.py`
   - `OAuthProvider.GITHUB` in `core/constants.py`
   - `POST /auth/github/callback` in `auth/router.py`
   - `AuthAPI.githubCallback()` in `src/lib/api.js` (one line, same pattern as `googleCallback`)

2. **OAuth `redirect_uri` needs to point at the frontend, not the backend.** The provider's consent screen redirects the browser to `redirect_uri` with `?code=...` in the URL — that has to be a page that can read the URL, i.e. a frontend route (`/auth/callback/google`, `/auth/callback/github`), not the backend's own `/api/v1/auth/google/callback` POST endpoint. This frontend already implements it this way; just make sure `GOOGLE_REDIRECT_URI` in `backend/.env` and the redirect URI registered in the Google Cloud Console both match `http://localhost:5173/auth/callback/google` (or your deployed origin).

3. **Agent roster**: `src/data/agents.js` mirrors `AgentName` / `AGENT_COLORS` / `AGENT_SELECTION_MATRIX` from `core/constants.py` (Strategic, Business, Financial, Technical, Customer, Risk, Data, Devil's Advocate, Reviewer, CEO) because that's the enum the actual API schemas (`SessionResponse.agents_selected`, WebSocket payloads) use. Note this differs from the class names in `agents/specialized/` (`CFOAgent`, `CTOAgent`, etc. — mapped in `orchestrator/nodes.py`'s `AGENT_MAP`), which looks like an earlier naming pass that didn't get reconciled with `constants.py`. Worth aligning on the backend before shipping; the frontend follows the schema contract since that's what actually crosses the wire.

4. **WebSocket URL**: `useBoardroomSocket(sessionId)` connects to `${VITE_WS_URL}/${sessionId}`, matching `EventType` values in `app/websocket/events.py` exactly (`agent_started`, `agent_finished`, `round_advanced`, `ceo_started`, `session_completed`, `error`). Confirm this matches the route registered in `app/websocket/router.py`.

5. **Report export** (PDF/Word/Slides buttons on the report page) call out to `ExportFormat` (`pdf`/`docx`/`ppt`) — hook these up to whatever endpoint `app/reports/router.py` exposes for `reports/generator.py`; there's no export route wired into `ReportsAPI` yet since it wasn't visible in the router.

## Environment variables

See `.env.example`. All `VITE_*` variables are public (bundled into the client) — don't put secrets here.

## Notes

- Every screen degrades gracefully: if a real API call fails (e.g. no backend running), the sign-in screen offers **demo mode**, which is the fastest way to review the design end-to-end.
- Reduced-motion is respected globally (`prefers-reduced-motion`), and focus states are visible for keyboard navigation.
- Mobile: sidebar collapses to a bottom tab bar (`MobileNav.jsx`) under `lg` breakpoint.
