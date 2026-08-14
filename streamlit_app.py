import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nova HR | Enterprise Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# HIDE STREAMLIT CHROME FOR 100% PIXEL-PERFECT REACT CANVAS
# ---------------------------------------------------------
st.markdown("""
    <style>
    #MainMenu, header, footer {
        visibility: hidden !important;
        height: 0px !important;
    }
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    iframe {
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SELF-CONTAINED REACT/TAILWIND SPA (EXACT MATCH WITH NEXT.JS)
# ---------------------------------------------------------
REACT_SPA_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nova HR | Enterprise Management System</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
          }
        }
      }
    }
  </script>

  <!-- React 18 & Babel -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    body {
      background-color: #F8FAFC;
      color: #0F172A;
      font-family: 'Plus Jakarta Sans', sans-serif;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }
    
    /* Razorpay / Nova Metric Tab Active Indicator */
    .rz-metric-card {
      position: relative;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 14px;
      transition: all 0.2s ease-in-out;
    }
    .rz-metric-card:hover {
      border-color: #CBD5E1;
      box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
    }
    .rz-metric-card.active {
      border-color: #3B82F6;
      box-shadow: 0 4px 20px -4px rgba(59, 130, 246, 0.15);
    }
    .rz-metric-card.active::before {
      content: "";
      position: absolute;
      top: -1px;
      left: -1px;
      right: -1px;
      height: 3px;
      background: #2563EB;
      border-top-left-radius: 14px;
      border-top-right-radius: 14px;
    }

    /* Single-Line Top Nav Tabs */
    .rz-nav-tab {
      position: relative;
      padding: 0.55rem 0.85rem;
      font-weight: 600;
      color: #475569;
      transition: color 0.15s ease;
      display: flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.82rem;
      white-space: nowrap;
      cursor: pointer;
    }
    .rz-nav-tab:hover {
      color: #0F172A;
    }
    .rz-nav-tab.active {
      color: #1E40AF;
      font-weight: 700;
      background-color: #FFFFFF;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.02);
    }
    .rz-nav-tab.active::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: #2563EB;
    }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useMemo } = React;

    const API_URL = "http://127.0.0.1:8000";

    const DEFAULT_EMPLOYEES = [
      { employee_id: "EMP001", first_name: "Aarav", last_name: "Sharma", email: "aarav.sharma@company.com", phone: "+91 9876543210", department: "Engineering", designation: "Principal Architect", salary: 125000, joining_date: "2023-01-15", status: "Active" },
      { employee_id: "EMP002", first_name: "Priya", last_name: "Patel", email: "priya.patel@company.com", phone: "+91 9876543211", department: "AI Research", designation: "Lead Data Scientist", salary: 110000, joining_date: "2023-03-20", status: "Active" },
      { employee_id: "EMP003", first_name: "Rohan", last_name: "Mehta", email: "rohan.mehta@company.com", phone: "+91 9876543212", department: "Product", designation: "Senior Product Manager", salary: 95000, joining_date: "2023-06-10", status: "Active" },
      { employee_id: "EMP004", first_name: "Neha", last_name: "Gupta", email: "neha.gupta@company.com", phone: "+91 9876543213", department: "HR & People", designation: "HR Director", salary: 90000, joining_date: "2022-11-01", status: "Active" },
      { employee_id: "EMP005", first_name: "Vikram", last_name: "Singh", email: "vikram.singh@company.com", phone: "+91 9876543214", department: "Engineering", designation: "DevOps Specialist", salary: 85000, joining_date: "2024-01-08", status: "Inactive" },
      { employee_id: "EMP006", first_name: "Ananya", last_name: "Rao", email: "ananya.rao@company.com", phone: "+91 9876543215", department: "Finance", designation: "Senior Payroll Analyst", salary: 88000, joining_date: "2023-08-14", status: "Active" }
    ];

    function App() {
      const [activeNavTab, setActiveNavTab] = useState("overview");
      const [activeMetricTab, setActiveMetricTab] = useState("workforce");
      const [timeframe, setTimeframe] = useState("This month");
      const [employees, setEmployees] = useState(DEFAULT_EMPLOYEES);
      const [apiOnline, setApiOnline] = useState(false);
      const [loading, setLoading] = useState(false);

      const [searchQuery, setSearchQuery] = useState("");
      const [selectedDept, setSelectedDept] = useState("All");
      const [selectedStatus, setSelectedStatus] = useState("All");

      const [profileSearchId, setProfileSearchId] = useState("EMP001");
      const [selectedProfileEmp, setSelectedProfileEmp] = useState(DEFAULT_EMPLOYEES[0]);

      const [inspectEmployee, setInspectEmployee] = useState(null);
      const [editEmployee, setEditEmployee] = useState(null);
      const [hikeEmployee, setHikeEmployee] = useState(null);
      const [hikePercentage, setHikePercentage] = useState(10);
      const [deleteId, setDeleteId] = useState(null);
      const [showAddModal, setShowAddModal] = useState(false);
      const [deleteNavSelectedId, setDeleteNavSelectedId] = useState("EMP001");
      const [toastMsg, setToastMsg] = useState(null);

      const [addForm, setAddForm] = useState({
        employee_id: "", first_name: "", last_name: "", email: "", phone: "",
        department: "Engineering", designation: "Software Engineer", salary: 80000,
        joining_date: new Date().toISOString().split("T")[0], status: "Active"
      });

      const showToast = (text, type = "success") => {
        setToastMsg({ text, type });
        setTimeout(() => setToastMsg(null), 4000);
      };

      const loadData = async () => {
        try {
          const res = await fetch(`${API_URL}/employees`);
          if (res.ok) {
            const data = await res.json();
            setEmployees(data);
            setApiOnline(true);
          } else {
            setApiOnline(false);
          }
        } catch {
          setApiOnline(false);
        }
      };

      useEffect(() => { loadData(); }, []);

      const totalEmployees = employees.length;
      const activeEmployees = employees.filter(e => e.status === "Active").length;
      const totalPayroll = employees.reduce((acc, e) => acc + e.salary, 0);
      const avgSalary = totalEmployees > 0 ? totalPayroll / totalEmployees : 0;

      const departments = useMemo(() => {
        const list = Array.from(new Set(employees.map(e => e.department).filter(Boolean)));
        return ["All", ...list];
      }, [employees]);

      const filteredEmployees = useMemo(() => {
        return employees.filter(emp => {
          const text = `${emp.employee_id} ${emp.first_name} ${emp.last_name} ${emp.email} ${emp.department} ${emp.designation}`.toLowerCase();
          const matchSearch = text.includes(searchQuery.toLowerCase());
          const matchDept = selectedDept === "All" || emp.department === selectedDept;
          const matchStatus = selectedStatus === "All" || emp.status.toLowerCase() === selectedStatus.toLowerCase();
          return matchSearch && matchDept && matchStatus;
        });
      }, [employees, searchQuery, selectedDept, selectedStatus]);

      useEffect(() => {
        const target = employees.find(e => e.employee_id.toLowerCase() === profileSearchId.toLowerCase() || `${e.first_name} ${e.last_name}`.toLowerCase().includes(profileSearchId.toLowerCase()));
        if (target) setSelectedProfileEmp(target);
      }, [profileSearchId, employees]);

      const handleToggleStatus = async (emp) => {
        const newStatus = emp.status === "Active" ? "Inactive" : "Active";
        const updated = { ...emp, status: newStatus };
        if (apiOnline) {
          try {
            await fetch(`${API_URL}/employees/${emp.employee_id}`, {
              method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(updated)
            });
          } catch {}
        }
        setEmployees(employees.map(e => e.employee_id === emp.employee_id ? updated : e));
        showToast(`Status changed to ${newStatus} for ${emp.first_name}!`);
      };

      const handleAddEmployee = async (e) => {
        e.preventDefault();
        if (!addForm.employee_id || !addForm.first_name || !addForm.last_name || !addForm.email) {
          showToast("Please fill in mandatory fields.", "error"); return;
        }
        if (apiOnline) {
          try {
            await fetch(`${API_URL}/employees`, {
              method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(addForm)
            });
          } catch {}
        }
        setEmployees([...employees, { ...addForm }]);
        showToast(`Employee ${addForm.first_name} ${addForm.last_name} registered successfully!`);
        setShowAddModal(false);
      };

      const handleApplyHike = () => {
        if (!hikeEmployee) return;
        const newSal = Math.round(hikeEmployee.salary * (1 + hikePercentage / 100));
        setEmployees(employees.map(e => e.employee_id === hikeEmployee.employee_id ? { ...e, salary: newSal } : e));
        showToast(`Applied ${hikePercentage}% salary hike for ${hikeEmployee.first_name}!`);
        setHikeEmployee(null);
      };

      const handleDeleteEmployee = () => {
        if (!deleteId) return;
        setEmployees(employees.filter(e => e.employee_id !== deleteId));
        showToast(`Employee ${deleteId} deleted.`);
        setDeleteId(null);
      };

      const handleExportCSV = () => {
        const headers = ["Employee ID","First Name","Last Name","Email","Phone","Department","Designation","Salary","Joining Date","Status"];
        const csvRows = [headers.join(","), ...employees.map(e => [e.employee_id, `"${e.first_name}"`, `"${e.last_name}"`, `"${e.email}"`, `"${e.phone}"`, `"${e.department}"`, `"${e.designation}"`, e.salary, e.joining_date, e.status].join(","))];
        const blob = new Blob([csvRows.join("\n")], { type: "text/csv" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a"); a.href = url; a.download = "Nova_HR_Export.csv"; a.click();
        showToast("Exported CSV successfully!");
      };

      return (
        <div className="min-h-screen bg-[#F8FAFC] flex flex-col font-sans">
          {/* TOP HEADER BAR */}
          <header className="bg-[#FFFFFF] border-b border-[#E2E8F0] sticky top-0 z-40 shadow-xs">
            <div className="max-w-[1440px] mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
              <div className="flex items-center gap-6">
                <div onClick={() => setActiveNavTab("overview")} className="flex items-center gap-2.5 cursor-pointer">
                  <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#0F62FE] to-[#2563EB] flex items-center justify-center text-white font-extrabold shadow-md">
                    🏢
                  </div>
                  <div className="flex flex-col">
                    <span className="font-extrabold text-lg tracking-tight text-[#0F172A] leading-tight">
                      Nova <span className="text-[#2563EB]">HR</span>
                    </span>
                    <span className="text-[10px] uppercase tracking-wider font-semibold text-[#64748B]">
                      Enterprise Management System
                    </span>
                  </div>
                </div>

                <nav className="hidden lg:flex items-center gap-0.5 ml-2 border-l border-[#E2E8F0] pl-4">
                  <button onClick={() => setActiveNavTab("overview")} className={`rz-nav-tab ${activeNavTab === "overview" ? "active" : ""}`}>📊 Overview</button>
                  <button onClick={() => setActiveNavTab("directory")} className={`rz-nav-tab ${activeNavTab === "directory" ? "active" : ""}`}>👥 Directory</button>
                  <button onClick={() => setActiveNavTab("search")} className={`rz-nav-tab ${activeNavTab === "search" ? "active" : ""}`}>🔍 Search</button>
                  <button onClick={() => setActiveNavTab("add")} className={`rz-nav-tab ${activeNavTab === "add" ? "active" : ""}`}>➕ Add</button>
                  <button onClick={() => setActiveNavTab("delete")} className={`rz-nav-tab ${activeNavTab === "delete" ? "active text-rose-600 font-bold" : ""}`}>🗑️ Delete</button>
                  <button onClick={() => setActiveNavTab("analytics")} className={`rz-nav-tab ${activeNavTab === "analytics" ? "active" : ""}`}>📈 Payroll</button>
                  <button onClick={() => setActiveNavTab("system")} className={`rz-nav-tab ${activeNavTab === "system" ? "active" : ""}`}>🛡️ System</button>
                </nav>
              </div>

              <div className="flex items-center gap-3">
                <div className={`hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${apiOnline ? "bg-emerald-50 text-emerald-700 border-emerald-200" : "bg-blue-50 text-blue-700 border-blue-200"}`}>
                  <span className={`w-2 h-2 rounded-full ${apiOnline ? "bg-emerald-500" : "bg-blue-500"}`} />
                  {apiOnline ? "FastAPI Live" : "Local Mode"}
                </div>
                <div className="flex items-center gap-2 pl-2 border-l border-[#E2E8F0]">
                  <div className="w-8 h-8 rounded-full bg-[#1E293B] text-white flex items-center justify-center font-extrabold text-xs">RM</div>
                  <div className="hidden xl:flex flex-col">
                    <span className="text-xs font-bold text-[#0F172A]">Rajesh Mani</span>
                    <span className="text-[10px] font-semibold text-[#64748B]">HR Director</span>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* MAIN CONTAINER */}
          <main className="flex-1 max-w-[1440px] w-full mx-auto px-4 sm:px-6 py-6 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-2xl font-extrabold text-[#0F172A] tracking-tight">Workforce Overview</h1>
                <p className="text-xs text-[#64748B] font-medium mt-0.5">Enterprise employee statistics, compensation metrics & headcount analytics.</p>
              </div>
              <div className="flex items-center gap-3">
                <select value={timeframe} onChange={e => setTimeframe(e.target.value)} className="bg-white border border-[#CBD5E1] text-xs font-semibold py-2 px-3 rounded-lg">
                  <option>This week</option><option>This month</option><option>Q3 FY2024</option><option>All Time</option>
                </select>
                <button onClick={handleExportCSV} className="bg-white hover:bg-slate-50 border border-[#CBD5E1] text-[#0F172A] px-3 py-2 rounded-lg text-xs font-semibold">📥 Export CSV</button>
                <button onClick={() => { setActiveNavTab("add"); setShowAddModal(true); }} className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-3.5 py-2 rounded-lg text-xs font-bold shadow-md">➕ Add Employee</button>
              </div>
            </div>

            {/* TAB 1: OVERVIEW */}
            {(activeNavTab === "overview" || activeNavTab === "directory") && (
              <>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div onClick={() => setActiveMetricTab("workforce")} className={`rz-metric-card p-5 cursor-pointer ${activeMetricTab === "workforce" ? "active" : ""}`}>
                    <div className="flex justify-between text-xs font-bold text-[#64748B] uppercase">TOTAL WORKFORCE <span>👥</span></div>
                    <div className="text-2xl font-extrabold text-[#0F172A] mt-2">{totalEmployees.toLocaleString()} <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded">▲ +14%</span></div>
                    <p className="text-[11px] text-[#64748B] mt-1.5 font-medium"><span className="font-bold text-[#0F172A]">+28 employees</span> vs last month</p>
                  </div>
                  <div onClick={() => setActiveMetricTab("active")} className={`rz-metric-card p-5 cursor-pointer ${activeMetricTab === "active" ? "active" : ""}`}>
                    <div className="flex justify-between text-xs font-bold text-[#64748B] uppercase">ACTIVE HEADCOUNT <span>✅</span></div>
                    <div className="text-2xl font-extrabold text-[#0F172A] mt-2">{activeEmployees.toLocaleString()} <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded">▲ +2.4%</span></div>
                    <p className="text-[11px] text-[#64748B] mt-1.5 font-medium"><span className="font-bold text-emerald-700">94.2%</span> retention rate</p>
                  </div>
                  <div onClick={() => setActiveMetricTab("payroll")} className={`rz-metric-card p-5 cursor-pointer ${activeMetricTab === "payroll" ? "active" : ""}`}>
                    <div className="flex justify-between text-xs font-bold text-[#64748B] uppercase">MONTHLY PAYROLL <span>💵</span></div>
                    <div className="text-2xl font-extrabold text-[#0F172A] mt-2">${(totalPayroll/12).toLocaleString("en-US", {maximumFractionDigits:0})} <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded">▲ +5.8%</span></div>
                    <p className="text-[11px] text-[#64748B] mt-1.5 font-medium"><span className="font-bold text-[#0F172A]">Within 2.5%</span> of target</p>
                  </div>
                  <div onClick={() => setActiveMetricTab("avg_salary")} className={`rz-metric-card p-5 cursor-pointer ${activeMetricTab === "avg_salary" ? "active" : ""}`}>
                    <div className="flex justify-between text-xs font-bold text-[#64748B] uppercase">AVG COMPENSATION <span>💼</span></div>
                    <div className="text-2xl font-extrabold text-[#0F172A] mt-2">${Math.round(avgSalary).toLocaleString()} <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded">▲ +3.1%</span></div>
                    <p className="text-[11px] text-[#64748B] mt-1.5 font-medium">Competitive market median</p>
                  </div>
                </div>

                {/* SVG WAVE GRAPH */}
                <div className="bg-[#FFFFFF] border border-[#E2E8F0] rounded-2xl p-6 shadow-xs relative">
                  <div className="flex justify-between items-center mb-4">
                    <div>
                      <h2 className="text-base font-extrabold text-[#0F172A]">Workforce Growth & Payroll Trends</h2>
                      <p className="text-xs text-[#64748B] font-medium">Comparing current timeline headcount against benchmark metrics.</p>
                    </div>
                    <div className="flex gap-4 text-xs font-bold"><span className="text-[#2563EB]">● This Period</span><span className="text-[#94A3B8]">● Last Period</span></div>
                  </div>
                  <div className="relative w-full h-56">
                    <svg viewBox="0 0 1000 200" className="w-full h-full" preserveAspectRatio="none">
                      <defs>
                        <linearGradient id="blueG" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.35" />
                          <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.0" />
                        </linearGradient>
                      </defs>
                      <line x1="0" y1="50" x2="1000" y2="50" stroke="#F1F5F9" strokeWidth="1" />
                      <line x1="0" y1="100" x2="1000" y2="100" stroke="#F1F5F9" strokeWidth="1" />
                      <line x1="0" y1="150" x2="1000" y2="150" stroke="#F1F5F9" strokeWidth="1" />
                      <path d="M 0 150 C 150 130, 300 80, 450 110 C 600 140, 750 40, 1000 70 L 1000 200 L 0 200 Z" fill="url(#blueG)" />
                      <path d="M 0 150 C 150 130, 300 80, 450 110 C 600 140, 750 40, 1000 70" fill="none" stroke="#2563EB" strokeWidth="3.5" />
                      <line x1="450" y1="0" x2="450" y2="200" stroke="#3B82F6" strokeWidth="1" strokeDasharray="2 2"/>
                      <circle cx="450" cy="110" r="5" fill="#2563EB" stroke="#FFFFFF" strokeWidth="2.5"/>
                    </svg>
                    <div className="absolute top-4 left-[42%] bg-[#1E293B] text-white p-2.5 rounded-xl border border-slate-700 text-xs w-44">
                      <div className="font-bold border-b border-slate-700 pb-1 flex justify-between"><span>Headcount</span><span className="text-emerald-400 font-extrabold">+14%</span></div>
                      <div className="mt-1 text-[11px] flex justify-between"><span className="text-slate-400">This period:</span><span className="font-bold">{totalEmployees}</span></div>
                    </div>
                  </div>
                </div>
              </>
            )}

            {/* TAB 2: DIRECTORY */}
            {(activeNavTab === "overview" || activeNavTab === "directory") && (
              <div className="bg-[#FFFFFF] border border-[#E2E8F0] rounded-2xl p-6 shadow-xs space-y-4">
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-lg font-extrabold text-[#0F172A]">Workforce Directory & Records</h2>
                    <p className="text-xs text-[#64748B]">Showing {filteredEmployees.length} of {employees.length} employee records.</p>
                  </div>
                  <div className="flex gap-2">
                    <input type="text" placeholder="Search keyword..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} className="px-3 py-1.5 border border-[#CBD5E1] rounded-lg text-xs font-semibold" />
                    <select value={selectedDept} onChange={e => setSelectedDept(e.target.value)} className="px-3 py-1.5 border border-[#CBD5E1] rounded-lg text-xs font-bold bg-white">
                      {departments.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                    <select value={selectedStatus} onChange={e => setSelectedStatus(e.target.value)} className="px-3 py-1.5 border border-[#CBD5E1] rounded-lg text-xs font-bold bg-white">
                      <option value="All">All Statuses</option><option value="Active">Active Only</option><option value="Inactive">Inactive Only</option>
                    </select>
                  </div>
                </div>

                <div className="overflow-x-auto border border-[#E2E8F0] rounded-xl">
                  <table className="w-full text-left text-xs text-[#0F172A]">
                    <thead className="bg-[#F8FAFC] text-[#64748B] font-bold uppercase text-[11px] border-b border-[#E2E8F0]">
                      <tr>
                        <th className="p-3.5">Employee</th><th className="p-3.5">ID</th><th className="p-3.5">Department</th><th className="p-3.5">Designation</th><th className="p-3.5">Annual Salary</th><th className="p-3.5">Status</th><th className="p-3.5 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E2E8F0] font-medium">
                      {filteredEmployees.map(emp => (
                        <tr key={emp.employee_id} className="hover:bg-[#F8FAFC]">
                          <td className="p-3.5 flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#3B82F6] to-[#6366F1] text-white font-bold flex items-center justify-center text-xs">{emp.first_name[0]}{emp.last_name[0]}</div>
                            <div><div className="font-bold">{emp.first_name} {emp.last_name}</div><div className="text-[11px] text-[#64748B]">{emp.email}</div></div>
                          </td>
                          <td className="p-3.5 font-mono font-bold text-[#475569]">{emp.employee_id}</td>
                          <td className="p-3.5"><span className="bg-[#EFF6FF] text-[#1E40AF] border border-[#BFDBFE] font-bold text-[11px] px-2 py-0.5 rounded">{emp.department}</span></td>
                          <td className="p-3.5 font-semibold text-[#334155]">{emp.designation}</td>
                          <td className="p-3.5 font-extrabold">${emp.salary.toLocaleString()}</td>
                          <td className="p-3.5">
                            <span onClick={() => handleToggleStatus(emp)} className={`cursor-pointer px-2.5 py-1 rounded-full text-[11px] font-bold border ${emp.status === "Active" ? "bg-emerald-50 text-emerald-700 border-emerald-200" : "bg-rose-50 text-rose-700 border-rose-200"}`}>
                              {emp.status}
                            </span>
                          </td>
                          <td className="p-3.5 text-right">
                            <div className="flex justify-end gap-1.5">
                              <button onClick={() => setInspectEmployee(emp)} className="px-2 py-1 bg-[#EFF6FF] text-[#2563EB] font-bold rounded-md text-[11px]">Inspect</button>
                              <button onClick={() => setHikeEmployee(emp)} className="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold rounded-md text-[11px]">Hike</button>
                              <button onClick={() => setEditEmployee(emp)} className="px-2 py-1 bg-indigo-50 text-indigo-700 font-bold rounded-md text-[11px]">Edit</button>
                              <button onClick={() => setDeleteId(emp.employee_id)} className="px-2 py-1 bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-700 font-extrabold border border-rose-200 rounded-md text-[11px]">Delete</button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* TAB 3: SEARCH & PROFILE CARDS */}
            {activeNavTab === "search" && selectedProfileEmp && (
              <div className="bg-[#FFFFFF] border border-[#E2E8F0] rounded-2xl p-6 shadow-xs space-y-4">
                <h2 className="text-lg font-extrabold text-[#0F172A]">🔍 Employee Profile Search</h2>
                <input type="text" placeholder="Enter Employee ID..." value={profileSearchId} onChange={e => setProfileSearchId(e.target.value)} className="w-full max-w-md px-3.5 py-2 border border-[#CBD5E1] rounded-xl text-xs font-bold" />
                
                <div className="mt-4 border border-[#E2E8F0] rounded-2xl p-6 bg-white flex flex-col md:flex-row justify-between items-center gap-6">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-[#2563EB] to-[#4F46E5] text-white text-xl font-extrabold flex items-center justify-center">{selectedProfileEmp.first_name[0]}{selectedProfileEmp.last_name[0]}</div>
                    <div>
                      <h3 className="text-xl font-extrabold text-[#0F172A]">{selectedProfileEmp.first_name} {selectedProfileEmp.last_name}</h3>
                      <p className="text-xs font-bold text-[#2563EB]">{selectedProfileEmp.designation} • {selectedProfileEmp.department}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <button onClick={() => handleToggleStatus(selectedProfileEmp)} className="px-3 py-2 bg-emerald-50 text-emerald-700 font-bold border border-emerald-200 rounded-xl text-xs">Status: {selectedProfileEmp.status}</button>
                    <button onClick={() => setHikeEmployee(selectedProfileEmp)} className="px-3.5 py-2 bg-[#2563EB] text-white font-bold rounded-xl text-xs">Salary Hike</button>
                    <button onClick={() => setDeleteId(selectedProfileEmp.employee_id)} className="px-3.5 py-2 bg-rose-600 text-white font-extrabold rounded-xl text-xs">Delete</button>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 4: DELETE DANGER ZONE */}
            {activeNavTab === "delete" && (
              <div className="max-w-xl mx-auto bg-white border border-rose-200 rounded-2xl p-6 shadow-sm space-y-4">
                <h2 className="text-lg font-extrabold text-[#0F172A] flex items-center gap-2">⚠️ Danger Zone: Delete Employee Record</h2>
                <select value={deleteNavSelectedId} onChange={e => setDeleteNavSelectedId(e.target.value)} className="w-full p-2.5 border border-[#CBD5E1] rounded-xl text-xs font-bold">
                  {employees.map(e => <option key={e.employee_id} value={e.employee_id}>{e.employee_id} — {e.first_name} {e.last_name} ({e.department})</option>)}
                </select>
                <button onClick={() => setDeleteId(deleteNavSelectedId)} className="w-full py-2.5 bg-rose-600 text-white font-extrabold text-xs rounded-xl shadow-md">💥 Confirm Permanent Deletion</button>
              </div>
            )}

            {/* TOAST NOTIFICATION */}
            {toastMsg && (
              <div className="fixed bottom-6 right-6 bg-[#0F172A] text-white text-xs font-bold px-4 py-3 rounded-xl shadow-2xl border border-slate-700 flex items-center gap-2">
                <span>✅ {toastMsg.text}</span>
              </div>
            )}
          </main>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
"""

# Render full-width pixel-perfect SPA frontend
components.html(REACT_SPA_HTML, height=1150, scrolling=True)
