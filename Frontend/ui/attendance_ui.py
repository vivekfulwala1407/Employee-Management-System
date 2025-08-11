import pandas as pd
import streamlit as st
from data import employee_data, attendance_data
import requests
import time

API_URL = "http://127.0.0.1:8000/api"

def get_employee_names():
    try:
        response = requests.get(f"{API_URL}/employees")
        if response.status_code == 200:
            employees = response.json()
            employee_options = [("All Employees", "")] + [(emp["name"], emp["empId"]) for emp in employees]
            return employee_options
        else:
            return [("All Employees", "")]
    except Exception as e:
        st.error(f"Error fetching employees: {str(e)}")
        return [("All Employees", "")]

def filter_attendance_data(df, selected_name, empid, start_date, end_date):
    filtered_df = df.copy()
    filter_empid = None
    
    if empid and empid.strip():
        filter_empid = empid.strip()

    elif selected_name and selected_name[1]:
        filter_empid = selected_name[1]
    
    if filter_empid:
        filtered_df = filtered_df[filtered_df['empId'] == filter_empid]
    
    if start_date and end_date:
        filtered_df['login_date_dt'] = pd.to_datetime(filtered_df['login_date'], errors='coerce')
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        filtered_df = filtered_df[
            (filtered_df['login_date_dt'] >= start_datetime) & 
            (filtered_df['login_date_dt'] <= end_datetime)
        ]
        filtered_df = filtered_df.drop('login_date_dt', axis=1)
    
    return filtered_df

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
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file, engine="openpyxl")
            elif uploaded_file.name.endswith(".xls"):
                df = pd.read_excel(uploaded_file, engine="xlrd")
            else:
                err = st.error("Unsupported file format. Please upload only csv or Excel file.")
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
    
    employee_options = get_employee_names()
    
    with st.form("filter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_name = st.selectbox(
                "Select Employee Name:",
                options=employee_options,
                format_func=lambda x: x[0],
            )
            empid = st.text_input(
                "Employee ID:",
                placeholder="Enter Employee ID to search",
            )
        
        with col2:
            start_date = st.date_input(
                "Start Date:",
                value=None,
            )
            end_date = st.date_input(
                "End Date:",
                value=None,
            )
        
        col_search, col_clear = st.columns([1, 1])
        with col_search:
            search_clicked = st.form_submit_button("Search", use_container_width=True)
        with col_clear:
            clear_clicked = st.form_submit_button("Clear Filters", use_container_width=True)

    if clear_clicked:
        st.session_state.filtered_data = None
        st.session_state.show_filtered = False
        st.rerun()

    if search_clicked:
        if not st.session_state.attendance.empty:
            if start_date and end_date and start_date > end_date:
                st.error("Start date cannot be after end date!")
            else:
                filtered_data = filter_attendance_data(
                    st.session_state.attendance, 
                    selected_name, 
                    empid, 
                    start_date, 
                    end_date
                )
                st.session_state.filtered_data = filtered_data
                st.session_state.show_filtered = True
        else:
            st.warning("No attendance data available to filter!")

    st.markdown("---")
    if hasattr(st.session_state, 'show_filtered') and st.session_state.show_filtered:
        st.subheader("Attendance Records")
        
        if not st.session_state.filtered_data.empty:            
            display_columns = ['empId', 'name', 'login_date', 'log_in_time', 'log_out_time', 'working_hours']
            st.dataframe(
                st.session_state.filtered_data[display_columns], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No records found matching your filter criteria.")
            
            if st.button("Show All Records"):
                st.session_state.show_filtered = False
                st.rerun()
    
    else:
        st.subheader("All Attendance Records")
        if not st.session_state.attendance.empty:
            st.info(f"Total {len(st.session_state.attendance)} attendance records")
            
            display_columns = ['empId', 'name', 'login_date', 'log_in_time', 'log_out_time', 'working_hours']
            st.dataframe(
                st.session_state.attendance[display_columns], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No attendance records found.")