class Employee:
    def __init__(
        self,
        employee_id,
        first_name,
        last_name,
        email,
        phone,
        department,
        designation,
        salary,
        joining_date,
        status,
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.department = department
        self.designation = designation
        self.salary = salary
        self.joining_date = joining_date
        self.status = status

    def display_info(self):
        print(f"Employee ID : {self.employee_id}")
        print(f"Name        : {self.first_name} {self.last_name}")
        print(f"Department  : {self.department}")
        print(f"Designation : {self.designation}")
        print(f"Salary      : {self.salary}")
        print(f"Status      : {self.status}")
        print("-" * 30)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_salary(self, new_salary):
        self.salary = new_salary

    def increment_salary(self, percentage):
        self.salary += self.salary * (percentage / 100)

    def update_department(self, new_department):
        self.department = new_department

    def update_status(self, new_status):
        self.status = new_status

    def change_designation(self, new_designation):
        self.designation = new_designation

    def is_active(self):
        return str(self.status).strip().lower() == "active"

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "designation": self.designation,
            "salary": float(self.salary) if self.salary is not None else 0.0,
            "joining_date": str(self.joining_date),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            employee_id=str(data.get("employee_id", "")),
            first_name=str(data.get("first_name", "")),
            last_name=str(data.get("last_name", "")),
            email=str(data.get("email", "")),
            phone=str(data.get("phone", "")),
            department=str(data.get("department", "")),
            designation=str(data.get("designation", "")),
            salary=float(data.get("salary", 0.0)),
            joining_date=str(data.get("joining_date", "")),
            status=str(data.get("status", "Active")),
        )