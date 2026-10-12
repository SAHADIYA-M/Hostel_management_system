import { useMemo, useState, useEffect } from "react";
import {
  BrowserRouter,
  NavLink,
  Routes,
  Route,
  useNavigate,
  useLocation,
  Navigate,
} from "react-router-dom";
import {
  LayoutDashboard, Building2, DoorOpen, Users, Wallet,
  Utensils, CalendarCheck, UserRound, Wrench, MessageSquare,
  Menu, Search, Plus, ArrowRight, X, CheckCircle2, User,
  Filter, Shield, RefreshCw, AlertCircle
} from "lucide-react";

import StatusBadge from "./components/StatusBadge.jsx";
import StudentPortal from "./components/StudentPortal.jsx";
import LoginPage from "./components/LoginPage.jsx";

// API Services
import authService from "./api/services/authService.js";
import hostelService from "./api/services/hostelService.js";
import studentService from "./api/services/studentService.js";
import feeService from "./api/services/feeService.js";
import messService from "./api/services/messService.js";
import attendanceService from "./api/services/attendanceService.js";
import visitorService from "./api/services/visitorService.js";
import maintenanceService from "./api/services/maintenanceService.js";

const navigation = [
  { label: "Dashboard", path: "/", icon: LayoutDashboard },
  { label: "Hostels & Staff", path: "/hostels", icon: Building2 },
  { label: "Rooms & Allotment", path: "/rooms", icon: DoorOpen },
  { label: "Students", path: "/students", icon: Users },
  { label: "Fees & Fines", path: "/fees-fines", icon: Wallet },
  { label: "Mess Subscriptions", path: "/mess", icon: Utensils },
  { label: "Attendance", path: "/attendance", icon: CalendarCheck },
  { label: "Visitors & Visits", path: "/visitors", icon: UserRound },
  { label: "Maintenance", path: "/maintenance", icon: Wrench },
  { label: "Complaints", path: "/complaints", icon: MessageSquare },
];

const titles = Object.fromEntries(
  navigation.map((item) => [item.path, item.label])
);

function Button({ children, onClick, secondary = false, disabled = false }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition ${
        secondary
          ? "border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
          : "bg-brand-600 text-white hover:bg-brand-700 shadow-sm"
      } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      {children}
    </button>
  );
}

function Field({ label, children }) {
  return (
    <label className="grid gap-1.5 text-sm font-medium text-slate-700">
      {label}
      {children}
    </label>
  );
}

function TextInput({
  value,
  onChange,
  type = "text",
  required = false,
  placeholder = "",
  pattern,
  maxLength,
  min,
  max,
  step,
  title,
}) {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      required={required}
      placeholder={placeholder}
      pattern={pattern}
      maxLength={maxLength}
      min={min}
      max={max}
      step={step}
      title={title}
      className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
    />
  );
}

