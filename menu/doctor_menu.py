from models import GeneralPractitioner, Specialist
from models import exceptions as excp
import csv
import os

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
    if id[0] != 'D' and len(id) != 5:
        raise excp.InvalidDoctorIDError()


def add_doctor():
# *************************************************************************************************************************************
    def add_gp():
        try:
            print("-"*5, "REGISTRATION NEW DOCTOR", '-'*5, "\n")
            #def __init__(self, name: str, age: int, contact_number: str, email: str, specialisation: str, available_days: list, is_available: bool, fee: float, home_visit: bool, doctor_id=None, _loading=False):
            name = input("Enter patient's name").title()
            age = int(input("Enter patient's age"))
            if not (0 <= age <= 120):
                raise ValueError("Invalid age")
            contact = input("Enter patient's phone number").strip()
            email = input("Enter patient's email")
            if '@' not in email:
                raise ValueError("Invalid email")
            days = """
===== DAYS AVAILABLE ====
1. Sunday
2. Monday
3. Tuesday
4. Wednesday
5. Thursday
6. Friday
7. Saturday
=====================
Enter your choices (separated by a comma): 
"""
            options = input(menu)
            available_days = []
            index = [str(i) for i in list(range(1, 8))]
            day = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"]
            options = ''.join(options.split(',')).split()

            for i in range(len(index)):
                if index[i] == option:
                    available_days.append(day[i])

            if not available_days:
                raise ValueError("Available days cannot be empty")
            
            fee = float(input("Enter doctor's fee:"))
            if fee <=0:
                raise ValueError("Invalid fee")
            home_visit = input("Availability for home visits (Y or N):")
            if home_visit.upper() == 'Y':
                home_visit = True
            elif home_visit.upper() == 'N':
                home_visit = False
            else:
                raise ValueError("Invalid input")
            
            instance = GeneralPractitioner(name, age, contact, email, 'General Practitioner', available_days, True, fee, home_visit)
        except:
            print('-'*5, "Registration Failed", "-"*5)
            print("Error:", e)

# *************************************************************************************************************************************

    def add_specialist():
        try:
            print("-"*5, "REGISTRATION NEW DOCTOR", '-'*5, "\n")
            #def __init__(self, name: str, age: int, contact_number: str, email: str, specialisation: str, available_days: list, is_available: bool, fee: float, home_visit: bool, doctor_id=None, _loading=False):
            name = input("Enter patient's name").title()
            age = int(input("Enter patient's age"))
            if not (0 <= age <= 120):
                raise ValueError("Invalid age")
            contact = input("Enter patient's phone number").strip()
            email = input("Enter patient's email")
            if '@' not in email:
                raise ValueError("Invalid email")
            days = """
===== DAYS AVAILABLE ====
1. Sunday
2. Monday
3. Tuesday
4. Wednesday
5. Thursday
6. Friday
7. Saturday
=====================
Enter your choices (separated by a comma): 
"""
            options = input(menu)
            available_days = []
            index = [str(i) for i in list(range(1, 8))]
            day = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"]
            options = ''.join(options.split(',')).split()

            for i in range(len(index)):
                if index[i] == option:
                    available_days.append(day[i])

            if not available_days:
                raise ValueError("Available days cannot be empty")
            
            fee = float(input("Enter doctor's fee:"))
            if fee <=0:
                raise ValueError("Invalid fee")
            home_visit = input("Availability for home visits (Y or N):")
            if home_visit.upper() == 'Y':
                home_visit = True
            elif home_visit.upper() == 'N':
                home_visit = False
            else:
                raise ValueError("Invalid input")
        
            specializations = {
    "Surgical": ["General Surgery", "Neurosurgery", "Orthopedic Surgery", "Plastic Surgery"],
    "Internal Medicine": ["Cardiology", "Gastroenterology", "Nephrology", "Rheumatology"],
    "Primary Care": ["Family Medicine", "Pediatrics", "Internal Medicine"]
}
            sp = """
==== SPECIALIZATION FIELDS ====
1. Surgical
2. Internal Medicine
3. Primary Care 
===============================
Choose option:
"""
            menu = '==== SPECIALIZATION FIELDS ====\n'
            sp_option = int(input(sp))
            specialisation = None
            specialisation_area = None
            if sp_option == 1:
                specialisation = "Surgical"
                for i, value in enumerate(specializations["Surgical"], start=1):
                    menu += f"{i}. {value}\n"
                else:
                    menu += """
===============================
Choose option:"""
                
                sp_area = int(input(menu))
                if not (1 <= sp_area <= len(specializations["Surgical"])):
                    raise ValueError("Invalid input")
                specialisation_area = specializations["Surgical"][sp_area-1]
            
            if sp_option == 2:
                specialisation = "Internal Medicine"
                for i, value in enumerate(specializations["Internal Medicine"], start=1):
                    menu += f"{i}. {value}\n"
                else:
                    menu += """
===============================
Choose option:"""
                
                sp_area = int(input(menu))
                if not (1 <= sp_area <= len(specializations["Internal Medicine"])):
                    raise ValueError("Invalid input")
                specialisation_area = specializations["Internal Medicine"][sp_area-1]
            
            if sp_option == 3:
                specialisation = "Primary Care "
                for i, value in enumerate(specializations["Primary Care "], start=1):
                    menu += f"{i}. {value}\n"
                else:
                    menu += """
===============================
Choose option:"""
                
                sp_area = int(input(menu))
                if not (1 <= sp_area <= len(specializations["Primary Care "])):
                    raise ValueError("Invalid input")
                specialisation_area = specializations["Primary Care "][sp_area-1]

            min_referral = True if input("Min referral required (1 for yes and any key for no)") == 1 else False
            
            instance = Specialist(name, age, contact, email, 'Specialist', available_days, True, specialisation_area, min_referral, fee, home_visit)
        except:
            print('-'*5, "Registration Failed", "-"*5)
            print("Error:", e)

