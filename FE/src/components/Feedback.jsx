import { IconAlert } from "./Icons.jsx";
import Modal from "./Modal.jsx";
import { btn } from "./FormField.jsx";

export function Banner({ tone = "alert", children }) {
  const styles = {
    alert: "border-alert/25 bg-alert-soft text-alert",
    transit: "border-transit/25 bg-transit-soft text-transit",
    signal: "border-signal/25 bg-signal-soft text-signal-dark",
  };
  return (
    <div
      role="alert"
      aria-live="polite"
      className={`flex items-start gap-2.5 rounded-md border px-3.5 py-3 text-sm ${styles[tone]}`}
    >
      <span className="mt-0.5 flex-none">
        <IconAlert />
      </span>
      <span>{children}</span>
    </div>
  );
}

export function Spinner({ className = "h-4 w-4 border-2 border-black/10 border-t-signal" }) {
  return <span aria-hidden="true" className={`inline-block animate-spin rounded-full ${className}`} />;
}

export function PageLoading({ label = "Loading..." }) {
  return (
    <div className="flex items-center justify-center gap-2.5 py-24 text-sm text-muted">
      <Spinner />
      {label}
    </div>
  );
}

export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-lg border border-dashed border-black/15 px-6 py-14 text-center">
      {Icon && (
        <span className="mb-1 flex h-10 w-10 items-center justify-center rounded-full bg-black/5 text-muted">
          <Icon />
        </span>
      )}
      <p className="font-display text-sm font-medium text-text">{title}</p>
      {description && <p className="max-w-xs text-sm text-muted">{description}</p>}
      {action}
    </div>
  );
}

export function ConfirmDialog({ open, onClose, onConfirm, title, description, confirmLabel = "Delete", loading }) {
  return (
    <Modal open={open} onClose={onClose} title={title} description={description} maxWidth="max-w-sm">
      <div className="flex justify-end gap-2.5">
        <button type="button" className={btn.secondary} onClick={onClose} disabled={loading}>
          Cancel
        </button>
        <button type="button" className={btn.danger} onClick={onConfirm} disabled={loading}>
          {loading && <Spinner className="h-3.5 w-3.5 border-2 border-alert/30 border-t-alert" />}
          {loading ? "Working..." : confirmLabel}
        </button>
      </div>
    </Modal>
  );
}