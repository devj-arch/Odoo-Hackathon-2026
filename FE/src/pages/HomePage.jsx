import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { IconTruck, IconMap, IconShield, IconWallet } from "../components/Icons.jsx";
import { logout as apiLogout } from "../lib/api.js";
import { clearSession, getStoredUser, getToken } from "../lib/auth.js";

// Mock data standing in for real API results until the dashboard endpoints exist.
const KPIS = [
  { label: "Active Vehicles", value: 42, hint: "of 50 total" },
  { label: "Available Vehicles", value: 18, hint: "ready to dispatch" },
  { label: "Vehicles in Maintenance", value: 6, hint: "In Shop" },
  { label: "Active Trips", value: 21, hint: "currently Dispatched" },
  { label: "Pending Trips", value: 5, hint: "Draft status" },
  { label: "Drivers On Duty", value: 27, hint: "of 35 total" },
  { label: "Fleet Utilization", value: "84%", hint: "last 7 days" },
];

const RECENT_TRIPS = [
  { id: "TRP-1042", route: "Ahmedabad → Surat", vehicle: "GJ-05 AB 1234", status: "Dispatched" },
  { id: "TRP-1041", route: "Pune → Mumbai", vehicle: "MH-12 CD 5678", status: "Completed" },
  { id: "TRP-1040", route: "Delhi → Jaipur", vehicle: "DL-08 EF 9012", status: "Draft" },
  { id: "TRP-1039", route: "Bengaluru → Chennai", vehicle: "KA-03 GH 3456", status: "Cancelled" },
];

const STATUS_STYLES = {
  Dispatched: "bg-signal-soft text-signal-dark",
  Completed: "bg-transit-soft text-transit",
  Draft: "bg-black/5 text-muted",
  Cancelled: "bg-alert-soft text-alert",
};

export default function HomePage() {
  const navigate = useNavigate();
  const user = getStoredUser();
  const [loggingOut, setLoggingOut] = useState(false);

  async function handleLogout() {
    setLoggingOut(true);
    try {
      const token = getToken();
      if (token) {
        // Best-effort: still log out locally even if this call fails
        // (e.g. token already expired).
        await apiLogout(token).catch(() => {});
      }
    } finally {
      clearSession();
      navigate("/login", { replace: true });
    }
  }

  return (
    <div className="min-h-screen w-full bg-paper">
      <header className="border-b border-black/10 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-sm bg-signal text-ink">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 6h13l3 4v6h-3" />
                <path d="M4 6v10h2" />
                <circle cx="8" cy="17" r="1.8" />
                <circle cx="16.5" cy="17" r="1.8" />
              </svg>
            </span>
            <span className="font-display text-lg font-semibold tracking-tight text-text">TransitOps</span>
          </div>

          <div className="flex items-center gap-4">
            {user && (
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-text">{user.name}</p>
                <p className="text-xs text-muted">{user.role}</p>
              </div>
            )}
            <button
              onClick={handleLogout}
              disabled={loggingOut}
              className="rounded-md border border-black/10 bg-white px-3.5 py-2 text-sm font-medium text-text transition hover:border-alert/40 hover:text-alert disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loggingOut ? "Signing out..." : "Sign out"}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="font-display text-2xl font-medium text-text">
              Welcome back{user ? `, ${user.name.split(" ")[0]}` : ""}
            </h1>
            <p className="mt-1 text-sm text-muted">Here's how your fleet is doing today.</p>
          </div>
          <div className="flex gap-2">
            {["All types", "All status", "All regions"].map((label) => (
              <button
                key={label}
                type="button"
                className="rounded-md border border-black/10 bg-white px-3 py-1.5 text-xs font-medium text-muted hover:text-text"
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <section className="mt-6 grid grid-cols-2 gap-3 md:grid-cols-4">
          {KPIS.map((kpi) => (
            <div key={kpi.label} className="rounded-lg border border-black/10 bg-white p-4">
              <p className="text-xs font-medium uppercase tracking-wide text-muted">{kpi.label}</p>
              <p className="mt-1.5 font-display text-2xl font-medium text-text">{kpi.value}</p>
              <p className="mt-0.5 text-xs text-muted">{kpi.hint}</p>
            </div>
          ))}
        </section>

        <section className="mt-8 grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div className="lg:col-span-2 rounded-lg border border-black/10 bg-white">
            <div className="flex items-center justify-between border-b border-black/10 px-5 py-3.5">
              <h2 className="font-display text-sm font-medium text-text">Recent trips</h2>
              <button type="button" className="text-xs font-medium text-signal-dark hover:underline">
                View all
              </button>
            </div>
            <ul className="divide-y divide-black/10">
              {RECENT_TRIPS.map((trip) => (
                <li key={trip.id} className="flex items-center justify-between px-5 py-3.5">
                  <div>
                    <p className="text-sm font-medium text-text">{trip.route}</p>
                    <p className="text-xs text-muted">
                      {trip.id} · {trip.vehicle}
                    </p>
                  </div>
                  <span
                    className={`rounded-full px-2.5 py-1 text-xs font-medium ${STATUS_STYLES[trip.status]}`}
                  >
                    {trip.status}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-lg border border-black/10 bg-white p-5">
            <h2 className="font-display text-sm font-medium text-text">Quick links</h2>
            <ul className="mt-3 space-y-2.5">
              {[
                { label: "Vehicle registry", Icon: IconTruck },
                { label: "Trip dispatch", Icon: IconMap },
                { label: "Driver compliance", Icon: IconShield },
                { label: "Fuel & expenses", Icon: IconWallet },
              ].map(({ label, Icon }) => (
                <li key={label}>
                  <button
                    type="button"
                    className="flex w-full items-center gap-3 rounded-md border border-black/10 px-3 py-2.5 text-left text-sm text-text hover:border-signal/40 hover:bg-signal-soft/40"
                  >
                    <span className="flex h-7 w-7 flex-none items-center justify-center rounded-sm border border-black/10 text-signal-dark">
                      <Icon />
                    </span>
                    {label}
                  </button>
                </li>
              ))}
            </ul>
            <p className="mt-4 text-xs text-muted">
              This dashboard is a placeholder - vehicle, trip, and expense modules aren't wired up yet.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}