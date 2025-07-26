import pandas as pd
import streamlit as st
from data import employee_data, attendance_data
import requests
import time

API_URL = "http://127.0.0.1:8000/api/attendance"

def render_attendance_tab():
    employee_data.initialize_state()
    st.title("Attendance Overview")

    st.markdown("---")

    st.subheader("Upload Attendance File")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            success = st.success("CSV File Loaded Successfully!")
            if success:
                response = requests.post(f"{API_URL}", files={"file": uploaded_file})
                if response.status_code == 200:
                    uploaded_data = response.json()
                    st.session_state.attendance = pd.DataFrame(uploaded_data)
                else:
                    st.error("Failed to store data.")
            time.sleep(1.5)
            success.empty()
            st.dataframe(df)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            success = st.success("Excel File Loaded Successfully!")
            if success:
                response = requests.post(f"{API_URL}", files={"file": uploaded_file})
                if response.status_code == 200:
                    uploaded_data = response.json()
                    st.session_state.attendance = pd.DataFrame(uploaded_data)
                else:
                    st.error("Failed to store data.")
            time.sleep(1.5)
            success.empty()
            st.dataframe(df)
        else:
            err = st.error("Unsupported file format. Please upload a .csv or Excel file.")
            time.sleep(1.5)
            err.empty()

    attendance_data.initialize_state()

    st.subheader("Attendance Records")

    if not st.session_state.attendance.empty:
        st.dataframe(st.session_state.attendance)
    else:
        null = st.info("No attendance records found.")
        time.sleep(2)
        null.empty()

