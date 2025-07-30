import streamlit as st
from ui import employee_ui, attendance_ui

tab = st.sidebar.selectbox("Choose Tab", ["Employees", "Attendance"])

if tab == "Employees":
    employee_ui.render_employee_tab()
elif tab == "Attendance":
    attendance_ui.render_attendance_tab()

