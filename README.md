# Employee Management System

A comprehensive, secure employee management system with role-based authentication, audit logging, and attendance tracking capabilities.

## Installation

### 1. Clone the Repository

git clone https://github.com/vivekfulwala1407/Employee-Management-System.git  
cd employee-management-system


### 2. Create Virtual Environment

python -m venv venv

# macOS
source venv/bin/activate


### 3. Install Dependencies

pip install -r requirements.txt



## Running the Application

### Start the Backend API

uvicorn main:app --reload


### Start the Frontend UI

streamlit run streamlit_app.py
