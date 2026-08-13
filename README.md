# 🏢 Enterprise HR Management System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=for-the-badge&logo=next.js&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

An end-to-end, executive-grade **Human Resource Management System** built with **Python**, **FastAPI**, **Streamlit**, **Next.js**, **SQLite/MySQL**, and **Plotly**. 

Features an executive web portal, real-time workforce analytics, full CRUD employee management (Add, View, Search, Update, Delete), automated CSV seeding, REST API backend, and one-click cloud deployment readiness for **Streamlit Cloud**.

🌐 **Live Streamlit App**: [https://enterprise-hr-management-system.streamlit.app/](https://enterprise-hr-management-system.streamlit.app/)

---

## 🌟 Key Features

* 📊 **Executive Dashboard & Workforce Analytics**: Real-time KPI metric cards (Total Workforce, Active Personnel, Monthly Payroll, Avg Salary), interactive department donut charts, and payroll allocation charts.
* 📋 **Workforce Directory & Quick Inspector**: Live search by keyword (Name, ID, Department, Designation, Email), department/status filters, formatted currency columns, inline quick inspector, and single-click CSV export.
* ➕ **Employee Registration**: Form input validation (Email regex check, phone validation, mandatory fields) with interactive success banners and balloons.
* 🔍 **Search & Employee Profile Cards**: Visual profile cards with direct management actions (**% Salary Hike Calculator** and **Status Toggle**).
* ✏️ **Employee Record Editor**: Edit any employee's details (Name, Email, Phone, Department, Designation, Salary, Status).
* 🗑️ **Safe Deletion Workflow**: Danger zone warning banner and safety confirmation checkbox before permanent record removal.
* 💾 **Dual Storage Persistence**: Zero-configuration SQLite engine (`data/hr_management.db`) with auto CSV seeding, and support for MySQL.
* ⚡ **Dual App Engines**: Run via **Streamlit UI** (`http://localhost:8501`) or **Next.js Frontend** (`http://localhost:3000`).

---

## 🏗️ Project Architecture & Structure

```
Enterprise-HR-Management-System/
│
├── streamlit_app.py        # Streamlit Web Application (Streamlit Cloud Entrypoint)
├── main.py                 # FastAPI REST API Backend Server
├── app.py                  # Interactive CLI Console App
│
├── frontend/               # Next.js Web Frontend App
│   ├── app/
│   │   ├── page.tsx        # Next.js Full CRUD Executive Web Portal
│   │   └── layout.tsx      # App Layout & Tailwind Configuration
│   └── package.json
│
├── models/
│   └── employee.py         # Employee Class & Serialization
│
├── schemas/
│   └── employee_schema.py  # Pydantic Request & Update Schemas
│
├── services/
│   ├── employee_service.py # Unified Business Logic Service
│   ├── db_service.py       # SQLite Engine & Auto CSV Seeding
│   ├── mysql_service.py    # MySQL Service Engine & Fallback
│   └── csv_service.py      # CSV Handling Utility
│
├── data/
│   ├── employees.csv       # Seed Employee Dataset
│   └── hr_management.db    # Auto-Generated SQLite DB File
│
├── utils/
│   └── logger.py           # Application Logging System
│
├── requirements.txt        # Production Dependencies
└── README.md
```

---

## 🔌 REST API Endpoints

FastAPI backend server runs on `http://127.0.0.1:8000` with interactive Swagger UI at `/docs`.

| Method | Endpoint | Description | Query Parameters |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Health Check & Info | - |
| `GET` | `/employees` | List Employees | `department`, `status`, `search` |
| `GET` | `/analytics/summary` | Aggregate HR Metrics & Department Stats | - |
| `GET` | `/employees/{employee_id}` | Get Single Employee Profile | - |
| `POST` | `/employees` | Register New Employee | Body: `EmployeeSchema` |
| `PUT` | `/employees/{employee_id}` | Update Employee Record / Salary | `salary`, Body: `EmployeeUpdateSchema` |
| `DELETE` | `/employees/{employee_id}` | Delete Employee Record | - |
| `POST` | `/seed` | Re-seed Database from CSV | - |

---

## 🚀 Local Installation & Quick Start

### 1. Clone & Setup Environment

```bash
git clone https://github.com/rjvibez/Enterprise-HR-Management-System.git
cd Enterprise-HR-Management-System
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Web App (Recommended)

```bash
streamlit run streamlit_app.py
```
*Access Web Portal at: [http://localhost:8501](http://localhost:8501)*

---

### 🌐 Option A: Run FastAPI Backend + Streamlit UI

**Terminal 1 (FastAPI Backend)**:
```bash
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Streamlit UI)**:
```bash
streamlit run streamlit_app.py
```
*The Streamlit sidebar will automatically display: `🟢 Mode: REST API Connected`.*

---

### ⚛️ Option B: Run Next.js Frontend (`localhost:3000`)

**Terminal 1 (FastAPI Backend)**:
```bash
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Next.js Frontend)**:
```bash
cd frontend
npm install
npm run dev
```
*Access Next.js Web App at: [http://localhost:3000](http://localhost:3000)*

---

## ☁️ Deploying to Streamlit Cloud

1. Push your repository to **GitHub**:
   ```bash
   git add .
   git commit -m "Upgrade Enterprise HR System with executive UI and Next.js frontend"
   git push origin main --force
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io)**.
3. Click **"New App"** and select repository: `Enterprise-HR-Management-System`.
4. Set Main File Path: `streamlit_app.py`.
5. Click **"Deploy!"**.

---

## 👤 Author

**Rajesh**  
AI Engineer | Python Developer | Machine Learning Specialist  
GitHub: [@rjvibez](https://github.com/rjvibez)
