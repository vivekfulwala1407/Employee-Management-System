import pandas as pd
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/employees"

def initialize_state():
    if "employees" not in st.session_state:
        response = requests.get(API_URL)
        if response.status_code == 200:
            st.session_state.employees = pd.DataFrame(response.json())
        else:
            st.session_state.employees = pd.DataFrame(columns=["empId", "name", "join_date", "status", "domain"])

    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None

def add_employee(empId, name, join_date, status, domain):
    new_entry = {
        "empId": empId,
        "name": name,
        "join_date": join_date,
        "status": status,
        "domain": domain
    }
    st.session_state.employees = pd.concat(
        [st.session_state.employees, pd.DataFrame([new_entry])],
        ignore_index=True
    )

def update_employee(index, empId, name, join_date, status, domain):
    st.session_state.employees.loc[index, "empId"] = empId
    st.session_state.employees.loc[index, "name"] = name
    st.session_state.employees.loc[index, "join_date"] = join_date
    st.session_state.employees.loc[index, "status"] = status
    st.session_state.employees.loc[index, "domain"] = domain

def delete_employee(index):
    st.session_state.employees.loc[index, "status"] = "Inactive"

