import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION - MUST BE FIRST STREAMLIT CALL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nova HR Enterprise Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
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
# MODERN CUSTOM CSS STYLING & RAZORPAY DESIGN SYSTEM
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background-color: #F8FAFC;
    }

    /* Remove excessive top container padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 95%;
    }

    /* Razorpay Top Header Bar */
    .rz-header {
        background: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        padding: 0.9rem 1.8rem;
        margin: -1rem -1rem 1.5rem -1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    .rz-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 800;
        font-size: 1.25rem;
        color: #0F172A;
    }
    .rz-badge {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    /* Razorpay Metric Tab Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
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
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
    }
    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .metric-title {
        font-size: 0.78rem;
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
        font-size: 0.8rem;
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

    /* Profile & Content Cards */
    .content-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.75rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }

    /* Status Badges */
    .status-badge-active {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.78rem;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        letter-spacing: 0.3px;
    }
    .status-badge-inactive {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.78rem;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        letter-spacing: 0.3px;
    }
    .dept-badge {
        background-color: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
        padding: 0.3rem 0.75rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-block;
    }

    /* Form styling enhancements */
    div[data-testid="stForm"] {
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 2rem;
        background-color: #FFFFFF;
        box-shadow: 0 4px 14px -3px rgba(0, 0, 0, 0.03);
    }

    /* Custom Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1.2rem;
    }
    .section-header h3 {
        margin: 0;
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.3px;
    }

    /* Streamlit Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        padding: 0.5rem 0.8rem;
        border-radius: 8px;
        transition: background 0.2s ease;
    }
    </style>
""", unsafe_allow_html=True)

# Check if services loaded
if not SERVICE_LOADED:
    st.error(f"❌ System initialization error: {SERVICE_ERROR}")

DEFAULT_API_URL = "http://127.0.0.1:8000"

@st.cache_resource
def get_service():
    if SERVICE_LOADED:
        return EmployeeService()
    return None

local_service = get_service()

def is_api_online(url):
    try:
        r = requests.get(f"{url}/", timeout=1.2)
        return r.status_code == 200
    except Exception:
        return False

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & SYSTEM SETTINGS
# ---------------------------------------------------------
st.sidebar.markdown("""
    <div style="padding: 0.5rem 0; text-align: left;">
        <div style="display: flex; align-items: center; gap: 0.8rem;">
            <div style="background: linear-gradient(135deg, #6366F1, #4F46E5); padding: 0.6rem; border-radius: 12px; font-size: 1.5rem; display: flex; align-items: center; justify-content: center;">
                🏢
            </div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.4px;">Nova HR</div>
                <div style="font-size: 0.78rem; color: #94A3B8; font-weight: 500;">Enterprise Management System</div>
            </div>
        </div>
    </div>
    <hr style="border:0; border-top:1px solid rgba(255,255,255,0.1); margin: 1.2rem 0;">
""", unsafe_allow_html=True)

api_url = st.sidebar.text_input("FastAPI Backend URL", value=DEFAULT_API_URL)
api_active = is_api_online(api_url)

if api_active:
    st.sidebar.markdown("""
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399 !important; padding: 0.6rem 0.9rem; border-radius: 10px; font-weight: 600; font-size: 0.83rem; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem;">
            <span>🟢</span> Mode: REST API Connected
        </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #818CF8 !important; padding: 0.6rem 0.9rem; border-radius: 10px; font-weight: 600; font-size: 0.83rem; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem;">
            <span>🔵</span> Mode: Standalone SQLite Engine
        </div>
    """, unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation Menu",
    (
        "📊 Dashboard",
        "📋 View Employees",
        "➕ Add Employee",
        "🔍 Search & Profile",
        "✏️ Update Employee",
        "🗑️ Delete Employee",
        "⚙️ System & Backup"
    )
)

st.sidebar.markdown("""
    <hr style="border:0; border-top:1px solid rgba(255,255,255,0.1); margin: 1.5rem 0;">
    <div style="font-size: 0.78rem; color: #64748B; text-align: center;">
        © 2026 Enterprise HR System<br>All rights reserved.
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA SERVICE INTEGRATION LAYER
# ---------------------------------------------------------
def fetch_all():
    if api_active:
        try:
            r = requests.get(f"{api_url}/employees")
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
            r = requests.get(f"{api_url}/analytics/summary")
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
            r = requests.get(f"{api_url}/employees/{emp_id}")
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
            r = requests.post(f"{api_url}/employees", json=emp_obj.to_dict())
            if r.status_code in [200, 201]:
                return True, "Employee registered successfully!"
            return False, r.json().get("detail", "Failed to register employee.")
        except Exception as e:
            return False, str(e)
    else:
        if local_service:
            if local_service.search_employee(emp_obj.employee_id):
                return False, f"Employee ID '{emp_obj.employee_id}' already exists."
            local_service.add_employee(emp_obj)
            return True, "Employee registered successfully into storage!"
        return False, "Local database service unavailable."

def update_emp(emp_id, update_data, salary_query=None):
    if api_active:
        try:
            params = {}
            if salary_query is not None:
                params["salary"] = salary_query
            r = requests.put(f"{api_url}/employees/{emp_id}", params=params, json=update_data)
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
            r = requests.delete(f"{api_url}/employees/{emp_id}")
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
# NOVA HR TOP HEADER BAR & HORIZONTAL NAVIGATION
# ---------------------------------------------------------
api_status_html = "🟢 REST API Live" if api_active else "🔵 Local SQLite Mode"
api_status_class = "rz-badge" if api_active else "rz-badge"

st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(15,23,42,0.05);">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 40px; height: 40px; border-radius: 12px; background: linear-gradient(135deg, #0F62FE, #2563EB); color: white; font-weight: 800; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(37,99,235,0.25);">
                🏢
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.2rem; color: #0F172A; line-height: 1.2; tracking-tight: -0.5px;">
                    Nova <span style="color: #2563EB;">HR</span>
                </div>
                <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">
                    Enterprise Management System
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; color: #1E40AF; padding: 0.3rem 0.8rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">
                {api_status_html}
            </div>
            <div style="display: flex; align-items: center; gap: 0.6rem; border-left: 1px solid #E2E8F0; padding-left: 1rem;">
                <div style="width: 34px; height: 34px; border-radius: 50%; background: #1E293B; color: white; font-weight: 800; font-size: 0.75rem; display: flex; align-items: center; justify-content: center;">
                    RM
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.78rem; font-weight: 800; color: #0F172A; line-height: 1.1;">Rajesh Mani</span>
                    <span style="font-size: 0.65rem; font-weight: 600; color: #64748B;">HR Director</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Horizontal Top Navigation Menu Tabs
menu = st.radio(
    "",
    [
        "📊 Overview",
        "📋 Directory",
        "🔍 Search",
        "➕ Add",
        "🗑️ Delete",
        "📈 Payroll",
        "⚙️ System"
    ],
    horizontal=True
)

st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 1: DASHBOARD / OVERVIEW
# ---------------------------------------------------------
if menu == "📊 Overview" or menu == "📊 Dashboard":
    st.markdown("""
        <div class="section-header">
            <h3>📊 Executive Overview & Workforce Analytics</h3>
        </div>
    """, unsafe_allow_html=True)

    analytics = fetch_analytics()
    employees = fetch_all()

    # KPI Metric Cards Grid
    c1, c2, c3, c4 = st.columns(4)

    tot_emp = analytics.get("total_employees", len(employees))
    act_emp = analytics.get("active_employees", sum(1 for e in employees if e.is_active()))
    tot_pay = analytics.get("total_payroll", sum(e.salary for e in employees))
    avg_sal = analytics.get("average_salary", (tot_pay / tot_emp) if tot_emp > 0 else 0)

    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Total Workforce</span>
                    <span class="metric-icon">👥</span>
                </div>
                <div class="metric-value text-indigo">{tot_emp}</div>
                <div class="metric-sub text-emerald">
                    <span>⚡ Registered Employees</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Active Personnel</span>
                    <span class="metric-icon">✅</span>
                </div>
                <div class="metric-value text-emerald">{act_emp}</div>
                <div class="metric-sub text-emerald">
                    <span>📈 {((act_emp/tot_emp)*100 if tot_emp>0 else 0):.1f}% Active Rate</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Monthly Payroll</span>
                    <span class="metric-icon">💵</span>
                </div>
                <div class="metric-value text-amber">${tot_pay:,.2f}</div>
                <div class="metric-sub text-amber">
                    <span>💼 Total Compensation</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Average Salary</span>
                    <span class="metric-icon">📊</span>
                </div>
                <div class="metric-value text-indigo">${avg_sal:,.2f}</div>
                <div class="metric-sub text-indigo">
                    <span>📈 Per Employee Avg</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Charts Section
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
                    df_dept,
                    values="Employees",
                    names="Department",
                    hole=0.5,
                    color_discrete_sequence=["#4F46E5", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6", "#3B82F6"]
                )
                fig_dept.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#FFFFFF', width=2))
                )
                fig_dept.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=340,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_dept, use_container_width=True)
            else:
                st.bar_chart(df_dept.set_index("Department"))
        else:
            st.info("No department metrics available.")

    with ch2:
        st.markdown("##### ⚡ Employee Status & Payroll Allocation")
        if employees:
            df_emp_all = pd.DataFrame([e.to_dict() for e in employees])
            dept_payroll = df_emp_all.groupby("department")["salary"].sum().reset_index()
            
            if HAS_PLOTLY:
                fig_pay = px.bar(
                    dept_payroll,
                    x="department",
                    y="salary",
                    labels={"department": "Department", "salary": "Total Payroll ($)"},
                    color="salary",
                    color_continuous_scale="Viridis",
                    text_auto="$.2s"
                )
                fig_pay.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=340,
                    xaxis_title="",
                    yaxis_title="Payroll Outflow ($)",
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_pay, use_container_width=True)
            else:
                st.bar_chart(dept_payroll.set_index("department"))
        else:
            st.info("No payroll data available.")

    if employees:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 📋 Quick Workforce Snapshot")
        df_emp = pd.DataFrame([e.to_dict() for e in employees])
        st.dataframe(
            df_emp[["employee_id", "first_name", "last_name", "department", "designation", "salary", "status"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "employee_id": st.column_config.TextColumn("ID"),
                "first_name": st.column_config.TextColumn("First Name"),
                "last_name": st.column_config.TextColumn("Last Name"),
                "department": st.column_config.TextColumn("Department"),
                "designation": st.column_config.TextColumn("Designation"),
                "salary": st.column_config.NumberColumn("Annual Salary ($)", format="$%.2f"),
                "status": st.column_config.TextColumn("Status")
            }
        )

# ---------------------------------------------------------
# MODULE 2: VIEW EMPLOYEES / DIRECTORY
# ---------------------------------------------------------
elif menu == "📋 Directory" or menu == "📋 View Employees":
    st.markdown("""
        <div class="section-header">
            <h3>📋 Workforce Directory</h3>
        </div>
    """, unsafe_allow_html=True)

    employees = fetch_all()

    if not employees:
        st.info("No employee records found in the system.")
    else:
        df = pd.DataFrame([e.to_dict() for e in employees])

        f1, f2, f3 = st.columns([2, 1, 1])

        with f1:
            search_term = st.text_input("🔍 Quick Search", placeholder="Search by Name, ID, Department, Designation, Email...")
        with f2:
            dept_opts = ["All"] + sorted(list(df["department"].dropna().unique()))
            selected_dept = st.selectbox("Department Filter", dept_opts)
        with f3:
            status_opts = ["All", "Active", "Inactive"]
            selected_status = st.selectbox("Status Filter", status_opts)

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

        st.caption(f"Showing **{len(filtered)}** of **{len(df)}** employee records")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                "employee_id": st.column_config.TextColumn("Employee ID"),
                "first_name": st.column_config.TextColumn("First Name"),
                "last_name": st.column_config.TextColumn("Last Name"),
                "email": st.column_config.LinkColumn("Email Address"),
                "phone": st.column_config.TextColumn("Phone"),
                "department": st.column_config.TextColumn("Department"),
                "designation": st.column_config.TextColumn("Designation"),
                "salary": st.column_config.NumberColumn("Annual Salary ($)", format="$%.2f"),
                "joining_date": st.column_config.DateColumn("Joining Date"),
                "status": st.column_config.TextColumn("Status")
            }
        )

        st.markdown("<br>", unsafe_allow_html=True)
        c_exp, c_dl = st.columns([3, 1])

        with c_dl:
            csv_bytes = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export Directory (CSV)",
                data=csv_bytes,
                file_name="employee_directory.csv",
                mime="text/csv",
                use_container_width=True
            )

        with st.expander("🔍 Interactive Quick Employee Inspector"):
            inspect_ids = filtered["employee_id"].tolist()
            if inspect_ids:
                selected_inspect_id = st.selectbox("Select Employee to Inspect", inspect_ids)
                target_emp = fetch_single(selected_inspect_id)
                if target_emp:
                    badge_class = "status-badge-active" if target_emp.is_active() else "status-badge-inactive"
                    st.markdown(f"""
                        <div class="content-card" style="margin-top:1rem;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="display:flex; align-items:center; gap:1.2rem;">
                                    <div style="background:#EEF2FF; color:#4338CA; border-radius:50%; width:60px; height:60px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:800;">
                                        {target_emp.first_name[0] if target_emp.first_name else 'E'}
                                    </div>
                                    <div>
                                        <h3 style="margin:0; color:#0F172A;">{target_emp.full_name()}</h3>
                                        <span class="dept-badge">{target_emp.department}</span> &nbsp;•&nbsp; <span style="color:#64748B; font-weight:600;">{target_emp.designation}</span>
                                    </div>
                                </div>
                                <div>
                                    <span class="{badge_class}">{target_emp.status.upper()}</span>
                                </div>
                            </div>
                            <hr style="margin: 1.2rem 0; border:0; border-top:1px solid #E2E8F0;">
                            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                                <div>
                                    <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">ID</span>
                                    <div style="font-weight:700; color:#0F172A;">{target_emp.employee_id}</div>
                                </div>
                                <div>
                                    <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Email</span>
                                    <div style="font-weight:600; color:#4F46E5;">{target_emp.email}</div>
                                </div>
                                <div>
                                    <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Phone</span>
                                    <div style="font-weight:600; color:#0F172A;">{target_emp.phone}</div>
                                </div>
                                <div>
                                    <span style="color:#64748B; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Salary</span>
                                    <div style="font-weight:800; color:#059669;">${target_emp.salary:,.2f}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 3: ADD EMPLOYEE
# ---------------------------------------------------------
elif menu == "➕ Add" or menu == "➕ Add Employee":
    st.markdown("""
        <div class="section-header">
            <h3>➕ Register New Employee Record</h3>
        </div>
    """, unsafe_allow_html=True)

    with st.form("add_employee_form", clear_on_submit=True):
        st.markdown("##### 👤 Personal & Employment Details")
        col_left, col_right = st.columns(2)

        with col_left:
            emp_id = st.text_input("Employee ID *", placeholder="e.g. EMP006")
            first_name = st.text_input("First Name *", placeholder="e.g. Ananya")
            last_name = st.text_input("Last Name *", placeholder="e.g. Verma")
            email = st.text_input("Email Address *", placeholder="e.g. ananya@company.com")
            phone = st.text_input("Phone Number *", placeholder="e.g. +1 555-0192")

        with col_right:
            department = st.text_input("Department *", placeholder="e.g. Data Analytics")
            designation = st.text_input("Designation *", placeholder="e.g. Senior Data Engineer")
            salary = st.number_input("Annual Salary ($) *", min_value=0.0, value=75000.0, step=1000.0)
            joining_date = st.date_input("Joining Date", value=datetime.date.today())
            status = st.selectbox("Employment Status", ["Active", "Inactive"])

        st.markdown("<br>", unsafe_allow_html=True)
        btn_submit = st.form_submit_button("✨ Register Employee Record", use_container_width=True)

    if btn_submit:
        if not emp_id.strip():
            st.error("❌ Employee ID is required.")
        elif not first_name.strip() or not last_name.strip():
            st.error("❌ Both First Name and Last Name are required.")
        elif not email.strip() or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email.strip()):
            st.error("❌ Please provide a valid email address.")
        elif not phone.strip():
            st.error("❌ Phone number is required.")
        elif not department.strip() or not designation.strip():
            st.error("❌ Department and Designation are required.")
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
                st.toast(f"Registered {first_name} {last_name} ({emp_id}) successfully!", icon="✅")
                try:
                    st.balloons()
                except Exception:
                    pass
            else:
                st.error(f"❌ {msg}")

# ---------------------------------------------------------
# MODULE 4: SEARCH & PROFILE
# ---------------------------------------------------------
elif menu == "🔍 Search" or menu == "🔍 Search & Profile":
    st.markdown("""
        <div class="section-header">
            <h3>🔍 Employee Profile & Quick Actions</h3>
        </div>
    """, unsafe_allow_html=True)

    c_search, c_btn = st.columns([4, 1])
    with c_search:
        search_id = st.text_input("Enter Employee ID", placeholder="e.g. EMP001").strip()

    if search_id:
        emp = fetch_single(search_id)
        if emp:
            badge_html = f'<span class="status-badge-active">● ACTIVE</span>' if emp.is_active() else f'<span class="status-badge-inactive">● INACTIVE</span>'

            st.markdown(f"""
                <div class="content-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="display:flex; align-items:center; gap:1.2rem;">
                            <div style="background:linear-gradient(135deg, #4F46E5, #3730A3); color:#FFFFFF; border-radius:50%; width:64px; height:64px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:800; box-shadow:0 4px 10px rgba(79, 70, 229, 0.3);">
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
                    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
                        <div>
                            <span style="color:#64748B; font-size:0.78rem; font-weight:700; text-transform:uppercase;">Employee ID</span>
                            <div style="font-weight:700; font-size:1.15rem; color:#0F172A;">{emp.employee_id}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.78rem; font-weight:700; text-transform:uppercase;">Email Address</span>
                            <div style="font-weight:600; font-size:1.05rem; color:#4F46E5;">{emp.email}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.78rem; font-weight:700; text-transform:uppercase;">Phone Number</span>
                            <div style="font-weight:600; font-size:1.05rem; color:#0F172A;">{emp.phone}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.78rem; font-weight:700; text-transform:uppercase;">Annual Compensation</span>
                            <div style="font-weight:800; font-size:1.3rem; color:#059669;">${emp.salary:,.2f}</div>
                        </div>
                        <div>
                            <span style="color:#64748B; font-size:0.78rem; font-weight:700; text-transform:uppercase;">Joining Date</span>
                            <div style="font-weight:600; font-size:1.05rem; color:#0F172A;">{emp.joining_date}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("##### ⚡ Direct Profile Management Actions")
            qa1, qa2, qa3 = st.columns(3)

            with qa1:
                hike_pct = st.number_input("Hike Percentage (%)", min_value=1.0, max_value=100.0, value=10.0, step=1.0, key="hike_input")
                if st.button(f"📈 Apply {hike_pct:.0f}% Salary Hike", use_container_width=True):
                    new_sal = emp.salary * (1 + (hike_pct / 100))
                    success, msg = update_emp(emp.employee_id, {"salary": new_sal}, salary_query=new_sal)
                    if success:
                        st.success(f"Salary updated to ${new_sal:,.2f}")
                        st.toast(f"Applied {hike_pct:.0f}% hike to {emp.full_name()}!", icon="📈")
                        st.rerun()
                    else:
                        st.error(msg)

            with qa2:
                toggle_st = "Inactive" if emp.is_active() else "Active"
                st.write("<br>", unsafe_allow_html=True)
                if st.button(f"🔄 Toggle Status to '{toggle_st}'", use_container_width=True):
                    success, msg = update_emp(emp.employee_id, {"status": toggle_st})
                    if success:
                        st.success(f"Status changed to {toggle_st}")
                        st.toast(f"Status updated to {toggle_st}!", icon="🔄")
                        st.rerun()
                    else:
                        st.error(msg)

            with qa3:
                st.write("<br>", unsafe_allow_html=True)
                with st.popover("✏️ Quick Edit Profile"):
                    with st.form("quick_edit_form"):
                        q_fn = st.text_input("First Name", value=emp.first_name)
                        q_ln = st.text_input("Last Name", value=emp.last_name)
                        q_em = st.text_input("Email", value=emp.email)
                        q_dp = st.text_input("Department", value=emp.department)
                        q_ds = st.text_input("Designation", value=emp.designation)
                        q_btn = st.form_submit_button("Save Quick Changes")

                    if q_btn:
                        q_up = {
                            "first_name": q_fn.strip(),
                            "last_name": q_ln.strip(),
                            "email": q_em.strip(),
                            "department": q_dp.strip(),
                            "designation": q_ds.strip()
                        }
                        s_q, m_q = update_emp(emp.employee_id, q_up)
                        if s_q:
                            st.success("Profile updated!")
                            st.rerun()
                        else:
                            st.error(m_q)
        else:
            st.error(f"❌ No employee record found matching ID '{search_id}'")

# ---------------------------------------------------------
# MODULE 5: UPDATE EMPLOYEE
# ---------------------------------------------------------
elif menu == "✏️ Update Employee":
    st.markdown("""
        <div class="section-header">
            <h3>✏️ Update Employee Record</h3>
        </div>
    """, unsafe_allow_html=True)

    employees = fetch_all()
    if not employees:
        st.warning("No employee records found in the database.")
    else:
        emp_map = {f"{e.employee_id} - {e.full_name()} ({e.department})": e.employee_id for e in employees}
        selected_key = st.selectbox("Select Employee to Modify", list(emp_map.keys()))

        target_id = emp_map[selected_key]
        emp = fetch_single(target_id)

        if emp:
            with st.form("update_employee_form"):
                st.markdown(f"##### Modifying Information for **{emp.full_name()}** (`{emp.employee_id}`)")
                u1, u2 = st.columns(2)

                with u1:
                    fn = st.text_input("First Name", value=emp.first_name)
                    ln = st.text_input("Last Name", value=emp.last_name)
                    em = st.text_input("Email Address", value=emp.email)
                    ph = st.text_input("Phone Number", value=emp.phone)

                with u2:
                    dp = st.text_input("Department", value=emp.department)
                    ds = st.text_input("Designation", value=emp.designation)
                    sal = st.number_input("Annual Salary ($)", value=float(emp.salary), step=500.0)
                    stt = st.selectbox("Status", ["Active", "Inactive"], index=0 if emp.is_active() else 1)

                st.markdown("<br>", unsafe_allow_html=True)
                btn_save = st.form_submit_button("💾 Save Employee Changes", use_container_width=True)

            if btn_save:
                up_payload = {
                    "first_name": fn.strip(),
                    "last_name": ln.strip(),
                    "email": em.strip(),
                    "phone": ph.strip(),
                    "department": dp.strip(),
                    "designation": ds.strip(),
                    "salary": float(sal),
                    "status": stt
                }
                success, msg = update_emp(target_id, up_payload, salary_query=float(sal))
                if success:
                    st.success(f"✅ {msg}")
                    st.toast("Employee updated successfully!", icon="🎉")
                else:
                    st.error(f"❌ {msg}")

# ---------------------------------------------------------
# MODULE 6: DELETE EMPLOYEE
# ---------------------------------------------------------
elif menu == "🗑️ Delete" or menu == "🗑️ Delete Employee":
    st.markdown("""
        <div class="section-header">
            <h3>🗑️ Delete Employee Record</h3>
        </div>
    """, unsafe_allow_html=True)

    employees = fetch_all()
    if not employees:
        st.warning("No employee records available for deletion.")
    else:
        emp_map = {f"{e.employee_id} - {e.full_name()} ({e.department})": e.employee_id for e in employees}
        selected_key = st.selectbox("Select Employee to Remove", list(emp_map.keys()))
        target_id = emp_map[selected_key]

        emp = fetch_single(target_id)

        if emp:
            st.markdown(f"""
                <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:14px; padding:1.5rem; margin-bottom:1.5rem;">
                    <h4 style="color:#991B1B; margin:0 0 0.5rem 0;">⚠️ Danger Zone: Permanent Deletion</h4>
                    <p style="color:#7F1D1D; margin:0;">
                        You are about to permanently remove employee <strong>{emp.full_name()}</strong> (ID: <code>{emp.employee_id}</code>) 
                        from <strong>{emp.department}</strong>. This action cannot be undone.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            confirm = st.checkbox("I understand this operation will permanently remove this record from the database.")

            if st.button("💥 Confirm Permanent Deletion", disabled=not confirm, use_container_width=True):
                success, msg = delete_emp(target_id)
                if success:
                    st.success(f"✅ {msg}")
                    st.toast(f"Employee {emp.full_name()} deleted successfully", icon="🗑️")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

# ---------------------------------------------------------
# MODULE 7: SYSTEM & BACKUP
# ---------------------------------------------------------
elif menu == "⚙️ System" or menu == "⚙️ System & Backup" or menu == "📈 Payroll":
    st.markdown("""
        <div class="section-header">
            <h3>⚙️ System Status, Data Backup & Seeding</h3>
        </div>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        st.markdown("### 💾 Storage & Connectivity Status")
        db_path = os.path.join("data", "hr_management.db")
        if os.path.exists(db_path):
            kb = os.path.getsize(db_path) / 1024
            st.success(f"SQLite Engine Active: `data/hr_management.db` ({kb:.1f} KB)")
        else:
            st.info("Database file will auto-create on first insertion.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset & Seed Database from Default CSV", use_container_width=True):
            if api_active:
                try:
                    r = requests.post(f"{api_url}/seed")
                    if r.status_code == 200:
                        st.success("Database re-seeded successfully via REST API!")
                        st.toast("Database re-seeded!", icon="🌱")
                    else:
                        st.error("Failed to re-seed via API.")
                except Exception as e:
                    st.error(str(e))
            else:
                if local_service and local_service.seed_from_csv():
                    st.success("Database re-seeded successfully from CSV file!")
                    st.toast("Database re-seeded!", icon="🌱")
                else:
                    st.error("Failed to seed from CSV.")

    with s2:
        st.markdown("### 📦 Backup & System Export")
        employees = fetch_all()
        if employees:
            df = pd.DataFrame([e.to_dict() for e in employees])
            csv_b = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📦 Download Complete System Database Backup (CSV)",
                data=csv_b,
                file_name=f"hr_database_backup_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No records available to backup.")
