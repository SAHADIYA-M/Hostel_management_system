export const hostels = [
  {
    Hostel_ID: 1,
    Name: "Ganga Boys Hostel",
    Address: "Campus North, Sector 2",
    Type: "Boys",
  },
  {
    Hostel_ID: 2,
    Name: "Yamuna Girls Hostel",
    Address: "Campus South, Sector 1",
    Type: "Girls",
  },
];

export const wardens = [
  {
    Warden_ID: 1,
    Name: "Dr. K. Radhakrishnan",
    Phone: "9876543210",
    Hostel_ID: 1,
  },
];

export const staff = [
  { Staff_ID: 1, Role: "Caretaker", Phone: "9123456780", Hostel_ID: 1 },
  { Staff_ID: 2, Role: "Electrician", Phone: "9123456781", Hostel_ID: 1 },
];

export const rooms = [
  {
    Hostel_ID: 1,
    Room_No: 101,
    Type: "Double AC",
    Capacity: 2,
    Current_Occupants: 1,
  },
  {
    Hostel_ID: 1,
    Room_No: 102,
    Type: "Triple Non-AC",
    Capacity: 3,
    Current_Occupants: 3,
  },
  {
    Hostel_ID: 2,
    Room_No: 201,
    Type: "Double AC",
    Capacity: 2,
    Current_Occupants: 0,
  },
];

export const students = [
  {
    Student_ID: 1001,
    FName: "Ashwin",
    LName: "K.",
    Reg_No: "REG2024001",
    Phone: "+919811122201",
    Hostel_ID: 1,
    Room_No: 101,
    Allot_Date: "2026-08-01",
    Mess_ID: 1,
  },
  {
    Student_ID: 1002,
    FName: "Rahul",
    LName: "Nair",
    Reg_No: "REG2024002",
    Phone: "+919811122202",
    Hostel_ID: 1,
    Room_No: 101,
    Allot_Date: "2026-08-01",
    Mess_ID: 1,
  },
  {
    Student_ID: 1007,
    FName: "Ananya",
    LName: "M.",
    Reg_No: "REG2024007",
    Phone: "+919811122207",
    Hostel_ID: 2,
    Room_No: 201,
    Allot_Date: "2026-08-01",
    Mess_ID: 2,
  },
];

export const fees = [
  {
    Fee_ID: 501,
    Due_Date: "2026-10-31",
    Amount: 45000,
    Status: "Pending",
    Student_ID: 1001,
  },
  {
    Fee_ID: 502,
    Due_Date: "2026-10-15",
    Amount: 45000,
    Status: "Paid",
    Student_ID: 1002,
  },
];

export const fines = [
  {
    FID: 701,
    Reason: "Late entry past hostel curfew",
    Amount: 500,
    Status: "Paid",
    Student_ID: 1001,
  },
];

export const messPlans = [
  { Mess_ID: 1, Type: "Kerala Non-Veg & Veg Meals", Cost: 4500 },
  { Mess_ID: 2, Type: "Traditional Kerala Pure Veg", Cost: 4000 },
];

export const attendance = [
  {
    Student_ID: 1001,
    Student_Name: "Ashwin K.",
    Room_No: 101,
    Date: "2026-10-11",
    Status: "Present",
  },
  {
    Student_ID: 1002,
    Student_Name: "Rahul Nair",
    Room_No: 101,
    Date: "2026-10-11",
    Status: "Present",
  },
];

export const visitors = [
  {
    Visitor_ID: 201,
    Name: "K. Radhakrishnan",
    Relation: "Father",
    Phone: "9845123456",
  },
];

export const visits = [
  {
    Student_ID: 1001,
    Student_Name: "Ashwin K.",
    Visitor_ID: 201,
    Visitor_Name: "K. Radhakrishnan",
    Relation: "Father",
    Visit_Date: "2026-10-10",
  },
];

export const maintenanceRequests = [
  {
    Request_ID: 301,
    Hostel_ID: 1,
    Room_No: 101,
    Description: "Ceiling fan speed regulator faulty",
    Date: "2026-10-09",
    Status: "In Progress",
  },
  {
    Request_ID: 302,
    Hostel_ID: 2,
    Room_No: null,
    Description: "Common area lighting issue",
    Date: "2026-10-10",
    Status: "Open",
  },
];

export const complaints = [
  {
    Complaint_ID: 401,
    Date: "2026-10-08",
    Description: "Wi-Fi access point in 2nd floor hallway disconnected",
    Status: "Open",
    Student_ID: 1001,
  },
];