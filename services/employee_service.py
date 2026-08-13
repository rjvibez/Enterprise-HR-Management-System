from services.db_service import DatabaseService
from services.mysql_service import MySQLService


class EmployeeService:

    def __init__(self, employees=None):
        self.employees = employees if employees else []

    def add_employee(self, employee):
        return DatabaseService.add_employee(employee)

    def get_all_employees(self, department=None, status=None, search=None):
        return DatabaseService.get_all_employees(department=department, status=status, search=search)

    def view_employees(self):
        employees = self.get_all_employees()

        if not employees:
            print("No employees found.")
            return

        for employee in employees:
            employee.display_info()

    def search_employee(self, employee_id):
        return DatabaseService.search_employee(employee_id)

    def update_employee(self, employee_id, update_data):
        return DatabaseService.update_employee(employee_id, update_data)

    def update_salary(self, employee_id, new_salary):
        return DatabaseService.update_salary(employee_id, new_salary)

    def delete_employee(self, employee_id):
        return DatabaseService.delete_employee(employee_id)

    def get_analytics_summary(self):
        return DatabaseService.get_analytics()

    def seed_from_csv(self, csv_path=None):
        if csv_path:
            return DatabaseService.seed_from_csv(csv_path)
        return DatabaseService.seed_from_csv()