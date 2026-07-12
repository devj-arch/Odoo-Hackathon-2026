import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  IconCheckCircle,
  IconAlertCircle,
  IconMap,
  IconSettings,
  IconChevronRight,
  IconBarChart3,
  IconTruck,
  IconUser,
} from "../components/Icons.jsx";
import { getDashboardKpis } from "../lib/api.js";
import Sidebar from "../components/Sidebar.jsx";

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchKpis();
  }, []);

  async function fetchKpis() {
    try {
      setLoading(true);
      const data = await getDashboardKpis();
      setKpis(data);
      setError("");
    } catch (err) {
      setError("Failed to load dashboard data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-paper md:pl-64">
      <Sidebar />

      {/* Main */}
      <main className="mx-auto max-w-7xl px-6 pt-20 pb-8 md:px-8 md:pt-8">
        <div className="mb-8">
          <h1 className="font-display text-3xl font-semibold text-text">Dashboard</h1>
          <p className="mt-1 text-sm text-muted">Real-time overview of your fleet operations</p>
        </div>

        {error && (
          <div className="mb-6 rounded-md border border-alert/25 bg-alert-soft px-4 py-3 text-sm text-alert">
            {error}
          </div>
        )}

        {loading ? (
          <div className="space-y-6">
            {/* Skeleton Loading */}
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div
                key={i}
                className="h-24 rounded-lg border border-black/10 bg-white"
              />
            ))}
          </div>
        ) : kpis ? (
          <>
            {/* KPI Grid */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 mb-8">
              <KpiCard
                title="Active Vehicles"
                value={kpis.active_vehicles}
                icon={IconTruck}
                color="signal"
              />
              <KpiCard
                title="Available Vehicles"
                value={kpis.available_vehicles}
                icon={IconCheckCircle}
                color="transit"
              />
              <KpiCard
                title="In Maintenance"
                value={kpis.vehicles_in_maintenance}
                icon={IconAlertCircle}
                color="alert"
              />
              <KpiCard
                title="Active Trips"
                value={kpis.active_trips}
                icon={IconMap}
                color="signal"
              />
              <KpiCard
                title="Pending Trips"
                value={kpis.pending_trips}
                icon={IconMap}
                color="muted"
              />
              <KpiCard
                title="Drivers On Duty"
                value={kpis.drivers_on_duty}
                icon={IconUser}
                color="signal"
              />
              <KpiCard
                title="Fleet Utilization"
                value={`${kpis.fleet_utilization_pct}%`}
                icon={IconBarChart3}
                color="transit"
              />
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <QuickActionCard
                title="Create Trip"
                description="Dispatch a new vehicle for delivery"
                to="/trips"
                icon={IconMap}
              />
              <QuickActionCard
                title="View Reports"
                description="Analytics and operational insights"
                to="/reports"
                icon={IconBarChart3}
              />
              <QuickActionCard
                title="Vehicle Registry"
                description="Manage your fleet inventory"
                to="/vehicles"
                icon={IconTruck}
              />
              <QuickActionCard
                title="Driver Management"
                description="Manage drivers and licenses"
                to="/drivers"
                icon={IconSettings}
              />
            </div>

            {/* Refresh Button */}
            <div className="mt-8 flex justify-center">
              <button
                onClick={fetchKpis}
                className="rounded-md border border-black/10 px-4 py-2 text-sm font-medium text-text hover:bg-paper-soft transition"
              >
                Refresh Data
              </button>
            </div>
          </>
        ) : null}
      </main>
    </div>
  );
}

function KpiCard({ title, value, icon: Icon, color }) {
  const colorMap = {
    signal: "text-signal bg-signal/10",
    transit: "text-transit bg-transit-soft",
    alert: "text-alert bg-alert-soft",
    muted: "text-muted bg-paper-soft",
  };

  return (
    <div className="rounded-lg border border-black/10 bg-white p-6 transition hover:border-black/20 hover:shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted font-medium">{title}</p>
          <p className="mt-2 font-display text-3xl font-semibold text-text">
            {value}
          </p>
        </div>
        <span className={`flex h-10 w-10 items-center justify-center rounded-lg ${colorMap[color]}`}>
          <Icon width="20" height="20" />
        </span>
      </div>
    </div>
  );
}

function QuickActionCard({ title, description, to, icon: Icon }) {
  return (
    <Link
      to={to}
      className="group flex items-start justify-between rounded-lg border border-black/10 bg-white p-6 transition hover:border-signal hover:shadow-md"
    >
      <div className="flex-1">
        <h3 className="font-display font-semibold text-text group-hover:text-signal transition">
          {title}
        </h3>
        <p className="mt-1 text-sm text-muted">{description}</p>
      </div>
      <span className="flex h-10 w-10 flex-none items-center justify-center text-muted group-hover:text-signal transition">
        <IconChevronRight />
      </span>
    </Link>
  );
}