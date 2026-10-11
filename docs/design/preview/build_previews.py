"""
Build HTML UI Design Previews and Export High-Resolution PNG Mockups
Tailored for Hostel Management System (aligned with docs/project-context.md & database/seed.sql)
Responsive across laptops, tablets, and mobile devices.
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DESIGN_DIR = BASE_DIR.parent
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_sidebar_html(active_id):
    items = [
        ("01-dashboard", "01-dashboard.html", "Dashboard", "📊", ""),
        ("02-students", "02-students.html", "Students", "🎓", "7"),
        ("03-rooms-allotment", "03-rooms-allotment.html", "Rooms & Allotment", "🛏️", "9"),
        ("04-fees-fines", "04-fees-fines.html", "Fees & Fines", "💳", "3 Pending"),
        ("05-mess", "05-mess.html", "Mess Plans", "🍽️", "3 Plans"),
        ("06-attendance", "06-attendance.html", "Attendance", "📅", "Today"),
        ("07-visitors", "07-visitors.html", "Visitor Log", "👥", "4 Visits"),
        ("08-maintenance-complaints", "08-maintenance-complaints.html", "Maintenance & Issues", "🔧", "4 Active"),
    ]

    nav_links = ""
    for item_id, href, label, icon, badge in items:
        is_active = "active" if item_id == active_id else ""
        badge_html = f'<span class="nav-badge">{badge}</span>' if badge else ""
        nav_links += f"""
        <a href="{href}" class="nav-item {is_active}">
            <div class="nav-item-left">
                <span style="font-size: 16px;">{icon}</span>
                <span>{label}</span>
            </div>
            {badge_html}
        </a>
        """

    return f"""
    <aside class="sidebar">
        <div class="sidebar-header">
            <div class="logo-badge">H</div>
            <div class="logo-text">
                <h1>HostelMS</h1>
                <span>Enterprise DBMS</span>
            </div>
        </div>

        <div class="hostel-selector-box">
            <label>Current Hostel</label>
            <div class="hostel-pill">
                <span>🏢 Ganga Boys Hostel</span>
                <span style="font-size: 11px; opacity: 0.7;">▼</span>
            </div>
        </div>

        <div class="sidebar-nav">
            <div class="nav-section-title">Hostel Operations</div>
            {nav_links}
        </div>

        <div class="sidebar-footer">
            <div class="user-avatar">SK</div>
            <div class="user-info">
                <h4>Dr. Suresh Kumar</h4>
                <p>Chief Warden • Hostel #1</p>
            </div>
        </div>
    </aside>
    """

def get_topbar_html(active_title):
    return f"""
    <header class="topbar">
        <div class="search-box">
            <span style="color: #94a3b8; font-size: 14px;">🔍</span>
            <input type="text" placeholder="Search student by name, Reg No, room, phone..." />
        </div>
        <div class="topbar-actions">
            <div class="system-status-indicator">
                <span class="dot-online"></span>
                <span>HostelMS • Online (Hostel #1 Active)</span>
            </div>
            <div style="font-size: 13px; font-weight: 500; color: #64748b; border-left: 1px solid #e2e8f0; padding-left: 16px;">
                📅 Sunday, Oct 11, 2026
            </div>
        </div>
    </header>
    """

def wrap_page(page_id, page_title, content_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - Hostel Management System</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        {get_sidebar_html(page_id)}
        <div class="main-wrapper">
            {get_topbar_html(page_title)}
            <main class="content-body">
                {content_html}
            </main>
        </div>
    </div>
</body>
</html>
"""

def get_student_sidebar_html(active_id):
    items = [
        ("overview", "#overview", "My Dashboard", "🏠", ""),
        ("room", "#room", "My Room & Roommate", "🛏️", "Room 101"),
        ("fees", "#fees", "My Fees & Fines", "💳", "Paid"),
        ("mess", "#mess", "My Mess Plan", "🍽️", "Active"),
        ("attendance", "#attendance", "My Attendance Log", "📅", "100%"),
        ("grievances", "#grievances", "Grievances & Repairs", "🔧", "2 Resolved"),
        ("visitors", "#visitors", "Registered Visitors", "👥", "2 Approved"),
    ]

    nav_links = ""
    for item_id, href, label, icon, badge in items:
        is_active = "active" if item_id == active_id else ""
        badge_html = f'<span class="nav-badge">{badge}</span>' if badge else ""
        nav_links += f"""
        <a href="{href}" class="nav-item {is_active}">
            <div class="nav-item-left">
                <span style="font-size: 16px;">{icon}</span>
                <span>{label}</span>
            </div>
            {badge_html}
        </a>
        """

    return f"""
    <aside class="sidebar">
        <div class="sidebar-header">
            <div class="logo-badge" style="background: linear-gradient(135deg, #10b981, #059669);">S</div>
            <div class="logo-text">
                <h1>HostelMS</h1>
                <span style="color: #34d399;">Student Portal</span>
            </div>
        </div>

        <div class="hostel-selector-box">
            <label>Resident Profile</label>
            <div class="hostel-pill" style="border-color: #059669;">
                <span>🎓 Rahul Sharma</span>
                <span style="font-size: 11px; background: #064e3b; color: #a7f3d0; padding: 2px 6px; border-radius: 4px;">#1001</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 6px;">
                🏢 Ganga Boys Hostel • Room 101
            </div>
        </div>

        <div class="sidebar-nav">
            <div class="nav-section-title">My Personal Space</div>
            {nav_links}

            <div class="nav-section-title" style="margin-top: 14px;">Switch View</div>
            <a href="01-dashboard.html" class="nav-item" style="border: 1px dashed #334155; color: #94a3b8;">
                <div class="nav-item-left">
                    <span style="font-size: 16px;">🛡️</span>
                    <span>Warden Admin View</span>
                </div>
                <span style="font-size: 12px;">→</span>
            </a>
        </div>

        <div class="sidebar-footer">
            <div class="user-avatar" style="background: #10b981;">RS</div>
            <div class="user-info">
                <h4>Rahul Sharma</h4>
                <p>REG2024001 • B.Tech CSE</p>
            </div>
        </div>
    </aside>
    """

def get_student_topbar_html(active_title):
    return f"""
    <header class="topbar">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a;">
                Student Self-Service Portal
            </div>
            <span class="badge badge-paid">Role: Student</span>
            <span class="badge badge-info">Hostel #1: Ganga Boys</span>
        </div>
        <div class="topbar-actions">
            <div class="system-status-indicator">
                <span class="dot-online"></span>
                <span>Logged in as: Rahul Sharma (REG2024001)</span>
            </div>
            <div style="font-size: 13px; font-weight: 500; color: #64748b; border-left: 1px solid #e2e8f0; padding-left: 16px;">
                📅 Sunday, Oct 11, 2026
            </div>
        </div>
    </header>
    """

def wrap_student_page(page_id, page_title, content_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - Hostel Management System</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        {get_student_sidebar_html(page_id)}
        <div class="main-wrapper">
            {get_student_topbar_html(page_title)}
            <main class="content-body">
                {content_html}
            </main>
        </div>
    </div>
</body>
</html>
"""

def generate_screens():
    screens = {}

    # 01: Dashboard
    screens["01-dashboard"] = wrap_page("01-dashboard", "Overview Dashboard", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Hostel Operations Dashboard</h2>
            <p>Real-time statistics across students, room allotments, and finance ledger</p>
        </div>
        <div class="header-actions">
            <a href="03-rooms-allotment.html" class="btn btn-outline">🛏️ Allot Room</a>
            <a href="02-students.html" class="btn btn-primary">+ Register Student</a>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Total Students</span>
                <div class="stat-icon-wrapper icon-blue">👥</div>
            </div>
            <div class="stat-value">7 Registered</div>
            <div class="stat-subtext"><span class="trend-up">5 Allotted</span> • 2 Pending Room</div>
        </div>
        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Room Occupancy</span>
                <div class="stat-icon-wrapper icon-emerald">🏢</div>
            </div>
            <div class="stat-value">62.5%</div>
            <div class="stat-subtext">5 Beds Occupied of 8 Total</div>
        </div>
        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Fee Collection</span>
                <div class="stat-icon-wrapper icon-amber">💰</div>
            </div>
            <div class="stat-value">₹95,000</div>
            <div class="stat-subtext"><span class="trend-warning">₹1,45,000 Pending</span> (3 students)</div>
        </div>
        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Open Issues</span>
                <div class="stat-icon-wrapper icon-rose">⚠️</div>
            </div>
            <div class="stat-value">4 Active</div>
            <div class="stat-subtext">2 Maintenance • 2 Complaints</div>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
        <!-- Left: Hostel Summary -->
        <div class="card-panel">
            <div class="panel-header">
                <h3>Hostel Summary & Warden Assignment</h3>
                <span class="badge badge-info">3 Hostels Managed</span>
            </div>
            <div class="table-responsive">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Hostel Name</th>
                            <th>Type</th>
                            <th>Assigned Warden</th>
                            <th>Staff Count</th>
                            <th>Capacity</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Ganga Boys Hostel</strong></td>
                            <td><span class="badge badge-info">Boys</span></td>
                            <td>Dr. Suresh Kumar (+919876543210)</td>
                            <td>3 Staff</td>
                            <td>
                                <div class="capacity-container">
                                    <div class="progress-bar-bg"><div class="progress-bar-fill fill-amber" style="width: 50%;"></div></div>
                                    <span>2/4 Beds</span>
                                </div>
                            </td>
                            <td><a href="03-rooms-allotment.html" class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Manage</a></td>
                        </tr>
                        <tr>
                            <td><strong>Yamuna Girls Hostel</strong></td>
                            <td><span class="badge badge-info">Girls</span></td>
                            <td>Prof. Meenakshi Sundaram (+919876543211)</td>
                            <td>3 Staff</td>
                            <td>
                                <div class="capacity-container">
                                    <div class="progress-bar-bg"><div class="progress-bar-fill fill-green" style="width: 40%;"></div></div>
                                    <span>2/5 Beds</span>
                                </div>
                            </td>
                            <td><a href="03-rooms-allotment.html" class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Manage</a></td>
                        </tr>
                        <tr>
                            <td><strong>Kaveri Boys Hostel</strong></td>
                            <td><span class="badge badge-info">Boys</span></td>
                            <td>Dr. Rajesh Pillai (+919876543212)</td>
                            <td>2 Staff</td>
                            <td>
                                <div class="capacity-container">
                                    <div class="progress-bar-bg"><div class="progress-bar-fill fill-green" style="width: 33%;"></div></div>
                                    <span>1/3 Beds</span>
                                </div>
                            </td>
                            <td><a href="03-rooms-allotment.html" class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Manage</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Right: Urgent Alerts -->
        <div class="card-panel">
            <div class="panel-header">
                <h3>🚨 Action Required</h3>
            </div>
            <div style="padding: 20px; display: flex; flex-direction: column; gap: 14px;">
                <div style="padding: 12px; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 6px;">
                    <div style="font-weight: 600; font-size: 13px; color: #b45309;">2 Students Unallotted</div>
                    <div style="font-size: 12px; color: #78350f; margin-top: 2px;">Vikram Rathore & Pooja Menon require room allocation.</div>
                </div>
                <div style="padding: 12px; background: #fef2f2; border-left: 4px solid #ef4444; border-radius: 6px;">
                    <div style="font-weight: 600; font-size: 13px; color: #b91c1c;">Water Cooler Filter Alert</div>
                    <div style="font-size: 12px; color: #7f1d1d; margin-top: 2px;">Hostel #1 main corridor filter maintenance pending.</div>
                </div>
                <div style="padding: 12px; background: #ecfdf5; border-left: 4px solid #10b981; border-radius: 6px;">
                    <div style="font-weight: 600; font-size: 13px; color: #047857;">Attendance Recorded</div>
                    <div style="font-size: 12px; color: #064e3b; margin-top: 2px;">Oct 10: 4 Present, 1 Absent marked.</div>
                </div>
            </div>
        </div>
    </div>
    """)

    # 02: Students
    screens["02-students"] = wrap_page("02-students", "Student Management", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Student Directory & Allotments</h2>
            <p>Registered students, assigned rooms, mess plans, and contact details</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-outline">📥 Export CSV</button>
            <button class="btn btn-primary">+ Register Student</button>
        </div>
    </div>

    <div class="card-panel">
        <div class="filter-bar">
            <div class="filter-group">
                <input type="text" placeholder="Filter by name or Reg No..." class="select-input" style="width: 240px;" />
                <select class="select-input">
                    <option>All Hostels (3)</option>
                    <option>Ganga Boys Hostel</option>
                    <option>Yamuna Girls Hostel</option>
                    <option>Kaveri Boys Hostel</option>
                </select>
                <select class="select-input">
                    <option>Allotment: All</option>
                    <option>Allotted Only</option>
                    <option>Unallotted Only</option>
                </select>
            </div>
            <div style="font-size: 13px; color: #64748b; font-weight: 500;">
                Showing <strong>7</strong> of 7 registered students
            </div>
        </div>

        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Full Name</th>
                        <th>Reg No</th>
                        <th>Phone</th>
                        <th>Assigned Room</th>
                        <th>Allot Date</th>
                        <th>Mess Plan</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#1001</td>
                        <td><strong>Rahul Sharma</strong></td>
                        <td><code>REG2024001</code></td>
                        <td>+919811122201</td>
                        <td><span class="badge badge-info">Ganga • Room 101</span></td>
                        <td>2026-08-01</td>
                        <td>North Indian Veg/Non-Veg</td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Edit</button></td>
                    </tr>
                    <tr>
                        <td>#1002</td>
                        <td><strong>Aditya Verma</strong></td>
                        <td><code>REG2024002</code></td>
                        <td>+919811122202</td>
                        <td><span class="badge badge-info">Ganga • Room 101</span></td>
                        <td>2026-08-01</td>
                        <td>North Indian Veg/Non-Veg</td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Edit</button></td>
                    </tr>
                    <tr>
                        <td>#1003</td>
                        <td><strong>Kavya Nair</strong></td>
                        <td><code>REG2024003</code></td>
                        <td>+919811122203</td>
                        <td><span class="badge badge-info">Yamuna • Room 201</span></td>
                        <td>2026-08-01</td>
                        <td>South Indian Pure Veg</td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Edit</button></td>
                    </tr>
                    <tr>
                        <td>#1004</td>
                        <td><strong>Ananya Iyer</strong></td>
                        <td><code>REG2024004</code></td>
                        <td>+919811122204</td>
                        <td><span class="badge badge-info">Yamuna • Room 202</span></td>
                        <td>2026-08-02</td>
                        <td>South Indian Pure Veg</td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Edit</button></td>
                    </tr>
                    <tr style="background: #fffbeb;">
                        <td>#1005</td>
                        <td><strong>Vikram Rathore</strong></td>
                        <td><code>REG2024005</code></td>
                        <td>+919811122205</td>
                        <td><span class="badge badge-pending">Unallotted</span></td>
                        <td>—</td>
                        <td>North Indian Veg/Non-Veg</td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Allot Room</button></td>
                    </tr>
                    <tr style="background: #fffbeb;">
                        <td>#1006</td>
                        <td><strong>Pooja Menon</strong></td>
                        <td><code>REG2024006</code></td>
                        <td>+919811122206</td>
                        <td><span class="badge badge-pending">Unallotted</span></td>
                        <td>—</td>
                        <td><span style="color: #94a3b8;">None</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Allot Room</button></td>
                    </tr>
                    <tr>
                        <td>#1007</td>
                        <td><strong>Siddharth Joshi</strong></td>
                        <td><code>REG2024007</code></td>
                        <td>+919811122207</td>
                        <td><span class="badge badge-info">Kaveri • Room 301</span></td>
                        <td>2026-08-05</td>
                        <td>Special Continental</td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Edit</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """)

    # 03: Rooms & Allotment
    screens["03-rooms-allotment"] = wrap_page("03-rooms-allotment", "Rooms & Capacity Management", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Room Registry & Capacity Enforcement</h2>
            <p>Room allocation registry with real-time occupancy status</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-primary">+ Allot Student to Room</button>
        </div>
    </div>

    <!-- Hostel Selector Tabs -->
    <div style="display: flex; gap: 8px; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; flex-wrap: wrap;">
        <button class="btn btn-primary" style="border-radius: 20px;">🏢 Ganga Boys Hostel (4 Rooms)</button>
        <button class="btn btn-outline" style="border-radius: 20px;">🏢 Yamuna Girls Hostel (3 Rooms)</button>
        <button class="btn btn-outline" style="border-radius: 20px;">🏢 Kaveri Boys Hostel (2 Rooms)</button>
    </div>

    <!-- Room Cards Grid -->
    <div class="stats-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 28px;">
        <!-- Room 101 (Full) -->
        <div class="card-panel" style="border-top: 4px solid #ef4444; margin-bottom: 0;">
            <div style="padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: 700; font-size: 18px;">Room 101</span>
                    <span class="badge badge-full">FULL</span>
                </div>
                <div style="font-size: 12.5px; color: #64748b; margin-bottom: 12px;">Double Sharing AC</div>
                <div class="progress-bar-bg" style="width: 100%; height: 8px; margin-bottom: 12px;">
                    <div class="progress-bar-fill fill-red" style="width: 100%;"></div>
                </div>
                <div style="font-size: 12px; color: #0f172a; margin-bottom: 14px;">
                    <strong>Occupants (2/2):</strong>
                    <div style="margin-top: 4px; color: #475569;">• Rahul Sharma (1001)</div>
                    <div style="color: #475569;">• Aditya Verma (1002)</div>
                </div>
                <button class="btn btn-outline" style="width: 100%; justify-content: center; font-size: 12px; padding: 6px;" disabled>Capacity Reached</button>
            </div>
        </div>

        <!-- Room 102 (Vacant) -->
        <div class="card-panel" style="border-top: 4px solid #10b981; margin-bottom: 0;">
            <div style="padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: 700; font-size: 18px;">Room 102</span>
                    <span class="badge badge-paid">VACANT</span>
                </div>
                <div style="font-size: 12.5px; color: #64748b; margin-bottom: 12px;">Double Sharing Non-AC</div>
                <div class="progress-bar-bg" style="width: 100%; height: 8px; margin-bottom: 12px;">
                    <div class="progress-bar-fill fill-green" style="width: 0%;"></div>
                </div>
                <div style="font-size: 12px; color: #0f172a; margin-bottom: 14px;">
                    <strong>Occupants (0/2):</strong>
                    <div style="margin-top: 4px; color: #94a3b8; font-style: italic;">No students assigned yet</div>
                    <div style="visibility: hidden;">Spacer</div>
                </div>
                <button class="btn btn-primary" style="width: 100%; justify-content: center; font-size: 12px; padding: 6px;">Allot Student</button>
            </div>
        </div>

        <!-- Room 103 (Vacant Deluxe) -->
        <div class="card-panel" style="border-top: 4px solid #10b981; margin-bottom: 0;">
            <div style="padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: 700; font-size: 18px;">Room 103</span>
                    <span class="badge badge-paid">VACANT</span>
                </div>
                <div style="font-size: 12.5px; color: #64748b; margin-bottom: 12px;">Single Deluxe</div>
                <div class="progress-bar-bg" style="width: 100%; height: 8px; margin-bottom: 12px;">
                    <div class="progress-bar-fill fill-green" style="width: 0%;"></div>
                </div>
                <div style="font-size: 12px; color: #0f172a; margin-bottom: 14px;">
                    <strong>Occupants (0/1):</strong>
                    <div style="margin-top: 4px; color: #94a3b8; font-style: italic;">Single vacancy available</div>
                    <div style="visibility: hidden;">Spacer</div>
                </div>
                <button class="btn btn-primary" style="width: 100%; justify-content: center; font-size: 12px; padding: 6px;">Allot Student</button>
            </div>
        </div>

        <!-- Room 104 (Vacant Triple) -->
        <div class="card-panel" style="border-top: 4px solid #10b981; margin-bottom: 0;">
            <div style="padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: 700; font-size: 18px;">Room 104</span>
                    <span class="badge badge-paid">VACANT</span>
                </div>
                <div style="font-size: 12.5px; color: #64748b; margin-bottom: 12px;">Triple Sharing Non-AC</div>
                <div class="progress-bar-bg" style="width: 100%; height: 8px; margin-bottom: 12px;">
                    <div class="progress-bar-fill fill-green" style="width: 0%;"></div>
                </div>
                <div style="font-size: 12px; color: #0f172a; margin-bottom: 14px;">
                    <strong>Occupants (0/3):</strong>
                    <div style="margin-top: 4px; color: #94a3b8; font-style: italic;">3 beds available</div>
                    <div style="visibility: hidden;">Spacer</div>
                </div>
                <button class="btn btn-primary" style="width: 100%; justify-content: center; font-size: 12px; padding: 6px;">Allot Student</button>
            </div>
        </div>
    </div>
    """)

    # 04: Fees & Fines
    screens["04-fees-fines"] = wrap_page("04-fees-fines", "Fee & Fine Ledger", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Student Fees & Disciplinary Fines</h2>
            <p>Fee invoice records and disciplinary fines registry</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-outline">Record Fine</button>
            <button class="btn btn-primary">+ Generate Fee Invoice</button>
        </div>
    </div>

    <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr);">
        <div class="stat-card">
            <div class="stat-label">Total Fee Billed</div>
            <div class="stat-value">₹2,40,000</div>
            <div class="stat-subtext">5 Active Invoices</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Collected Fees</div>
            <div class="stat-value" style="color: #059669;">₹95,000</div>
            <div class="stat-subtext"><span class="trend-up">2 Paid Invoices</span> (Rahul, Kavya)</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Outstanding Fees & Fines</div>
            <div class="stat-value" style="color: #dc2626;">₹1,46,300</div>
            <div class="stat-subtext"><span class="trend-warning">3 Fees + 2 Fines Pending</span></div>
        </div>
    </div>

    <!-- Fees Table -->
    <div class="card-panel" style="margin-bottom: 24px;">
        <div class="panel-header">
            <h3>Hostel Fee Records</h3>
            <span class="badge badge-info">Due Date: 2026-10-31</span>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Fee ID</th>
                        <th>Student Name</th>
                        <th>Reg No</th>
                        <th>Amount</th>
                        <th>Due Date</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#501</td>
                        <td>Rahul Sharma</td>
                        <td><code>REG2024001</code></td>
                        <td>₹45,000.00</td>
                        <td>2026-10-31</td>
                        <td><span class="badge badge-paid">PAID</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Receipt</button></td>
                    </tr>
                    <tr>
                        <td>#502</td>
                        <td>Aditya Verma</td>
                        <td><code>REG2024002</code></td>
                        <td>₹45,000.00</td>
                        <td>2026-10-31</td>
                        <td><span class="badge badge-pending">PENDING</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Mark Paid</button></td>
                    </tr>
                    <tr>
                        <td>#503</td>
                        <td>Kavya Nair</td>
                        <td><code>REG2024003</code></td>
                        <td>₹50,000.00</td>
                        <td>2026-10-31</td>
                        <td><span class="badge badge-paid">PAID</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Receipt</button></td>
                    </tr>
                    <tr>
                        <td>#504</td>
                        <td>Ananya Iyer</td>
                        <td><code>REG2024004</code></td>
                        <td>₹55,000.00</td>
                        <td>2026-10-31</td>
                        <td><span class="badge badge-pending">PENDING</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Mark Paid</button></td>
                    </tr>
                    <tr>
                        <td>#505</td>
                        <td>Siddharth Joshi</td>
                        <td><code>REG2024007</code></td>
                        <td>₹45,000.00</td>
                        <td>2026-10-31</td>
                        <td><span class="badge badge-pending">PENDING</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Mark Paid</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Fines Table -->
    <div class="card-panel">
        <div class="panel-header">
            <h3>Disciplinary Fines Registry</h3>
            <span class="badge badge-pending">Disciplinary Registry</span>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>FID</th>
                        <th>Student Name</th>
                        <th>Reason / Infraction</th>
                        <th>Fine Amount</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#701</td>
                        <td>Rahul Sharma (1001)</td>
                        <td>Late entry past 10:30 PM curfew</td>
                        <td>₹500.00</td>
                        <td><span class="badge badge-paid">PAID</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">View</button></td>
                    </tr>
                    <tr>
                        <td>#702</td>
                        <td>Aditya Verma (1002)</td>
                        <td>Unauthorized electric kettle in room</td>
                        <td>₹1,000.00</td>
                        <td><span class="badge badge-pending">PENDING</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Collect</button></td>
                    </tr>
                    <tr>
                        <td>#703</td>
                        <td>Siddharth Joshi (1007)</td>
                        <td>Noise violation during quiet hours</td>
                        <td>₹300.00</td>
                        <td><span class="badge badge-pending">PENDING</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Collect</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """)

    # 05: Mess
    screens["05-mess"] = wrap_page("05-mess", "Mess Management", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Mess Packages & Student Subscriptions</h2>
            <p>Student mess meal packages and monthly billing</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-primary">+ Add New Mess Plan</button>
        </div>
    </div>

    <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 28px;">
        <div class="card-panel" style="margin-bottom: 0;">
            <div style="padding: 24px;">
                <span class="badge badge-paid" style="margin-bottom: 12px;">Mess #1</span>
                <h3 style="font-size: 17px; font-weight: 700; margin-bottom: 8px;">North Indian Veg & Non-Veg</h3>
                <div style="font-size: 26px; font-weight: 700; color: #2563eb; margin-bottom: 12px;">₹4,500 <span style="font-size: 13px; color: #64748b; font-weight: 400;">/ month</span></div>
                <div style="font-size: 13px; color: #475569; margin-bottom: 16px;">4 Meals daily • Chicken & Paneer 3x weekly</div>
                <div style="padding-top: 14px; border-top: 1px solid #e2e8f0; font-size: 12.5px; font-weight: 600;">
                    👥 3 Students Enrolled:
                    <div style="color: #64748b; font-weight: 400; margin-top: 4px;">Rahul Sharma, Aditya Verma, Vikram Rathore</div>
                </div>
            </div>
        </div>

        <div class="card-panel" style="margin-bottom: 0;">
            <div style="padding: 24px;">
                <span class="badge badge-paid" style="margin-bottom: 12px;">Mess #2</span>
                <h3 style="font-size: 17px; font-weight: 700; margin-bottom: 8px;">South Indian Pure Veg</h3>
                <div style="font-size: 26px; font-weight: 700; color: #2563eb; margin-bottom: 12px;">₹4,000 <span style="font-size: 13px; color: #64748b; font-weight: 400;">/ month</span></div>
                <div style="font-size: 13px; color: #475569; margin-bottom: 16px;">Pure vegetarian • Traditional meals & filter coffee</div>
                <div style="padding-top: 14px; border-top: 1px solid #e2e8f0; font-size: 12.5px; font-weight: 600;">
                    👥 2 Students Enrolled:
                    <div style="color: #64748b; font-weight: 400; margin-top: 4px;">Kavya Nair, Ananya Iyer</div>
                </div>
            </div>
        </div>

        <div class="card-panel" style="margin-bottom: 0;">
            <div style="padding: 24px;">
                <span class="badge badge-paid" style="margin-bottom: 12px;">Mess #3</span>
                <h3 style="font-size: 17px; font-weight: 700; margin-bottom: 8px;">Special Dietary & Continental</h3>
                <div style="font-size: 26px; font-weight: 700; color: #2563eb; margin-bottom: 12px;">₹5,200 <span style="font-size: 13px; color: #64748b; font-weight: 400;">/ month</span></div>
                <div style="font-size: 13px; color: #475569; margin-bottom: 16px;">Custom high-protein menu • Fresh salad & fruit bar</div>
                <div style="padding-top: 14px; border-top: 1px solid #e2e8f0; font-size: 12.5px; font-weight: 600;">
                    👥 1 Student Enrolled:
                    <div style="color: #64748b; font-weight: 400; margin-top: 4px;">Siddharth Joshi</div>
                </div>
            </div>
        </div>
    </div>
    """)

    # 06: Attendance
    screens["06-attendance"] = wrap_page("06-attendance", "Daily Attendance", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Hostel Night Attendance Log</h2>
            <p>Mark daily hostel night attendance by hostel and room</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-outline">📅 Change Date</button>
            <button class="btn btn-primary">💾 Save Attendance Checklist</button>
        </div>
    </div>

    <div class="card-panel">
        <div class="filter-bar">
            <div class="filter-group">
                <label style="font-size: 13px; font-weight: 600;">Attendance Date:</label>
                <input type="date" value="2026-10-10" class="date-input" />
                <select class="select-input">
                    <option>All Allotted Students (5)</option>
                    <option>Ganga Boys Hostel (2)</option>
                    <option>Yamuna Girls Hostel (2)</option>
                    <option>Kaveri Boys Hostel (1)</option>
                </select>
            </div>
            <div style="display: flex; gap: 12px;">
                <span class="badge badge-paid">Present: 4</span>
                <span class="badge badge-absent">Absent: 1</span>
            </div>
        </div>

        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Student Name</th>
                        <th>Room</th>
                        <th>Previous Day (Oct 09)</th>
                        <th>Attendance Status (Oct 10)</th>
                        <th>Quick Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#1001</td>
                        <td><strong>Rahul Sharma</strong></td>
                        <td><span class="badge badge-info">Ganga • 101</span></td>
                        <td><span class="badge badge-paid">Present</span></td>
                        <td><span class="badge badge-paid" style="font-size: 13px; padding: 6px 14px;">✓ PRESENT</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Toggle Absent</button></td>
                    </tr>
                    <tr>
                        <td>#1002</td>
                        <td><strong>Aditya Verma</strong></td>
                        <td><span class="badge badge-info">Ganga • 101</span></td>
                        <td><span class="badge badge-absent">Absent</span></td>
                        <td><span class="badge badge-paid" style="font-size: 13px; padding: 6px 14px;">✓ PRESENT</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Toggle Absent</button></td>
                    </tr>
                    <tr>
                        <td>#1003</td>
                        <td><strong>Kavya Nair</strong></td>
                        <td><span class="badge badge-info">Yamuna • 201</span></td>
                        <td><span class="badge badge-paid">Present</span></td>
                        <td><span class="badge badge-paid" style="font-size: 13px; padding: 6px 14px;">✓ PRESENT</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Toggle Absent</button></td>
                    </tr>
                    <tr style="background: #fef2f2;">
                        <td>#1004</td>
                        <td><strong>Ananya Iyer</strong></td>
                        <td><span class="badge badge-info">Yamuna • 202</span></td>
                        <td><span class="badge badge-paid">Present</span></td>
                        <td><span class="badge badge-absent" style="font-size: 13px; padding: 6px 14px;">✕ ABSENT</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Mark Present</button></td>
                    </tr>
                    <tr>
                        <td>#1007</td>
                        <td><strong>Siddharth Joshi</strong></td>
                        <td><span class="badge badge-info">Kaveri • 301</span></td>
                        <td><span class="badge badge-paid">Present</span></td>
                        <td><span class="badge badge-paid" style="font-size: 13px; padding: 6px 14px;">✓ PRESENT</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Toggle Absent</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """)

    # 07: Visitors
    screens["07-visitors"] = wrap_page("07-visitors", "Visitor Registry & Log", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Visitor Registry & Visit Logs</h2>
            <p>Visitor entry records and check-in history</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-primary">+ Log New Visitor</button>
        </div>
    </div>

    <div class="card-panel">
        <div class="panel-header">
            <h3>Registered Visitors & Visit Records</h3>
            <span class="badge badge-info">Hostel Check-in Records</span>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Visit Date</th>
                        <th>Visitor Name</th>
                        <th>Relationship</th>
                        <th>Visitor Phone</th>
                        <th>Student Visited</th>
                        <th>Hostel & Room</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>2026-10-10</strong></td>
                        <td>Arun Verma</td>
                        <td>Brother</td>
                        <td>+919845011114</td>
                        <td>Aditya Verma (#1002)</td>
                        <td><span class="badge badge-info">Ganga • 101</span></td>
                        <td><span class="badge badge-paid">Completed</span></td>
                    </tr>
                    <tr>
                        <td><strong>2026-10-08</strong></td>
                        <td>Gopinath Nair</td>
                        <td>Father</td>
                        <td>+919845011113</td>
                        <td>Kavya Nair (#1003)</td>
                        <td><span class="badge badge-info">Yamuna • 201</span></td>
                        <td><span class="badge badge-paid">Completed</span></td>
                    </tr>
                    <tr>
                        <td><strong>2026-10-05</strong></td>
                        <td>Ramesh Sharma</td>
                        <td>Father</td>
                        <td>+919845011111</td>
                        <td>Rahul Sharma (#1001)</td>
                        <td><span class="badge badge-info">Ganga • 101</span></td>
                        <td><span class="badge badge-paid">Completed</span></td>
                    </tr>
                    <tr>
                        <td><strong>2026-10-05</strong></td>
                        <td>Sunita Sharma</td>
                        <td>Mother</td>
                        <td>+919845011112</td>
                        <td>Rahul Sharma (#1001)</td>
                        <td><span class="badge badge-info">Ganga • 101</span></td>
                        <td><span class="badge badge-paid">Completed</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """)

    # 08: Maintenance & Complaints
    screens["08-maintenance-complaints"] = wrap_page("08-maintenance-complaints", "Maintenance & Complaints", """
    <div class="page-header">
        <div class="page-title-group">
            <h2>Maintenance Requests & Student Complaints</h2>
            <p>Hostel facility repairs and student grievance tracking</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-outline">+ New Maintenance Ticket</button>
            <button class="btn btn-primary">+ Lodge Student Complaint</button>
        </div>
    </div>

    <!-- Maintenance Table -->
    <div class="card-panel" style="margin-bottom: 24px;">
        <div class="panel-header">
            <h3>Hostel & Room Maintenance Requests</h3>
            <span class="badge badge-info">Maintenance Work Orders</span>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Req ID</th>
                        <th>Hostel</th>
                        <th>Scope / Room</th>
                        <th>Issue Description</th>
                        <th>Date</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#301</td>
                        <td>Ganga Boys</td>
                        <td><span class="badge badge-info">Room 101</span></td>
                        <td>Ceiling fan speed regulator not functioning</td>
                        <td>2026-10-08</td>
                        <td><span class="badge badge-resolved">RESOLVED</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">View</button></td>
                    </tr>
                    <tr>
                        <td>#302</td>
                        <td>Ganga Boys</td>
                        <td><span class="badge badge-progress">Hostel-wide</span></td>
                        <td>Main corridor water cooler filter replacement required</td>
                        <td>2026-10-09</td>
                        <td><span class="badge badge-progress">IN PROGRESS</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Update</button></td>
                    </tr>
                    <tr>
                        <td>#303</td>
                        <td>Yamuna Girls</td>
                        <td><span class="badge badge-info">Room 201</span></td>
                        <td>Bathroom door latch loose</td>
                        <td>2026-10-09</td>
                        <td><span class="badge badge-open">OPEN</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Assign Staff</button></td>
                    </tr>
                    <tr>
                        <td>#304</td>
                        <td>Kaveri Boys</td>
                        <td><span class="badge badge-progress">Hostel-wide</span></td>
                        <td>Solar water heater pressure valve inspection</td>
                        <td>2026-10-10</td>
                        <td><span class="badge badge-open">OPEN</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Assign Staff</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Complaints Table -->
    <div class="card-panel">
        <div class="panel-header">
            <h3>Student Grievances & Complaints</h3>
            <span class="badge badge-pending">Student Grievance Log</span>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Comp ID</th>
                        <th>Filed By</th>
                        <th>Complaint Description</th>
                        <th>Date Filed</th>
                        <th>Current Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#401</td>
                        <td>Rahul Sharma (1001)</td>
                        <td>Wi-Fi access point in 1st floor wing keeps dropping connection</td>
                        <td>2026-10-07</td>
                        <td><span class="badge badge-resolved">RESOLVED</span></td>
                        <td><button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">Log Notes</button></td>
                    </tr>
                    <tr>
                        <td>#402</td>
                        <td>Kavya Nair (1003)</td>
                        <td>Hot water supply delayed in morning hours</td>
                        <td>2026-10-09</td>
                        <td><span class="badge badge-progress">IN PROGRESS</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Resolve</button></td>
                    </tr>
                    <tr>
                        <td>#403</td>
                        <td>Siddharth Joshi (1007)</td>
                        <td>Mess breakfast timing does not align with morning lab schedule</td>
                        <td>2026-10-10</td>
                        <td><span class="badge badge-open">OPEN</span></td>
                        <td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">Resolve</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """)

    # 09: Student Portal (Personal Student Self-Service View)
    screens["09-student-portal"] = wrap_student_page("09-student-portal", "Student Self-Service Portal", """
    <!-- Student Hero Profile Banner -->
    <div class="student-hero-card" id="overview">
        <div class="student-profile-left">
            <div class="student-large-avatar">RS</div>
            <div class="student-meta">
                <h2>Rahul Sharma</h2>
                <div class="student-meta-tags">
                    <span class="student-badge-pill">REG: REG2024001</span>
                    <span>•</span>
                    <span class="student-badge-pill">Student ID #1001</span>
                    <span>•</span>
                    <span>📞 +919811122201</span>
                    <span>•</span>
                    <span>B.Tech Computer Science (Year 3)</span>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <button class="btn btn-outline" style="background: rgba(255,255,255,0.08); color: white; border-color: rgba(255,255,255,0.2);">🔧 Report Room Repair</button>
            <button class="btn btn-primary">+ Lodge Grievance</button>
        </div>
    </div>

    <!-- Strict Role-Based Isolation & Safeguard Notice -->
    <div class="isolation-banner">
        <div>
            <strong>🔒 Personal Resident Space:</strong> This view is strictly filtered to your student record (<code>Student_ID: 1001</code>). Boys and Girls hostels are separated into independent buildings. Your assigned Warden is <strong>Dr. Suresh Kumar</strong> (+919876543210).
        </div>
        <span class="badge badge-active" style="background: #dcfce7; color: #15803d; border-color: #86efac;">Authorized Resident</span>
    </div>

    <!-- Student Metric Cards -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">My Allotted Bed</span>
                <div class="stat-icon-wrapper icon-blue">🛏️</div>
            </div>
            <div class="stat-value">Room 101</div>
            <div class="stat-subtext">Ganga Boys • Double Sharing AC (Bed 1 of 2)</div>
        </div>

        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Outstanding Balance</span>
                <div class="stat-icon-wrapper icon-emerald">💳</div>
            </div>
            <div class="stat-value" style="color: #059669;">₹0.00</div>
            <div class="stat-subtext"><span class="trend-up">All Dues Cleared</span> (Fee ₹45,000 Paid)</div>
        </div>

        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Active Mess Plan</span>
                <div class="stat-icon-wrapper icon-amber">🍽️</div>
            </div>
            <div class="stat-value" style="font-size: 22px;">North Indian</div>
            <div class="stat-subtext">Veg & Non-Veg • ₹4,500/month (Mess #1)</div>
        </div>

        <div class="stat-card">
            <div class="stat-card-top">
                <span class="stat-label">Night Attendance</span>
                <div class="stat-icon-wrapper icon-emerald">📅</div>
            </div>
            <div class="stat-value" style="color: #059669;">100%</div>
            <div class="stat-subtext">Oct 10: Present • Oct 09: Present</div>
        </div>
    </div>

    <!-- Two-Column Interactive Details Grid -->
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
        
        <!-- Left Column: Finances, Grievances, Attendance -->
        <div>
            <!-- Financial Ledger (Fee & Fine) -->
            <div class="card-panel" id="fees" style="margin-bottom: 24px;">
                <div class="panel-header">
                    <h3>💳 My Fees & Disciplinary Fines</h3>
                    <span class="badge badge-paid">No Pending Dues</span>
                </div>
                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Record Ref</th>
                                <th>Description / Item</th>
                                <th>Amount</th>
                                <th>Due / Incurred Date</th>
                                <th>Status</th>
                                <th>Receipt</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>FEE-501</code></td>
                                <td>Semester Hostel Rent & Mess Package</td>
                                <td>₹45,000.00</td>
                                <td>2026-10-31</td>
                                <td><span class="badge badge-paid">PAID</span></td>
                                <td><button class="btn btn-outline" style="padding: 3px 8px; font-size: 11.5px;">View Receipt</button></td>
                            </tr>
                            <tr>
                                <td><code>FINE-701</code></td>
                                <td>Disciplinary Fine: Late entry past 10:30 PM curfew</td>
                                <td>₹500.00</td>
                                <td>2026-10-06</td>
                                <td><span class="badge badge-paid">PAID</span></td>
                                <td><button class="btn btn-outline" style="padding: 3px 8px; font-size: 11.5px;">Receipt</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Grievances & Maintenance Tickets -->
            <div class="card-panel" id="grievances" style="margin-bottom: 24px;">
                <div class="panel-header">
                    <h3>🔧 My Complaints & Maintenance Requests</h3>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-outline" style="padding: 4px 10px; font-size: 12px;">+ Request Repair</button>
                        <button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;">+ New Complaint</button>
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Ticket ID</th>
                                <th>Category</th>
                                <th>Description</th>
                                <th>Date Filed</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>COMP-401</code></td>
                                <td>Student Grievance</td>
                                <td>Wi-Fi access point in 1st floor wing keeps dropping connection</td>
                                <td>2026-10-07</td>
                                <td><span class="badge badge-resolved">RESOLVED</span></td>
                            </tr>
                            <tr>
                                <td><code>REQ-301</code></td>
                                <td>Room Maintenance</td>
                                <td>Ceiling fan speed regulator not functioning in Room 101</td>
                                <td>2026-10-08</td>
                                <td><span class="badge badge-resolved">RESOLVED</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Attendance History -->
            <div class="card-panel" id="attendance">
                <div class="panel-header">
                    <h3>📅 My Night Attendance History</h3>
                    <span class="badge badge-info">Verified by Warden Dr. Suresh Kumar</span>
                </div>
                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Hostel & Room</th>
                                <th>Roll Call Session</th>
                                <th>Attendance Status</th>
                                <th>Remarks</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>2026-10-10</strong></td>
                                <td>Ganga Boys • Room 101</td>
                                <td>Night Curfew Verification (10:00 PM)</td>
                                <td><span class="badge badge-present">✓ PRESENT</span></td>
                                <td>Marked in room by Warden</td>
                            </tr>
                            <tr>
                                <td><strong>2026-10-09</strong></td>
                                <td>Ganga Boys • Room 101</td>
                                <td>Night Curfew Verification (10:00 PM)</td>
                                <td><span class="badge badge-present">✓ PRESENT</span></td>
                                <td>Marked in room by Warden</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Right Column: Roommate, Visitors, Staff Contacts -->
        <div>
            <!-- Room & Roommate Card -->
            <div class="card-panel" id="room" style="margin-bottom: 24px;">
                <div class="panel-header">
                    <h3>🛏️ Room 101 Details</h3>
                    <span class="badge badge-info">Double AC</span>
                </div>
                <div style="padding: 20px;">
                    <div style="font-size: 13px; color: #64748b; margin-bottom: 14px;">
                        Ganga Boys Hostel • 1st Floor, East Wing<br>
                        <strong>Capacity:</strong> 2 Students (Occupancy: 2/2)
                    </div>

                    <div style="font-weight: 600; font-size: 12.5px; text-transform: uppercase; color: #475569; margin-bottom: 10px; letter-spacing: 0.5px;">
                        Occupants
                    </div>

                    <!-- Bed 1: Current Student -->
                    <div class="roommate-card" style="border-left: 3px solid #2563eb;">
                        <div class="user-avatar" style="background: #2563eb; width: 34px; height: 34px; font-size: 12px;">RS</div>
                        <div>
                            <div style="font-weight: 600; font-size: 13px; color: #0f172a;">Rahul Sharma (You)</div>
                            <div style="font-size: 11.5px; color: #64748b;">Bed 1 • Allotted: Aug 01, 2026</div>
                        </div>
                    </div>

                    <!-- Bed 2: Roommate -->
                    <div class="roommate-card">
                        <div class="user-avatar" style="background: #64748b; width: 34px; height: 34px; font-size: 12px;">AV</div>
                        <div>
                            <div style="font-weight: 600; font-size: 13px; color: #0f172a;">Aditya Verma</div>
                            <div style="font-size: 11.5px; color: #64748b;">Bed 2 • REG2024002 • 📞 +919811122202</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Approved Visitors -->
            <div class="card-panel" id="visitors" style="margin-bottom: 24px;">
                <div class="panel-header">
                    <h3>👥 Approved Visitors</h3>
                    <button class="btn btn-outline" style="padding: 3px 8px; font-size: 11px;">+ Add</button>
                </div>
                <div style="padding: 16px;">
                    <div class="contact-pill-item">
                        <div>
                            <div style="font-weight: 600;">Ramesh Sharma</div>
                            <div style="font-size: 11.5px; color: #64748b;">Father • +919845011111</div>
                        </div>
                        <span class="badge badge-paid" style="font-size: 11px;">Visited Oct 05</span>
                    </div>

                    <div class="contact-pill-item">
                        <div>
                            <div style="font-weight: 600;">Sunita Sharma</div>
                            <div style="font-size: 11.5px; color: #64748b;">Mother • +919845011112</div>
                        </div>
                        <span class="badge badge-paid" style="font-size: 11px;">Visited Oct 05</span>
                    </div>
                </div>
            </div>

            <!-- Emergency & Hostel Staff Contacts -->
            <div class="card-panel">
                <div class="panel-header">
                    <h3>📞 Hostel #1 Staff Contacts</h3>
                </div>
                <div style="padding: 16px;">
                    <div class="contact-pill-item">
                        <div>
                            <div style="font-weight: 600;">Dr. Suresh Kumar</div>
                            <div style="font-size: 11.5px; color: #64748b;">Assigned Hostel Warden (Male)</div>
                        </div>
                        <a href="tel:+919876543210" style="color: #2563eb; font-weight: 600; font-size: 12px; text-decoration: none;">Call</a>
                    </div>

                    <div class="contact-pill-item">
                        <div>
                            <div style="font-weight: 600;">Head Caretaker</div>
                            <div style="font-size: 11.5px; color: #64748b;">Hostel Staff • Room Inquiries</div>
                        </div>
                        <a href="tel:+919123456780" style="color: #2563eb; font-weight: 600; font-size: 12px; text-decoration: none;">Call</a>
                    </div>

                    <div class="contact-pill-item">
                        <div>
                            <div style="font-weight: 600;">Night Security Guard</div>
                            <div style="font-size: 11.5px; color: #64748b;">Main Gate & Night Entry</div>
                        </div>
                        <a href="tel:+919123456782" style="color: #2563eb; font-weight: 600; font-size: 12px; text-decoration: none;">Call</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)

    # Write out each HTML screen
    for key, content in screens.items():
        file_path = BASE_DIR / f"{key}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated HTML: {file_path.name}")

    # Build Clean Navigation Index
    index_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Hostel Management System - Screen Directory</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body style="padding: 40px; background: #0f172a; color: white; display: flex; flex-direction: column; align-items: center;">
    <div style="max-width: 960px; width: 100%;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
            <div>
                <h1 style="font-size: 28px; margin-bottom: 4px;">Hostel Management System — UI Screens</h1>
                <p style="color: #94a3b8;">High-fidelity interactive UI design previews with role-based access & gender hostel separation.</p>
            </div>
            <a href="00-ui-kit.html" class="btn btn-outline" style="background: #1e293b; color: #cbd5e1; border-color: #334155;">🎨 View UI Kit</a>
        </div>

        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <span class="badge badge-paid" style="background: #064e3b; color: #a7f3d0; border-color: #059669; font-size: 11px; margin-bottom: 6px;">NEW: Student View</span>
                    <h2 style="font-size: 18px; margin-bottom: 4px;">🎓 Screen 09: Student Self-Service Portal</h2>
                    <p style="color: #94a3b8; font-size: 13px;">Personalized resident view displaying strictly student-specific room, fee ledger, roommate, attendance, and grievances.</p>
                </div>
                <a href="09-student-portal.html" class="btn btn-primary" style="background: #10b981; border-color: #059669;">Open Student Portal →</a>
            </div>
        </div>

        <h3 style="font-size: 14px; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px; margin-bottom: 12px;">Warden & Administrative Management Screens</h3>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
    """
    for key, label, icon in [
        ("01-dashboard", "01: Overview / Dashboard", "📊"),
        ("02-students", "02: Student Management", "🎓"),
        ("03-rooms-allotment", "03: Rooms & Room Allotment", "🛏️"),
        ("04-fees-fines", "04: Fee & Fine Ledger", "💳"),
        ("05-mess", "05: Mess Subscriptions", "🍽️"),
        ("06-attendance", "06: Student Attendance", "📅"),
        ("07-visitors", "07: Visitor Registry & Log", "👥"),
        ("08-maintenance-complaints", "08: Maintenance & Complaints", "🔧"),
    ]:
        index_html += f"""
            <a href="{key}.html" style="background: #1e293b; padding: 18px; border-radius: 10px; text-decoration: none; color: white; display: flex; align-items: center; gap: 14px; border: 1px solid #334155; transition: transform 0.15s ease;">
                <span style="font-size: 24px;">{icon}</span>
                <div>
                    <div style="font-weight: 600; font-size: 14.5px;">{label}</div>
                    <div style="font-size: 12px; color: #94a3b8;">Warden view →</div>
                </div>
            </a>
        """
    index_html += """
        </div>
    </div>
</body>
</html>"""

    with open(BASE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Generated Navigation Hub: index.html")

def export_screenshots():
    screen_keys = [
        "00-ui-kit",
        "01-dashboard",
        "02-students",
        "03-rooms-allotment",
        "04-fees-fines",
        "05-mess",
        "06-attendance",
        "07-visitors",
        "08-maintenance-complaints",
        "09-student-portal"
    ]

    for key in screen_keys:
        html_file = BASE_DIR / f"{key}.html"
        out_png = DESIGN_DIR / f"{key}.png"
        file_url = html_file.as_uri()

        cmd = [
            EDGE_EXE,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1440,900",
            f"--screenshot={out_png}",
            file_url
        ]
        print(f"Exporting {key}.png via Headless Edge...")
        subprocess.run(cmd, check=True)
        print(f"Exported: {out_png}")

if __name__ == "__main__":
    generate_screens()
    export_screenshots()
    print("ALL 10 SCREENS GENERATED AND EXPORTED SUCCESSFULLY.")
