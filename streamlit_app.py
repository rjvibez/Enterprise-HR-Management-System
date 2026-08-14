import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION - MUST BE FIRST STREAMLIT CALL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nova HR Enterprise Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import os
import sys
import datetime
import re
import requests
import pandas as pd

# Safe import of Plotly with Streamlit native chart fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Safe import of local services
try:
    from services.employee_service import EmployeeService
    from models.employee import Employee
    SERVICE_LOADED = True
except Exception as e:
    SERVICE_LOADED = False
    SERVICE_ERROR = str(e)

# ---------------------------------------------------------
# EXECUTIVE CSS DESIGN SYSTEM (NOVA HR / RAZORPAY THEME)
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

    /* Global Body & Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }

    #MainMenu, header, footer {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* Container Spacing */
    .main .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 96% !important;
    }

    /* Sidebar Hiding for Clean Header Layout */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Nova Header Bar */
    .nova-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 0.9rem 1.6rem;
        margin-bottom: 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
    }
    .nova-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .nova-brand-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0F62FE, #2563EB);
        color: white;
        font-weight: 800;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
    }
    .nova-brand-title {
        font-weight: 800;
        font-size: 1.2rem;
        color: #0F172A;
        line-height: 1.1;
        letter-spacing: -0.4px;
    }
    .nova-brand-sub {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Top User Badge & Status */
    .nova-[#2563EB]-pill {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .nova-profile-badge {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        border-left: 1px solid #E2E8F0;
        padding-left: 1rem;
    }
    .nova-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #1E293B;
        color: white;
        font-weight: 800;
        font-size: 0.78rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    /* Linked Tabbed Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.25rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04);
        transition: all 0.2s ease-in-out;
        position: relative;
    }
    .metric-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 16px -2px rgba(59, 130, 246, 0.12);
    }
    .metric-card.active-card::before {
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
    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .metric-title {
        font-size: 0.76rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 0.4rem;
        letter-spacing: -0.7px;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .text-emerald { color: #059669; }
    .text-indigo { color: #2563EB; }
    .text-amber { color: #D97706; }
    .text-rose { color: #E11D48; }

    /* Content Cards */
    .content-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.75rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }

    /* Badges */
    .status-badge-active {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.76rem;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .status-badge-inactive {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.76rem;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .dept-badge {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 0.25rem 0.7rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.78rem;
        display: inline-block;
    }

    /* Forms */
    div[data-testid="stForm"] {
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.75rem;
        background-color: #FFFFFF;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }

    /* Horizontal Radio Tabs Styling */
    div[role="radiogroup"] {
        display: flex;
        flex-wrap: nowrap;
        gap: 0.3rem !important;
        background: #FFFFFF;
        padding: 0.4rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        overflow-x: auto;
    }
    div[role="radiogroup"] label {
        background: transparent !important;
        border: none !important;
        padding: 0.45rem 0.85rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        color: #475569 !important;
        white-space: nowrap !important;
        cursor: pointer !important;
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background: #EFF6FF !important;
        color: #1E40AF !important;
        font-weight: 700 !important;
        border: 1px solid #BFDBFE !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BACKEND API & DATA SERVICE INITIALIZATION
# ---------------------------------------------------------
DEFAULT_API_URL = "http://127.0.0.1:8000"

@st.cache_resource
def get_local_service():
    if SERVICE_LOADED:
        try:
            return EmployeeService()
        except Exception:
            return None
    return None

local_service = get_local_service()

def is_api_online(url=DEFAULT_API_URL):
    try:
        r = requests.get(f"{url}/", timeout=1.2)
        return r.status_code == 200
    except Exception:
        return False

api_active = is_api_online()

def fetch_all():
    if api_active:
        try:
            r = requests.get(f"{DEFAULT_API_URL}/employees")
            if r.status_code == 200:
                return [Employee.from_dict(d) for d in r.json()]
        except Exception:
            pass
    if local_service:
        return local_service.get_all_employees()
    return []

def fetch_analytics():
    if api_active:
        try:
            r = requests.get(f"{DEFAULT_API_URL}/analytics/summary")
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
    if local_service:
        return local_service.get_analytics_summary()
    return {}

def fetch_single(emp_id):
    if api_active:
        try:
            r = requests.get(f"{DEFAULT_API_URL}/employees/{emp_id}")
            if r.status_code == 200:
                return Employee.from_dict(r.json())
        except Exception:
            pass
    if local_service:
        return local_service.search_employee(emp_id)
    return None

def create_emp(emp_obj):
    if api_active:
        try:
            r = requests.post(f"{DEFAULT_API_URL}/employees", json=emp_obj.to_dict())
            if r.status_code == 200:
                return True, "Employee registered successfully via API!"
            return False, r.json().get("detail", "Error creating employee.")
        except Exception as e:
            return False, str(e)
    else:
        if local_service:
            if local_service.search_employee(emp_obj.employee_id):
                return False, f"Employee ID '{emp_obj.employee_id}' already exists."
            local_service.add_employee(emp_obj)
            return True, "Employee registered successfully into local storage!"
        return False, "Local database service unavailable."

def update_emp(emp_id, update_data, salary_query=None):
    if api_active:
        try:
            params = {}
            if salary_query is not None:
                params["salary"] = salary_query
            r = requests.put(f"{DEFAULT_API_URL}/employees/{emp_id}", params=params, json=update_data)
            if r.status_code == 200:
                return True, "Employee updated successfully!"
            return False, r.json().get("detail", "Error updating employee.")
        except Exception as e:
            return False, str(e)
    else:
        if local_service:
            success = local_service.update_employee(emp_id, update_data)
            if success:
                return True, "Employee updated successfully!"
            return False, "Employee record not found."
        return False, "Local database service unavailable."

def delete_emp(emp_id):
    if api_active:
        try:
            r = requests.delete(f"{DEFAULT_API_URL}/employees/{emp_id}")
            if r.status_code == 200:
                return True, "Employee deleted successfully!"
            return False, r.json().get("detail", "Error deleting employee.")
        except Exception as e:
            return False, str(e)
    else:
        if local_service:
            if local_service.delete_employee(emp_id):
                return True, "Employee deleted successfully!"
            return False, "Employee record not found."
        return False, "Local database service unavailable."

# ---------------------------------------------------------
# NOVA HR TOP HEADER BAR (EXACT NEXT.JS MATCH)
# ---------------------------------------------------------
api_badge = "🟢 REST API Live" if api_active else "🔵 Standalone SQLite Mode"

st.markdown(f"""
    <div class="nova-header">
        <div class="nova-brand">
            <div class="nova-brand-icon">🏢</div>
            <div>
                <div class="nova-brand-title">Nova <span style="color:#2563EB;">HR</span></div>
                <div class="nova-brand-sub">Enterprise Management System</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="nova-[#2563EB]-pill">{api_badge}</div>
            <div class="nova-profile-badge">
                <div class="nova-avatar">RM</div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.78rem; font-weight: 800; color: #0F172A; line-height: 1.1;">Rajesh Mani</span>
                    <span style="font-size: 0.65rem; font-weight: 600; color: #64748B;">HR Director</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SINGLE-LINE TOP HORIZONTAL NAVIGATION TABS
# ---------------------------------------------------------
nav_tab = st.radio(
    "Nav",
    ["Overview", "Directory", "Search", "Add", "Delete", "Payroll", "System"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 1: OVERVIEW (DASHBOARD & WAVE CHART)
# ---------------------------------------------------------
if nav_tab == "Overview":
    analytics = fetch_analytics()
    employees = fetch_all()

    tot_emp = analytics.get("total_employees", len(employees))
    act_emp = analytics.get("active_employees", sum(1 for e in employees if e.is_active()))
    tot_pay = analytics.get("total_payroll", sum(e.salary for e in employees))
    avg_sal = analytics.get("average_salary", (tot_pay / tot_emp) if tot_emp > 0 else 0)

    # 4 Linked KPI Cards with top blue indicator line
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class="metric-card active-card">
                <div class="metric-header">
                    <span class="metric-title">Total Workforce</span>
                    <span style="font-size:1.1rem;">👥</span>
                </div>
                <div class="metric-value text-indigo">{tot_emp:,}</div>
                <div class="metric-sub text-emerald">
                    <span>▲ +14%</span> • +28 employees vs last month
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Active Headcount</span>
                    <span style="font-size:1.1rem;">✅</span>
                </div>
                <div class="metric-value text-emerald">{act_emp:,}</div>
                <div class="metric-sub text-emerald">
                    <span>▲ +2.4%</span> • {((act_emp/tot_emp)*100 if tot_emp>0 else 0):.1f}% active retention
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Monthly Payroll</span>
                    <span style="font-size:1.1rem;">💵</span>
                </div>
                <div class="metric-value text-indigo">${(tot_pay/12):,.0f}</div>
                <div class="metric-sub text-emerald">
                    <span>▲ +5.8%</span> • Within annual budget
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Avg Compensation</span>
                    <span style="font-size:1.1rem;">💼</span>
                </div>
                <div class="metric-value text-indigo">${round(avg_sal):,}</div>
                <div class="metric-sub text-emerald">
                    <span>▲ +3.1%</span> • Competitive benchmark
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # SVG Wave Chart Container (Matching Razorpay / Nova Growth Chart)
    st.markdown(f"""
        <div class="content-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <div>
                    <h3 style="margin:0; font-weight:800; color:#0F172A; font-size:1.1rem;">Workforce Growth & Payroll Trends</h3>
                    <p style="margin:0.2rem 0 0 0; font-size:0.78rem; color:#64748B;">Comparing current period headcount against benchmark metrics.</p>
                </div>
                <div style="display:flex; gap:1rem; font-size:0.75rem; font-weight:700;">
                    <span style="color:#2563EB;">● This Period</span>
                    <span style="color:#94A3B8;">● Last Period</span>
                </div>
            </div>
            <div style="position:relative; width:100%; height:200px;">
                <svg viewBox="0 0 1000 200" style="width:100%; height:100%;" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="stBlueGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.35"/>
                            <stop offset="100%" stop-color="#3B82F6" stop-opacity="0.0"/>
                        </linearGradient>
                    </defs>
                    <line x1="0" y1="50" x2="1000" y2="50" stroke="#F1F5F9" stroke-width="1"/>
                    <line x1="0" y1="100" x2="1000" y2="100" stroke="#F1F5F9" stroke-width="1"/>
                    <line x1="0" y1="150" x2="1000" y2="150" stroke="#F1F5F9" stroke-width="1"/>
                    <path d="M 0 150 C 150 130, 300 80, 450 110 C 600 140, 750 40, 1000 70 L 1000 200 L 0 200 Z" fill="url(#stBlueGrad)" />
                    <path d="M 0 150 C 150 130, 300 80, 450 110 C 600 140, 750 40, 1000 70" fill="none" stroke="#2563EB" stroke-width="3.5" />
                    <line x1="450" y1="0" x2="450" y2="200" stroke="#3B82F6" stroke-width="1" stroke-dasharray="2 2"/>
                    <circle cx="450" cy="110" r="5" fill="#2563EB" stroke="#FFFFFF" stroke-width="2.5"/>
                </svg>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.72rem; font-weight:700; color:#94A3B8; margin-top:0.5rem;">
                <span>MAY 12</span><span>MAY 13</span><span>MAY 14</span><span>MAY 15</span><span>MAY 16</span><span>MAY 17</span><span>MAY 18</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Department Analytics Grid
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("##### 🏢 Department Distribution")
        dept_dict = analytics.get("departments", {})
        if not dept_dict and employees:
            dept_dict = {}
            for e in employees:
                d = e.department or "Unassigned"
                dept_dict[d] = dept_dict.get(d, 0) + 1

        if dept_dict:
            df_dept = pd.DataFrame(list(dept_dict.items()), columns=["Department", "Employees"])
            if HAS_PLOTLY:
                fig_dept = px.pie(
                    df_dept, values="Employees", names="Department", hole=0.5,
                    color_discrete_sequence=["#2563EB", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6", "#3B82F6"]
                )
                fig_dept.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
                st.plotly_chart(fig_dept, use_container_width=True)
            else:
                st.bar_chart(df_dept.set_index("Department"))

    with ch2:
        st.markdown("##### ⚡ Payroll Outflow by Department")
        if employees:
            df_emp_all = pd.DataFrame([e.to_dict() for e in employees])
            dept_payroll = df_emp_all.groupby("department")["salary"].sum().reset_index()
            if HAS_PLOTLY:
                fig_pay = px.bar(
                    dept_payroll, x="department", y="salary",
                    color="salary", color_continuous_scale="Blues", text_auto="$.2s"
                )
                fig_pay.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, coloraxis_showscale=False)
                st.plotly_chart(fig_pay, use_container_width=True)
            else:
                st.bar_chart(dept_payroll.set_index("department"))

# ---------------------------------------------------------
# TAB 2: DIRECTORY (WORKFORCE DIRECTORY & EXPORT)
# ---------------------------------------------------------
elif nav_tab == "Directory":
    st.markdown("### 📋 Workforce Directory & Records")
    employees = fetch_all()

    if employees:
        df = pd.DataFrame([e.to_dict() for e in employees])
        f1, f2, f3 = st.columns([2, 1, 1])

        with f1:
            search_term = st.text_input("🔍 Quick Keyword Search", placeholder="Search Name, ID, Dept, Designation, Email...")
        with f2:
            dept_opts = ["All"] + sorted(list(df["department"].dropna().unique()))
            selected_dept = st.selectbox("Department Filter", dept_opts)
        with f3:
            selected_status = st.selectbox("Status Filter", ["All", "Active", "Inactive"])

        filtered = df.copy()
        if selected_dept != "All":
            filtered = filtered[filtered["department"] == selected_dept]
        if selected_status != "All":
            filtered = filtered[filtered["status"].str.lower() == selected_status.lower()]
        if search_term:
            q = search_term.lower()
            filtered = filtered[
                filtered["employee_id"].astype(str).str.lower().str.contains(q) |
                filtered["first_name"].astype(str).str.lower().str.contains(q) |
                filtered["last_name"].astype(str).str.lower().str.contains(q) |
                filtered["department"].astype(str).str.lower().str.contains(q) |
                filtered["designation"].astype(str).str.lower().str.contains(q) |
                filtered["email"].astype(str).str.lower().str.contains(q)
            ]

        st.caption(f"Showing **{len(filtered)}** of **{len(df)}** registered employees.")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                "employee_id": st.column_config.TextColumn("ID"),
                "first_name": st.column_config.TextColumn("First Name"),
                "last_name": st.column_config.TextColumn("Last Name"),
                "email": st.column_config.LinkColumn("Email"),
                "phone": st.column_config.TextColumn("Phone"),
                "department": st.column_config.TextColumn("Department"),
                "designation": st.column_config.TextColumn("Designation"),
                "salary": st.column_config.NumberColumn("Annual Salary ($)", format="$%.2f"),
                "joining_date": st.column_config.DateColumn("Joining Date"),
                "status": st.column_config.TextColumn("Status")
            }
        )

        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Directory CSV",
            data=csv_bytes,
            file_name="nova_hr_directory.csv",
            mime="text/csv",
            use_container_width=False
        )

# ---------------------------------------------------------
# TAB 3: SEARCH & PROFILE CARDS
# ---------------------------------------------------------
elif nav_tab == "Search":
    st.markdown("### 🔍 Search & Visual Profile Cards")
    search_id = st.text_input("Enter Employee ID or Name", value="EMP001").strip()

    if search_id:
        emp = fetch_single(search_id)
        if emp:
            badge_html = f'<span class="status-badge-active">● ACTIVE</span>' if emp.is_active() else f'<span class="status-badge-inactive">● INACTIVE</span>'

            st.markdown(f"""
                <div class="content-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="display:flex; align-items:center; gap:1.2rem;">
                            <div style="background:linear-gradient(135deg, #2563EB, #4F46E5); color:#FFFFFF; border-radius:50%; width:64px; height:64px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:800; box-shadow:0 4px 10px rgba(37,99,235,0.3);">
                                {emp.first_name[0] if emp.first_name else 'E'}
                            </div>
                            <div>
                                <h2 style="margin:0; font-size:1.6rem; color:#0F172A; font-weight:800;">{emp.full_name()}</h2>
                                <span class="dept-badge">{emp.department}</span> &nbsp;•&nbsp; <span style="color:#64748B; font-weight:600;">{emp.designation}</span>
                            </div>
                        </div>
                        <div>{badge_html}</div>
                    </div>
                    <hr style="margin: 1.5rem 0; border:0; border-top:1px solid #E2E8F0;">
                    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                        <div>
                            <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">ID</span>
                            <div style="font-weight:700; font-size:1.1rem; color:#0F172A;">{emp.employee_id}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Email</span>
                            <div style="font-weight:600; color:#2563EB;">{emp.email}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Phone</span>
                            <div style="font-weight:600; color:#0F172A;">{emp.phone}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Salary</span>
                            <div style="font-weight:800; font-size:1.1rem; color:#0F172A;">${emp.salary:,.2f}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Salary Hike & Actions
            st.markdown("##### 💼 Direct Profile Management Actions")
            ac1, ac2 = st.columns(2)
            with ac1:
                hike_pct = st.slider("Apply Salary Hike (%)", min_value=1, max_value=50, value=10)
                new_sal = emp.salary * (1 + hike_pct / 100)
                st.caption(f"New Proposed Salary: **${new_sal:,.2f}** (+${(new_sal - emp.salary):,.2f})")
                if st.button("Apply Salary Hike", type="primary"):
                    update_emp(emp.employee_id, {"salary": new_sal})
                    st.success(f"Salary updated for {emp.full_name()}!")
                    st.rerun()

            with ac2:
                toggle_btn = "Deactivate Employee" if emp.is_active() else "Activate Employee"
                if st.button(toggle_btn):
                    new_st = "Inactive" if emp.is_active() else "Active"
                    update_emp(emp.employee_id, {"status": new_st})
                    st.success(f"Status changed to {new_st}!")
                    st.rerun()

# ---------------------------------------------------------
# TAB 4: ADD EMPLOYEE
# ---------------------------------------------------------
elif nav_tab == "Add":
    st.markdown("### ➕ Register New Employee")
    with st.form("add_employee_form", clear_on_submit=True):
        col_left, col_right = st.columns(2)
        with col_left:
            emp_id = st.text_input("Employee ID *", placeholder="e.g. EMP007")
            first_name = st.text_input("First Name *", placeholder="e.g. Rajesh")
            last_name = st.text_input("Last Name *", placeholder="e.g. Mani")
            email = st.text_input("Email Address *", placeholder="e.g. rajesh.mani@company.com")
            phone = st.text_input("Phone Number *", placeholder="e.g. +91 9876543219")

        with col_right:
            department = st.text_input("Department *", placeholder="e.g. Engineering")
            designation = st.text_input("Designation *", placeholder="e.g. Senior Software Engineer")
            salary = st.number_input("Annual Salary ($) *", min_value=0.0, value=85000.0, step=1000.0)
            joining_date = st.date_input("Joining Date", value=datetime.date.today())
            status = st.selectbox("Employment Status", ["Active", "Inactive"])

        btn_submit = st.form_submit_button("✨ Save Employee Registration", use_container_width=True)

    if btn_submit:
        if not emp_id.strip() or not first_name.strip() or not last_name.strip():
            st.error("❌ Please fill in all mandatory fields.")
        elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", email.strip()):
            st.error("❌ Please provide a valid email address.")
        else:
            new_emp = Employee(
                employee_id=emp_id.strip(),
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                email=email.strip(),
                phone=phone.strip(),
                department=department.strip(),
                designation=designation.strip(),
                salary=float(salary),
                joining_date=str(joining_date),
                status=status
            )
            success, msg = create_emp(new_emp)
            if success:
                st.success(f"🎉 {msg}")
                try:
                    st.balloons()
                except Exception:
                    pass
            else:
                st.error(f"❌ {msg}")

# ---------------------------------------------------------
# TAB 5: DELETE EMPLOYEE (DANGER ZONE)
# ---------------------------------------------------------
elif nav_tab == "Delete":
    st.markdown("### 🗑️ Employee Safe Deletion Workflow")
    employees = fetch_all()

    if employees:
        emp_map = {f"{e.employee_id} - {e.full_name()} ({e.department})": e.employee_id for e in employees}
        selected_key = st.selectbox("Select Employee Record to Remove", list(emp_map.keys()))
        target_id = emp_map[selected_key]
        emp = fetch_single(target_id)

        if emp:
            st.markdown(f"""
                <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:14px; padding:1.5rem; margin:1rem 0;">
                    <h4 style="color:#991B1B; margin:0 0 0.5rem 0;">⚠️ Danger Zone: Permanent Deletion</h4>
                    <p style="color:#7F1D1D; margin:0;">
                        You are about to permanently remove employee <strong>{emp.full_name()}</strong> (ID: <code>{emp.employee_id}</code>). Action cannot be undone.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            confirm = st.checkbox("I confirm permanent removal of this record.")
            if st.button("💥 Permanently Delete Employee", disabled=not confirm, type="primary"):
                success, msg = delete_emp(target_id)
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

# ---------------------------------------------------------
# TAB 6: PAYROLL ANALYTICS
# ---------------------------------------------------------
elif nav_tab == "Payroll":
    st.markdown("### 📈 Payroll Allocation & Department Analytics")
    employees = fetch_all()
    if employees:
        df = pd.DataFrame([e.to_dict() for e in employees])
        dept_pay = df.groupby("department")["salary"].agg(["sum", "mean", "count"]).reset_index()
        dept_pay.columns = ["Department", "Total Payroll ($)", "Average Salary ($)", "Employee Count"]
        
        st.dataframe(dept_pay, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 7: SYSTEM HEALTH
# ---------------------------------------------------------
elif nav_tab == "System":
    st.markdown("### 🛡️ System Health & Storage Engine")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("REST API Backend", "Online" if api_active else "Offline", delta="FastAPI v2.0")
    with s2:
        st.metric("Database Engine", "SQLite Engine", delta="hr_management.db")
    with s3:
        st.metric("Total Records", len(fetch_all()))
