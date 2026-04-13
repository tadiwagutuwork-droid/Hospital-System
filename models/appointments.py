from .person import Person #parent class
from storage import FileHandling
import os
import csv
import random


# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # go up one level

# It was to import the module from another directory
# filepath = os.path.join("data", "appointments.csv") -> works on any OS 

    # def writing to csv():
    #     file_path = os.path.join('..', 'data', 'patients.csv') -> to get file path
    #     a need to pass in file_path as a parameter

# import datetime

# current_date = datetime.date.today()
# current_time = datetime.datetime.now().time()
# ALSO ADD YOUR OWN INPUT DATE - for schedules

# Remember: current_time.strftime("%H:%M:%S")


# So -> we create a list based on all csv inputs right as instances
# then we put all the instances in a list (for doctor or patient)
# then i will use appointment menu to search for the name or id of our patient
# using a for loop,
# do it will be like this
# if new patient -> create new instance
# for instance in instances:
#     if search in (instance.name, instance.patient_id, instance.doctor_id): - it will ask for which doctor first - and whether GP or specialist and ask for specialisation
#         work on that specific instance
#         ask for date, and time, notes as well
# --------we create an instance with Appointment(patient/doctor)
# else:
#     patient not found
#     create patient


#Before entering appointment menu, one should ask for existing doctor or patient, if yes, then load csv details into a list of instances else create a new doctor or patient instance
class Appointments(FileHandling):
    #It takes an instance of the Patient and Doctor 
    #so patient asks which doctor and we have to get the doctors id, and also to load it in our appointments.csv
    def __init__(self, patient, doctor, specialisation, fee, date: str, time: str, notes: str, appointment_id=None, paid=False, _loading =False):
        self.__appointment_id = self.make_record() if not _loading and appointment_id is None else appointment_id
        self.__patientID = patient # -> its the ID
        self.__doctorID = doctor # -> its the ID
        self.__specialisation = specialisation
        self.__fee = fee
        self.__date = date
        self.__time = time
        self.__status = 'pending' #by default, status is set to pending
        self.__notes = notes
        self.__paid = paid
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._filepath = os.path.join(base_dir, '..', 'data', 'appointments.csv')
        #avoiding an infinite loop of creating instances
        if not _loading:
            self.save_to_csv()
        print("Appointment Successfully Booked!")

    def confirm(self):
        if self.__status == 'pending':
            self.__status = 'confirmed'
            self.update_record()
        elif self.__status == 'confirmed':
            raise ValueError("Already confirmed")
        else:
            raise ValueError("Transition Not Allowed")

    def complete(self):
        if self.__status == "confirmed":
            self.__status = 'completed'
            self.update_record()
            self.billing_records()
        elif self.__status == 'completed':
            raise ValueError("Already completed")
        else:
            raise ValueError("Transition Not Allowed")
        

    def cancel(self):
        if self.__status in ('pending', 'confirmed'):
            self.__status = 'cancelled'
            self.update_record()
        elif self.__status == 'cancelled':
            raise ValueError("Already cancelled")
        else:
            raise ValueError("Transition Not Allowed")

    def to_dict(self) -> dict:
        """return all attributes as a flat dictionary for CSV writing"""
        return {'Appointment ID': self.__appointment_id,
                'Patient ID': self.__patientID,
                "Doctor ID": self.__doctorID,
                'Specialisation': self.__specialisation,
                'Fee': self.__fee,
                'Date': self.__date,
                'Time': self.__time,
                'Status': self.__status, 
                'Notes': self.__notes,
                'Paid': self.__paid
                }
    
    
    @classmethod
    #in appointment's menu, u will need to cancel a specific appointment, so u will create a list of instance, search and then change the status
    def from_dict(cls, data: dict): #creates a Appointment class
        instance = cls(data['Patient ID'], data['Doctor ID'], data['Specialisation'], data['Fee'], data['Date'], data['Time'], data['Notes'], data['Appointment ID'], data['Paid'], _loading=True)
        return instance
    
    @classmethod
    def load_from_csv(cls) -> list:
        """read all rows from CSV and return a list of objects"""
        #This is all the patients in the hospital system
        instances = []
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'appointments.csv')
        file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
        if file_is_empty:
            raise FileNotFoundError("File is Empty")
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = cls.from_dict(row)
                instances.append(instance)
        return instances
    
    def update_record(self):
        #ask record to update specifically for that class
        value_id = self.__appointment_id
        if len(value_id) != 5 or value_id[0] != 'A':
            raise ValueError("Invalid input - ID required")

        filepath = self._filepath
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            rows = list(reader)
            

        for row in rows:
            if row['Appointment ID'] == value_id:
                row['Status'] = self.__status
                break
        else:
            raise ValueError(f"{value_id} does not exist")
        
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def make_record(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, '..', 'data', 'identification.txt')

        if os.path.getsize(filepath) == 0:
            number = 1
        else:
            with open(filepath, 'r') as file:
                lines = file.readlines()
            number = int(lines[-2].strip()[1:]) + 1  # strip 'A', convert to int, increment

        record = f"A{number:04d}"

        if os.path.getsize(filepath) == 0:
            with open(filepath, 'w') as file:
                file.writelines(['0\n', '0\n', record + '\n', '0\n'])
        else:
            lines[-2] = record + '\n'
            with open(filepath, 'w') as file:
                file.writelines(lines)

        return record
    
    def billing_records(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, '..', 'data', 'billing.csv')
        
        row = {'Appointment ID': self.__appointment_id,
                'Patient ID': self.__patientID,
                "Doctor ID": self.__doctorID,
                'Date': self.__date,
                'Time': self.__time,
                'Status': self.__status, 
                'Bill': self.__fee,
                'Paid': self.__paid
                }
        
        file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0

        with open(filepath, "a", newline='') as csvfile:
            fieldnames = list(row.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if file_is_empty: #avoid writing another header
                writer.writeheader()
            writer.writerow(row)
        
    def payment(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, '..', 'data', 'billing.csv')

        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        match = [row for row in rows if (row['Appointment ID'] == self.__appointment_id)]
        if not match: #nothing is found
            raise ValueError(f"{self.__patientID} not Found or System Error")
        instance = Appointments(match['Patient ID'], match['Doctor ID'], match['Specialisation'], match['Fee'], match['Date'], match['Time'], match['Notes'], match['Appointment ID'], match['Paid'], _loading=True)
        match[0]['Paid'] = 'True'
        self.__paid = True
        to_write = [i for i in rows if i['Appointment ID'] != self.__appointment_id] + match

            
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(to_write)
    
    def update_specific_record(self, specific, value):
        value_id = self.__appointment_id
        if len(value_id) != 5 or value_id[0] != 'A':
            raise ValueError("Invalid input - ID required")

        filepath = self._filepath
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            rows = list(reader)

        for row in rows:
            if row['Appointment ID'] == value_id:
                row[specific] = value
                break
        else:
            raise ValueError(f"{value_id} does not exist")
        
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    @property
    def fee(self):
        return self.__fee
    
    @property
    def specialisation(self):
        return self.__specialisation
    
    @property
    def date(self):
        return self.__date
    
    @property
    def time(self):
        return self.__time
    
    @property
    def status(self):
        return self.__status
    
    @property
    def notes(self):
        return self.__notes
    
    @property
    def paid(self):
        return self.__paid
    
    @fee.setter
    def fee(self, value):
        try:
            if not isinstance(value, (float, int)):
                raise ValueError("ONLY STRINGS ALLOWED")
            self.__fee = value
            specific = 'Fee'
            self.update_specific_record(specific, value)
        except ValueError:
            print('Incorrect values provided!')
    
    @date.setter
    def date(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("ONLY STRINGS ALLOWED")
            self.__date = value
            specific = 'Date'
            self.update_specific_record(specific, value)
        except ValueError:
            print('Incorrect values provided!')
    
    @time.setter
    def time(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("ONLY STRINGS ALLOWED")
            self.__time = value
            specific = 'Time'
            self.update_specific_record(specific, value)
        except ValueError:
            print('Incorrect values provided!')
    
    @status.setter
    def status(self, value):
        try:
            if not isinstance(value, bool):
                raise ValueError("ONLY BOOLEANS ALLOWED")
            self.__status = value
            specific = 'Status'
            self.update_specific_record(specific, value)
        except ValueError:
            print('Incorrect values provided!')
    
    @notes.setter
    def notes(self, value):
        try:
            if not isinstance(value, str) or value.strip() == '':
                raise ValueError("ONLY STRINGS ALLOWED")
            self.__notes = value
            specific = 'Notes'
            self.update_specific_record(specific, value)
        except ValueError:
            print('Incorrect values provided!')
    
    @paid.setter
    def paid(self, value):
        try:
            if not isinstance(value, bool):
                raise ValueError("ONLY BOOLEANS ALLOWED")
            specific = 'Paid'
            self.__paid = value
            self.update_specific_record(specific, value)
        except ValueError:
            print('Incorrect values provided!')