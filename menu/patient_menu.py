from models import Patient
from models import exceptions as excp
import os
import csv
from datetime import date

def filepath_func():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'patients.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")

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

def validate_id(id):
    if id[0] != 'P' and len(id) != 5:
        raise excp.InvalidPatientIDError()
    

#please use setters and getters for everything instead csv file details and please use functions for redundant code for abstraction
def register():
    try:
        print("-"*5, "REGISTRATION NEW PATIENT", '-'*5, "\n")
        name = input("Enter patient's name").title()
        age = int(input("Enter patient's age"))
        if not (0 <= age <= 120):
            raise ValueError("Invalid age")
        contact = input("Enter patient's phone number").strip()
        email = input("Enter patient's email")
        if '@' not in email:
            raise ValueError("Invalid email")
        blood_type = input("Enter blood type").upper()
        if blood_type not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            raise ValueError("Invalid blood type")
        medical_history = []
        medical = input("Enter previous medical condition (Enter 0 to terminate)").strip()
        while medical != '0':
            medical_history.append(medical.title())
            medical = input("Enter previous medical condition (Enter 0 to terminate)").strip()

        current_date = date.today()
        registration_date = current_date.strftime("%d-%m-%Y")
        is_active = True
        patient = Patient(name, age, contact, email, blood_type, medical_history, registration_date, is_active)
        print('-'*5, "Registration Complete", "-"*5)

    except (ValueError, TypeError) as e:
        print('-'*5, "Registration Failed", "-"*5)
        print("Error:", e)


def view_all_patients():
    filepath = filepath_func()

    rows, fieldnames = read_csv(filepath)

    for row in rows:
        print(row)
    
def search_patients_id():
    patient_id = input("Enter patient's ID").upper()
    validate_id(patient_id)

    filepath = filepath_func()
    rows, fieldnames = read_csv(filepath)

    match = [row for row in rows if row['Patient ID'] == patient_id]
    if not match:
        raise excp.PatientNotFoundError()
    else:
        for i in match:
            print(match)
    
def search_patients_name():
    patient_name = input("Enter patient's name").title()

    filepath = filepath_func()
    rows, fieldnames = read_csv(filepath)

    match = list()
    for row in rows:
        if patient_name in row['Name']:
            match.append(row)

    if not match:
        raise excp.PatientNotFoundError()
    else:
        for i in match:
            print(match)

def update_patient_details():
    patient_id = input("Enter patient's ID").upper()
    validate_id(patient_id)
    
    filepath = filepath_func()
    rows, fieldnames = read_csv(filepath)

    data = [row for row in rows if row['Patient ID'] == patient_id]
    if not data:
        raise excp.PatientNotFoundError()
    elif len(data) > 1:
        raise excp.DuplicateID('Patient')
    else:
        instance = Patient(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data['Blood Type'], data['Medical History'].split('; '), data['Registration Date'], data['Active'] == True, data['Patient ID'],  _loading=True)
        medical = input("Enter medical condition").strip()
        if medical == '':
            raise ValueError("Medical Record cannot be empty")
        instance.add_medical_history(medical)
        medical_record = instance.get_medical_history()
        to_write = [i for i in rows if i['Patient ID'] != patient_id] + [{'Patient ID': data['Patient ID'], 
                'Name': data['Name'],
                'Age': data['Age'],
                'Contact Number': data['Contact Number'],
                'Email': data['Email'],
                'Blood Type': data['Blood Type'], 
                'Medical History': {"; ".join(medical_record)},
                'Registration Date': data['Registration Date'], 
                'Active': data['Active']
                }]
        
        write_csv(filepath, to_write, fieldnames)

def view_medical_history():
    patient_id = input("Enter patient's ID").upper()
    validate_id(patient_id)

    filepath = filepath_func()
    rows, fieldnames = read_csv(filepath)

    data = [row for row in rows if row['Patient ID'] == patient_id]
    if not data:
        raise excp.PatientNotFoundError()
    elif len(data) > 1:
        raise excp.DuplicateID('Patient')
    else:
        medical_history = data[0]
        print(f"""
Patient ID: {medical_history['Patient ID']}
Name: {medical_history['Name']}
Age: {medical_history['Age']}
Medical History: {medical_history['Medical History']}
""")
        
def deactivate_patient():
    patient_id = input("Enter patient's ID").upper()
    validate_id(patient_id)
    
    filepath = filepath_func()
    rows, fieldnames = read_csv(filepath)

    data = [row for row in rows if row['Patient ID'] == patient_id]
    if not data:
        raise excp.PatientNotFoundError()
    elif len(data) > 1:
        raise excp.DuplicateID('Patient')
    else:
        instance = Patient(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data['Blood Type'], data['Medical History'].split('; '), data['Registration Date'], data['Active'] == True, data['Patient ID'],  _loading=True)
        instance.deactivate()
        to_write = [i for i in rows if i['Patient ID'] != patient_id] + [{'Patient ID': data['Patient ID'], 
                'Name': data['Name'],
                'Age': data['Age'],
                'Contact Number': data['Contact Number'],
                'Email': data['Email'],
                'Blood Type': data['Blood Type'], 
                'Medical History': data['Medical History'].split('; '),
                'Registration Date': data['Registration Date'], 
                'Active': False
                }]
        
        write_csv(filepath, to_write, fieldnames)

def patient_submenu():
    patient_management_menu = """
-- PATIENT MANAGEMENT --
1. Register New Patient
2. View All Patients
3. Search Patient by ID
4. Search Patient by Name
5. Update Patient Details
6. View Patient Medical History
7. Deactivate Patient
0. Back to Main Menu
========================
Enter option: 
========================
"""
    
    try:
        option = int(input(patient_management_menu))

        if not (0 <= option <= 7):
            raise ValueError()
        if option == 0:
            main_menu()
        elif option == 1:
            register()
        elif option == 2:
            view_all_patients()
        elif option == 3:
            search_patients_id()
        elif option == 4:
            search_patients_name()
        elif option == 5:
            update_patient_details()
        elif option == 6:
            deactivate_patient()
        else:
            register()
    except ValueError:
        print("Error: Incorrect input")

def main_menu():
    #Go back to main menu
    pass
    


    


    



    


    