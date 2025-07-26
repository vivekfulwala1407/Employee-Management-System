from fastapi import FastAPI, APIRouter, HTTPException, UploadFile , File
from config import collection, attendance_collection
from database.models import Emp, AttendanceRecord
from database.schemas import all_employees, individual_employee, list_serial, parse_time, individual_serial
# from database.schemas import  individual_attendance, all_attendance
import csv
from io import StringIO
from datetime import datetime
from typing import List

app = FastAPI()
# router = APIRouter()
router = APIRouter(prefix="/api", tags=["emp"])

# @router.get("/")
# async def read_root():
#     return {"message": "Welcome"}

@router.get("/employees")
async def get_employees():
    emps = collection.find( )
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
    attendances = attendance_collection.find()
    return list_serial(attendances)

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
        csv_data = StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(csv_data)
        
        records = []
        for row in reader:
            try:
                record = {
                    "employee_id": row["employee_id"].strip(),
                    "login_date": row["login_date"].strip(),
                    "log_in_time": parse_time(row["log_in_time"].strip()),
                    "log_out_time": parse_time(row["log_out_time"].strip())
                }
                records.append(record)

            except Exception as e:
                raise HTTPException(status_code=422, detail=f"Error in row: {str(e)}")
        
        if records:
            result = attendance_collection.insert_many(records)
            return {
                "message": "Upload successful",
                "inserted_count": len(result.inserted_ids)
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        await file.close()

app.include_router(router)
   # will get the data from the file and convert it to our format suppose JSON format
   # will save data to backend and return the data