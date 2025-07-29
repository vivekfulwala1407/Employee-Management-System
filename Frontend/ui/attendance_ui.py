import pandas as pd
import streamlit as st
from data import employee_data, attendance_data
import requests
import time

API_URL = "http://127.0.0.1:8000/api"

def render_attendance_tab():
    employee_data.initialize_state()
    st.title("Attendance Overview")
    st.markdown("---")
    st.subheader("Upload Attendance File")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(uploaded_file)
            else:
                err = st.error("Unsupported file format. Please upload a .csv or Excel file.")
                time.sleep(1.5)
                err.empty()
                return

            with st.spinner("Uploading file..."):
                try:
                    response = requests.post(
                        f"{API_URL}/attendance/upload",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                    )
                    
                    if response.status_code == 201:
                        result = response.json()
                        st.success(f"Upload successful! Inserted {result['inserted_count']} records - Matched: {result['matched_employees']}, Unmatched: {result['unmatched_employees']}")
                        attendance_data.initialize_state()
                        time.sleep(1)
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
            
                except Exception as e:
                    st.error(f"Upload failed: {str(e)}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            time.sleep(1.5)

    attendance_data.initialize_state()

    st.markdown("---")
    st.subheader("Attendance Records")

    if not st.session_state.attendance.empty:
        st.dataframe(st.session_state.attendance, use_container_width=True)
    
        
    else:
        st.info("No attendance records found.")