# *************************************************************************************************************************************
    menu = """
===== ADD DOCTOR ====
1. New General Practitioner
2. New Specialist

=====================
Enter your choice: """
    
    try:
        option = int(input(menu))
        if option == 1:
            add_gp()
        elif option == 2:
            add_specialist()
        else:
            raise ValueError("Invalid input")
    except (TypeError, ValueError) as e:
        print("Error", e)

def view_all_doctors():
    def print_rows(rows):
        for row in rows:
            print(row)

    def print_all_rows(rows1, rows2):
        for row in rows:
            print(row)

    menu = """
===== TYPE OF DOCTOR ====
1. General Practitioners
2. Specialists
3. All Doctors
=====================
Enter your choice: """
        
    choice = int(input(menu))

    if not (1 <= choice <= 3):
        raise ValueError("Invalid Input")
    elif choice == 1:
        filepath = filepath_func_gp()
    elif choice == 2:
        filepath = filepath_func_sp()
    else:
        filepath1 = filepath_func_gp()
        filepath2 = filepath_func_sp()
        rows1, fieldnames = read_csv(filepath)
        rows2, fieldnames = read_csv(filepath)

    if choice in {1, 2}:
        rows, fieldnames = read_csv(filepath)
        print_rows(rows)
    else:
        print_all_rows(rows1, rows2)
    

