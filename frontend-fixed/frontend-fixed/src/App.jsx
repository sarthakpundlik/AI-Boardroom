import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AppShell from "./components/layout/AppShell";
import PageLoader from "./components/ui/PageLoader";

import SignIn from "./pages/SignIn";
import OAuthCallback from "./pages/OAuthCallback";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import NewSession from "./pages/NewSession";
import Session from "./pages/Session";
import Reports from "./pages/Reports";
import ReportDetail from "./pages/ReportDetail";
import Notifications from "./pages/Notifications";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

function RootRedirect() {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <PageLoader />;
  return <Navigate to={isAuthenticated ? "/dashboard" : "/sign-in"} replace />;
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<RootRedirect />} />
            <Route path="/sign-in" element={<SignIn />} />
            <Route path="/auth/callback/:provider" element={<OAuthCallback />} />

            <Route
              element={
                <ProtectedRoute>
                  <AppShell />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/projects/:id" element={<ProjectDetail />} />
              <Route path="/new-session" element={<NewSession />} />
              <Route path="/session/:sessionId" element={<Session />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/reports/:id" element={<ReportDetail />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/settings" element={<Settings />} />
            </Route>

            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}
