const STYLES = {
  // Vehicle statuses
  Available: "bg-transit-soft text-transit",
  "On Trip": "bg-signal-soft text-signal-dark",
  "In Shop": "bg-alert-soft text-alert",
  Retired: "bg-black/5 text-muted",

  // Driver statuses
  "Off Duty": "bg-black/5 text-muted",
  Suspended: "bg-alert-soft text-alert",

  // Trip statuses
  Draft: "bg-black/5 text-muted",
  Dispatched: "bg-signal-soft text-signal-dark",
  Completed: "bg-transit-soft text-transit",
  Cancelled: "bg-alert-soft text-alert",

  // Maintenance
  Open: "bg-alert-soft text-alert",
  Closed: "bg-transit-soft text-transit",
};

export default function StatusBadge({ status, className = "" }) {
  const style = STYLES[status] || "bg-black/5 text-muted";
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium whitespace-nowrap ${style} ${className}`}
    >
      {status}
    </span>
  );
}