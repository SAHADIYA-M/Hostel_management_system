import { useState, useEffect } from "react";
import {
  Shield, Bed, Wallet, Utensils, CalendarCheck, Phone,
  UserCheck, AlertCircle, Plus, CheckCircle2, Wrench, MessageSquare, RefreshCw, LogOut, Building2
} from "lucide-react";
import StatusBadge from "./StatusBadge";
import portalService from "../api/services/portalService";
import maintenanceService from "../api/services/maintenanceService";

export default function StudentPortal({ currentUser, onLogout }) {
  const selectedStudentId = currentUser?.student_id;
  const [portalData, setPortalData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modals
  const [complaintModal, setComplaintModal] = useState(false);
  const [repairModal, setRepairModal] = useState(false);
  const [formDesc, setFormDesc] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");

  async function fetchPortal(id) {
    setLoading(true);
    setError(null);
    try {
      const data = await portalService.getStudentPortal(id);
      setPortalData(data);
      // Synchronize cached user name in localStorage if outdated
      try {
        const stored = localStorage.getItem("hostel_user");
        if (stored) {
          const parsed = JSON.parse(stored);
          const fullName = `${data.fname} ${data.lname}`.trim();
          if (parsed.name !== fullName) {
            parsed.name = fullName;
            localStorage.setItem("hostel_user", JSON.stringify(parsed));
          }
        }
      } catch (e) {
        // Ignore localStorage error
      }
    } catch (err) {
      console.error("Failed to load student portal data:", err);
      setError(err.message || "Failed to load portal data from backend API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchPortal(selectedStudentId);
  }, [selectedStudentId]);

  async function handleLodgeComplaint(e) {
    e.preventDefault();
    if (!formDesc.trim()) return;
    try {
      await maintenanceService.createComplaint({
        student_id: selectedStudentId,
        description: formDesc.trim(),
        date: new Date().toISOString().split("T")[0],
        status: "Open",
      });
      setActionSuccess("Grievance lodged successfully!");
      setFormDesc("");
      setComplaintModal(false);
      fetchPortal(selectedStudentId);
      setTimeout(() => setActionSuccess(""), 4000);
    } catch (err) {
      alert("Error submitting complaint: " + err.message);
    }
  }

  async function handleReportRepair(e) {
    e.preventDefault();
    if (!formDesc.trim() || !portalData?.hostel_id) return;
    try {
      await maintenanceService.create({
        hostel_id: portalData.hostel_id,
        room_no: portalData.room_no,
        description: formDesc.trim(),
        date: new Date().toISOString().split("T")[0],
        status: "Open",
      });
      setActionSuccess("Room repair ticket submitted successfully!");
      setFormDesc("");
      setRepairModal(false);
      fetchPortal(selectedStudentId);
      setTimeout(() => setActionSuccess(""), 4000);
    } catch (err) {
      alert("Error submitting repair request: " + err.message);
    }
  }

  if (loading && !portalData) {
    return (
      <div className="flex h-96 flex-col items-center justify-center gap-3 text-slate-500">
        <RefreshCw className="animate-spin text-brand-600" size={32} />
        <p className="text-sm font-medium">Loading Student Self-Service Portal...</p>
      </div>
    );
  }

  if (error && !portalData) {
    return (
      <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-800">
        <div className="flex items-center gap-3">
          <AlertCircle size={24} />
          <h3 className="font-bold">Unable to Connect to Portal API</h3>
        </div>
        <p className="mt-2 text-sm">{error}</p>
        <button
          onClick={() => fetchPortal(selectedStudentId)}
          className="mt-4 rounded-xl bg-rose-600 px-4 py-2 text-sm font-semibold text-white hover:bg-rose-700"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  const {
    fname, lname, reg_no, phone, hostel_id, hostel_name, hostel_type, hostel_address,
    room_no, room_type, room_capacity, roommates = [], warden, staff_contacts = [],
    mess, fees = [], fines = [], attendance = [], complaints = [], maintenance_tickets = [], visitors = []
  } = portalData || {};

  const initials = `${fname?.[0] || ""}${lname?.[0] || ""}`.toUpperCase();
  const totalPending = [...fees, ...fines]
    .filter((i) => i.status === "Pending")
    .reduce((sum, i) => sum + Number(i.amount || 0), 0);

  const presentCount = attendance.filter((a) => a.status === "Present").length;
  const attendanceRate = attendance.length ? Math.round((presentCount / attendance.length) * 100) : 100;

  return (
    <div className="space-y-6">
      {/* Top App Header */}
      <div className="sticky top-0 z-20 flex items-center justify-between border-b border-slate-200/80 bg-white/90 px-4 py-3 backdrop-blur sm:px-8 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-brand-600 p-1 text-white shadow-md shadow-brand-600/30">
            <img
              src="/logo.png"
              alt="Logo"
              className="h-full w-full object-contain"
              onError={(e) => {
                e.currentTarget.style.display = "none";
                const fallback = e.currentTarget.nextElementSibling;
                if (fallback) fallback.style.display = "flex";
              }}
            />
            <div className="flex h-full w-full items-center justify-center">
              <Building2 size={18} />
            </div>
          </div>
          <div>
            <h1 className="font-bold text-slate-900 text-sm">Hostel Management System</h1>
            <p className="text-[10px] text-slate-400">Student Self-Service Portal</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-brand-600 text-xs font-bold text-white">{initials}</span>
            <div>
              <p className="text-xs font-bold text-slate-900">{fname} {lname}</p>
              <p className="text-[10px] text-slate-500">{reg_no} • Resident</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="inline-flex items-center gap-1.5 rounded-xl border border-rose-200 bg-rose-50 px-3 py-1.5 text-xs font-bold text-rose-700 hover:bg-rose-100 transition"
          >
            <LogOut size={14} /> Sign Out
          </button>
        </div>
      </div>

      <div className="mx-auto max-w-[1400px] space-y-6 px-4 py-6 sm:px-8">
      {actionSuccess && (
        <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-800">
          <CheckCircle2 size={18} />
          {actionSuccess}
        </div>
      )}

      {/* Student Hero Card */}
      <div className="relative overflow-hidden rounded-3xl bg-slate-900 p-6 text-white shadow-xl sm:p-8">
        <div className="relative z-10 flex flex-wrap items-center justify-between gap-6">
          <div className="flex items-center gap-5">
            <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-tr from-brand-600 to-sky-400 text-2xl font-black text-white shadow-lg">
              {initials}
            </div>
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h1 className="text-2xl font-black tracking-tight sm:text-3xl">{fname} {lname}</h1>
                <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold tracking-wide text-brand-300">
                  REG: {reg_no}
                </span>
                <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-sky-300">
                  {hostel_type || "Hostel"} Resident
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-300">
                {hostel_name ? `${hostel_name} • Room ${room_no || "Un-allotted"}` : "Hostel Pending Allotment"}
                {phone && ` • 📞 ${phone}`}
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => { setFormDesc(""); setRepairModal(true); }}
              className="inline-flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-4 py-2.5 text-sm font-semibold text-white backdrop-blur transition hover:bg-white/20"
            >
              <Wrench size={16} /> Report Room Repair
            </button>
            <button
              onClick={() => { setFormDesc(""); setComplaintModal(true); }}
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-600/30 transition hover:bg-brand-500"
            >
              <Plus size={16} /> Lodge Grievance
            </button>
          </div>
        </div>

        <div className="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-brand-500/20 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-sky-500/20 blur-3xl" />
      </div>


      {/* 4 Personal KPI Cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {/* KPI 1: Allotted Bed */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">My Allotted Bed</span>
            <span className="rounded-xl bg-sky-50 p-2.5 text-sky-600"><Bed size={19} /></span>
          </div>
          <p className="mt-3 text-2xl font-black text-slate-900">
            {room_no ? `Room ${room_no}` : "Un-allotted"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {hostel_name || "No Hostel"} {room_type ? `• ${room_type}` : ""}
          </p>
        </div>

        {/* KPI 2: Outstanding Balance */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Outstanding Dues</span>
            <span className="rounded-xl bg-emerald-50 p-2.5 text-emerald-600"><Wallet size={19} /></span>
          </div>
          <p className={`mt-3 text-2xl font-black ${totalPending > 0 ? "text-amber-600" : "text-emerald-600"}`}>
            ₹{totalPending.toLocaleString("en-IN")}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {totalPending === 0 ? "All fees & fines cleared" : "Payment required"}
          </p>
        </div>

        {/* KPI 3: Mess Plan */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Active Mess Plan</span>
            <span className="rounded-xl bg-indigo-50 p-2.5 text-indigo-600"><Utensils size={19} /></span>
          </div>
          <p className="mt-3 text-lg font-bold text-slate-900 truncate">
            {mess?.type || "Standard Mess"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {mess?.cost ? `₹${Number(mess.cost).toLocaleString("en-IN")}/month` : "Active"}
          </p>
        </div>

        {/* KPI 4: Night Attendance */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Night Attendance</span>
            <span className="rounded-xl bg-violet-50 p-2.5 text-violet-600"><CalendarCheck size={19} /></span>
          </div>
          <p className="mt-3 text-2xl font-black text-slate-900">{attendanceRate}%</p>
          <p className="mt-1 text-xs text-slate-500">
            {attendance.length > 0 ? `${presentCount}/${attendance.length} roll calls attended` : "All records clear"}
          </p>
        </div>
      </div>

      {/* Main 2-Column Split */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left Column (2 Cols wide): Ledger, Grievances, Attendance */}
        <div className="space-y-6 lg:col-span-2">
          {/* My Fees & Fines */}
          <div className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 p-5">
              <div className="flex items-center gap-2">
                <Wallet className="text-brand-600" size={18} />
                <h3 className="font-bold text-slate-900">My Fees & Disciplinary Fines</h3>
              </div>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold ${totalPending === 0 ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"}`}>
                {totalPending === 0 ? "No Pending Dues" : `₹${totalPending.toLocaleString("en-IN")} Pending`}
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-5 py-3">Record Ref</th>
                    <th className="px-5 py-3">Description / Reason</th>
                    <th className="px-5 py-3">Amount</th>
                    <th className="px-5 py-3">Due / Incurred</th>
                    <th className="px-5 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {fees.map((f) => (
                    <tr key={`fee-${f.fee_id}`} className="hover:bg-slate-50/60">
                      <td className="whitespace-nowrap px-5 py-3.5 font-mono text-xs font-semibold text-slate-600">FEE-{f.fee_id}</td>
                      <td className="px-5 py-3.5 text-slate-800 font-medium">Semester Hostel Rent & Mess Fee</td>
                      <td className="whitespace-nowrap px-5 py-3.5 font-semibold text-slate-900">₹{Number(f.amount).toLocaleString("en-IN")}</td>
                      <td className="whitespace-nowrap px-5 py-3.5 text-slate-500 text-xs">{f.due_date}</td>
                      <td className="whitespace-nowrap px-5 py-3.5"><StatusBadge status={f.status} /></td>
                    </tr>
                  ))}
                  {fines.map((fn) => (
                    <tr key={`fine-${fn.fid}`} className="hover:bg-slate-50/60">
                      <td className="whitespace-nowrap px-5 py-3.5 font-mono text-xs font-semibold text-amber-600">FINE-{fn.fid}</td>
                      <td className="px-5 py-3.5 text-slate-800 font-medium">{fn.reason}</td>
                      <td className="whitespace-nowrap px-5 py-3.5 font-semibold text-slate-900">₹{Number(fn.amount).toLocaleString("en-IN")}</td>
                      <td className="whitespace-nowrap px-5 py-3.5 text-slate-500 text-xs">—</td>
                      <td className="whitespace-nowrap px-5 py-3.5"><StatusBadge status={fn.status} /></td>
                    </tr>
                  ))}
                  {fees.length === 0 && fines.length === 0 && (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-sm text-slate-400">No fee or fine invoices found.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* My Grievances & Maintenance Tickets */}
          <div className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 p-5">
              <div className="flex items-center gap-2">
                <MessageSquare className="text-brand-600" size={18} />
                <h3 className="font-bold text-slate-900">My Grievances & Maintenance Requests</h3>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-5 py-3">Type</th>
                    <th className="px-5 py-3">Description</th>
                    <th className="px-5 py-3">Filed Date</th>
                    <th className="px-5 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {complaints.map((c) => (
                    <tr key={`comp-${c.complaint_id}`} className="hover:bg-slate-50/60">
                      <td className="whitespace-nowrap px-5 py-3.5 text-xs font-semibold text-slate-500">Complaint #{c.complaint_id}</td>
                      <td className="px-5 py-3.5 text-slate-800 font-medium">{c.description}</td>
                      <td className="whitespace-nowrap px-5 py-3.5 text-slate-500 text-xs">{c.date}</td>
                      <td className="whitespace-nowrap px-5 py-3.5"><StatusBadge status={c.status} /></td>
                    </tr>
                  ))}
                  {maintenance_tickets.map((m) => (
                    <tr key={`maint-${m.request_id}`} className="hover:bg-slate-50/60">
                      <td className="whitespace-nowrap px-5 py-3.5 text-xs font-semibold text-sky-600">Room Repair #{m.request_id}</td>
                      <td className="px-5 py-3.5 text-slate-800 font-medium">{m.description}</td>
                      <td className="whitespace-nowrap px-5 py-3.5 text-slate-500 text-xs">{m.date}</td>
                      <td className="whitespace-nowrap px-5 py-3.5"><StatusBadge status={m.status} /></td>
                    </tr>
                  ))}
                  {complaints.length === 0 && maintenance_tickets.length === 0 && (
                    <tr>
                      <td colSpan={4} className="py-8 text-center text-sm text-slate-400">No active complaints or repair orders.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column (1 Col wide): Roommates, Contacts, Visitors */}
        <div className="space-y-6">
          {/* Room & Roommate Details */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900">Room Details & Occupants</h3>
              <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                {room_no ? `Room ${room_no}` : "Un-allotted"}
              </span>
            </div>
            <p className="mt-1 text-xs text-slate-500">
              Capacity: {room_capacity || 2} Students • {hostel_name}
            </p>

            <div className="mt-4 space-y-3">
              {/* Self */}
              <div className="flex items-center gap-3 rounded-xl border border-brand-200 bg-brand-50/50 p-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600 text-xs font-bold text-white">
                  {initials}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-bold text-slate-900">{fname} {lname} (You)</p>
                  <p className="text-xs text-slate-500">{reg_no} • Resident</p>
                </div>
              </div>

              {/* Roommates */}
              {roommates.map((rm) => (
                <div key={rm.student_id} className="flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50 p-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-200 text-xs font-bold text-slate-700">
                    {rm.fname?.[0]}{rm.lname?.[0]}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold text-slate-900">{rm.fname} {rm.lname}</p>
                    <p className="text-xs text-slate-500">{rm.reg_no} {rm.phone ? `• 📞 ${rm.phone}` : ""}</p>
                  </div>
                </div>
              ))}

              {roommates.length === 0 && (
                <p className="py-2 text-center text-xs text-slate-400">No other roommates in this room.</p>
              )}
            </div>
          </div>

          {/* Assigned Hostel Staff Contacts */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
            <h3 className="font-bold text-slate-900">Hostel Authority Contacts</h3>
            <p className="mt-1 text-xs text-slate-500">Emergency & administrative contact details</p>

            <div className="mt-4 space-y-3">
              {warden && (
                <div className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50 p-3">
                  <div>
                    <span className="rounded bg-sky-100 px-1.5 py-0.5 text-[10px] font-bold text-sky-800 uppercase">Warden</span>
                    <p className="mt-1 text-sm font-bold text-slate-900">{warden.name}</p>
                  </div>
                  <a
                    href={`tel:${warden.phone}`}
                    className="inline-flex items-center gap-1.5 rounded-lg bg-white px-2.5 py-1.5 text-xs font-semibold text-brand-600 shadow-sm border border-slate-200 hover:bg-slate-50"
                  >
                    <Phone size={12} /> {warden.phone}
                  </a>
                </div>
              )}

              {staff_contacts.map((st) => (
                <div key={st.staff_id} className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50 p-3">
                  <div>
                    <span className="rounded bg-slate-200 px-1.5 py-0.5 text-[10px] font-bold text-slate-700 uppercase">{st.role}</span>
                    <p className="mt-1 text-xs font-medium text-slate-700">Staff #{st.staff_id}</p>
                  </div>
                  <a
                    href={`tel:${st.phone}`}
                    className="inline-flex items-center gap-1.5 rounded-lg bg-white px-2.5 py-1.5 text-xs font-semibold text-slate-600 shadow-sm border border-slate-200 hover:bg-slate-50"
                  >
                    <Phone size={12} /> {st.phone}
                  </a>
                </div>
              ))}
            </div>
          </div>

          {/* Approved Visitors */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900">Registered Visitors</h3>
              <UserCheck className="text-brand-600" size={18} />
            </div>
            <p className="mt-1 text-xs text-slate-500">Authorized guardians and guest logs</p>

            <div className="mt-4 space-y-2.5">
              {visitors.map((v, idx) => (
                <div key={idx} className="rounded-xl border border-slate-100 bg-slate-50 p-3">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-bold text-slate-900">{v.name}</p>
                    <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-700">{v.relation}</span>
                  </div>
                  <p className="mt-1 text-xs text-slate-500">Visited on {v.visit_date} • 📞 {v.phone}</p>
                </div>
              ))}

              {visitors.length === 0 && (
                <p className="py-2 text-center text-xs text-slate-400">No visits logged for this student.</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Lodge Complaint Modal */}
      {complaintModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-slate-900">Lodge Student Grievance</h3>
            <p className="mt-1 text-xs text-slate-500">Submit a formal complaint to your hostel warden.</p>
            <form onSubmit={handleLodgeComplaint} className="mt-4 space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-700">Description of Issue</label>
                <textarea
                  required
                  rows={4}
                  value={formDesc}
                  onChange={(e) => setFormDesc(e.target.value)}
                  placeholder="Describe the complaint in detail..."
                  className="mt-1 w-full rounded-xl border border-slate-200 p-3 text-sm outline-none focus:border-brand-500"
                />
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setComplaintModal(false)}
                  className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
                >
                  Submit Grievance
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Report Repair Modal */}
      {repairModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-slate-900">Report Room Repair</h3>
            <p className="mt-1 text-xs text-slate-500">
              Request maintenance for Room {room_no || "Your Room"} in {hostel_name || "Hostel"}.
            </p>
            <form onSubmit={handleReportRepair} className="mt-4 space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-700">Maintenance Details</label>
                <textarea
                  required
                  rows={4}
                  value={formDesc}
                  onChange={(e) => setFormDesc(e.target.value)}
                  placeholder="Describe electrical, plumbing, or furniture repair needed..."
                  className="mt-1 w-full rounded-xl border border-slate-200 p-3 text-sm outline-none focus:border-brand-500"
                />
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setRepairModal(false)}
                  className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700"
                >
                  Submit Work Order
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      </div>{/* end padding wrapper */}
    </div>
  );
}
