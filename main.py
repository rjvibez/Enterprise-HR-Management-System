from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from services.employee_service import EmployeeService
from models.employee import Employee
from schemas.employee_schema import EmployeeSchema, EmployeeUpdateSchema

app = FastAPI(
    title="Enterprise HR Management System API",
    description="REST API for Enterprise HR Management System",
    version="2.0"
)

# Enable CORS for local and deployment access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

employee_service = EmployeeService()


@app.get("/")
def home():
    return {
        "status": "online",
        "system": "Enterprise HR Management System API",
        "version": "2.0",
        "docs_url": "/docs"
    }


@app.get("/employees")
def get_employees(
    department: Optional[str] = Query(None, description="Filter by department"),
    status: Optional[str] = Query(None, description="Filter by status (Active/Inactive)"),
    search: Optional[str] = Query(None, description="Search term for ID, Name, Designation")
):
    employees = employee_service.get_all_employees(
        department=department,
        status=status,
        search=search
    )
    return [employee.to_dict() for employee in employees]


@app.get("/analytics/summary")
def get_analytics():
    return employee_service.get_analytics_summary()


@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    employee = employee_service.search_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.to_dict()


@app.post("/employees")
def add_employee(employee: EmployeeSchema):
    if employee_service.search_employee(employee.employee_id):
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists."
        )

    new_employee = Employee(
        employee_id=employee.employee_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        phone=employee.phone,
        department=employee.department,
        designation=employee.designation,
        salary=employee.salary,
        joining_date=employee.joining_date,
        status=employee.status,
    )

    employee_service.add_employee(new_employee)
    return {"message": "Employee added successfully", "employee_id": employee.employee_id}


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: str,
    update_data: EmployeeUpdateSchema,
    salary: Optional[float] = Query(None, description="Legacy query param for salary update")
):
    existing = employee_service.search_employee(employee_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")

    data = update_data.model_dump(exclude_unset=True)
    if salary is not None:
        data["salary"] = salary

    if not data:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    success = employee_service.update_employee(employee_id, data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update employee.")

    return {"message": "Employee updated successfully", "employee_id": employee_id}


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    if not employee_service.delete_employee(employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully", "employee_id": employee_id}


@app.post("/seed")
def reseed_database():
    success = employee_service.seed_from_csv()
    if success:
        return {"message": "Database successfully reseeded from CSV"}
    raise HTTPException(status_code=500, detail="Failed to seed database from CSV")