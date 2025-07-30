import time
import streamlit as st
from data import employee_data
import requests

API_URL = "http://127.0.0.1:8000/api/employees"

def render_employee_tab():
    employee_data.initialize_state()

    col_left, col_right = st.columns([8, 2])
    with col_left:
        st.title("Employee Management")
    with col_right:
        if st.button("Add Employee"):
            st.session_state.show_add_form = True
            st.session_state.edit_index = None

    if "show_delete_modal" in st.session_state and st.session_state.show_delete_modal:
        emp_name = st.session_state.get("delete_emp_name", "Unknown")
        emp_id = st.session_state.get("delete_emp_id", "Unknown")
        
        st.markdown("---")
        st.warning("Confirm Delete")
        st.write(f"Are you sure you want to delete employee {emp_name} (ID: {emp_id})?")
        
        col_yes, col_no, col_space = st.columns([1, 2, 6])
        
        with col_yes:
            if st.button("Yes"):
                index = st.session_state.delete_index
                response = requests.delete(f"{API_URL}/{emp_id}")
                if response.status_code == 200:
                    st.success("Employee deleted successfully!")
                    employee_data.delete_employee(index)
                else:
                    st.error("Failed to delete employee.")
                
                st.session_state.show_delete_modal = False
                if "delete_emp_name" in st.session_state:
                    del st.session_state.delete_emp_name
                if "delete_emp_id" in st.session_state:
                    del st.session_state.delete_emp_id
                if "delete_index" in st.session_state:
                    del st.session_state.delete_index
                st.rerun()
        
        with col_no:
            if st.button("Cancel"):
                st.session_state.show_delete_modal = False
                if "delete_emp_name" in st.session_state:
                    del st.session_state.delete_emp_name
                if "delete_emp_id" in st.session_state:
                    del st.session_state.delete_emp_id
                if "delete_index" in st.session_state:
                    del st.session_state.delete_index
                st.rerun()
        
        st.markdown("---")

    if st.session_state.show_add_form and st.session_state.edit_index is None:
        with st.form("add_form", clear_on_submit=True):
            empId = st.text_input("Employee ID")
            name = st.text_input("Employee Name")
            join_date = st.date_input("Join Date")
            status = st.selectbox("Status", ["Active", "Inactive"])
            domain = st.text_input("Domain")
            submitted = st.form_submit_button("Add")
            if submitted:
                if not empId or not name or not domain:
                    st.error("Please fill in all required fields!")
                else:
                    response = requests.post(f"{API_URL}", json={
                        "empId": empId,
                        "name": name,
                        "join_date": str(join_date),
                        "status": status,
                        "domain": domain
                    })
                    if response.status_code == 200:
                        employee_data.add_employee(empId, name, join_date, status, domain)
                        st.success("Employee added successfully!")
                        time.sleep(1)
                        st.session_state.show_add_form = False
                        st.rerun()
                    elif response.status_code == 400:
                        error_detail = response.json().get("detail", "Employee ID already exists!")
                        st.error(error_detail)
                    else:
                        st.error("Failed to add employee. Please try again.")

    if not st.session_state.employees.empty:
        st.subheader("Employee List")

        for index, row in st.session_state.employees.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 1, 1])

            if st.session_state.edit_index == index:
                with col1:
                    new_empId = st.text_input("Edit ID", value=row["empId"], key=f"edit_id_{index}")
                with col2:
                    new_name = st.text_input("Edit Name", value=row["name"], key=f"edit_name_{index}")
                with col3:
                    new_join_date = st.date_input("Edit Join Date", value=row["join_date"], key=f"edit_join_date_{index}")
                with col4:
                    new_status = st.selectbox("Edit Status", ["Active", "Inactive"], index=0 if row["status"] == "Active" else 1, key=f"edit_status_{index}")
                with col5:
                    new_domain = st.text_input("Edit Domain", value=row["domain"], key=f"edit_domain_{index}")
                with col6:
                    if st.button("✔️", key=f"save_{index}"):
                        response = requests.put(f"{API_URL}/{row['empId']}", json={
                            "empId": new_empId,
                            "name": new_name,
                            "join_date": str(new_join_date),
                            "status": new_status,
                            "domain": new_domain
                        })
                        if response.status_code != 200:
                            st.error("Failed to update employee.")
                        else:
                            st.success("Employee updated successfully!")
                        employee_data.update_employee(index, new_empId, new_name, new_join_date, new_status, new_domain)
                        st.session_state.edit_index = None
                        st.rerun()
                with col7:
                    if st.button("╳", key=f"cancel_{index}"):
                        st.session_state.edit_index = None
                        st.rerun()

            else:
                col1.write(row["empId"])
                col2.write(row["name"])
                col3.write(row["join_date"])
                col4.write(row["status"])
                col5.write(row["domain"])
                with col6:
                    if st.button("🖊️", key=f"edit_{index}"):
                        st.session_state.edit_index = index
                        st.session_state.show_add_form = False
                        st.rerun()
                with col7:
                    if st.button("🗑️", key=f"delete_{index}"):
                        st.session_state.show_delete_modal = True
                        st.session_state.delete_emp_name = row["name"]
                        st.session_state.delete_emp_id = row["empId"]
                        st.session_state.delete_index = index
                        st.rerun()