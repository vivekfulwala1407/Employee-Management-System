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

def individual_serial(attendance) -> dict:
    return {
        "employee_id": attendance.get("employee_id", ""),
        "login_date": str(attendance["login_date"]),
        "log_in_time": attendance["log_in_time"],
        "log_out_time": attendance["log_out_time"]
    }

def list_serial(attendances) -> List[dict]:
    return [individual_serial(attendance) for attendance in attendances]

def enriched_attendance_serial(attendance) -> dict:
    employee_details = attendance.get("employee_details", [])
    
    if employee_details:
        emp = employee_details[0]
        return {
            "empId": emp.get("empId", ""),
            "name": emp.get("name", ""),
            "login_date": str(attendance["login_date"]),
            "log_in_time": attendance["log_in_time"],
            "log_out_time": attendance["log_out_time"]
        }
    else:
        original_id = attendance.get("original_employee_id", attendance.get("employee_id", ""))
        return {
            "empId": str(original_id),
            "name": "Unknown Employee",
            "login_date": str(attendance["login_date"]),
            "log_in_time": attendance["log_in_time"],
            "log_out_time": attendance["log_out_time"]
        }

def all_enriched_attendance(attendances) -> List[dict]:
    return [enriched_attendance_serial(attendance) for attendance in attendances]

def parse_time(time_str: str) -> str:
    try:
        dt = datetime.strptime(time_str.upper(), "%I:%M %p")
        return dt.strftime("%I:%M %p")
    except ValueError:
        return time_str