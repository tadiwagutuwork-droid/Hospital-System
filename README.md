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
│   ├── appointments.csv     # Records of all scheduled visits
│   ├── billing.csv          # Invoices and payment statuses
│   ├── gp.csv               # General Practitioner details
│   ├── medical_records.csv  # Patient clinical history
│   ├── patients.csv         # Personal information of registered patients
│   └── specialist.csv       # Specialist doctor details
│   └── identification.txt       # System IDs or authentication keys
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
```

## OOP Concepts Demonstrated

```
**Encapsulation**
all sensitive attributes use private double-underscore
naming and are accessed only through validated properties. Medical history
returns a copy of the internal list, never the original. Appointment status
can only change through defined transition methods — never set directly.

**Inheritance**
`Patient` and `Doctor` both inherit from the abstract
`Person` class. `GeneralPractitioner` and `Specialist` extend `Doctor`,
each adding their own attributes and overriding key methods. `super().__init__()`
is called correctly throughout the hierarchy.

**Polymorphism**
`get_info()` and `calculate_fee()` are implemented
differently across `GeneralPractitioner` and `Specialist`. A list of mixed
doctor types can be iterated and the same method call produces different
results depending on the actual object type.

**Abstraction**
`Person` uses Python's `ABC` and `@abstractmethod` and
cannot be instantiated directly. `StorageMixin` enforces a consistent
persistence interface across all storable classes by declaring
`save_to_csv()`, `to_dict()`, and `from_dict()` as abstract methods.
```

## Technical Skills Applied

- Python 3 — OOP, relative imports, package structure, `__init__.py`
- `abc` module — abstract base classes and abstract methods
- `csv` module — reading and writing structured data
- `os` module — cross-platform file path handling with `os.path.join()`
- Custom exception handling — meaningful error messages throughout
- Property descriptors — `fget`, `fset`, validated setters and getters
- Git — version controlled throughout development with Git Bash

## How to Run

```bash
git clone https://github.com/tadiwagutuwork-droid/Hospital-System
cd Hospital-System
python main.py
```

## What I Learned

This project taught me more than any tutorial. Key lessons:

- Infinite recursion from wrongly implemented property getters — and why
  the private attribute name must differ from the property name
- How `os.path.join()` makes file paths work across operating systems
- How abstract classes enforce architecture decisions across a codebase
- How to structure a multi-file Python project with relative imports
- How to debug systematically by writing testers for each class in isolation

## Author

Tadiwa Gutu

GitHub: ```https://github.com/tadiwagutuwork-droid```

LinkedIn: ```www.linkedin.com/in/tadiwa-gutu```
