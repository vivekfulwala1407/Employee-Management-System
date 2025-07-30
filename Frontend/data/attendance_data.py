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
    
    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = None
    
    if "show_filtered" not in st.session_state:
        st.session_state.show_filtered = False
