import { useEffect } from "react";
import { IconX } from "./Icons.jsx";

export default function Modal({ open, onClose, title, description, children, maxWidth = "max-w-lg" }) {
  useEffect(() => {
    if (!open) return;
    function onKey(e) {
      if (e.key === "Escape") onClose?.();
    }
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto px-4 py-8 sm:items-center">
      <div
        className="fixed inset-0 bg-ink/50 backdrop-blur-[1px]"
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className={`relative w-full ${maxWidth} rounded-xl border border-black/10 bg-white shadow-xl`}
      >
        <div className="flex items-start justify-between gap-4 border-b border-black/10 px-5 py-4">
          <div>
            <h2 className="font-display text-base font-medium text-text">{title}</h2>
            {description && <p className="mt-0.5 text-sm text-muted">{description}</p>}
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close dialog"
            className="flex h-8 w-8 flex-none items-center justify-center rounded-md text-muted transition hover:bg-black/5 hover:text-text"
          >
            <IconX />
          </button>
        </div>
        <div className="max-h-[75vh] overflow-y-auto px-5 py-5">{children}</div>
      </div>
    </div>
  );
}