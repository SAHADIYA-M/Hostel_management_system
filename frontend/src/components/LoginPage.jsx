import { useState } from "react";
import { Building2, ArrowRight, AlertCircle, Loader2 } from "lucide-react";
import authService from "../api/services/authService";

export default function LoginPage({ onLoginSuccess }) {
  const [role, setRole] = useState("student"); // 'student' | 'warden'

  // Student credentials (pre-filled with valid DB record)
  const [studentRegNo, setStudentRegNo] = useState("REG2024001");
  const [studentPhone, setStudentPhone] = useState("+919811122201");

  // Warden credentials (pre-filled with valid DB record)
  const [wardenId, setWardenId] = useState("1");
  const [wardenPhone, setWardenPhone] = useState("+919876543210");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleStudentSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await authService.studentLogin(studentRegNo, studentPhone);
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
    setLoading(true);
    try {
      const user = await authService.wardenLogin(wardenId, wardenPhone);
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
        <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-600 text-white shadow-md shadow-brand-600/20">
          <Building2 size={24} />
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Hostel<span className="text-brand-600">MS</span>
        </h1>
        <p className="mt-1 text-sm text-slate-500">Hostel Management System</p>
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
                placeholder="e.g. REG2024001"
                value={studentRegNo}
                onChange={(e) => setStudentRegNo(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">
                Registered Mobile Number
              </label>
              <input
                type="tel"
                required
                placeholder="e.g. +919811122201"
                value={studentPhone}
                onChange={(e) => setStudentPhone(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
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
                placeholder="e.g. +919876543210"
                value={wardenPhone}
                onChange={(e) => setWardenPhone(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20"
              />
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
