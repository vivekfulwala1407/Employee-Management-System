from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from config import collection, attendance_collection
from database.models import Emp, AttendanceRecord
from database.schemas import all_employees, individual_employee, list_serial, parse_time, individual_serial, enriched_attendance_serial, all_enriched_attendance
from pymongo import errors as pymongo_errors
import csv
from io import StringIO
from datetime import datetime
from typing import List
from bson import ObjectId

app = FastAPI()
router = APIRouter(prefix="/api", tags=["emp"])

@router.get("/employees")
async def get_employees():
    emps = collection.find()
    return all_employees(emps)

@router.get("/employees/{empId}")
async def get_employee(empId: str):
    emp = collection.find_one({"empId": empId})
    if emp:
        return individual_employee(emp)
    raise HTTPException(status_code=404, detail="Employee not found")

@router.post("/employees")
async def create_employee(emp: Emp):
    try:
        emp_dict = emp.dict()
        emp_dict["join_date"] = str(emp_dict["join_date"])
        data = collection.insert_one(emp_dict)
        return {"status_code": 200, "empId": str(data.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Some error occurred: {e}")

@router.put("/employees")
async def update_employee(emp: Emp):
    try:
        emp_dict = emp.dict()
        emp_dict["join_date"] = str(emp_dict["join_date"])
        data = collection.update_one({"empId": emp.empId}, {"$set": emp_dict})
        if data.modified_count == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"status_code": 200, "message": "Employee updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Some error occurred: {e}")

@router.put("/employees/{empId}")
async def update_employee_by_id(empId: str, emp: Emp):
    try:
        emp_dict = emp.dict()
        emp_dict["join_date"] = str(emp_dict["join_date"])
        data = collection.update_one({"empId": empId}, {"$set": emp_dict})
        if data.modified_count == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"status_code": 200, "message": "Employee updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Some error occurred: {e}")

@router.delete("/employees/{empId}")
async def delete_employee(empId: str):
    try:
        data = collection.delete_one({"empId": empId})
        if data.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"status_code": 200, "message": "Employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Some error occurred: {e}")

@router.get("/attendance", response_model=List[dict])
async def get_all_attendance():
    pipeline = [
        {
            "$lookup": {
                "from": "employees",
                "let": {"emp_id": "$employee_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$or": [
                                    {"$eq": ["$_id", "$$emp_id"]}, 
                                    {"$eq": ["$empId", "$$emp_id"]} 
                                ]
                            }
                        }
                    }
                ],
                "as": "employee_details"
            }
        }
    ]
    
    attendances = list(attendance_collection.aggregate(pipeline))
    return all_enriched_attendance(attendances)

@router.get("/attendance/{employee_id}", response_model=dict)
async def get_employee_attendance(employee_id: str):
    attendance = attendance_collection.find_one({"employee_id": employee_id})
    if not attendance:
        raise HTTPException(status_code=404, detail="Employee not found")
    return individual_serial(attendance)

@router.post("/attendance/upload", status_code=201)
async def upload_attendance(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        try:
            csv_data = StringIO(contents.decode('utf-8'))
        except UnicodeDecodeError:
            raise HTTPException(422, "File must be UTF-8 encoded")

        reader = csv.DictReader(csv_data)
        
        if not reader.fieldnames:
            raise HTTPException(422, "CSV has no headers")
        
        required = {"employee_id", "login_date", "log_in_time", "log_out_time"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise HTTPException(422, f"Missing columns: {', '.join(missing)}")

        employees = list(collection.find({}, {"empId": 1, "_id": 1}))
        employee_map = {emp["empId"]: emp["_id"] for emp in employees}

        records = []
        matched_count = 0
        unmatched_count = 0
        
        for i, row in enumerate(reader, 1):
            try:
                employee_id = row["employee_id"].strip()
                if employee_id in employee_map:
                    matched_employee_id = employee_map[employee_id]
                    matched_count += 1
                else:
                    matched_employee_id = employee_id
                    unmatched_count += 1
                
                records.append({
                    "employee_id": matched_employee_id,
                    "login_date": row["login_date"].strip(),
                    "log_in_time": parse_time(row["log_in_time"].strip()),
                    "log_out_time": parse_time(row["log_out_time"].strip())
                })
            except Exception as e:
                raise HTTPException(422, f"Row {i} error: {str(e)}")

        if not records:
            raise HTTPException(400, "No valid records found")
        
        try:
            result = attendance_collection.insert_many(records)
            return {
                "message": "Upload successful",
                "inserted_count": len(result.inserted_ids),
                "matched_employees": matched_count,
                "unmatched_employees": unmatched_count
            }
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")
    finally:
        await file.close()

app.include_router(router)
