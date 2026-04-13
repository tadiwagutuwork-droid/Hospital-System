from patient_menu import patient_submenu
from doctor_menu import doctor_submenu
from appointment_menu import appointment_submenu
from billing_menu import billing_submenu
from medical_records_menu import medical_records_submenu

def main_menu_function():
    # Go back to main menu
    main_menu = """
====================================================================
                  HOSPITAL MANAGEMENT SYSTEM
====================================================================
1. Patient Management
2. Doctor Management
3. Appointment Management
4. Medical Records
5. Billing
0. Exit
====================================================================
Enter your choice: """
    
    try:
        while True:
            option = int(input(main_menu))

            if not (0 <= option <= 5):
                raise ValueError()
            if option == 0:
                print("Thank you for utilizing the Hospital Management System!")
                break
            elif option == 1:
                patient_submenu()
            elif option == 2:
                doctor_submenu()
            elif option == 3:
                appointment_submenu()
            elif option == 4:
                medical_records_submenu()
            else:
                billing_submenu()
    except ValueError:
        print("Error: Incorrect input")

