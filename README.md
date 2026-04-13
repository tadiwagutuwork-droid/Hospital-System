# Hospital Management System

A console-based Hospital Management System built entirely in Python from scratch.
This project was designed to demonstrate real-world software engineering principles
— not as a tutorial exercise, but as a fully functional system built through
independent problem solving.

## What It Does

- Register, update, search, and manage patients and doctors
- Book, confirm, complete, and cancel appointments
- Create and view medical records linked to patients and doctors
- Generate bills for completed appointments
- Persist all data to CSV files — loaded on startup, saved on every change
- Custom error handling throughout for robustness

## Project Structure
```
Hospital-System/
├── main.py                  # Entry point
├── data/                    # CSV storage files
├── models/                  # Core class hierarchy
│   ├── __init__.py
│   ├── appointments.py       # Appointment with status transitions
│   ├── doctor.py            # Doctor, GeneralPractitioner, Specialist
│   └── exceptions.py    # MedicalRecord
│   └── medical_records.py    # MedicalRecord
│   ├── patient.py           # Patient (inherits Person)
│   ├── person.py            # Abstract base class
├── storage/                 # Persistence layer
│   ├── __init__.py
│   └── csv_handler.py       # CSV read/write utilities
│   ├── storage_mixin.py     # Abstract StorageMixin
└── menu/                    # Menu layer
│   ├── __init__.py
│   ├── appointment_menu.py
│   ├── billing_menu.py
│   ├── doctor_menu.py     
│   ├── main_menu.py
│   ├──medical_records_menu.py
│   ├── patient_menu.py


