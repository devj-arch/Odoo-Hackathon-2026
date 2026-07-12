import { useState } from "react";
import { Link } from "react-router-dom";
import { IconMail, IconAlert } from "../components/Icons.jsx";
import { forgotPassword, ApiError } from "../lib/api.js";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      // The backend always returns the same generic message here whether
      // or not the email exists, so this can't be used to enumerate
      // registered accounts - we just reflect that message back.
      await forgotPassword(email);
      setSent(true);
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
        {sent ? (
          <div className="text-center" role="status">
            <span className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-full bg-transit-soft text-transit">
              <IconMail />
            </span>
            <h1 className="font-display text-xl font-medium text-text">Check your inbox</h1>
            <p className="mt-2 text-sm text-muted">
              If an account exists for <span className="text-text">{email}</span>, we've sent a
              link to reset your password. It expires in 30 minutes.
            </p>
            <Link
              to="/login"
              className="mt-6 inline-block text-sm font-medium text-signal-dark hover:underline"
            >
              Back to sign in
            </Link>
          </div>
        ) : (
          <>
            <h1 className="font-display text-2xl font-medium text-text">Reset your password</h1>
            <p className="mt-2 text-sm text-muted">
              Enter the email on your account and we'll send you a reset link.
            </p>

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
                <label htmlFor="email" className="block text-sm font-medium text-text mb-1.5">
                  Work email
                </label>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted">
                    <IconMail />
                  </span>
                  <input
                    id="email"
                    type="email"
                    required
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@fleetco.com"
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
                {loading ? "Sending..." : "Send reset link"}
              </button>
            </form>

            <p className="mt-6 text-center text-sm text-muted">
              Remembered it?{" "}
              <Link to="/login" className="text-signal-dark hover:underline">
                Back to sign in
              </Link>
            </p>
          </>
        )}
      </div>
    </div>
  );
}