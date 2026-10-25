import { useState, useEffect } from "react";
import { Building2, ArrowRight, AlertCircle, Loader2 } from "lucide-react";
import authService from "../api/services/authService";

export default function LoginPage({ onLoginSuccess }) {
  const [role, setRole] = useState("student"); // 'student' | 'warden'

  // Neutralize forward/back arrow navigation while on login page so stale protected views cannot be accessed
  useEffect(() => {
    window.history.pushState(null, "", window.location.href);
    const handlePopState = () => {
      window.history.pushState(null, "", window.location.href);
    };
    window.addEventListener("popstate", handlePopState);
    return () => {
      window.removeEventListener("popstate", handlePopState);
    };
  }, []);

  // Student credentials (empty by default — placeholders guide the user)
  const [studentRegNo, setStudentRegNo] = useState("");
  const [studentPhone, setStudentPhone] = useState("");

  // Warden credentials (empty by default — placeholders guide the user)
  const [wardenId, setWardenId] = useState("");
  const [wardenPhone, setWardenPhone] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const INDIAN_PHONE_REGEX = /^(\+91)?[6-9]\d{9}$/;
  const REG_NO_REGEX = /^REG\d{7}$/;

  async function handleStudentSubmit(e) {
    e.preventDefault();
    setError("");

    const cleanReg = studentRegNo.trim().toUpperCase();
    const cleanPhone = studentPhone.trim();

    if (!REG_NO_REGEX.test(cleanReg)) {
      setError("Registration number must be exactly 10 characters: 'REG' followed by 7 digits (e.g. REG2024001).");
      return;
    }
    if (!INDIAN_PHONE_REGEX.test(cleanPhone)) {
      setError("Mobile number must be a valid 10-digit Indian phone number starting with 6, 7, 8, or 9 (optional '+91' prefix, e.g. 9811122201).");
      return;
    }

    setLoading(true);
    try {
      const user = await authService.studentLogin(cleanReg, cleanPhone);
      onLoginSuccess(user);
    } catch (err) {
      setError(err.message || "Invalid registration number or phone number.");
    } finally {
      setLoading(false);
    }
  }

  async function handleWardenSubmit(e) {
    e.preventDefault();
    setError("");

    const cleanPhone = wardenPhone.trim();
    if (!INDIAN_PHONE_REGEX.test(cleanPhone)) {
      setError("Mobile number must be a valid 10-digit Indian phone number starting with 6, 7, 8, or 9 (optional '+91' prefix, e.g. 9876543210).");
      return;
    }

    setLoading(true);
    try {
      const user = await authService.wardenLogin(wardenId, cleanPhone);
      onLoginSuccess(user);
    } catch (err) {
      setError(err.message || "Invalid Warden ID or phone number.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4 py-12">
      {/* Brand Header */}
      <div className="mb-8 text-center">
        <div className="mx-auto mb-4 flex h-24 w-24 items-center justify-center overflow-hidden rounded-2xl bg-white p-1.5 shadow-sm border border-slate-200/80">
          <img
            src="/logo.png"
            alt="Hostel Management System Logo"
            className="h-full w-full object-contain rounded-xl"
            onError={(e) => {
              e.currentTarget.style.display = "none";
              const fallback = e.currentTarget.nextElementSibling;
              if (fallback) fallback.style.display = "flex";
            }}
          />
          <div className="hidden h-full w-full items-center justify-center rounded-xl bg-brand-600 text-white">
            <Building2 size={28} />
          </div>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Hostel Management System
        </h1>
        <p className="mt-1 text-sm text-slate-500">Student & Warden Access Portal</p>
      </div>

      {/* Main Card */}
      <div className="w-full max-w-md rounded-2xl border border-slate-200/80 bg-white p-7 shadow-sm sm:p-8">
        {/* Role Toggle */}
        <div className="mb-6 grid grid-cols-2 gap-1 rounded-xl bg-slate-100 p-1">
          <button
            type="button"
            onClick={() => {
              setRole("student");
              setError("");
            }}
            className={`rounded-lg py-2 text-xs font-semibold transition ${
              role === "student"
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Student Portal
          </button>
          <button
            type="button"
            onClick={() => {
              setRole("warden");
              setError("");
            }}
            className={`rounded-lg py-2 text-xs font-semibold transition ${
              role === "warden"
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Warden Admin
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-5 flex items-start gap-2.5 rounded-xl border border-rose-200 bg-rose-50 p-3.5 text-xs text-rose-700">
            <AlertCircle size={16} className="mt-0.5 shrink-0" />
            <div className="flex-1">{error}</div>
          </div>
        )}

        {/* Student Form */}
        {role === "student" && (
          <form onSubmit={handleStudentSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-700">
                Registration Number
              </label>
              <input
                type="text"
                required
                maxLength={10}
                pattern="^REG[0-9]{7}$"
                placeholder="e.g. REG2024001"
                title="10 characters: REG followed by 7 digits"
                value={studentRegNo}
                onChange={(e) => setStudentRegNo(e.target.value.toUpperCase())}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm uppercase text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
              <p className="mt-1 text-[11px] text-slate-400">10 characters: REG followed by 7 digits (e.g. REG2024001)</p>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">
                Registered Mobile Number
              </label>
              <input
                type="tel"
                required
                maxLength={13}
                pattern="^(\+91)?[6-9][0-9]{9}$"
                placeholder="e.g. 9811122201 or +919811122201"
                title="10-digit Indian mobile number starting with 6, 7, 8, or 9 (optional +91)"
                value={studentPhone}
                onChange={(e) => setStudentPhone(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
              <p className="mt-1 text-[11px] text-slate-400">10 digits starting with 6, 7, 8, or 9 (optional +91)</p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 size={16} className="animate-spin" /> Signing In…
                </>
              ) : (
                <>
                  Sign In to Student Portal <ArrowRight size={15} />
                </>
              )}
            </button>
          </form>
        )}

        {/* Warden Form */}
        {role === "warden" && (
          <form onSubmit={handleWardenSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-700">
                Warden ID
              </label>
              <input
                type="number"
                min="1"
                required
                placeholder="e.g. 1"
                value={wardenId}
                onChange={(e) => setWardenId(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">
                Registered Phone Number
              </label>
              <input
                type="tel"
                required
                maxLength={13}
                pattern="^(\+91)?[6-9][0-9]{9}$"
                placeholder="e.g. 9876543210 or +919876543210"
                title="10-digit Indian mobile number starting with 6, 7, 8, or 9 (optional +91)"
                value={wardenPhone}
                onChange={(e) => setWardenPhone(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
              <p className="mt-1 text-[11px] text-slate-400">10 digits starting with 6, 7, 8, or 9 (optional +91)</p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 size={16} className="animate-spin" /> Signing In…
                </>
              ) : (
                <>
                  Sign In to Admin Dashboard <ArrowRight size={15} />
                </>
              )}
            </button>
          </form>
        )}


      </div>

      {/* Subtle footer */}
      <p className="mt-8 text-center text-xs text-slate-400">
        Hostel Management System • Role-Based Access
      </p>
    </div>
  );
}
