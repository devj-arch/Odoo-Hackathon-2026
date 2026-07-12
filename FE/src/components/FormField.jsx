export function Field({ label, htmlFor, hint, error, children, required }) {
  return (
    <div>
      <label htmlFor={htmlFor} className="block text-sm font-medium text-text mb-1.5">
        {label}
        {required && <span className="text-alert"> *</span>}
      </label>
      {children}
      {hint && !error && <p className="mt-1.5 text-xs text-muted">{hint}</p>}
      {error && <p className="mt-1.5 text-xs text-alert">{error}</p>}
    </div>
  );
}

const inputClass =
  "w-full rounded-md border border-black/10 bg-white px-3 py-2.5 text-sm text-text placeholder:text-muted/70 outline-none transition focus:border-signal focus:ring-2 focus:ring-signal/20 disabled:bg-black/5 disabled:text-muted";

export function Input(props) {
  return <input {...props} className={`${inputClass} ${props.className || ""}`} />;
}

export function Select({ children, ...props }) {
  return (
    <div className="relative">
      <select {...props} className={`${inputClass} appearance-none pr-9 ${props.className || ""}`}>
        {children}
      </select>
      <span className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-muted">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
          <path d="m6 9 6 6 6-6" />
        </svg>
      </span>
    </div>
  );
}

export function TextArea(props) {
  return <textarea {...props} className={`${inputClass} min-h-[80px] resize-y ${props.className || ""}`} />;
}

export const btn = {
  primary:
    "inline-flex items-center justify-center gap-2 rounded-md bg-signal px-4 py-2.5 text-sm font-semibold text-ink transition hover:bg-signal-dark disabled:cursor-not-allowed disabled:opacity-60",
  secondary:
    "inline-flex items-center justify-center gap-2 rounded-md border border-black/10 bg-white px-4 py-2.5 text-sm font-medium text-text transition hover:border-black/20 disabled:cursor-not-allowed disabled:opacity-60",
  danger:
    "inline-flex items-center justify-center gap-2 rounded-md border border-alert/30 bg-alert-soft px-4 py-2.5 text-sm font-medium text-alert transition hover:bg-alert/15 disabled:cursor-not-allowed disabled:opacity-60",
  ghost:
    "inline-flex items-center justify-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium text-muted transition hover:bg-black/5 hover:text-text disabled:cursor-not-allowed disabled:opacity-60",
};