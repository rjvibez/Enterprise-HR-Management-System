from models.employee import Employee
from services.db_service import DatabaseService
from utils.logger import logger

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False


class MySQLService:

    @staticmethod
    def get_connection():
        if not MYSQL_AVAILABLE:
            return None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="BrandNewDay@898",
                database="hr_management",
                connection_timeout=2
            )
            return connection
        except Exception as e:
            logger.warning(f"MySQL connection failed ({e}). Falling back to SQLite database service.")
            return None

    @classmethod
    def search_employee(cls, employee_id):
        conn = cls.get_connection()
        if conn is None:
            return DatabaseService.search_employee(employee_id)

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            employee = cursor.fetchone()
            cursor.close()
            conn.close()

            if employee:
                return Employee(
                    employee_id=employee[0],
                    first_name=employee[1],
                    last_name=employee[2],
                    email=employee[3],
                    phone=employee[4],
                    department=employee[5],
                    designation=employee[6],
                    salary=float(employee[7]),
                    joining_date=employee[8],
                    status=employee[9],
                )
            return None
        except Exception as e:
            logger.error(f"MySQL error in search_employee: {e}")
            return DatabaseService.search_employee(employee_id)

    @classmethod
    def get_all_employees(cls):
        conn = cls.get_connection()
        if conn is None:
            return DatabaseService.get_all_employees()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            employees = []
            for row in rows:
                employees.append(
                    Employee(
                        employee_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        email=row[3],
                        phone=row[4],
                        department=row[5],
                        designation=row[6],
                        salary=float(row[7]),
                        joining_date=row[8],
                        status=row[9],
                    )
                )
            return employees
        except Exception as e:
            logger.error(f"MySQL error in get_all_employees: {e}")
            return DatabaseService.get_all_employees()

    @classmethod
    def add_employee(cls, employee):
        conn = cls.get_connection()
        if conn is None:
            return DatabaseService.add_employee(employee)

        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO employees
            (employee_id, first_name, last_name, email, phone,
             department, designation, salary, joining_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
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
            )
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"MySQL error in add_employee: {e}")
            return DatabaseService.add_employee(employee)

    @classmethod
    def update_salary(cls, employee_id, new_salary):
        conn = cls.get_connection()
        if conn is None:
            return DatabaseService.update_salary(employee_id, new_salary)

        try:
            cursor = conn.cursor()
            query = "UPDATE employees SET salary = %s WHERE employee_id = %s"
            cursor.execute(query, (new_salary, employee_id))
            conn.commit()
            updated = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return updated
        except Exception as e:
            logger.error(f"MySQL error in update_salary: {e}")
            return DatabaseService.update_salary(employee_id, new_salary)

    @classmethod
    def update_employee(cls, employee_id, update_data):
        conn = cls.get_connection()
        if conn is None:
            return DatabaseService.update_employee(employee_id, update_data)
        return DatabaseService.update_employee(employee_id, update_data)

    @classmethod
    def delete_employee(cls, employee_id):
        conn = cls.get_connection()
        if conn is None:
            return DatabaseService.delete_employee(employee_id)

        try:
            cursor = conn.cursor()
            query = "DELETE FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return deleted
        except Exception as e:
            logger.error(f"MySQL error in delete_employee: {e}")
            return DatabaseService.delete_employee(employee_id)