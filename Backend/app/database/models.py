from pydantic import BaseModel, Field
from datetime import date

class Emp(BaseModel):
    empId: str
    name: str
    join_date: date
    status: str
    domain: str

class AttendanceRecord(BaseModel):
    employee_id: str = Field(...)
    login_date: str = Field(...)
    log_in_time: str = Field(...)
    log_out_time: str = Field(...)

