import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser } from "../lib/api.js";
import { getSession } from "../lib/auth.js";

export default function HomePage() {
  const navigate = useNavigate();

  useEffect(() => {
    async function checkAuth() {
      const session = getSession();
      if (!session || !session.token) {
        navigate("/login");
        return;
      }

      try {
        await getCurrentUser();
        navigate("/dashboard", { replace: true });
      } catch (err) {
        navigate("/login", { replace: true });
      }
    }

    checkAuth();
  }, [navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-paper">
      <div className="text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-md bg-signal text-ink mx-auto mb-4">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M4 6h13l3 4v6h-3" />
            <path d="M4 6v10h2" />
            <circle cx="8" cy="17" r="1.8" />
            <circle cx="16.5" cy="17" r="1.8" />
          </svg>
        </div>
        <p className="font-display text-lg font-semibold text-text mb-2">TransitOps</p>
        <p className="text-muted">Loading your dashboard...</p>
      </div>
    </div>
  );
}