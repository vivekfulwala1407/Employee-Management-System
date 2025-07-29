import pandas as pd
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/attendance"

def initialize_state():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            attendance_data = response.json()
            if attendance_data:
                st.session_state.attendance = pd.DataFrame(attendance_data)
            else:
                st.session_state.attendance = pd.DataFrame(columns=[
                    "empId", 
                    "name",
                    "login_date", 
                    "log_in_time", 
                    "log_out_time"
                ])
        else:
            st.error("Failed to load attendance data from API.")
            st.session_state.attendance = pd.DataFrame(columns=[
                "empId", 
                "name",
                "login_date", 
                "log_in_time", 
                "log_out_time"
            ])
    except Exception as e:
        st.error(f"Error loading attendance data: {str(e)}")
        st.session_state.attendance = pd.DataFrame(columns=[
            "empId", 
            "name",
            "login_date", 
            "log_in_time", 
            "log_out_time"
        ])

    if "show_upload_form" not in st.session_state:
        st.session_state.show_upload_form = False

def add_attendance(employee_id, login_date, log_in_time, log_out_time):
    new_entry = {
        "empId": employee_id,
        "name": "Manual Entry",
        "login_date": login_date,
        "log_in_time": log_in_time,
        "log_out_time": log_out_time,
        "status": "manual"
    }
    
    new_df = pd.DataFrame([new_entry])
    st.session_state.attendance = pd.concat(
        [st.session_state.attendance, new_df],
        ignore_index=True
    )

def process_uploaded_file(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")
        
        required_columns = ["employee_id", "login_date", "log_in_time", "log_out_time"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in uploaded file")
        
        df["status"] = "uploaded"
        df.rename(columns={"employee_id": "empId"}, inplace=True)
        df["name"] = "Unknown" 
        
        st.session_state.attendance = pd.concat(
            [st.session_state.attendance, df],
            ignore_index=True
        )
        return True
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return False

def get_attendance_records():
    """Return current attendance records"""
    return st.session_state.attendance.copy()

def clear_attendance_data():
    """Clear all attendance records"""
    st.session_state.attendance = pd.DataFrame(columns=[
        "empId", 
        "name",
        "login_date", 
        "log_in_time", 
        "log_out_time",
        "status"
    ])