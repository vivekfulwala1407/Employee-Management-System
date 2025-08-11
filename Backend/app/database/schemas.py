from typing import List
from datetime import datetime, timedelta

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
    login_time = attendance.get("log_in_time", "")
    logout_time = attendance.get("log_out_time", "")
    working_hours = calculate_working_hours(login_time, logout_time)

    if employee_details:
        emp = employee_details[0]
        return {
            "empId": emp.get("empId", ""),
            "name": emp.get("name", ""),
            "login_date": str(attendance["login_date"]),
            "log_in_time": login_time,
            "log_out_time": logout_time,
            "working_hours": working_hours
        }
    else:
        original_id = attendance.get("original_employee_id", attendance.get("employee_id", ""))
        return {
            "empId": str(original_id),
            "name": "Unknown Employee",
            "login_date": str(attendance["login_date"]),
            "log_in_time": login_time,
            "log_out_time": logout_time,
            "working_hours": working_hours
        }


def all_enriched_attendance(attendances) -> List[dict]:
    return [enriched_attendance_serial(attendance) for attendance in attendances]

def parse_time(time_str: str) -> str:
    try:
        dt = datetime.strptime(time_str.upper(), "%I:%M %p")
        return dt.strftime("%I:%M %p")
    except ValueError:
        return time_str

def calculate_working_hours(login_time: str, logout_time: str) -> str:
    try:
        format = "%I:%M %p"
        login_dt = datetime.strptime(login_time.strip().upper(), format)
        logout_dt = datetime.strptime(logout_time.strip().upper(), format)

        if logout_dt < login_dt:
            logout_dt += timedelta(days=1)

        duration = logout_dt - login_dt
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours} hrs {minutes} mins"

    except Exception:
        return "Invalid time"

