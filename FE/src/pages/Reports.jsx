import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  IconChevronLeft,
  IconAlert,
  IconBarChart3,
  IconTrendingUp,
} from "../components/Icons.jsx";
import {
  listVehicles,
  getVehicleOperationalCost,
  getVehicleRoi,
  getVehicleFuelEfficiency,
  listFuelLogs,
  listExpenses,
} from "../lib/api.js";

export default function Reports() {
  const [vehicles, setVehicles] = useState([]);
  const [selectedVehicleId, setSelectedVehicleId] = useState(null);
  const [metrics, setMetrics] = useState({
    operationalCost: null,
    roi: null,
    fuelEfficiency: null,
  });
  const [loading, setLoading] = useState(true);
  const [metricsLoading, setMetricsLoading] = useState(false);
  const [error, setError] = useState("");
  const [fuelLogs, setFuelLogs] = useState([]);
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    fetchInitialData();
  }, []);

  async function fetchInitialData() {
    try {
      setLoading(true);
      const [vehiclesData, fuelData, expenseData] = await Promise.all([
        listVehicles(),
        listFuelLogs(),
        listExpenses(),
      ]);
      setVehicles(vehiclesData || []);
      setFuelLogs(fuelData || []);
      setExpenses(expenseData || []);

      if (vehiclesData && vehiclesData.length > 0) {
        setSelectedVehicleId(vehiclesData[0].id);
        await fetchVehicleMetrics(vehiclesData[0].id);
      }
    } catch (err) {
      setError("Failed to load reports");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function fetchVehicleMetrics(vehicleId) {
    try {
      setMetricsLoading(true);
      const [costData, roiData, efficiencyData] = await Promise.all([
        getVehicleOperationalCost(vehicleId),
        getVehicleRoi(vehicleId),
        getVehicleFuelEfficiency(vehicleId),
      ]);

      setMetrics({
        operationalCost: costData,
        roi: roiData,
        fuelEfficiency: efficiencyData,
      });
    } catch (err) {
      console.error("Failed to fetch metrics:", err);
    } finally {
      setMetricsLoading(false);
    }
  }

  function handleVehicleChange(e) {
    const vehicleId = parseInt(e.target.value);
    setSelectedVehicleId(vehicleId);
    fetchVehicleMetrics(vehicleId);
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
    }).format(amount);
  };

  const selectedVehicle = vehicles.find((v) => v.id === selectedVehicleId);
  const vehicleFuelLogs = fuelLogs.filter((log) => log.vehicle_id === selectedVehicleId);
  const vehicleExpenses = expenses.filter((exp) => exp.vehicle_id === selectedVehicleId);

  const totalFuelCost = vehicleFuelLogs.reduce((sum, log) => sum + log.cost, 0);
  const totalExpenses = vehicleExpenses.reduce((sum, exp) => sum + exp.amount, 0);
  const totalFuelLiters = vehicleFuelLogs.reduce((sum, log) => sum + log.liters, 0);

  return (
    <div className="min-h-screen bg-paper">
      {/* Header */}
      <header className="border-b border-black/10 bg-white">
        <div className="mx-auto max-w-7xl px-6 py-4 md:px-8">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-sm text-muted hover:text-text transition mb-4"
          >
            <IconChevronLeft width="18" height="18" />
            Back to Dashboard
          </Link>
          <h1 className="font-display text-2xl font-semibold text-text">Reports & Analytics</h1>
          <p className="mt-1 text-sm text-muted">Fleet performance and operational insights</p>
        </div>
      </header>

      {/* Main */}
      <main className="mx-auto max-w-7xl px-6 py-8 md:px-8">
        {error && (
          <div className="mb-6 flex items-start gap-3 rounded-md border border-alert/25 bg-alert-soft px-4 py-3 text-sm text-alert">
            <IconAlert width="18" height="18" className="flex-shrink-0 mt-0.5" />
            {error}
          </div>
        )}

        {loading ? (
          <div className="space-y-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-32 rounded-lg border border-black/10 bg-white" />
            ))}
          </div>
        ) : (
          <>
            {/* Vehicle Selector */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-text mb-3">
                Select Vehicle for Detailed Analysis
              </label>
              <select
                value={selectedVehicleId || ""}
                onChange={handleVehicleChange}
                className="w-full max-w-sm rounded-md border border-black/10 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-signal focus:ring-2 focus:ring-signal/20"
              >
                {vehicles.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.model} ({v.registration_number})
                  </option>
                ))}
              </select>
            </div>

            {selectedVehicle && (
              <>
                {/* Vehicle Details */}
                <div className="mb-8 rounded-lg border border-black/10 bg-white p-6">
                  <h2 className="font-display text-lg font-semibold text-text mb-4">
                    {selectedVehicle.model}
                  </h2>
                  <div className="grid grid-cols-2 gap-6 sm:grid-cols-4">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                        Registration
                      </p>
                      <p className="mt-2 font-semibold text-text">
                        {selectedVehicle.registration_number}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                        Type
                      </p>
                      <p className="mt-2 font-semibold text-text">
                        {selectedVehicle.type}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                        Capacity
                      </p>
                      <p className="mt-2 font-semibold text-text">
                        {selectedVehicle.max_capacity} kg
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                        Odometer
                      </p>
                      <p className="mt-2 font-semibold text-text">
                        {selectedVehicle.odometer.toLocaleString()} km
                      </p>
                    </div>
                  </div>
                </div>

                {/* Metrics Grid */}
                <div className="mb-8">
                  <h2 className="font-display text-lg font-semibold text-text mb-4">
                    Key Metrics
                  </h2>

                  {metricsLoading ? (
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                      {[1, 2, 3].map((i) => (
                        <div
                          key={i}
                          className="h-32 rounded-lg border border-black/10 bg-white"
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                      {/* Operational Cost */}
                      <div className="rounded-lg border border-black/10 bg-white p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                              Operational Cost
                            </p>
                            <p className="mt-3 font-display text-2xl font-semibold text-text">
                              {metrics.operationalCost
                                ? formatCurrency(metrics.operationalCost.total_operational_cost)
                                : "—"}
                            </p>
                          </div>
                          <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-signal/10 text-signal">
                            <IconBarChart3 />
                          </span>
                        </div>
                        {metrics.operationalCost && (
                          <div className="space-y-2 border-t border-black/10 pt-4">
                            <div className="flex justify-between text-sm">
                              <span className="text-muted">Fuel Cost:</span>
                              <span className="font-medium text-text">
                                {formatCurrency(metrics.operationalCost.fuel_cost)}
                              </span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-muted">Maintenance:</span>
                              <span className="font-medium text-text">
                                {formatCurrency(metrics.operationalCost.maintenance_cost)}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Fuel Efficiency */}
                      <div className="rounded-lg border border-black/10 bg-white p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                              Fuel Efficiency
                            </p>
                            <p className="mt-3 font-display text-2xl font-semibold text-text">
                              {metrics.fuelEfficiency
                                ? `${metrics.fuelEfficiency.fuel_efficiency_km_per_liter.toFixed(2)} km/L`
                                : "—"}
                            </p>
                          </div>
                          <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-transit-soft text-transit">
                            <IconTrendingUp />
                          </span>
                        </div>
                        {metrics.fuelEfficiency && (
                          <div className="space-y-2 border-t border-black/10 pt-4">
                            <div className="flex justify-between text-sm">
                              <span className="text-muted">Total Distance:</span>
                              <span className="font-medium text-text">
                                {metrics.fuelEfficiency.total_distance_km.toLocaleString()} km
                              </span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-muted">Total Fuel:</span>
                              <span className="font-medium text-text">
                                {metrics.fuelEfficiency.total_fuel_liters.toFixed(2)} L
                              </span>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* ROI */}
                      <div className="rounded-lg border border-black/10 bg-white p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                              Return on Investment
                            </p>
                            <p className="mt-3 font-display text-2xl font-semibold text-text">
                              {metrics.roi
                                ? `${metrics.roi.roi_pct.toFixed(2)}%`
                                : "—"}
                            </p>
                          </div>
                          <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-alert-soft text-alert">
                            <IconBarChart3 />
                          </span>
                        </div>
                        {metrics.roi && (
                          <div className="space-y-2 border-t border-black/10 pt-4">
                            <div className="flex justify-between text-sm">
                              <span className="text-muted">Revenue:</span>
                              <span className="font-medium text-text">
                                {formatCurrency(metrics.roi.total_revenue)}
                              </span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-muted">Costs:</span>
                              <span className="font-medium text-text">
                                {formatCurrency(metrics.roi.total_costs)}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* Summary Tables */}
                <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
                  {/* Fuel Summary */}
                  <section>
                    <h3 className="font-display text-lg font-semibold text-text mb-4">
                      Fuel Summary
                    </h3>
                    <div className="space-y-3">
                      <div className="rounded-lg border border-black/10 bg-white p-4">
                        <p className="text-sm text-muted">Total Fuel Liters</p>
                        <p className="mt-2 font-display text-2xl font-semibold text-text">
                          {totalFuelLiters.toFixed(2)} L
                        </p>
                      </div>
                      <div className="rounded-lg border border-black/10 bg-white p-4">
                        <p className="text-sm text-muted">Total Fuel Cost</p>
                        <p className="mt-2 font-display text-2xl font-semibold text-text">
                          {formatCurrency(totalFuelCost)}
                        </p>
                      </div>
                      <div className="rounded-lg border border-black/10 bg-white p-4">
                        <p className="text-sm text-muted">Average Cost Per Liter</p>
                        <p className="mt-2 font-display text-2xl font-semibold text-text">
                          {totalFuelLiters > 0
                            ? formatCurrency(totalFuelCost / totalFuelLiters)
                            : "—"}
                        </p>
                      </div>
                    </div>
                  </section>

                  {/* Expense Summary */}
                  <section>
                    <h3 className="font-display text-lg font-semibold text-text mb-4">
                      Expense Summary
                    </h3>
                    <div className="space-y-3">
                      <div className="rounded-lg border border-black/10 bg-white p-4">
                        <p className="text-sm text-muted">Total Expenses</p>
                        <p className="mt-2 font-display text-2xl font-semibold text-text">
                          {formatCurrency(totalExpenses)}
                        </p>
                      </div>
                      <div className="rounded-lg border border-black/10 bg-white p-4">
                        <p className="text-sm text-muted">Number of Records</p>
                        <p className="mt-2 font-display text-2xl font-semibold text-text">
                          {vehicleExpenses.length}
                        </p>
                      </div>
                      <div className="rounded-lg border border-black/10 bg-white p-4">
                        <p className="text-sm text-muted">Combined Operational Cost</p>
                        <p className="mt-2 font-display text-2xl font-semibold text-text">
                          {formatCurrency(totalFuelCost + totalExpenses)}
                        </p>
                      </div>
                    </div>
                  </section>
                </div>
              </>
            )}
          </>
        )}
      </main>
    </div>
  );
}