# 🏢 Employee Management System API

A lightweight RESTful API built with **FastAPI** and **Pydantic** to manage employee records with full CRUD (Create, Read, Update, Delete) operations and file-based JSON persistence.

This project was developed as a hands-on milestone to explore backend architecture, REST API conventions, request schema validation, and parameter handling in modern Python.

---

## 🚀 Features

- **Full CRUD Capabilities**:
  - `GET /view`: Retrieve all employee records.
  - `GET /emp/{employee_id}`: Search for an employee by unique ID.
  - `GET /sort`: Sort employee records by age, experience, or salary in ascending or descending order.
  - `POST /add`: Add new employee records with strict schema validation.
  - `PUT /update/{emp_id}`: Partially update specific employee fields dynamically.
  - `DELETE /delete/{emp_id}`: Remove an employee record from the system.
- **Robust Schema Validation**: Powered by Pydantic v2 with custom field validators (e.g., ID auto-uppercasing and whitespace trimming), value ranges, and constrained literal types for departments and designations.
- **Interactive Documentation**: Auto-generated OpenAPI / Swagger UI and ReDoc pages available out of the box.
- **Zero Heavy Setup**: File-backed storage (`employees.json`) allows running without setting up external database servers.

---

## 🛠️ Tech Stack

- **Python 3**
- **FastAPI**: Modern, fast web framework for building APIs.
- **Pydantic v2**: Data validation and parsing using Python type hints.
- **Uvicorn**: Lightning-fast ASGI server implementation.

---

## 📁 Project Structure

```text
Basic-Employee-Manangment-System/
│
├── main.py              # FastAPI app instance, endpoints, and storage logic
├── schemas.py           # Pydantic schemas (Employee & EmployeeForUpdate)
├── employees.json       # JSON data store for employee records
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ⚡ Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Basic-Employee-Manangment-System
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API Server
```bash
uvicorn main:app --reload
```

The application will be live at `http://127.0.0.1:8000`.

---

## 📖 API Documentation & Endpoints

Once the application is running, access the interactive documentation directly in your browser:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Summary of Routes

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Service health status check |
| `GET` | `/about` | Brief API overview |
| `GET` | `/view` | Retrieve full list of employees |
| `GET` | `/emp/{employee_id}` | Retrieve single employee by ID (e.g., `E001`) |
| `GET` | `/sort?sort_by={field}&order={order}` | Sort by `age`, `salary`, or `experience` (`asec` / `desc`) |
| `POST` | `/add` | Add a new employee record |
| `PUT` | `/update/{emp_id}` | Update existing employee details |
| `DELETE` | `/delete/{emp_id}` | Delete an employee by ID |

---

## 📝 Example Request Payload (`POST /add`)

```json
{
  "id": "E015",
  "name": "Arjun Sharma",
  "city": "Bengaluru",
  "age": 28,
  "gender": "male",
  "department": "Engineering",
  "designation": "Software Engineer",
  "experience": 3,
  "salary": 72000,
  "employment_type": "Full-time",
  "status": "Active"
}
```

