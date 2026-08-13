from typing import Optional
from pydantic import BaseModel, EmailStr


class EmployeeSchema(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    department: str
    designation: str
    salary: float
    joining_date: str
    status: str = "Active"


class EmployeeUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[str] = None
    status: Optional[str] = None