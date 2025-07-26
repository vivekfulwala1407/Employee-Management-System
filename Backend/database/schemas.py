from typing import List
from datetime import datetime

def individual_employee(emp):
    return {
        "empId": str(emp["empId"]),
        "name": str(emp["name"]),
        "join_date": str(emp["join_date"]),
        "status": str(emp["status"]),
        "domain": str(emp["domain"])
    }

def all_employees(emps):
    return [individual_employee(emp) for emp in emps]


# def individual_attendance(attendance_record):
#     return {
#         "employee_id": str(attendance_record.get("employee_id", "")),
#         "login_date": str(attendance_record["login_date"]),
#         "log_in_time": str(attendance_record["log_in_time"]),
#         "log_out_time": str(attendance_record["log_out_time"]),
#     }

# def all_attendance(att):
#     return [individual_attendance(attendance_record) for attendance_record in att]

def individual_serial(attendance) -> dict:
    return {
        "employee_id": attendance["employee_id"],
        "login_date": str(attendance["login_date"]),
        "log_in_time": attendance["log_in_time"],
        "log_out_time": attendance["log_out_time"]
    }

def list_serial(attendances) -> List[dict]:
    return [individual_serial(attendance) for attendance in attendances]

def parse_time(time_str: str) -> str:
    """Convert time string to consistent format"""
    try:
        dt = datetime.strptime(time_str.upper(), "%I:%M %p")
        return dt.strftime("%I:%M %p")
    except ValueError:
        return time_str