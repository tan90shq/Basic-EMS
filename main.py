# ==============================================================================
# EMPLOYEE MANAGEMENT SYSTEM - REST API
# ==============================================================================
# This module implements a RESTful API for managing employee records using FastAPI.
# It supports full CRUD (Create, Read, Update, Delete) operations, input validation,
# custom error handling, and JSON-based file persistence.
# ==============================================================================

# Core framework imports for routing, parameter validation, and HTTP exceptions
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from schemas import Employee, EmployeeForUpdate


# ----------------------------------------------------
# APPLICATION INSTANCE
# ----------------------------------------------------
# Registers the FastAPI app and builds interactive documentation at /docs and /redoc
app = FastAPI(title="Employee Management System API", description="Complete Full CRUD API (GET, POST, PUT, DELETE).")


# ----------------------------------------------------
# HELPER FUNCTIONS: FILE PERSISTENCE (READ / WRITE)
# ----------------------------------------------------
def data_loader():
    # Opens 'employees.json' in read mode ("r") and parses JSON text into a Python list of dictionaries
    with open("employees.json", "r") as f:
        data = json.load(f)
    return data


def data_paster(data):
    # Opens 'employees.json' in write mode ("w") and saves the Python list as formatted JSON (indent=2)
    with open("employees.json", "w") as f:
        json.dump(data, f, indent=2)
    return data


# ----------------------------------------------------
# 1. READ: Standard GET Endpoints
# ----------------------------------------------------
@app.get("/")
def home():
    # Root endpoint returning a basic welcoming dictionary serialized to JSON
    return {"message": "This is Employee Management System"}


@app.get("/health")
def health_check():
    # Health check endpoint for uptime and container health monitoring
    return {'status': 'OK'}


@app.get("/about")
def about():
    # Simple GET route providing introductory information about this API
    return {"About": "this is a sample api."}


@app.get("/view")
def view():
    # Reads all employee records from 'employees.json' and returns the full list
    data = data_loader()
    return data


# ----------------------------------------------------
# 1. READ (by ID): View Single Employee with Path Parameter
# Example: /emp/E005
# ----------------------------------------------------
@app.get("/emp/{employee_id}")
def view_emp(employee_id: str = Path(..., description="Enter valid employee ID", examples=["E005"])):
    # Step 1: Load employee list from storage
    data = data_loader()

    # Step 2: Search for an employee with matching ID (case-insensitive with .upper())
    for employee in data:
        if employee_id.upper() == employee["id"]:
            return employee  # Match found! Return employee dictionary (HTTP 200 OK)

    # Step 3: If loop completes without match, raise HTTP 404 Not Found error
    raise HTTPException(status_code=404, detail="Employee not found")


# ----------------------------------------------------
# 1. READ (Sorted): Sort Employees with Query Parameters
# Example: /sort?sort_by=salary&order=desc
# ----------------------------------------------------
@app.get("/sort")
def sort(sort_by: str = Query(..., description="choose from age, salary or experience"), order: str = Query("asec", description="choose between asec or desc")):
    valid_options = ["age", "experience", "salary"]

    # Validation 1: Check if requested sort field is supported
    if sort_by not in valid_options:
        raise HTTPException(status_code=400, detail=f"Enter valid option : {valid_options}")

    # Validation 2: Check if sort order is valid ('asec' or 'desc')
    if order not in ["asec", "desc"]:
        raise HTTPException(status_code=400, detail="Enter valid option : ['asec','desc']")

    # Load data and sort using Python's sorted() with lambda key and ternary reverse flag
    data = data_loader()
    return sorted(data, key=lambda item: item[sort_by], reverse=False if order == "asec" else True)


# ----------------------------------------------------
# 2. CREATE: POST Endpoint (Add New Employee)
# URL: http://127.0.0.1:8000/add
# ----------------------------------------------------
@app.post("/add")
def add_employee(employee: Employee):
    # Step 1: Read current employee list from disk into memory
    data = data_loader()

    # Step 2: Prevent duplicate IDs - check if employee ID already exists
    for i in data:
        if employee.id == i["id"]:
            raise HTTPException(status_code=400, detail="Employee already exists")

    # Step 3: Convert Pydantic model instance into dictionary and append to list
    data.append(employee.model_dump())

    # Step 4: Save updated list back to file and return HTTP 201 Created
    data_paster(data)
    return JSONResponse(status_code=201, content={"message": "Employee data successfully added"})


# ----------------------------------------------------
# 3. UPDATE: PUT Endpoint (Partial / Full Update)
# URL: http://127.0.0.1:8000/update/{emp_id}
# ----------------------------------------------------
# Takes 'emp_id' from URL path and 'update_emp' from JSON request body
@app.put("/update/{emp_id}")
def update(emp_id: str, update_emp: EmployeeForUpdate):
    # Step 1: Load employee list from disk
    data = data_loader()

    # Step 2: Search for matching employee using Python's for-else loop construct:
    # - If found: executes 'break' to immediately exit the loop, skipping the 'else:' block.
    # - If NOT found: loop finishes naturally without break, triggering the 'else:' block.
    for emp_data in data:
        if emp_id.upper() == emp_data["id"]:
            break
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Step 3: Extract ONLY the fields explicitly provided in request payload (exclude_unset=True)
    update_requested = update_emp.model_dump(exclude_unset=True)

    # Step 4: Mutate the employee dictionary directly in place
    for key, value in update_requested.items():
        emp_data[key] = value

    # Step 5: Save the mutated list to disk and return HTTP 200 OK
    data_paster(data)
    return JSONResponse(status_code=200, content={"message": "Employee data successfully updated"})


# ----------------------------------------------------
# 4. DELETE: DELETE Endpoint (Remove Employee)
# URL: http://127.0.0.1:8000/delete/{emp_id}
# ----------------------------------------------------
@app.delete("/delete/{emp_id}")
def data_delete(emp_id: str):
    # Step 1: Load employee list from storage
    data = data_loader()

    # Step 2: Search for matching employee using for-else loop construct
    for emp_data in data:
        if emp_id.upper() == emp_data["id"]:
            break
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Step 3: Remove the matching employee dictionary from the list
    data.remove(emp_data)

    # Step 4: Save the updated list back to file and return HTTP 200 OK
    data_paster(data)
    return JSONResponse(status_code=200, content={"message": "Employee deleted successfully"})
    