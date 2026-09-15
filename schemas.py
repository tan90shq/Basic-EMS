# ==============================================================================
# SCHEMAS DEFINITION MODULE
# ==============================================================================
# This module defines the Pydantic models (data schemas) used across the application.
# Pydantic models serve three major purposes in FastAPI:
#   1. Request Validation: Ensuring incoming request payloads match expected types and rules.
#   2. Serialization / Data Modeling: Parsing and structuring data into Python objects.
#   3. API Documentation: Auto-generating OpenAPI / Swagger schemas with constraints & examples.
# ==============================================================================

from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Literal, Optional


# ----------------------------------------------------
# 1. EMPLOYEE CREATION / BASE SCHEMA
# ----------------------------------------------------
# Used for POST '/add'. Every field is mandatory (required) to create a complete profile.
class Employee(BaseModel):
    id: Annotated[str, Field(..., description="ID of the employee", examples=["E001"])]
    name: Annotated[str, Field(..., max_length=50, description="name of the employee")]
    city: Annotated[str, Field(..., description="where the employee lives")]
    age: Annotated[int, Field(..., gt=18, lt=60, description="Age must be strictly between 19 and 59")]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description='must be one of ["male","female","others"]')]
    department: Annotated[Literal["Engineering", "HR", "Finance", "Marketing"], Field(..., description='must be one of ["Engineering","HR","Finance","Marketing"]')]
    designation: Annotated[Literal["Software Engineer", "QA Engineer", "HR Executive", "Recruiter", "Financial Analyst", "Accountant", "Marketing Executive", "Content Specialist"], Field(..., description="valid employee designation")]
    experience: Annotated[int, Field(..., ge=0, description="Years of experience (non-negative)")]
    salary: Annotated[int, Field(..., ge=0, description="Monthly/Annual salary in INR (non-negative)")]
    employment_type: str
    status: Literal["Active", "Inactive"]

    # FIELD VALIDATOR: Automatically clean and normalize ID (e.g. "  e001  " -> "E001")
    @field_validator("id")
    @classmethod
    def id_validator(cls, value: str) -> str:
        return value.strip().upper()


# ----------------------------------------------------
# 2. EMPLOYEE UPDATE SCHEMA (PARTIAL UPDATES)
# ----------------------------------------------------
# Used for PUT '/update/{emp_id}'. Every field defaults to None.
# This allows partial updates: client sends ONLY the fields they wish to update (e.g., just salary).
class EmployeeForUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, max_length=50, description="name of the employee")] = None
    city: Annotated[Optional[str], Field(default=None, description="where the employee lives")] = None
    age: Annotated[Optional[int], Field(default=None, gt=18, lt=60, description="Age must be strictly between 19 and 59")] = None
    gender: Annotated[Optional[Literal["male", "female", "others"]], Field(default=None, description='must be one of ["male","female","others"]')] = None
    department: Annotated[Optional[Literal["Engineering", "HR", "Finance", "Marketing"]], Field(default=None, description='must be one of ["Engineering","HR","Finance","Marketing"]')] = None
    designation: Annotated[Optional[Literal["Software Engineer", "QA Engineer", "HR Executive", "Recruiter", "Financial Analyst", "Accountant", "Marketing Executive", "Content Specialist"]], Field(default=None, description="valid employee designation")] = None
    experience: Annotated[Optional[int], Field(default=None, ge=0, description="Years of experience (non-negative)")] = None
    salary: Annotated[Optional[int], Field(default=None, ge=0, description="Monthly/Annual salary in INR (non-negative)")] = None
    employment_type: Optional[str] = None
    status: Optional[Literal["Active", "Inactive"]] = None