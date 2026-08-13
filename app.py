from models.employee import Employee
from services.employee_service import EmployeeService
from utils.logger import logger

# Create Employee Service
employee_service = EmployeeService()

while True:
    print("\n===== Enterprise HR Management System =====")
    print("1. View Employees")
    print("2. Search Employee")
    print("3. Add Employee")
    print("4. Delete Employee")
    print("5. Update Salary")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        employee_service.view_employees()

    elif choice == "2":
        employee_id = input("Enter Employee ID: ").strip()

        employee = employee_service.search_employee(employee_id)

        if employee:
            employee.display_info()
        else:
            print("Employee not found.")

    elif choice == "3":
        employee_id = input("Employee ID: ").strip()

        if not employee_id:
            print("Employee ID cannot be empty.")
            continue

        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        department = input("Department: ")
        designation = input("Designation: ")

        try:
            salary = float(input("Salary: "))
        except ValueError:
            print("Invalid salary. Please enter a numeric value.")
            continue

        joining_date = input("Joining Date (YYYY-MM-DD): ")
        status = input("Status: ")

        new_employee = Employee(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            department=department,
            designation=designation,
            salary=salary,
            joining_date=joining_date,
            status=status,
        )

        employee_service.add_employee(new_employee)

        print("Employee added successfully.")
        logger.info(f"Employee {employee_id} added successfully.")

    elif choice == "4":
        employee_id = input("Enter Employee ID to delete: ").strip()

        if employee_service.delete_employee(employee_id):
            print("Employee deleted successfully.")
        else:
            print("Employee not found.")

    elif choice == "5":
        employee_id = input("Enter Employee ID: ").strip()

        try:
            new_salary = float(input("Enter New Salary: "))
        except ValueError:
            print("Invalid salary. Please enter a numeric value.")
            continue

        if employee_service.update_salary(employee_id, new_salary):
            print("Salary updated successfully.")
        else:
            print("Employee not found.")

    elif choice == "6":
        print("Thank you for using Enterprise HR Management System.")
        break

    else:
        print("Invalid choice. Please try again.")