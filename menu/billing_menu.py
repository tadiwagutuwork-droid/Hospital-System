from models import Appointments
from models import Patient
from models import exceptions as excp
import appointment_menu as app
import patient_menu as patient
import os
import csv
import datetime

# see completed appointments and paid, we remove them from csv file

# see total bill of patients by ID -> if bill is not there it means its zero or patient doesnt exist

# get patients who owe bill and see their total bills

# also create Exception hierarchy
def get_bill_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'billing.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")
    return filepath

def get_patient_details(id):
    filepath = patient.filepath_func()
    rows, fieldnames = patient.read_csv(filepath)

    match = list()
    for row in rows:
        if id in row['Patient ID']:
            match.append(row)

    if not match:
        raise excp.PatientNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID("Patient")
    else:
        data = match[0]
        instance = Patient(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data['Blood Type'], data['Medical History'].split('; '), data['Registration Date'], data['Active'] == True, data['Patient ID'],  _loading=True)

        return instance

def show_bill():
    patient_id =  app.validate_patientID(input("Enter patient's ID: "))
    bill = get_patient_bill(patient_id)
    patient = get_patient_details(id)

    bill_receipt = f"""
======= PATIENT BILL DETAILS ========

Patient ID: {patient.patient_id}
Name: {patient.name}
Age: {patient.age}
Contact Number: {patient.contact_number}
Email: {patient.email}

\tBill Total: R{bill:.2f}
"""

def get_patient_bill(id):
    filepath = get_bill_path()
    rows, fieldnames = app.read_csv(filepath)
    
    match = [row for row in rows if (row['Patient ID'] == id and row['Paid'] != 'True')]
    if not match:
        raise excp.PatientNotFoundError()
    elif len(match) > 1:
        total_bill = 0
        for row in match:
            total_bill += float(row['Bill'])
        round(total_bill, 2)
    else:
        total_bill = float(match[0]['Bill'])
        return round(total_bill, 2)

def settle_bill():
    app_filepath = app.get_filepath()
    rows, fieldnames = app.read_csv(app_filepath)
    app_id = app.validate_appointment(input("Enter appointment ID to settle:"))
    
    match = []
    for row in rows:
        if row['Appointment ID'] == app_id and row['Paid'] != 'True':
            match.append(row)
    else:
        if len(match) > 1:
            raise excp.DuplicateID('Appointment')
        elif not match:
            raise excp.AppointmentNotFoundError()
    
    data = match[0]
    instance = Appointments(data['Patient ID'], data['Doctor ID'], data['Specialisation'], data['Fee'], data['Date'], data['Time'], data['Notes'], data['Appointment ID'], data['Paid'], _loading=True)
    instance.payment()

def clear_paid():
    #use it when you exist or enter menu
    filepath = get_bill_path()
    rows, fieldnames = app.read_csv(filepath)

    to_write = list()
    for row in rows:
        if row['Paid'] != 'True':
            to_write.append(row)
    else:
        if not to_write:
            print("No rows to clear")  
    
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(to_write)
    

def billing_submenu():
    clear_paid()
    billing_management_menu = """
--- BILLING MANAGEMENT ---
1. Get Bill of Patient
2. Settle Bill
0. Back to Main Menu
========================
Enter option: 
========================
"""
    
    try:
        option = int(input(billing_management_menu))

        if not (0 <= option <= 2):
            raise ValueError()
        if option == 0:
            main_menu()
        elif option == 1:
            show_bill()
        else:
            settle_bill()
    except ValueError:
        print("Error: Incorrect input")

def main_menu():
    pass
