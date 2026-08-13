import csv
from models.employee import Employee


class CSVService:

    @staticmethod
    def load_employees(file_path):
        employees = []

        with open(file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                employee = Employee(
                    employee_id=row["employee_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                    phone=row["phone"],
                    department=row["department"],
                    designation=row["designation"],
                    salary=float(row["salary"]),
                    joining_date=row["joining_date"],
                    status=row["status"],
                )

                employees.append(employee)

        return employees

    @staticmethod
    def save_employees(file_path, employees):
        with open(file_path, mode="w", newline="") as file:
            fieldnames = [
                "employee_id",
                "first_name",
                "last_name",
                "email",
                "phone",
                "department",
                "designation",
                "salary",
                "joining_date",
                "status",
            ]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for employee in employees:
                writer.writerow(
                    {
                        "employee_id": employee.employee_id,
                        "first_name": employee.first_name,
                        "last_name": employee.last_name,
                        "email": employee.email,
                        "phone": employee.phone,
                        "department": employee.department,
                        "designation": employee.designation,
                        "salary": employee.salary,
                        "joining_date": employee.joining_date,
                        "status": employee.status,
                    }
                )