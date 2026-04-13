from models import Medical_Records
from models import exceptions as excp
import csv
import os
import appointment_menu as app
import patient_menu as patient

# we need to see specific medical record of patient
# delete record
# main menu
def get_filepath():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'medical_records.csv')
    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if file_is_empty:
        raise FileNotFoundError("File is Empty")
    return filepath

def get_record():
    filepath = get_filepath()
    return app.read_csv(filepath)

def validate_medical_record(id):
    id = id.upper()
    if id[0] != 'M' and len(id) != 5:
        raise excp.InvalidMedicalRecordIDError()
 
    rows, fieldnames = get_record()
    
    match = [row for row in rows if row['Patient ID'] == id]
    if not match:
        raise excp.MedicalRecordNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID('Medical Record')
    else:
        return id

def view_medical_record():
    md_record_id = validate_medical_record(input("Enter medical record ID:"))

    rows, fieldnames = get_record()
    match = [row for row in rows if row['Record ID'] == md_record_id]
    if not match:
        raise excp.MedicalRecordNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID('Medical Record')
    else:
        row = match[0]
        view = f"""
======== MEDICAL RECORD =========
Record ID: {row['Record ID']}
Patient ID: {row['Patient ID']}
Doctor ID: {row['']}
Appointment ID: {row['Doctor ID']}
Diagnosis: {row['Diagnosis']}
Prescription: {row['Prescription']}
Date Created: {row['Date Created']}
=================================
"""
        print(view)

def delete_record():
    md_record_id = validate_medical_record(input("Enter medical record ID:"))

    filepath = get_filepath()
    rows, fieldnames = get_record()
    match = [row for row in rows if row['Record ID'] == md_record_id]
    if not match:
        raise excp.MedicalRecordNotFoundError()
    elif len(match) > 1:
        raise excp.DuplicateID('Medical Record')
    to_write = [row for row in rows if row['Record ID'] != md_record_id]

    patient.write_csv(filepath, to_write, fieldnames)

def main_menu():
    pass

def medical_records_submenu():
    medical_record_menu = """
--- MEDICAL RECORDS MANAGEMENT ---
1. View Patient Medical Record
2. Delete Medical Record
0. Back to Main Menu
"""
    try:
        option = int(input(medical_record_menu))

        if not (0 <= option <= 2):
            raise ValueError()
        if option == 0:
            main_menu()
        elif option == 1:
            view_medical_record()
        else:
            delete_record()
    except ValueError:
        print("Error: Incorrect input")

