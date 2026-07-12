import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { IconLock, IconEye, IconEyeOff, IconAlert } from "../components/Icons.jsx";
import { resetPassword, ApiError } from "../lib/api.js";

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") || "";

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!token) {
      setError("This reset link is missing its token. Request a new one.");
      return;
    }

    if (newPassword.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords don't match.");
      return;
    }

    setLoading(true);
    try {
      await resetPassword({ token, newPassword });
      setDone(true);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Couldn't reach the server. Check your connection and try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-paper px-6 py-12">
      <div className="w-full max-w-sm">
        {done ? (
          <div className="text-center" role="status">
            <span className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-full bg-transit-soft text-transit">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="m5 13 4 4L19 7" />
              </svg>
            </span>
            <h1 className="font-display text-xl font-medium text-text">Password updated</h1>
            <p className="mt-2 text-sm text-muted">You can now sign in with your new password.</p>
            <Link
              to="/login"
              className="mt-6 inline-block rounded-md bg-signal px-4 py-2.5 text-sm font-semibold text-ink transition hover:bg-signal-dark"
            >
              Go to sign in
            </Link>
          </div>
        ) : (
          <>
            <h1 className="font-display text-2xl font-medium text-text">Choose a new password</h1>
            <p className="mt-2 text-sm text-muted">Make it something you haven't used before.</p>

            {!token && (
              <div
                role="alert"
                className="mt-6 flex items-start gap-2.5 rounded-md border border-alert/25 bg-alert-soft px-3.5 py-3 text-sm text-alert"
              >
                <span className="mt-0.5 flex-none">
                  <IconAlert />
                </span>
                <span>
                  No reset token found in this link. Go back to{" "}
                  <Link to="/forgot-password" className="underline">
                    forgot password
                  </Link>{" "}
                  and request a new one.
                </span>
              </div>
            )}

            {error && (
              <div
                role="alert"
                aria-live="polite"
                className="mt-6 flex items-start gap-2.5 rounded-md border border-alert/25 bg-alert-soft px-3.5 py-3 text-sm text-alert"
              >
                <span className="mt-0.5 flex-none">
                  <IconAlert />
                </span>
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="mt-6 space-y-5" noValidate>
              <div>
                <label htmlFor="newPassword" className="block text-sm font-medium text-text mb-1.5">
                  New password
                </label>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted">
                    <IconLock />
                  </span>
                  <input
                    id="newPassword"
                    type={showPassword ? "text" : "password"}
                    required
                    autoComplete="new-password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="At least 8 characters"
                    className="w-full rounded-md border border-black/10 bg-white pl-10 pr-10 py-2.5 text-sm text-text placeholder:text-muted/70 outline-none transition focus:border-signal focus:ring-2 focus:ring-signal/20"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((v) => !v)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-text"
                  >
                    {showPassword ? <IconEyeOff /> : <IconEye />}
                  </button>
                </div>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-text mb-1.5">
                  Confirm password
                </label>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted">
                    <IconLock />
                  </span>
                  <input
                    id="confirmPassword"
                    type={showPassword ? "text" : "password"}
                    required
                    autoComplete="new-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter password"
                    className="w-full rounded-md border border-black/10 bg-white pl-10 pr-3 py-2.5 text-sm text-text placeholder:text-muted/70 outline-none transition focus:border-signal focus:ring-2 focus:ring-signal/20"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-md bg-signal py-2.5 text-sm font-semibold text-ink transition hover:bg-signal-dark disabled:cursor-not-allowed disabled:opacity-60 flex items-center justify-center gap-2"
              >
                {loading && (
                  <span
                    aria-hidden="true"
                    className="h-3.5 w-3.5 rounded-full border-2 border-ink/30 border-t-ink animate-spin"
                  />
                )}
                {loading ? "Updating..." : "Update password"}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}