function SelectInput({ value, onChange, options }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 outline-none focus:border-brand-500"
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

function Modal({ title, onClose, children }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white p-6 shadow-2xl">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-lg font-bold">{title}</h2>
          <button onClick={onClose} aria-label="Close">
            <X size={20} />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

function DataTable({ columns, rows, emptyText = "No records found." }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            {columns.map((column) => (
              <th key={column.key} className="whitespace-nowrap px-5 py-3 font-semibold">
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {rows.map((row, index) => (
            <tr key={row._key ?? index} className="hover:bg-slate-50/80">
              {columns.map((column) => (
                <td key={column.key} className="whitespace-nowrap px-5 py-4 text-slate-700">
                  {column.render
                    ? column.render(row)
                    : row[column.key] ?? "—"}
                </td>
              ))}
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="px-5 py-10 text-center text-slate-400">
                {emptyText}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function Dashboard({ currentUser, data, refreshData }) {
  const navigate = useNavigate();
  const isWarden = currentUser?.role === "WARDEN" && currentUser.hostel_id;

  const scopedRooms = isWarden ? data.rooms.filter((r) => r.hostel_id === currentUser.hostel_id) : data.rooms;
  const scopedStudents = isWarden ? data.students.filter((s) => s.hostel_id === currentUser.hostel_id) : data.students;
  const scopedStudentIds = new Set(scopedStudents.map((s) => s.student_id));
  const scopedMaintenance = isWarden ? data.maintenanceRequests.filter((m) => m.hostel_id === currentUser.hostel_id) : data.maintenanceRequests;
  const scopedFees = isWarden ? data.fees.filter((f) => scopedStudentIds.has(f.student_id)) : data.fees;
  const scopedFines = isWarden ? data.fines.filter((f) => scopedStudentIds.has(f.student_id)) : data.fines;
  const scopedComplaints = isWarden ? data.complaints.filter((c) => scopedStudentIds.has(c.student_id)) : data.complaints;

  const metrics = [
    { label: isWarden ? "Assigned Hostel" : "Total Hostels", value: isWarden ? (currentUser.hostel_name || "1") : data.hostels.length, icon: Building2, color: "bg-indigo-50 text-indigo-600" },
    { label: "Total Rooms", value: scopedRooms.length, icon: DoorOpen, color: "bg-sky-50 text-sky-600" },
    {
      label: "Available Capacity",
      value: scopedRooms.reduce((sum, room) => sum + Math.max(0, room.capacity - (room.current_occupants || 0)), 0),
      icon: CheckCircle2,
      color: "bg-emerald-50 text-emerald-600",
    },
    { label: "Registered Students", value: scopedStudents.length, icon: Users, color: "bg-violet-50 text-violet-600" },
    {
      label: "Pending Fees & Fines",
      value: [...scopedFees, ...scopedFines].filter((item) => item.status === "Pending").length,
      icon: Wallet,
      color: "bg-amber-50 text-amber-600",
    },
    { label: "Open Maintenance", value: scopedMaintenance.filter((item) => item.status === "Open").length, icon: Wrench, color: "bg-rose-50 text-rose-600" },
    { label: "Open Complaints", value: scopedComplaints.filter((item) => item.status === "Open").length, icon: MessageSquare, color: "bg-orange-50 text-orange-600" },
  ];

  return (
    <div className="space-y-7">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wider text-slate-400">
            {currentUser?.hostel_name ? `Warden Administration • ${currentUser.hostel_name}` : "Warden Administration"}
          </p>
          <h2 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-900">Hostel Command Center</h2>
          <p className="mt-1 text-slate-500">Live operational data synchronized with PostgreSQL database.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button secondary onClick={refreshData}><RefreshCw size={15} /> Refresh DB</Button>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="group rounded-2xl border border-slate-200/70 bg-white p-5 shadow-card transition-all duration-200 hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg">
            <div className="flex items-center justify-between">
              <span className={`rounded-xl p-3 ${color}`}><Icon size={21} /></span>
              <ArrowRight size={16} className="text-slate-300" />
            </div>
            <p className="mt-5 text-sm text-slate-500">{label}</p>
            <p className="mt-1 text-3xl font-bold text-slate-900">{value}</p>
          </div>
        ))}
      </div>

      <section className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm">
        <h3 className="font-bold text-slate-900">Quick Administrative Actions</h3>
        <p className="mt-1 text-sm text-slate-500">Jump directly to common tasks.</p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Button onClick={() => navigate("/students")}><Plus size={16} /> Register Student</Button>
          <Button secondary onClick={() => navigate("/attendance")}><CalendarCheck size={16} /> Mark Attendance</Button>
          <Button secondary onClick={() => navigate("/maintenance")}><Wrench size={16} /> Log Maintenance Request</Button>
          <Button secondary onClick={() => navigate("/complaints")}><MessageSquare size={16} /> Review Complaints</Button>
        </div>
      </section>

      <section className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
        <div className="border-b border-slate-100 p-5">
          <h3 className="font-bold text-slate-900">Recent Maintenance Work Orders</h3>
        </div>
        <DataTable
          columns={[
            { key: "request_id", label: "Request ID" },
            { key: "hostel_name", label: "Hostel" },
            { key: "room_no", label: "Room", render: (r) => r.room_no ? `Room ${r.room_no}` : "Hostel-wide" },
            { key: "description", label: "Description" },
            { key: "date", label: "Date" },
            { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
          ]}
          rows={scopedMaintenance.slice(0, 5)}
        />
      </section>
    </div>
  );
}

function RecordPage({ page, data, refreshData, currentUser }) {
  const isWarden = currentUser?.role === "WARDEN" && currentUser.hostel_id;
  const [search, setSearch] = useState("");
  const [selectedHostel, setSelectedHostel] = useState(isWarden ? String(currentUser.hostel_id) : "all");
  const [modal, setModal] = useState(false);
  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [statusError, setStatusError] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [form, setForm] = useState({});
  // Optimistic local status overrides: { "fee:12": "Paid", "fine:7": "Pending", ... }
  const [localStatuses, setLocalStatuses] = useState({});
  const navigate = useNavigate();

  // Helper: get the display status from local override or DB row
  const getStatus = (type, id, row) => localStatuses[`${type}:${id}`] ?? row.status;

  // Mark status locally for instant feedback
  const setOptimisticStatus = (type, id, status) =>
    setLocalStatuses((prev) => ({ ...prev, [`${type}:${id}`]: status }));

  // Rollback optimistic status on failure
  const rollbackStatus = (type, id) =>
    setLocalStatuses((prev) => { const n = { ...prev }; delete n[`${type}:${id}`]; return n; });

  const setField = (key, value) => setForm((old) => ({ ...old, [key]: value }));

  const config = {
    "/hostels": { title: "Hostels & Staff", fields: [] },
    "/rooms": { title: "Rooms & Allotment", fields: ["hostel_id", "room_no", "type", "capacity"] },
    "/students": { title: "Students", fields: ["fname", "lname", "reg_no", "phone", "hostel_id", "room_no", "mess_id"] },
    "/fees-fines": { title: "Fees & Fines", fields: ["due_date", "amount", "student_id"] },
    "/mess": { title: "Mess Subscriptions", fields: ["type", "cost"] },
    "/attendance": { title: "Attendance", fields: [] },
    "/visitors": { title: "Visitors & Visits Log", fields: ["name", "relation", "phone"] },
    "/maintenance": { title: "Maintenance Requests", fields: ["hostel_id", "room_no", "description", "date"] },
    "/complaints": { title: "Student Complaints", fields: ["date", "description", "student_id"] },
  };

  const current = config[page];

  // Scoped students for modal & foreign-key references
  const scopedStudents = isWarden
    ? data.students.filter((s) => s.hostel_id === currentUser.hostel_id)
    : data.students;
  const scopedStudentIds = new Set(scopedStudents.map((s) => s.student_id));

  // Filtered rows: Warden only accesses records for their own assigned hostel
  const rows = useMemo(() => {
    let result = [];
    if (page === "/hostels") {
      result = isWarden ? data.hostels.filter((h) => h.hostel_id === currentUser.hostel_id) : data.hostels;
    } else if (page === "/rooms") {
      result = isWarden ? data.rooms.filter((r) => r.hostel_id === currentUser.hostel_id) : data.rooms;
    } else if (page === "/students") {
      // 1 warden gets/accesses student information about their own hostel only
      result = isWarden ? data.students.filter((s) => s.hostel_id === currentUser.hostel_id) : data.students;
    } else if (page === "/fees-fines") {
      result = isWarden ? data.fees.filter((f) => scopedStudentIds.has(f.student_id)) : data.fees;
    } else if (page === "/mess") {
      result = data.messPlans;
    } else if (page === "/attendance") {
      const forDate = data.attendance.filter((r) => r.date === date);
      result = isWarden ? forDate.filter((r) => r.hostel_id === currentUser.hostel_id) : forDate;
    } else if (page === "/visitors") {
      result = data.visitors;
    } else if (page === "/maintenance") {
      result = isWarden ? data.maintenanceRequests.filter((m) => m.hostel_id === currentUser.hostel_id) : data.maintenanceRequests;
    } else if (page === "/complaints") {
      result = isWarden ? data.complaints.filter((c) => scopedStudentIds.has(c.student_id)) : data.complaints;
    }

    // Apply manual filter only if not warden locked
    if (!isWarden && selectedHostel !== "all") {
      result = result.filter((r) => String(r.hostel_id) === selectedHostel);
    }

    // Apply Search
    if (search.trim()) {
      const term = search.toLowerCase();
      result = result.filter((row) =>
        Object.values(row).some((val) =>
          String(val ?? "").toLowerCase().includes(term)
        )
      );
    }
    return result;
  }, [data, page, isWarden, currentUser, selectedHostel, search, date]);

  async function handleAddRecord(e) {
    e.preventDefault();
    setMessage("");
    setErrorMessage("");

    const indianPhoneRegex = /^(\+91)?[6-9]\d{9}$/;
    const regNoRegex = /^REG\d{7}$/;
    const nameRegex = /^[A-Za-z][A-Za-z\s.]*$/;

    // Pattern validations conforming to Indian mobile standards and mock data
    if (form.phone && !indianPhoneRegex.test(form.phone.trim())) {
      setErrorMessage("Mobile number must be a valid 10-digit Indian phone number starting with 6, 7, 8, or 9 (optional '+91' prefix, e.g. 9811122201).");
      return;
    }

    if (page === "/students") {
      const cleanReg = (form.reg_no || "").trim().toUpperCase();
      if (!regNoRegex.test(cleanReg)) {
        setErrorMessage("Registration number must be exactly 10 characters: 'REG' followed by 7 digits (e.g. REG2024001).");
        return;
      }
      if (form.fname && !nameRegex.test(form.fname.trim())) {
        setErrorMessage("First name must contain letters, spaces, or dots only.");
        return;
      }
      if (form.lname && !nameRegex.test(form.lname.trim())) {
        setErrorMessage("Last name must contain letters, spaces, or dots only.");
        return;
      }
      if (!form.phone) {
        setErrorMessage("Mobile number is required.");
        return;
      }
      if (form.room_no) {
        const rNo = Number(form.room_no);
        if (isNaN(rNo) || rNo < 100 || rNo > 999) {
          setErrorMessage("Room number must be between 100 and 999.");
          return;
        }
      }
    } else if (page === "/visitors") {
      if (form.name && !nameRegex.test(form.name.trim())) {
        setErrorMessage("Visitor name must contain letters, spaces, or dots only.");
        return;
      }
      if (!form.phone) {
        setErrorMessage("Visitor phone number is required.");
        return;
      }
    } else if (page === "/rooms") {
      const rNo = Number(form.room_no);
      if (isNaN(rNo) || rNo < 100 || rNo > 999) {
        setErrorMessage("Room number must be between 100 and 999.");
        return;
      }
      const cap = Number(form.capacity);
      if (isNaN(cap) || cap < 1 || cap > 10) {
        setErrorMessage("Room capacity must be between 1 and 10.");
        return;
      }
    } else if (page === "/fees-fines") {
      const amt = Number(form.amount);
      if (isNaN(amt) || amt <= 0) {
        setErrorMessage("Amount must be greater than 0.");
        return;
      }
    } else if (page === "/mess") {
      const cost = Number(form.cost);
      if (isNaN(cost) || cost <= 0) {
        setErrorMessage("Mess cost must be greater than 0.");
        return;
      }
    } else if (page === "/maintenance" || page === "/complaints") {
      if (!form.description || form.description.trim().length < 5) {
        setErrorMessage("Description must be at least 5 characters.");
        return;
      }
    }

    try {
      if (page === "/rooms") {
        const roomHostelId = isWarden ? currentUser.hostel_id : Number(form.hostel_id);
        await hostelService.createRoom({
          hostel_id: roomHostelId,
          room_no: Number(form.room_no),
          type: form.type || "Double Sharing AC",
          capacity: Number(form.capacity),
        });
      } else if (page === "/students") {
        // Enforce warden's hostel when student is added by warden
        const studentHostelId = isWarden ? currentUser.hostel_id : (form.hostel_id ? Number(form.hostel_id) : null);
        await studentService.create({
          fname: form.fname.trim(),
          lname: form.lname.trim(),
          reg_no: form.reg_no.trim().toUpperCase(),
          phone: form.phone.trim(),
          hostel_id: studentHostelId,
          room_no: form.room_no ? Number(form.room_no) : null,
          allot_date: form.room_no ? new Date().toISOString().split("T")[0] : null,
          mess_id: form.mess_id ? Number(form.mess_id) : null,
        });
      } else if (page === "/fees-fines") {
        await feeService.createFee({
          due_date: form.due_date,
          amount: Number(form.amount),
          status: "Pending",
          student_id: Number(form.student_id),
        });
      } else if (page === "/mess") {
        await messService.createMessPlan({
          type: form.type,
          cost: Number(form.cost),
        });
      } else if (page === "/visitors") {
        await visitorService.createVisitor({
          name: form.name.trim(),
          relation: form.relation || "Father",
          phone: form.phone.trim(),
        });
      } else if (page === "/maintenance") {
        const maintHostelId = isWarden ? currentUser.hostel_id : Number(form.hostel_id);
        await maintenanceService.create({
          hostel_id: maintHostelId,
          room_no: form.room_no ? Number(form.room_no) : null,
          description: form.description,
          date: form.date,
          status: "Open",
        });
      } else if (page === "/complaints") {
        await maintenanceService.createComplaint({
          student_id: Number(form.student_id),
          description: form.description,
          date: form.date,
          status: "Open",
        });
      }

      setMessage("Record saved successfully to live PostgreSQL database.");
      setForm({});
      setModal(false);
      refreshData();
    } catch (err) {
      setErrorMessage(err.message || "Failed to save record.");
    }
  }

  async function handleUpdateStatus(row, newStatus) {
    setStatusError("");
    // Determine key for optimistic update
    let type, id;
    if (page === "/fees-fines")       { type = "fee";        id = row.fee_id; }
    else if (page === "/maintenance") { type = "maintenance"; id = row.request_id; }
    else if (page === "/complaints")  { type = "complaint";   id = row.complaint_id; }
    else if (page === "/attendance")  { type = "attendance";  id = `${row.student_id}_${row.date}`; }

    // Optimistically update UI instantly
    if (type) setOptimisticStatus(type, id, newStatus);

    try {
      if (page === "/attendance") {
        await attendanceService.mark({ student_id: row.student_id, date: date, status: newStatus });
      } else if (page === "/fees-fines") {
        await feeService.updateFeeStatus(row.fee_id, newStatus);
      } else if (page === "/maintenance") {
        await maintenanceService.updateStatus(row.request_id, newStatus);
      } else if (page === "/complaints") {
        await maintenanceService.updateComplaintStatus(row.complaint_id, newStatus);
      }
      refreshData();
    } catch (err) {
      // Rollback optimistic update on failure
      if (type) rollbackStatus(type, id);
      setStatusError("Failed to update status: " + (err.message || "Unknown error"));
    }
  }

  async function handleToggleFine(fid, currentStatus) {
    setStatusError("");
    const next = currentStatus === "Paid" ? "Pending" : "Paid";
    // Optimistic update
    setOptimisticStatus("fine", fid, next);
    try {
      await feeService.updateFineStatus(fid, next);
      refreshData();
    } catch (err) {
      rollbackStatus("fine", fid);
      setStatusError("Failed to update fine: " + (err.message || "Unknown error"));
    }
  }

  async function handleMarkAllPresent() {
    try {
      // 1 warden can only mark all students are present attendances on their own hostel only
      const targetHostelId = isWarden
        ? currentUser.hostel_id
        : (selectedHostel !== "all" ? Number(selectedHostel) : null);

      await attendanceService.markBulk({
        date: date,
        hostel_id: targetHostelId,
        status: "Present",
      });
      const hostelTitle = isWarden
        ? currentUser.hostel_name
        : (targetHostelId ? `Hostel #${targetHostelId}` : "All Hostels");
      setMessage(`All students in ${hostelTitle} marked Present for ${date}`);
      refreshData();
    } catch (err) {
      alert("Error: " + err.message);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">{current.title}</h2>
          <p className="mt-1 text-sm text-slate-500">
            {isWarden
              ? `Live database management for ${currentUser.hostel_name}.`
              : `Live database management for ${current.title.toLowerCase()}.`}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Hostel Segregation Filter / Warden Scope Badge */}
          {isWarden ? (
            <div className="flex items-center gap-2 rounded-xl border border-brand-200 bg-brand-50/70 px-3.5 py-2 text-xs font-semibold text-brand-800 shadow-sm">
              <Building2 size={16} className="text-brand-600" />
              <span>Assigned Hostel: <strong className="text-slate-900">{currentUser.hostel_name}</strong></span>
            </div>
          ) : (
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-1.5 shadow-sm">
              <Filter size={15} className="text-slate-400" />
              <select
                value={selectedHostel}
                onChange={(e) => setSelectedHostel(e.target.value)}
                className="bg-transparent text-sm font-semibold text-slate-700 outline-none"
              >
                <option value="all">🏢 All Hostels (Boys & Girls)</option>
                {data.hostels.map((h) => (
                  <option key={h.hostel_id} value={String(h.hostel_id)}>
                    {h.name} ({h.type})
                  </option>
                ))}
              </select>
            </div>
          )}

          {current.fields.length > 0 && (
            <Button onClick={() => { setForm({}); setMessage(""); setErrorMessage(""); setModal(true); }}>
              <Plus size={17} /> Add record
            </Button>
          )}
        </div>
      </div>

      {message && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-800">
          {message}
        </div>
      )}
      {errorMessage && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-800">
          {errorMessage}
        </div>
      )}

      {/* Hostels View */}
      {page === "/hostels" && (
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {rows.map((hostel) => (
            <div key={hostel.hostel_id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <span className={`rounded-xl p-3 ${hostel.type === "Girls" ? "bg-rose-50 text-rose-600" : "bg-sky-50 text-sky-600"}`}>
                  <Building2 size={24} />
                </span>
                <span className={`rounded-full px-3 py-1 text-xs font-bold ${hostel.type === "Girls" ? "bg-rose-100 text-rose-700" : "bg-sky-100 text-sky-700"}`}>
                  {hostel.type} Hostel
                </span>
              </div>
              <h3 className="mt-4 text-xl font-bold text-slate-900">{hostel.name}</h3>
              <p className="mt-1 text-sm text-slate-500">{hostel.address}</p>

              <div className="mt-4 border-t border-slate-100 pt-4 space-y-2 text-sm">
                <p className="font-semibold text-slate-800">
                  Warden: <span className="font-normal text-slate-600">{hostel.warden_name || "Unassigned"}</span>
                </p>
                <p className="font-semibold text-slate-800">
                  Phone: <span className="font-normal text-slate-600">{hostel.warden_phone || "—"}</span>
                </p>
                <p className="font-semibold text-slate-800">
                  Assigned Staff: <span className="font-normal text-slate-600">{hostel.staff_count || 0} members</span>
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Rooms View */}
      {page === "/rooms" && (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {rows.map((room) => {
            const full = (room.current_occupants || 0) >= room.capacity;
            return (
              <div key={`${room.hostel_id}-${room.room_no}`} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <DoorOpen className="text-brand-600" size={20} />
                    <span className="font-bold text-lg text-slate-900">Room {room.room_no}</span>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${full ? "bg-rose-100 text-rose-700" : "bg-emerald-100 text-emerald-700"}`}>
                    {full ? "Full" : "Available"}
                  </span>
                </div>
                <p className="mt-2 text-xs text-slate-500">{room.type} • {room.hostel_name}</p>
                <p className="mt-3 text-sm font-medium">Occupancy: {room.current_occupants || 0} / {room.capacity}</p>
                <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
                  <div
                    className={`h-full ${full ? "bg-rose-500" : "bg-emerald-500"}`}
                    style={{ width: `${Math.min(100, ((room.current_occupants || 0) / room.capacity) * 100)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Attendance View Filter */}
      {page === "/attendance" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="rounded-lg bg-brand-50 p-1.5 text-brand-600">
                  <Building2 size={18} />
                </span>
                <h3 className="font-bold text-slate-900">
                  {currentUser?.hostel_name || "Hostel"} Attendance Roster
                </h3>
                {currentUser?.hostel_type && (
                  <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-700">
                    {currentUser.hostel_type} Hostel
                  </span>
                )}
              </div>
              <p className="mt-1 text-xs text-slate-500">
                Official daily attendance log for students residing in{" "}
                <strong className="text-slate-700">{currentUser?.hostel_name || "assigned hostel"}</strong>.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-500">Attendance Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="mt-1 block rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm font-medium text-slate-800 outline-none focus:border-brand-500 focus:bg-white"
                />
              </div>
              <div className="pt-5">
                <Button onClick={handleMarkAllPresent}>
                  <CheckCircle2 size={16} /> Mark All Present ({currentUser?.hostel_name ? currentUser.hostel_name.split(" ")[0] : "Hostel"})
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Table for Lists */}
      {page !== "/hostels" && page !== "/rooms" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 p-4">
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2">
              <Search size={17} className="text-slate-400" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search live records..."
                className="min-w-0 bg-transparent text-sm outline-none"
              />
            </div>
            <span className="text-sm font-medium text-slate-500">{rows.length} records</span>
          </div>

          <DataTable
            columns={
              page === "/students"
                ? [
                    { key: "student_id", label: "Student ID" },
                    { key: "fname", label: "Name", render: (r) => `${r.fname} ${r.lname}` },
                    { key: "reg_no", label: "Reg No" },
                    { key: "phone", label: "Phone" },
                    { key: "hostel_name", label: "Hostel", render: (r) => r.hostel_name || "Un-allotted" },
                    { key: "room_no", label: "Room", render: (r) => r.room_no ? `Room ${r.room_no}` : "Un-allotted" },
                    { key: "mess_type", label: "Mess Plan", render: (r) => r.mess_type || "None" },
                  ]
                : page === "/fees-fines"
                ? [
                    { key: "fee_id", label: "Fee Ref", render: (r) => `FEE-${r.fee_id}` },
                    { key: "student_name", label: "Student Name" },
                    { key: "reg_no", label: "Reg No" },
                    { key: "amount", label: "Amount", render: (r) => `₹${Number(r.amount).toLocaleString("en-IN")}` },
                    { key: "due_date", label: "Due Date" },
                    { key: "status", label: "Status", render: (r) => <StatusBadge status={getStatus("fee", r.fee_id, r)} /> },
                    {
                      key: "action",
                      label: "Toggle Status",
                      render: (r) => (
                        <select
                          value={getStatus("fee", r.fee_id, r)}
                          onChange={(e) => handleUpdateStatus(r, e.target.value)}
                          className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs"
                        >
                          <option value="Pending">Pending</option>
                          <option value="Paid">Paid</option>
                        </select>
                      ),
                    },
                  ]
                : page === "/mess"
                ? [
                    { key: "mess_id", label: "Mess ID" },
                    { key: "type", label: "Meal Type" },
                    { key: "cost", label: "Cost", render: (r) => `₹${Number(r.cost).toLocaleString("en-IN")}/mo` },
                    { key: "enrolled_count", label: "Enrolled Students" },
                  ]
                : page === "/attendance"
                ? [
                    { key: "student_id", label: "Student ID" },
                    {
                      key: "student_name",
                      label: "Student",
                      render: (r) => (
                        <div>
                          <p className="font-semibold text-slate-900">{r.student_name}</p>
                          <p className="text-xs text-slate-400">Hostel: {r.hostel_name || currentUser?.hostel_name || "—"}</p>
                        </div>
                      ),
                    },
                    { key: "reg_no", label: "Reg No" },
                    {
                      key: "hostel_name",
                      label: "Assigned Hostel",
                      render: (r) => (
                        <span className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700">
                          <Building2 size={13} className="text-brand-600" />
                          {r.hostel_name || currentUser?.hostel_name || "—"}
                        </span>
                      ),
                    },
                    { key: "room_no", label: "Room", render: (r) => r.room_no ? `Room ${r.room_no}` : "—" },
                    { key: "date", label: "Date" },
                    { key: "status", label: "Status", render: (r) => <StatusBadge status={getStatus("attendance", `${r.student_id}_${r.date}`, r)} /> },
                    {
                      key: "action",
                      label: "Change Status",
                      render: (r) => (
                        <select
                          value={getStatus("attendance", `${r.student_id}_${r.date}`, r)}
                          onChange={(e) => handleUpdateStatus(r, e.target.value)}
                          className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs"
                        >
                          <option value="Present">Present</option>
                          <option value="Absent">Absent</option>
                        </select>
                      ),
                    },
                  ]
                : page === "/visitors"
                ? [
                    { key: "visitor_id", label: "Visitor ID" },
                    { key: "name", label: "Visitor Name" },
                    { key: "relation", label: "Relation" },
                    { key: "phone", label: "Phone" },
                  ]
                : page === "/maintenance"
                ? [
                    { key: "request_id", label: "Ticket ID" },
                    { key: "hostel_name", label: "Hostel" },
                    { key: "room_no", label: "Room", render: (r) => r.room_no ? `Room ${r.room_no}` : "Common" },
                    { key: "description", label: "Description" },
                    { key: "date", label: "Date" },
                    { key: "status", label: "Status", render: (r) => <StatusBadge status={getStatus("maintenance", r.request_id, r)} /> },
                    {
                      key: "action",
                      label: "Update",
                      render: (r) => (
                        <select
                          value={getStatus("maintenance", r.request_id, r)}
                          onChange={(e) => handleUpdateStatus(r, e.target.value)}
                          className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs"
                        >
                          <option value="Open">Open</option>
                          <option value="In Progress">In Progress</option>
                          <option value="Resolved">Resolved</option>
                        </select>
                      ),
                    },
                  ]
                : page === "/complaints"
                ? [
                    { key: "complaint_id", label: "Complaint ID" },
                    { key: "student_name", label: "Student" },
                    { key: "reg_no", label: "Reg No" },
                    { key: "description", label: "Description" },
                    { key: "date", label: "Date" },
                    { key: "status", label: "Status", render: (r) => <StatusBadge status={getStatus("complaint", r.complaint_id, r)} /> },
                    {
                      key: "action",
                      label: "Update",
                      render: (r) => (
                        <select
                          value={getStatus("complaint", r.complaint_id, r)}
                          onChange={(e) => handleUpdateStatus(r, e.target.value)}
                          className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs"
                        >
                          <option value="Open">Open</option>
                          <option value="In Progress">In Progress</option>
                          <option value="Resolved">Resolved</option>
                        </select>
                      ),
                    },
                  ]
                : []
            }
            rows={rows}
          />
        </section>
      )}

      {/* Status error toast */}
      {statusError && (
        <div className="mb-4 flex items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-xs font-semibold text-rose-700">
          <span>{statusError}</span>
          <button onClick={() => setStatusError("")} className="ml-auto text-rose-500 hover:text-rose-700 font-bold text-sm leading-none">&times;</button>
        </div>
      )}

      {/* Disciplinary Fines Table in Fees View */}
      {page === "/fees-fines" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="p-5 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-bold text-slate-900">Disciplinary Fines (Separate Entity: FINE)</h3>
            <span className="text-xs text-slate-500">
              {(isWarden ? data.fines.filter((f) => scopedStudentIds.has(f.student_id)) : data.fines).length} fine records
            </span>
          </div>
          <DataTable
            columns={[
              { key: "fid", label: "Fine Ref", render: (r) => `FINE-${r.fid}` },
              { key: "student_name", label: "Student Name" },
              { key: "reg_no", label: "Reg No" },
              { key: "reason", label: "Infraction Reason" },
              { key: "amount", label: "Amount", render: (r) => `₹${Number(r.amount).toLocaleString("en-IN")}` },
              { key: "status", label: "Status", render: (r) => <StatusBadge status={getStatus("fine", r.fid, r)} /> },
              {
                key: "action",
                label: "Toggle Status",
                render: (r) => {
                  const fineStatus = getStatus("fine", r.fid, r);
                  return (
                    <button
                      onClick={() => handleToggleFine(r.fid, fineStatus)}
                      className={`rounded-lg px-2.5 py-1 text-xs font-bold transition ${
                        fineStatus === "Paid"
                          ? "border border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100"
                          : "border border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100"
                      }`}
                    >
                      Mark {fineStatus === "Paid" ? "Pending" : "Paid"}
                    </button>
                  );
                },
              },
            ]}
            rows={isWarden ? data.fines.filter((f) => scopedStudentIds.has(f.student_id)) : data.fines}
          />
        </section>
      )}

      {/* Add Modal */}
      {modal && (
        <Modal title={`Add ${current.title} Record`} onClose={() => { setModal(false); setErrorMessage(""); }}>
          <form onSubmit={handleAddRecord} className="space-y-4">
            {errorMessage && (
              <div className="rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs font-semibold text-rose-700">
                {errorMessage}
              </div>
            )}
            {current.fields.map((key) => (
              <Field key={key} label={key.replace("_", " ").toUpperCase()}>
                {key === "date" || key === "due_date" ? (
                  <TextInput type="date" value={form[key] || ""} onChange={(v) => setField(key, v)} required />
                ) : key === "hostel_id" ? (
                  isWarden ? (
                    <div className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm font-semibold text-slate-800">
                      {currentUser.hostel_name} ({currentUser.hostel_type} Hostel)
                    </div>
                  ) : (
                    <SelectInput
                      value={form[key] || String(data.hostels[0]?.hostel_id || "")}
                      onChange={(v) => setField(key, v)}
                      options={data.hostels.map((h) => ({ value: String(h.hostel_id), label: `${h.name} (${h.type})` }))}
                    />
                  )
                ) : key === "student_id" ? (
                  <SelectInput
                    value={form[key] || String(scopedStudents[0]?.student_id || "")}
                    onChange={(v) => setField(key, v)}
                    options={scopedStudents.map((s) => ({ value: String(s.student_id), label: `${s.fname} ${s.lname} (${s.reg_no})` }))}
                  />
                ) : key === "mess_id" ? (
                  <SelectInput
                    value={form[key] || ""}
                    onChange={(v) => setField(key, v)}
                    options={[{ value: "", label: "No Mess Plan" }, ...data.messPlans.map((m) => ({ value: String(m.mess_id), label: `${m.type} (₹${m.cost})` }))]}
                  />
                ) : key === "phone" ? (
                  <div>
                    <TextInput
                      type="tel"
                      value={form[key] || ""}
                      onChange={(v) => setField(key, v)}
                      required
                      maxLength={13}
                      pattern="^(\+91)?[6-9][0-9]{9}$"
                      placeholder="e.g. 9811122201 or +919811122201"
                      title="10-digit Indian phone number starting with 6, 7, 8, or 9 (optional +91)"
                    />
                    <p className="mt-1 text-[11px] text-slate-400">10 digits starting with 6, 7, 8, or 9 (optional +91)</p>
                  </div>
                ) : key === "reg_no" ? (
                  <div>
                    <TextInput
                      type="text"
                      value={form[key] || ""}
                      onChange={(v) => setField(key, v.toUpperCase())}
                      required
                      maxLength={10}
                      pattern="^REG[0-9]{7}$"
                      placeholder="e.g. REG2024001"
                      title="10 characters: REG followed by 7 digits"
                    />
                    <p className="mt-1 text-[11px] text-slate-400">Exactly 10 characters: REG followed by 7 digits (e.g. REG2024001)</p>
                  </div>
                ) : key === "fname" || key === "lname" || key === "name" ? (
                  <TextInput
                    type="text"
                    value={form[key] || ""}
                    onChange={(v) => setField(key, v)}
                    required
                    pattern="^[A-Za-z][A-Za-z\s\.]*$"
                    placeholder={key === "fname" ? "e.g. Rahul" : key === "lname" ? "e.g. Nair" : "e.g. K. Radhakrishnan"}
                    title="Letters, spaces, or dots only"
                  />
                ) : key === "relation" ? (
                  <SelectInput
                    value={form[key] || "Father"}
                    onChange={(v) => setField(key, v)}
                    options={[
                      { value: "Father", label: "Father" },
                      { value: "Mother", label: "Mother" },
                      { value: "Guardian", label: "Guardian" },
                      { value: "Brother", label: "Brother" },
                      { value: "Sister", label: "Sister" },
                    ]}
                  />
                ) : key === "type" && page === "/rooms" ? (
                  <SelectInput
                    value={form[key] || "Double Sharing AC"}
                    onChange={(v) => setField(key, v)}
                    options={[
                      { value: "Double Sharing AC", label: "Double Sharing AC" },
                      { value: "Double Sharing Non-AC", label: "Double Sharing Non-AC" },
                      { value: "Single Deluxe", label: "Single Deluxe" },
                      { value: "Triple Sharing Non-AC", label: "Triple Sharing Non-AC" },
                    ]}
                  />
                ) : key === "room_no" ? (
                  <TextInput
                    type="number"
                    value={form[key] ?? ""}
                    onChange={(v) => setField(key, v)}
                    required={page === "/rooms"}
                    min={100}
                    max={999}
                    placeholder="e.g. 101 (100–999)"
                  />
                ) : key === "capacity" ? (
                  <TextInput
                    type="number"
                    value={form[key] ?? ""}
                    onChange={(v) => setField(key, v)}
                    required
                    min={1}
                    max={10}
                    placeholder="e.g. 2 (1–10)"
                  />
                ) : key === "amount" || key === "cost" ? (
                  <TextInput
                    type="number"
                    value={form[key] ?? ""}
                    onChange={(v) => setField(key, v)}
                    required
                    min={1}
                    step={1}
                    placeholder={key === "cost" ? "e.g. 4500" : "e.g. 45000"}
                  />
                ) : key === "description" ? (
                  <textarea
                    value={form[key] || ""}
                    onChange={(e) => setField(key, e.target.value)}
                    required
                    rows={3}
                    placeholder="Provide details (at least 5 characters)..."
                    className="w-full rounded-xl border border-slate-200 p-3 text-sm outline-none focus:border-brand-500"
                  />
                ) : (
                  <TextInput value={form[key] || ""} onChange={(v) => setField(key, v)} required />
                )}
              </Field>
            ))}
            <div className="flex justify-end gap-3 pt-3">
              <Button secondary onClick={() => { setModal(false); setErrorMessage(""); }}>Cancel</Button>
              <button type="submit" className="rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-700">
                Save to Database
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}

function AppShell({ currentUser, onLogout }) {
  const [data, setData] = useState({
    hostels: [],
    rooms: [],
    students: [],
    fees: [],
    fines: [],
    messPlans: [],
    attendance: [],
    visitors: [],
    visits: [],
    maintenanceRequests: [],
    complaints: [],
  });
  const [loading, setLoading] = useState(true);
  const [backendError, setBackendError] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const title = titles[location.pathname] || "Dashboard";

  async function loadAllData() {
    setLoading(true);
    setBackendError(null);
    try {
      const [
        hostels, rooms, students, fees, fines, messPlans,
        attendance, visitors, visits, maintenance, complaints
      ] = await Promise.all([
        hostelService.getAll(),
        hostelService.getRooms(),
        studentService.getAll(),
        feeService.getFees(),
        feeService.getFines(),
        messService.getMessPlans(),
        attendanceService.getAttendance(),
        visitorService.getVisitors(),
        visitorService.getVisits(),
        maintenanceService.getAll(),
        maintenanceService.getAllComplaints(),
      ]);

      setData({
        hostels,
        rooms,
        students,
        fees,
        fines,
        messPlans,
        attendance,
        visitors,
        visits,
        maintenanceRequests: maintenance,
        complaints,
      });
    } catch (err) {
      console.error("Backend connection failed:", err);
      setBackendError(err.message || "Could not connect to FastAPI backend at http://localhost:8000/api.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAllData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      {sidebarOpen && (
        <button
          aria-label="Close navigation"
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 z-30 bg-slate-950/30 lg:hidden"
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col bg-white border-r border-slate-200/80 shadow-sm transition-transform lg:translate-x-0 ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="flex h-20 items-center justify-between border-b border-slate-100 px-6">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-brand-600 p-2.5 text-white shadow-md shadow-brand-600/30">
              <Building2 size={22} />
            </div>
            <div>
              <h1 className="font-bold text-slate-900">Hostel<span className="text-brand-600">MS</span></h1>
              <p className="text-xs text-slate-400">PostgreSQL Edition</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto p-4">
          {navigation.map(({ label, path, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition ${
                  isActive
                    ? path === "/portal"
                      ? "bg-slate-900 text-white shadow-sm"
                      : "bg-brand-50 text-brand-700"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`
              }
            >
              <Icon size={19} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-slate-100 p-4 bg-slate-50/50 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">API Backend</span>
            <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold ${backendError ? "bg-rose-100 text-rose-700" : "bg-emerald-100 text-emerald-700"}`}>
              {backendError ? "Offline" : "Connected"}
            </span>
          </div>
          <p className="text-[11px] text-slate-400">FastAPI + psycopg 3 + Supabase</p>
          <div className="rounded-xl bg-sky-50 border border-sky-100 px-3 py-2">
            <p className="text-[11px] font-bold text-sky-800 truncate">{currentUser?.name}</p>
            <p className="text-[10px] text-sky-600">Warden • {currentUser?.hostel_name}</p>
          </div>
          <button
            onClick={onLogout}
            className="w-full rounded-xl border border-rose-200 bg-rose-50 py-2 text-xs font-bold text-rose-700 hover:bg-rose-100 transition"
          >
            Sign Out
          </button>
        </div>
      </aside>

      {/* Content Area */}
      <div className="min-h-screen lg:pl-72">
        <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-200/80 bg-white/90 px-4 backdrop-blur sm:px-8">
          <div className="flex items-center gap-3">
            <button className="rounded-lg p-2 hover:bg-slate-100 lg:hidden" onClick={() => setSidebarOpen(true)}>
              <Menu size={22} />
            </button>
            <div>
              <p className="text-xs font-medium text-slate-400">Hostel Management /</p>
              <h2 className="font-bold text-slate-900">{title}</h2>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className={`hidden rounded-full px-3 py-1 text-xs font-semibold sm:block ${backendError ? "bg-rose-100 text-rose-700" : "bg-emerald-50 text-emerald-700"}`}>
              {backendError ? "Backend Disconnected" : "Live Database Mode"}
            </div>
          </div>
        </header>

        <main className="mx-auto max-w-[1600px] p-4 sm:p-8">
          {backendError && (
            <div className="mb-6 flex items-center justify-between rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-800 shadow-sm">
              <div className="flex items-center gap-3">
                <AlertCircle size={20} />
                <div>
                  <p className="font-bold text-sm">Cannot reach FastAPI backend server</p>
                  <p className="text-xs text-rose-700">Ensure the backend is running (`uvicorn app.main:app --reload` on port 8000).</p>
                </div>
              </div>
              <button
                onClick={loadAllData}
                className="rounded-xl bg-rose-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-rose-700"
              >
                Retry
              </button>
            </div>
          )}

          {navigation.some((item) => item.path === location.pathname && item.path !== "/") ? (
            <RecordPage currentUser={currentUser} page={location.pathname} data={data} refreshData={loadAllData} />
          ) : (
            <Dashboard currentUser={currentUser} data={data} refreshData={loadAllData} />
          )}
        </main>
      </div>
    </div>
  );
}

function AppContent() {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem("hostel_user");
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  // Guard against browser back-forward cache (bfcache), popstate & multi-tab logout
  useEffect(() => {
    function verifyAuthAndPreventCache() {
      const saved = localStorage.getItem("hostel_user");
      if (!saved) {
        if (currentUser) {
          setCurrentUser(null);
        }
        if (window.location.pathname !== "/login") {
          window.location.replace("/login");
        }
      }
    }

    // Listens for page restores from bfcache (browser back/forward button)
    window.addEventListener("pageshow", verifyAuthAndPreventCache);
    // Listens for history navigation popstate events
    window.addEventListener("popstate", verifyAuthAndPreventCache);
    // Listens for session invalidation in another tab
    const handleStorageChange = (e) => {
      if (e.key === "hostel_user" && !e.newValue) {
        setCurrentUser(null);
        window.location.replace("/login");
      }
    };
    window.addEventListener("storage", handleStorageChange);

    return () => {
      window.removeEventListener("pageshow", verifyAuthAndPreventCache);
      window.removeEventListener("popstate", verifyAuthAndPreventCache);
      window.removeEventListener("storage", handleStorageChange);
    };
  }, [currentUser]);

  function handleLoginSuccess(user) {
    setCurrentUser(user);
    try {
      localStorage.setItem("hostel_user", JSON.stringify(user));
      sessionStorage.setItem("hostel_user", JSON.stringify(user));
    } catch (e) {
      console.error("Storage set error:", e);
    }
    // Replace history entry so /login cannot be navigated back to
    if (user.role === "STUDENT") {
      navigate("/portal", { replace: true });
    } else {
      navigate("/", { replace: true });
    }
  }

  async function handleLogout() {
    try {
      await authService.logout();
    } catch (e) {
      console.warn("Logout notification error:", e);
    }

    try {
      localStorage.removeItem("hostel_user");
      localStorage.clear();
      sessionStorage.clear();
    } catch (e) {
      console.error("Storage clear error:", e);
    }

    setCurrentUser(null);

    // Overwrite current history state and replace location to /login
    // This removes the protected page from the forward/back history stack
    window.history.replaceState(null, "", "/login");
    navigate("/login", { replace: true });
  }

  return (
    <Routes>
      {/* Public Login Route */}
      <Route
        path="/login"
        element={
          currentUser ? (
            <Navigate to={currentUser.role === "STUDENT" ? "/portal" : "/"} replace />
          ) : (
            <LoginPage onLoginSuccess={handleLoginSuccess} />
          )
        }
      />

      {/* Student Portal (Protected for STUDENT) */}
      <Route
        path="/portal"
        element={
          !currentUser ? (
            <Navigate to="/login" replace />
          ) : currentUser.role !== "STUDENT" ? (
            <Navigate to="/" replace />
          ) : (
            <div className="min-h-screen bg-slate-50">
              <StudentPortal currentUser={currentUser} onLogout={handleLogout} />
            </div>
          )
        }
      />

      {/* Warden Administration Routes (Protected for WARDEN) */}
      {navigation.map((item) => (
        <Route
          key={item.path}
          path={item.path}
          element={
            !currentUser ? (
              <Navigate to="/login" replace />
            ) : currentUser.role !== "WARDEN" ? (
              <Navigate to="/portal" replace />
            ) : (
              <AppShell currentUser={currentUser} onLogout={handleLogout} />
            )
          }
        />
      ))}

      {/* Fallback Catch-all Route */}
      <Route
        path="*"
        element={
          !currentUser ? (
            <Navigate to="/login" replace />
          ) : (
            <Navigate to={currentUser.role === "STUDENT" ? "/portal" : "/"} replace />
          )
        }
      />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}