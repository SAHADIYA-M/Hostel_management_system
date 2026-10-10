# UI/UX Design & Export Guidelines

This directory stores exported UI design wireframes and high-fidelity mockups for the **Hostel Management System**.

---

## 🔗 Official Figma Project Link

All UI/UX designs, wireframes, component styles, and screen mockups **must strictly be created and maintained in the official team Figma file**:

👉 **[Hostel Management System — UI Design (Figma)](https://www.figma.com/design/OIT1nOvW1WjS5YMywyweEy/Hostel-Management-System--UI-Design?t=7D2VjWokgU2jFMMr-1)**

> ⚠️ **Important:** Do not create separate personal Figma files or unlinked drafts. All team members must collaborate directly within this shared project to ensure a single source of truth for the frontend implementation.

---

## 📱 Required Screens & Modules (Aligned with Relational Schema)

Designs must reflect the entities, attributes, and relationships defined in [`docs/project-context.md`](file:///c:/Projects/Hostel_management_system/docs/project-context.md):

1. **Dashboard / Overview:**
   - Summary statistics (total students, room occupancy rate, pending maintenance, open complaints, fee collection status).
   - Quick navigation shortcuts.
2. **Hostels & Wardens / Staff:**
   - Hostel profiles (`Hostel_ID`, name, address, type).
   - Assigned Warden details and hostel Staff list.
3. **Rooms & Room Allotment:**
   - Room registry (`(Hostel_ID, Room_No)`, type, capacity, current occupancy).
   - Student allotment interface with capacity validation indicators.
4. **Student Management:**
   - Student roster (`Student_ID`, name, `Reg_No`, phone).
   - Assigned room and mess subscription details.
5. **Mess Subscriptions:**
   - Mess types (`Mess_ID`, type, monthly cost).
   - Enrolled student list.
6. **Fees & Fines:**
   - Student fee tracking (`Fee_ID`, due date, amount, status: `PAID` / `PENDING`).
   - Fine management (`FID`, reason, amount, status: `PAID` / `PENDING`).
7. **Daily Attendance:**
   - Date selector and student attendance checklist (`PRESENT` / `ABSENT` / `ON_LEAVE`).
8. **Visitors & Visit Log:**
   - Visitor registry (`Visitor_ID`, name, relation, phone).
   - Visit log records linked to students (`Visit_Date`).
9. **Maintenance & Complaints:**
   - Maintenance requests (hostel-wide vs room-specific, status, cost).
   - Student complaints and resolution tracking.

---

## 📤 Step-by-Step Figma Export Instructions

Follow these exact steps when exporting frames from Figma:

### Step 1: Prepare Frames in Figma
1. Ensure all screens are enclosed within top-level **Frames** (recommended desktop width: `1440px` or `1920px`).
2. Label each frame cleanly in Figma using lowercase kebab-case (e.g., `01-dashboard`, `02-students-list`).

### Step 2: Configure Export Settings
1. Select the screen frame you want to export.
2. In the right-hand sidebar, navigate to the **Export** section at the bottom.
3. Click the **`+`** button to create an export configuration.
4. Set the export format:
   - **Format:** `PNG` (for full screen mockups and wireframes) or `SVG` (for icons and scalable vectors).
   - **Resolution:** `2x` (recommended for crisp viewing in documentation) or `1x`.

### Step 3: Export the Image
1. Click the **Export [Frame Name]** button in the sidebar.
2. Download the exported image file to your local computer.

---

## 💾 Save Location & File Naming Conventions

### Save Location
Place all exported images directly into this directory:
```
docs/design/
```

### Standardized Naming Convention
Use lowercase, hyphen-separated (kebab-case) file names with two-digit sequence prefixes:

| Screen / Feature | Expected File Name |
|---|---|
| Admin / Warden Dashboard | `01-dashboard.png` |
| Student Directory & Profiles | `02-students.png` |
| Rooms & Allocation View | `03-rooms-allotment.png` |
| Fee & Fine Tracking | `04-fees-fines.png` |
| Mess Management | `05-mess.png` |
| Student Attendance | `06-attendance.png` |
| Visitor Log | `07-visitors.png` |
| Maintenance & Complaints | `08-maintenance-complaints.png` |
| Component UI Kit / Style Guide (Optional) | `00-ui-kit.png` |

---

## 🚀 Git Commit & Push Workflow

After saving the exported files into `docs/design/`, commit and push them to the repository using PowerShell:

```powershell
# 1. Check newly added design files
git status

# 2. Stage the exported images in docs/design/
git add docs/design/

# 3. Commit with a descriptive message
git commit -m "docs(design): export and add Figma UI screens for <screen-name>"

# 4. Push to your branch
git push origin <your-branch-name>
```
