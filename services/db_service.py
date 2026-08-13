import os
import sqlite3
import csv
from models.employee import Employee
from utils.logger import logger

DB_FILE = os.path.join("data", "hr_management.db")
CSV_FILE = os.path.join("data", "employees.csv")


class DatabaseService:
    @staticmethod
    def get_connection():
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls):
        """Initialize database table and seed from CSV if table is empty."""
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    department TEXT,
                    designation TEXT,
                    salary REAL,
                    joining_date TEXT,
                    status TEXT
                )
            """)
            conn.commit()

            # Check if empty, seed from CSV if available
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]

            if count == 0 and os.path.exists(CSV_FILE):
                cls.seed_from_csv(CSV_FILE, conn)

            cursor.close()
            conn.close()
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")

    @classmethod
    def seed_from_csv(cls, csv_path=CSV_FILE, conn=None):
        should_close = False
        if conn is None:
            conn = cls.get_connection()
            should_close = True

        try:
            if not os.path.exists(csv_path):
                return False

            cursor = conn.cursor()
            with open(csv_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emp_id = row.get("employee_id", "").strip()
                    if not emp_id:
                        continue
                    
                    try:
                        salary_val = float(row.get("salary", 0.0))
                    except (ValueError, TypeError):
                        salary_val = 0.0

                    cursor.execute("""
                        INSERT OR REPLACE INTO employees 
                        (employee_id, first_name, last_name, email, phone, department, designation, salary, joining_date, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        emp_id,
                        row.get("first_name", "").strip(),
                        row.get("last_name", "").strip(),
                        row.get("email", "").strip(),
                        row.get("phone", "").strip(),
                        row.get("department", "").strip(),
                        row.get("designation", "").strip(),
                        salary_val,
                        row.get("joining_date", "").strip(),
                        row.get("status", "Active").strip().capitalize()
                    ))
            conn.commit()
            if should_close:
                cursor.close()
                conn.close()
            logger.info("Database successfully seeded from CSV.")
            return True
        except Exception as e:
            logger.error(f"Error seeding database from CSV: {e}")
            if should_close and conn:
                conn.close()
            return False

    @classmethod
    def get_all_employees(cls, department=None, status=None, search=None):
        cls.init_db()
        conn = cls.get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM employees WHERE 1=1"
        params = []

        if department and department != "All":
            query += " AND LOWER(department) = LOWER(?)"
            params.append(department)

        if status and status != "All":
            query += " AND LOWER(status) = LOWER(?)"
            params.append(status)

        if search:
            query += " AND (LOWER(employee_id) LIKE ? OR LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ? OR LOWER(department) LIKE ? OR LOWER(designation) LIKE ?)"
            term = f"%{search.lower()}%"
            params.extend([term, term, term, term, term])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        employees = []
        for row in rows:
            employees.append(
                Employee(
                    employee_id=row["employee_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                    phone=row["phone"],
                    department=row["department"],
                    designation=row["designation"],
                    salary=float(row["salary"]) if row["salary"] is not None else 0.0,
                    joining_date=row["joining_date"],
                    status=row["status"],
                )
            )
        return employees

    @classmethod
    def search_employee(cls, employee_id):
        cls.init_db()
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE LOWER(employee_id) = LOWER(?)", (employee_id.strip(),))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Employee(
                employee_id=row["employee_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                department=row["department"],
                designation=row["designation"],
                salary=float(row["salary"]) if row["salary"] is not None else 0.0,
                joining_date=row["joining_date"],
                status=row["status"],
            )
        return None

    @classmethod
    def add_employee(cls, employee):
        cls.init_db()
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO employees
            (employee_id, first_name, last_name, email, phone, department, designation, salary, joining_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee.employee_id,
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department,
            employee.designation,
            employee.salary,
            employee.joining_date,
            employee.status,
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @classmethod
    def update_employee(cls, employee_id, update_data):
        cls.init_db()
        conn = cls.get_connection()
        cursor = conn.cursor()

        fields = []
        params = []
        for key, value in update_data.items():
            if key != "employee_id":
                fields.append(f"{key} = ?")
                params.append(value)

        if not fields:
            conn.close()
            return False

        params.append(employee_id)
        query = f"UPDATE employees SET {', '.join(fields)} WHERE LOWER(employee_id) = LOWER(?)"

        cursor.execute(query, params)
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated

    @classmethod
    def update_salary(cls, employee_id, new_salary):
        return cls.update_employee(employee_id, {"salary": float(new_salary)})

    @classmethod
    def delete_employee(cls, employee_id):
        cls.init_db()
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM employees WHERE LOWER(employee_id) = LOWER(?)", (employee_id.strip(),))
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted

    @classmethod
    def get_analytics(cls):
        employees = cls.get_all_employees()
        total_count = len(employees)
        active_count = sum(1 for e in employees if e.is_active())
        inactive_count = total_count - active_count
        total_payroll = sum(e.salary for e in employees)
        avg_salary = (total_payroll / total_count) if total_count > 0 else 0.0

        departments = {}
        for e in employees:
            dept = e.department.strip() if e.department else "Unassigned"
            departments[dept] = departments.get(dept, 0) + 1

        return {
            "total_employees": total_count,
            "active_employees": active_count,
            "inactive_employees": inactive_count,
            "total_payroll": round(total_payroll, 2),
            "average_salary": round(avg_salary, 2),
            "departments": departments,
        }
