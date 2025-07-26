from pydantic import BaseModel, Field
from datetime import date

class Emp(BaseModel):
    empId: str
    name: str
    join_date: date
    status: str
    domain: str

# class AttendanceRecord(BaseModel):
#     employee_id: str
#     login_date: date
#     log_in_time: str
#     log_out_time: str

    # employee_id: str = Field(..., example="EMP001")
    # login_date: date = Field(..., example="2025-07-01")
    # log_in_time: str = Field(..., example="9:00 AM")
    # log_out_time: str = Field(..., example="6:00 PM")

class AttendanceRecord(BaseModel):
    employee_id: str = Field(..., examples=["EMP001"])
    login_date: str = Field(..., examples=["2025-07-01"])
    log_in_time: str = Field(..., examples=["9:00 AM"])
    log_out_time: str = Field(..., examples=["6:00 PM"])