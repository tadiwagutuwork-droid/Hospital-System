from models import Appointments
from models import Patient
from models import exceptions as excp
import os
import csv
import datetime

# import datetime

# current_date = datetime.date.today()
# current_time = datetime.datetime.now().time()
# ALSO ADD YOUR OWN INPUT DATE - for schedules

def filepath_func_gp():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'gp.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")
    return filepath

def filepath_func_sp():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'specialist.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")
    return filepath

def get_filepath():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'appointments.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")
    return filepath


def read_csv(filepath):
    with open(filepath, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        fieldnames = reader.fieldnames
    
    return rows, fieldnames

def write_csv(filepath, to_write, fieldnames):
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(to_write)

def validate_patientID(id):
    id = (id.upper()).strip()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'patients.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")
    if id[0] != 'P' and len(id) != 5:
        raise excp.InvalidDoctorIDError()
    
    rows, fieldnames = read_csv(filepath)
    
    match = [row for row in rows if row['Patient ID'] == id]
    if not match:
        raise excp.PatientNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID('Patient')
    else:
        return id

def validate_doctor(filepath, id):
    id = (id.upper()).strip()
    if id[0] != 'D' and len(id) != 5:
        raise excp.InvalidDoctorIDError()
    
    rows, fieldnames = read_csv(filepath)
    
    match = [row for row in rows if row['Doctor ID'] == id]
    if not match:
        raise excp.DoctorNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID('Doctor')
    else:
        print("Valid Doctor ID")
        return id

def validate_appointment(filepath, id):
    id = (id.upper()).strip()
    if id[0] != 'A' and len(id) != 5:
        raise excp.InvalidAppointmentIDError()
    
    rows, fieldnames = read_csv(filepath)
    
    match = [row for row in rows if row['Appointment ID'] == id]
    if not match:
        raise excp.AppointmentNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID('Appointment')
    else:
        print("Valid Appointment ID")
        return id, match

def validate_doctorID(id):
    menu = """
===== TYPE OF DOCTOR ====
1. General Practitioner
2. Specialist
=====================
Enter your choice: """
        
    choice = int(input(menu))

    if not (1 <= choice <= 2):
        raise ValueError("Invalid Input")
    elif choice == 1:
        filepath = filepath_func_gp()
        return validate_doctor(filepath, id)
    else:
        filepath = filepath_func_sp()
        return validate_doctor(filepath, id)

def get_fee(doctor_id, choice):
    filepath = fee = None
    if choice == 1:
        filepath = filepath_func_gp()
        fee = 'Consultation Fee'
    else:
        filepath = filepath_func_sp()
        fee = 'Procedure Fee'
    
    rows, fieldnames = read_csv(filepath)
    data = [row for row in rows if row['Doctor ID'] == doctor_id]
    if not data:
        raise excp.DoctorNotFoundError()
    elif len(data) > 1:
        raise excp.DuplicateID('Doctor')
        d = data[0]
        return  d[fee]

def search_appointment(id):
    filepath = get_filepath()
    id, match = validate_appointment(filepath, id)

    rows, fieldnames = read_csv(filepath)
    row = match[0]
    instance = Appointments(row['Patient ID'], row['Doctor ID'], row['Specialisation'], row['Fee'], row['Date'], row['Time'], row['Notes'], row['Appointment ID'], row['Paid'], _loading=True)
    return instance
    
def book_appointment():
    try:
        #self, patient, doctor, specialisation, fee, date: str, time: str, notes: str, appointment_id=None, paid=False, _loading =False
        date = input("Enter date (DD-MM-YYYY): ")
        valid_date = datetime.strptime(date, "%d-%m-%Y")
        time = input("Enter time (HH:MM) in 24h format: ")
        valid_time = datetime.strptime(time, "%H:%M").time()

        patient_id = validate_patientID(input("Enter patient's ID:"))
        doctor_id = validate_doctorID(input("Enter doctor's ID:"))
        specialisation = None
        menu = """
===== TYPE OF DOCTOR ====
1. General Practitioner
2. Specialist
=====================
Enter your choice: """
        
        choice = int(input(menu))
        if not (1 <= choice <= 2):
            raise ValueError("Invalid Input")
        elif choice == 1:
            specialisation = 'General Practitioner'
        else:
            specialisation = 'Specialist'

        notes = input("Enter additional notes:")
        fee = get_fee(doctor_id, choice)
        appointment = Appointments(patient_id, doctor_id, specialisation, fee, valid_date, valid_time, notes)
    except ValueError as e:
        print("Error:", e)


def view_all_appointments():
    filepath = get_filepath()
    rows, fieldnames = read_csv(filepath)

    for row in rows:
        print(row)

def view_appointments_patient():
    patient_id = validate_patientID(input("Enter patient's ID:"))

    filepath = get_filepath()
    rows, fieldnames = read_csv(filepath)

    match = [row for row in rows if row['Patient ID'] == patient_id]
    if not match:
        print(f"No appointments available for Patient {patient_id}")
    else:
        for row in match:
            print(row)

def view_appointments_doctor():
    doctor_id = validate_patientID(input("Enter doctor's ID:"))

    filepath = get_filepath()
    rows, fieldnames = read_csv(filepath)

    match = [row for row in rows if row['Doctor ID'] == doctor_id]
    if not match:
        print(f"No appointments available for Doctor {doctor_id}")
    else:
        for row in match:
            print(row)

def confirm_appointment():
    app_id = input('Enter appointment ID:')
    app_instance = search_appointment(app_id)

    app_instance.confirm()

def cancel_appointment():
    app_id = input('Enter appointment ID:')
    app_instance = search_appointment(app_id)

    app_instance.cancel()

def complete_appointment():
    app_id = input('Enter appointment ID:')
    app_instance = search_appointment(app_id)

    app_instance.complete()

def appointment_submenu():
    appointment_management_menu = """
--- APPOINTMENT MANAGEMENT ---
1. Book Appointment
2. View All Appointments
3. View Appointments by Patient
4. View Appointments by Doctor
5. Confirm Appointment
6. Complete Appointment
7. Cancel Appointment
0. Back to Main Menu
========================
Enter option: 
========================
"""

    try:
        option = int(input(appointment_management_menu))

        if not (0 <= option <= 7):
            raise ValueError()
        if option == 0:
            main_menu()
        elif option == 1:
            book_appointment()
        elif option == 2:
            view_all_appointments()
        elif option == 3:
            view_appointments_patient()
        elif option == 4:
            view_appointments_doctor()
        elif option == 5:
            confirm_appointment()
        elif option == 6:
            complete_appointment()
        else:
            cancel_appointment()
    except ValueError:
        print("Error: Incorrect input")

def main_menu():
    #Go back to main menu
    pass

