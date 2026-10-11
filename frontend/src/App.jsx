import { useMemo, useState } from "react";
import {
  BrowserRouter,
  NavLink,
  Routes,
  Route,
  useNavigate,
  useLocation,
} from "react-router-dom";
import {
  LayoutDashboard, Building2, DoorOpen, Users, Wallet,
  Utensils, CalendarCheck, UserRound, Wrench, MessageSquare,
  Menu, Search, Plus, ArrowRight, X, CheckCircle2,
} from "lucide-react";
import StatusBadge from "./components/StatusBadge.jsx";

import {
  hostels,
  wardens,
  staff,
  rooms,
  students,
  fees,
  fines,
  messPlans,
  attendance,
  visitors,
  visits,
  maintenanceRequests,
  complaints,
} from "./Data/mockData.jsx";


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

const initialData = {
  hostels,
  wardens,
  staff,
  rooms,
  students,
  fees,
  fines,
  messPlans,
  attendance,
  visitors,
  visits,
  maintenanceRequests,
  complaints,
};

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
          : "bg-brand-600 text-white hover:bg-brand-700"
      }`}
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

function TextInput({ value, onChange, type = "text", required = false }) {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      required={required}
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

function Dashboard({ data }) {
  const metrics = [
    { label: "Total Hostels", value: data.hostels.length, icon: Building2, color: "bg-indigo-50 text-indigo-600" },
    { label: "Total Rooms", value: data.rooms.length, icon: DoorOpen, color: "bg-sky-50 text-sky-600" },
    {
      label: "Available Capacity",
      value: data.rooms.reduce((sum, room) => sum + Math.max(0, room.Capacity - room.Current_Occupants), 0),
      icon: CheckCircle2,
      color: "bg-emerald-50 text-emerald-600",
    },
    { label: "Registered Students", value: data.students.length, icon: Users, color: "bg-violet-50 text-violet-600" },
    {
      label: "Pending Fees & Fines",
      value: [...data.fees, ...data.fines].filter((item) => item.Status === "Pending").length,
      icon: Wallet,
      color: "bg-amber-50 text-amber-600",
    },
    { label: "Open Maintenance", value: data.maintenanceRequests.filter((item) => item.Status === "Open").length, icon: Wrench, color: "bg-rose-50 text-rose-600" },
    { label: "Open Complaints", value: data.complaints.filter((item) => item.Status === "Open").length, icon: MessageSquare, color: "bg-orange-50 text-orange-600" },
  ];

  const navigate = useNavigate();

  return (
    <div className="space-y-7">
      <div>
        <p className="text-sm text-slate-500">Overview</p>
        <h2 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-900"> Welcome to your dashboard</h2>
        <p className="mt-2 text-slate-500">Here's what's happening across your hostels.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map(({ label, value, icon: Icon, color }) => (
         <div key={label} className="group rounded-2xl border border-slate-200/70 bg-white p-5 shadow-card transition-all duration-200 hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg">
            <div className="flex items-center justify-between">
              <span className={`rounded-xl p-3 ${color}`}><Icon size={21} /></span>
              <ArrowRight size={16} className="text-slate-300" />
            </div>
            <p className="mt-5 text-sm text-slate-500">{label}</p>
            <p className="mt-1 text-3xl font-bold">{value}</p>
          </div>
        ))}
      </div>

      <section className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm">
        <h3 className="font-bold">Quick actions</h3>
        <p className="mt-1 text-sm text-slate-500">Jump directly to common tasks.</p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Button onClick={() => navigate("/students")}><Plus size={16} /> Register Student</Button>
          <Button secondary onClick={() => navigate("/attendance")}><CalendarCheck size={16} /> Mark Attendance</Button>
          <Button secondary onClick={() => navigate("/maintenance")}><Wrench size={16} /> Log Maintenance Request</Button>
        </div>
      </section>

      <section className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
        <div className="border-b border-slate-100 p-5">
          <h3 className="font-bold">Recent maintenance requests</h3>
        </div>
        <DataTable
          columns={[
            { key: "Request_ID", label: "Request ID" },
            { key: "Description", label: "Description" },
            { key: "Date", label: "Date" },
            { key: "Status", label: "Status", render: (row) => <StatusBadge status={row.Status} /> },
          ]}
          rows={data.maintenanceRequests.slice(0, 5)}
        />
      </section>
    </div>
  );
}

function RecordPage({ page, data, updateData }) {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [modal, setModal] = useState(false);
  const [message, setMessage] = useState("");
  const [selectedMess, setSelectedMess] = useState("1");
  const [date, setDate] = useState("2026-10-11");
  const [form, setForm] = useState({});
  const navigate = useNavigate();

  const setField = (key, value) => setForm((old) => ({ ...old, [key]: value }));

  const config = {
    "/hostels": { key: "hostels", title: "Hostels & Staff", columns: ["Hostel_ID", "Name", "Address", "Type"], fields: ["Name", "Address", "Type"] },
    "/rooms": { key: "rooms", title: "Rooms & Allotment", columns: ["Hostel_ID", "Room_No", "Type", "Capacity", "Current_Occupants"], fields: ["Hostel_ID", "Room_No", "Type", "Capacity"] },
    "/students": { key: "students", title: "Students", columns: ["Student_ID", "FName", "LName", "Reg_No", "Phone", "Hostel_ID", "Room_No", "Mess_ID"], fields: ["FName", "LName", "Reg_No", "Phone"] },
    "/fees-fines": { key: "fees", title: "Fees & Fines", columns: ["Fee_ID", "Due_Date", "Amount", "Status", "Student_ID"], fields: ["Due_Date", "Amount", "Student_ID"] },
    "/mess": { key: "messPlans", title: "Mess Subscriptions", columns: ["Mess_ID", "Type", "Cost"], fields: ["Type", "Cost"] },
    "/attendance": { key: "attendance", title: "Attendance", columns: ["Student_ID", "Student_Name", "Room_No", "Date", "Status"], fields: [] },
    "/visitors": { key: "visitors", title: "Visitors & Visits Log", columns: ["Visitor_ID", "Name", "Relation", "Phone"], fields: ["Name", "Relation", "Phone"] },
    "/maintenance": { key: "maintenanceRequests", title: "Maintenance Requests", columns: ["Request_ID", "Hostel_ID", "Room_No", "Description", "Date", "Status"], fields: ["Hostel_ID", "Description", "Date"] },
    "/complaints": { key: "complaints", title: "Student Complaints", columns: ["Complaint_ID", "Date", "Description", "Status", "Student_ID"], fields: ["Date", "Description", "Student_ID"] },
  };

  const current = config[page];

  const rows = useMemo(() => {
    if (page === "/visitors") {
      return data.visitors;
    }
    if (page === "/mess") {
      return data.messPlans;
    }
    let result = data[current.key] || [];

    if (page === "/students") {
      if (filter === "unallotted") result = result.filter((r) => !r.Hostel_ID || !r.Room_No);
      else if (filter !== "all") result = result.filter((r) => String(r.Hostel_ID) === filter);
    }

    if (page === "/attendance") {
      result = result.filter((r) => r.Date === date);
    }

    if (page === "/mess") {
      result = result.filter((r) => String(r.Mess_ID) === selectedMess);
    }

    if (search.trim()) {
      const term = search.toLowerCase();
      result = result.filter((row) =>
        Object.values(row).some((value) =>
          String(value ?? "").toLowerCase().includes(term)
        )
      );
    }
    return result;
  }, [data, current, page, search, filter, date, selectedMess]);

  function addRecord(e) {
    e.preventDefault();
    const key = current.key;
    const list = data[key] || [];
    const idField = Object.keys(list[0] || {}).find((k) => k.endsWith("_ID") || k === "FID");
    const nextId = list.reduce((max, row) => Math.max(max, Number(row[idField]) || 0), 0) + 1;

    let record = { ...form };
    for (const [keyName, value] of Object.entries(record)) {
      if (value === "") record[keyName] = null;
    }

    if (idField && record[idField] == null) record[idField] = nextId;

    if (page === "/students") {
      if (data.students.some((s) => s.Reg_No.toLowerCase() === String(record.Reg_No || "").toLowerCase())) {
        setMessage("Registration number must be unique.");
        return;
      }
      record.Student_ID = nextId;
      record.Hostel_ID = null;
      record.Room_No = null;
      record.Allot_Date = null;
      record.Mess_ID = record.Mess_ID ? Number(record.Mess_ID) : null;
    }

    if (page === "/maintenance") {
      record.Request_ID = nextId;
      record.Hostel_ID = Number(record.Hostel_ID);
      record.Room_No = record.Room_No ? Number(record.Room_No) : null;
      record.Status = "Open";
    }

    if (page === "/complaints") {
      record.Complaint_ID = nextId;
      record.Student_ID = Number(record.Student_ID);
      record.Status = "Open";
    }

    if (page === "/fees-fines") {
      record.Fee_ID = nextId;
      record.Amount = Number(record.Amount);
      record.Student_ID = Number(record.Student_ID);
      record.Status = "Pending";
    }

    updateData((old) => ({ ...old, [key]: [...old[key], record] }));
    setForm({});
    setMessage("Record added to local mock data.");
    setModal(false);
  }

  function updateStatus(row, status) {
    const key = current.key;
    updateData((old) => ({
      ...old,
      [key]: old[key].map((item) => item === row || (
        page === "/attendance" && item.Student_ID === row.Student_ID && item.Date === row.Date
      ) ? { ...item, Status: status } : item),
    }));
  }

  if (!current) return <div>Page not found.</div>;

  const statusOptions = page === "/attendance"
    ? ["Present", "Absent"]
    : page === "/fees-fines"
      ? ["Pending", "Paid"]
      : ["Open", "In Progress", "Resolved"];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">{current.title}</h2>
          <p className="mt-1 text-sm text-slate-500">
            Manage and review your {current.title.toLowerCase()} records.
          </p>
        </div>
        {current.fields.length > 0 && (
          <Button onClick={() => { setForm({}); setMessage(""); setModal(true); }}>
            <Plus size={17} /> Add record
          </Button>
        )}
      </div>

      {message && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          {message}
        </div>
      )}

      {page === "/hostels" && (
        <div className="grid gap-4 md:grid-cols-2">
          {data.hostels.map((hostel) => (
            <div key={hostel.Hostel_ID} className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm">
              <Building2 className="mb-3 text-brand-600" size={24} />
              <h3 className="font-bold">{hostel.Name}</h3>
              <p className="mt-1 text-sm text-slate-500">{hostel.Address}</p>
              <p className="mt-3 text-sm">Type: {hostel.Type}</p>
              <p className="mt-2 text-sm">Hostel ID: {hostel.Hostel_ID}</p>
              {data.wardens.filter((w) => w.Hostel_ID === hostel.Hostel_ID).map((w) => (
                <p key={w.Warden_ID} className="mt-3 border-t pt-3 text-sm text-slate-600">
                  Warden: {w.Name} · {w.Phone}
                </p>
              ))}
              {data.staff.filter((s) => s.Hostel_ID === hostel.Hostel_ID).map((s) => (
                <p key={s.Staff_ID} className="mt-1 text-sm text-slate-500">
                  {s.Role} · {s.Phone}
                </p>
              ))}
            </div>
          ))}
        </div>
      )}

      {page === "/rooms" && (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {data.rooms.map((room) => {
            const full = room.Current_Occupants >= room.Capacity;
            return (
              <div key={`${room.Hostel_ID}-${room.Room_No}`} className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm">
                <div className="flex justify-between">
                  <DoorOpen className="text-brand-600" />
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${full ? "bg-rose-100 text-rose-700" : "bg-emerald-100 text-emerald-700"}`}>
                    {full ? "Full" : "Available"}
                  </span>
                </div>
                <h3 className="mt-4 text-xl font-bold">Room {room.Room_No}</h3>
                <p className="text-sm text-slate-500">{room.Type} · Hostel {room.Hostel_ID}</p>
                <p className="mt-3 text-sm">Occupancy: {room.Current_Occupants}/{room.Capacity}</p>
                <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                  <div className={`h-full ${full ? "bg-rose-500" : "bg-emerald-500"}`} style={{ width: `${Math.min(100, room.Current_Occupants / room.Capacity * 100)}%` }} />
                </div>
                <Button
                  secondary
                  disabled={full}
                  onClick={() => navigate("/students")}
                >
                  {full ? "Room full" : "Manage student allotment"}
                </Button>
              </div>
            );
          })}
        </div>
      )}

      {page === "/attendance" && (
        <div className="max-w-xs">
          <Field label="Attendance date">
            <TextInput type="date" value={date} onChange={setDate} />
          </Field>
          <Button onClick={() => updateData((old) => ({
            ...old,
            attendance: old.attendance.map((r) => r.Date === date ? { ...r, Status: "Present" } : r),
          }))}>
            <CheckCircle2 size={16} /> Mark All Present
          </Button>
        </div>
      )}

      {page === "/mess" && (
        <div className="max-w-sm">
          <Field label="Select mess plan">
            <SelectInput value={selectedMess} onChange={setSelectedMess} options={data.messPlans.map((m) => ({ value: String(m.Mess_ID), label: `${m.Type} — ₹${m.Cost}` }))} />
          </Field>
          <p className="mt-2 text-sm text-slate-500">
            Subscribed students: {data.students.filter((s) => String(s.Mess_ID) === selectedMess).length}
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            {data.students.filter((s) => String(s.Mess_ID) === selectedMess).map((s) => (
              <span key={s.Student_ID} className="rounded-lg bg-white px-3 py-2 text-sm shadow-sm">
                {s.FName} {s.LName} · {s.Reg_No}
              </span>
            ))}
          </div>
        </div>
      )}

      {page === "/students" && (
        <div className="flex flex-wrap gap-3">
          <select value={filter} onChange={(e) => setFilter(e.target.value)} className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm">
            <option value="all">All students</option>
            <option value="unallotted">Un-allotted students</option>
            {data.hostels.map((h) => <option key={h.Hostel_ID} value={String(h.Hostel_ID)}>Hostel {h.Hostel_ID}</option>)}
          </select>
        </div>
      )}

      <section className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 p-4">
          <div className="flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2">
            <Search size={17} className="text-slate-400" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={page === "/students" ? "Search name or Reg_No..." : "Search records..."}
              className="min-w-0 bg-transparent text-sm outline-none"
            />
          </div>
          <span className="text-sm text-slate-500">{rows.length} records</span>
        </div>

        <DataTable
          columns={[
            ...current.columns.map((key) => ({
              key,
              label: key,
              render: (row) => {
                if (key === "Status") return <StatusBadge status={row.Status} />;
                if (key === "Amount" || key === "Cost") return `₹${Number(row[key]).toLocaleString("en-IN")}`;
                if (key === "Room_No" && row[key] == null) return "Un-allotted";
                return row[key] ?? "—";
              },
            })),
            ...(page === "/attendance" || page === "/fees-fines" || page === "/maintenance" || page === "/complaints"
              ? [{
                  key: "_action",
                  label: "Update status",
                  render: (row) => (
                    <select
                      value={row.Status}
                      onChange={(e) => updateStatus(row, e.target.value)}
                      className="rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-xs"
                    >
                      {statusOptions.map((status) => <option key={status}>{status}</option>)}
                    </select>
                  ),
                }]
              : []),
          ]}
          rows={rows}
        />
      </section>

      {page === "/fees-fines" && (
        <section className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
          <div className="p-5"><h3 className="font-bold">Fines</h3></div>
          <DataTable
            columns={[
              { key: "FID", label: "FID" },
              { key: "Reason", label: "Reason" },
              { key: "Amount", label: "Amount", render: (r) => `₹${Number(r.Amount).toLocaleString("en-IN")}` },
              { key: "Status", label: "Status", render: (r) => <StatusBadge status={r.Status} /> },
              { key: "Student_ID", label: "Student_ID" },
              { key: "action", label: "Update", render: (r) => <button onClick={() => updateData((old) => ({ ...old, fines: old.fines.map((f) => f.FID === r.FID ? { ...f, Status: f.Status === "Paid" ? "Pending" : "Paid" } : f) }))} className="text-brand-600">Toggle</button> },
            ]}
            rows={data.fines}
          />
        </section>
      )}

      {page === "/visitors" && (
        <section className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
          <div className="p-5"><h3 className="font-bold">Visit logs</h3></div>
          <DataTable columns={[
            { key: "Student_ID", label: "Student_ID" },
            { key: "Student_Name", label: "Student Name" },
            { key: "Visitor_ID", label: "Visitor_ID" },
            { key: "Visitor_Name", label: "Visitor Name" },
            { key: "Relation", label: "Relation" },
            { key: "Visit_Date", label: "Visit Date" },
          ]} rows={data.visits} />
        </section>
      )}

      {modal && (
        <Modal title={`Add ${current.title} record`} onClose={() => setModal(false)}>
          <form onSubmit={addRecord} className="space-y-4">
            {current.fields.map((key) => (
              <Field key={key} label={key}>
                {key === "Date" || key === "Due_Date" ? (
                  <TextInput type="date" value={form[key] || ""} onChange={(v) => setField(key, v)} required />
                ) : key === "Hostel_ID" ? (
                  <SelectInput value={form[key] || String(data.hostels[0]?.Hostel_ID || "")} onChange={(v) => setField(key, v)} options={data.hostels.map((h) => ({ value: String(h.Hostel_ID), label: h.Name }))} />
                ) : key === "Student_ID" ? (
                  <SelectInput value={form[key] || String(data.students[0]?.Student_ID || "")} onChange={(v) => setField(key, v)} options={data.students.map((s) => ({ value: String(s.Student_ID), label: `${s.FName} ${s.LName} (${s.Student_ID})` }))} />
                ) : key === "Type" && page === "/hostels" ? (
                  <SelectInput value={form[key] || "Boys"} onChange={(v) => setField(key, v)} options={[{ value: "Boys", label: "Boys" }, { value: "Girls", label: "Girls" }]} />
                ) : key === "Amount" || key === "Cost" || key === "Capacity" || key === "Room_No" ? (
                  <TextInput type="number" value={form[key] ?? ""} onChange={(v) => setField(key, v)} required={key !== "Room_No"} />
                ) : key === "Description" || key === "Reason" || key === "Address" ? (
                  <textarea value={form[key] || ""} onChange={(e) => setField(key, e.target.value)} required rows={3} className="w-full rounded-xl border border-slate-200 p-3" />
                ) : (
                  <TextInput value={form[key] || ""} onChange={(v) => setField(key, v)} required />
                )}
              </Field>
            ))}
            <div className="flex justify-end gap-3 pt-3">
              <Button secondary onClick={() => setModal(false)}>Cancel</Button>
              <button type="submit" className="rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white">Save record</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}

function AppShell() {
  const [data, updateData] = useState(initialData);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const title = titles[location.pathname] || "Dashboard";

  return (
    <div className="min-h-screen bg-slate-50">
      {sidebarOpen && (
        <button aria-label="Close navigation" onClick={() => setSidebarOpen(false)} className="fixed inset-0 z-30 bg-slate-950/30 lg:hidden" />
      )}
      <aside className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col bg-white shadow-sm transition-transform lg:translate-x-0 ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="flex h-20 items-center gap-3 border-b border-slate-100 px-6">
          <div className="rounded-xl bg-brand-600 p-2.5 text-white"><Building2 size={22} /></div>
          <div><h1 className="font-bold">Hostel<span className="text-brand-600">Hub</span></h1><p className="text-xs text-slate-400">Management System</p></div>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto p-4">
          {navigation.map(({ label, path, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) => `flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${isActive ? "bg-brand-50 text-brand-700" : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"}`}
            >
              <Icon size={19} /> {label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-slate-100 p-4">
          <p className="text-xs text-slate-400">College DBMS Project</p>
          <p className="mt-1 text-sm font-medium text-slate-600">Frontend prototype</p>
        </div>
      </aside>

      <div className="min-h-screen lg:pl-72">
        <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-100 bg-white/90 px-4 backdrop-blur sm:px-8">
          <div className="flex items-center gap-3">
            <button className="rounded-lg p-2 hover:bg-slate-100 lg:hidden" onClick={() => setSidebarOpen(true)}><Menu size={22} /></button>
            <div><p className="text-xs text-slate-400">Hostel Management /</p><h2 className="font-bold">{title}</h2></div>
          </div>
          <div className="hidden rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 sm:block">Mock data mode</div>
        </header>

        <main className="mx-auto max-w-[1600px] p-4 sm:p-8">
          <Routes>
            <Route path="/" element={<Dashboard data={data} />} />
            {navigation.filter((item) => item.path !== "/").map((item) => (
              <Route key={item.path} path={item.path} element={<RecordPage page={item.path} data={data} updateData={updateData} />} />
            ))}
            <Route path="*" element={<Dashboard data={data} />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  );
}