def search_doctors_id():
    doctor_id = input("Enter doctor's ID").upper()
    validate_id(doctor_id)
    
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
    else:
        filepath = filepath_func_sp()

    with open(filepath, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        fieldnames = reader.fieldnames

    match = [row for row in rows if row['Doctor ID'] == doctor_id]
    
    if not match:
        print(f"Doctor '{doctor_id}' Not Found")
    else:
        for i in match:
            print(match)

def search_doctor_name():
    doctor_name = input("Enter doctor's name").title()
    
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
    else:
        filepath = filepath_func_sp()

    rows, fieldnames = read_csv(filepath)
    match = list()
    for row in rows:
        if doctor_name in row['Name']:
            match.append(row)

    if not match:
        print(f"Doctor '{doctor_name}' Not Found")
    else:
        for i in match:
            print(match)
    
def view_availability():
    days_menu = """
===== DAYS AVAILABLE ====
1. Sunday
2. Monday
3. Tuesday
4. Wednesday
5. Thursday
6. Friday
7. Saturday
=====================
Enter your choices (separated by a comma): 
"""
    option = int(input(days_menu))
    if not (1 <= option <= 7):
        raise ValueError("Invalid input: Out of bounds".title())
    days = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"]

    day = None
    for i, value in enumerate(days, start=1):
        if i == option:
            day = days[i-1]
            break

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
    else:
        filepath = filepath_func_sp()
        
    rows, fieldnames = read_csv(filepath)
    match = list()
    for row in rows:
        temp = row['Available Days'].split('; ')
        if day in temp:
            match.append(row)

    if not match:
        print(f"Availability Not Found")
    else:
        for i in match:
            print(match)

def update_availability():
    doctor_id = input("Enter doctor's ID").upper()
    validate_id(doctor_id)
    filepath = None

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
    else:
        filepath = filepath_func_sp()

    if doctor_id[0] != 'D' and len(doctor_id) != 5:
        raise excp.InvalidDoctorIDError()
    
    rows, fieldnames = read_csv(filepath)
    data = [row for row in rows if row['Doctor ID'] == doctor_id]
    if not data:
        print(f"Doctor '{doctor_id}' Not Found")
    elif len(data) > 1:
        raise excp.DuplicateID('Doctor')
    else:
        instance = None
        if choice == 1:
            instance = GeneralPractitioner(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data["Specialisation"], data['Available Days'].split('; '), data['Availability'], data['Consultation Fee'], data['Home Visit'], data['Doctor ID'], _loading=True)
            av = True if input("Enter 1 for Availaible and any key for Not Availiable:") == '1' else False

            medical_record = instance.change_availability()
            to_write = [i for i in rows if i['Doctor ID'] != doctor_id] + [{
"Doctor ID": {data['Doctor ID']},
'Name': {data['Name']},
'Age': { data['Age']},
'Contact Number': { data['Contact Number']},
'Email': {data['Email']},
'Specialisation': {data["Specialisation"]},
'Available Days': {data['Available Days']},
'Availability': {av},
'Consultation Fee': {data['Consultation Fee']},
'Home Visit': {data['Home Visit']}
                }]
            write_csv(filepath, to_write, fieldnames)

        else:
            instance = Specialist(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data["Specialisation"], data['Available Days'].split('; '), data['Availability'], data['Specialisation Area'], data['Procedure Fee'], data['Min Referral'], data['Doctor ID'], _loading=True)
            av = True if input("Enter 1 for Availaible and any key for Not Availiable:") == '1' else False

            medical_record = instance.change_availability()
            to_write = [i for i in rows if i['Doctor ID'] != doctor_id] + [{
"Doctor ID": {data['Doctor ID']},
'Name': {data['Name']},
'Age': { data['Age']},
'Contact Number': { data['Contact Number']},
'Email': {data['Email']},
'Specialisation': {data["Specialisation"]},
'Available Days': {data['Available Days']},
'Availability': {av},
'Specialisation Area': {data['Specialisation Area']},
'Procedure Fee': {data['Procedure Fee']},
'Min Referral': {data['Min Referral']}
                }]
            write_csv(filepath, to_write, fieldnames)
        
def doctor_submenu():
    doctor_management_menu = """
--- DOCTOR MANAGEMENT ---
1. Add New Doctor (GP or Specialist)
2. View All Doctors
3. Search Doctor by ID
4. View Available Doctors by Day
5. Update Doctor Availability
0. Back to Main Menu
========================
Enter option: 
========================
"""
    
    try:
        option = int(input(doctor_management_menu))

        if not (0 <= option <= 6):
            raise ValueError()
        if option == 0:
            main_menu()
        elif option == 1:
            add_doctor()
        elif option == 2:
            view_all_doctors()
        elif option == 3:
            search_doctors_id()
        elif option == 4:
            search_doctor_name()
        elif option == 5:
            view_availability()
        else:
            update_availability()
    except ValueError:
        print("Error: Incorrect input")

def main_menu():
    pass