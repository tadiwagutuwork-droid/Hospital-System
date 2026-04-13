from storage import FileHandling
from .person import Person
import exceptions as excp
import os
import csv
import random

# filepath = os.path.join("data", "patients.csv") -> works on any OS 
# It was to import the module from another directory


    # def writing to csv():
    #     file_path = os.path.join('..', 'data', 'patients.csv') -> to get file path
    #     a need to pass in file_path as a parameter

#remember to auto-generate the IDs
class Patient(Person, FileHandling): #inherits two classes
    def __init__(self, name: str, age: int, contact_number: str, email: str, blood_type: str, medical_history: list, registration_date: str, is_active: bool, patient_id=None, _loading=False):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._filepath = os.path.join(base_dir, '..', 'data', 'patients.csv')
        Person.__init__(self, name, age, contact_number, email)
        self.__patient_id = self.make_record() if not _loading and patient_id is None else patient_id
        self.__blood_type = blood_type
        self.__medical_history = medical_history
        self.__registration_date = registration_date
        self.__is_active = is_active
        if not _loading:
            self.save_to_csv()

    def get_info(self):
        info = f"""
======= PATIENT DETAILS ========

Patient ID: {self.__patient_id}
Name: {self.name}
Age: {self.age}
Contact Number: {self.contact_number}
Email: {self.email}
Blood Type: {self.__blood_type}
Medical History: "{"; ".join(self.__medical_history)}"
Registration Date: {self.__registration_date}
Active: {self.__is_active}
"""
        return info
    
    def add_medical_history(self, condition: str):
        condition = condition.strip()
        if not condition:
            raise ValueError("Condition cannot be blank")
        self.__medical_history.append(condition.capitalize())
        self.update_record()

    def get_medical_history(self) -> list:
        return self.__medical_history.copy()
    
    def deactivate(self):
        self.__is_active = False
    
    # Remember that it will inherit this from FileHandling
    # def save_to_csv(self, filepath: str):
    #     pass

    #abstract methods below
    def to_dict(self) -> dict:
        """return all attributes as a flat dictionary for CSV writing"""
        return {'Patient ID': self.__patient_id,
                'Name': self.name,
                'Age': self.age,
                'Contact Number': self.contact_number,
                'Email': self.email,
                'Blood Type': self.__blood_type, 
                'Medical History': "; ".join(self.__medical_history),
                'Registration Date': self.__registration_date, 
                'Active': self.__is_active
                }
        
    @classmethod
    def from_dict(cls, data: dict): #creates a Patient class
        #def __init__(self, name: str, age: int, contact_number: str, email: str, patient_id: str, blood_type: str, medical_history: list, registration_date: str, is_active: bool):
        instance = cls(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data['Blood Type'], data['Medical History'].split('; '), data['Registration Date'], data['Active'] == 'True', data['Patient ID'],  _loading=True)
        return instance
    
    @classmethod
    def load_from_csv(cls) -> list:
        """read all rows from CSV and return a list of objects"""
        #This is all the patients in the hospital system
        instances = []
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'patients.csv')
        file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
        if file_is_empty:
            raise FileNotFoundError("File is Empty")
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = cls.from_dict(row)
                instances.append(instance)
        return instances


    def __str__(self):
        return f"\"Patient[{self.__patient_id}: {self.name}, Age: {self.age}]\""
    
    def update_record(self):
        #ask record to update specifically for that class
        value_id = self.__patient_id
        if len(value_id) != 5 or value_id[0] != 'P':
            raise excp.InvalidPatientIDError()

        filepath = self._filepath
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        for row in rows:
            if row['Patient ID'] == value_id:
                row['Medical History'] = "; ".join(self.__medical_history)
                break
        else:
            raise excp.PatientNotFoundError()
        
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def make_record(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, '..', 'data', 'identification.txt')

        with open(filepath, 'r') as file:
            lines = file.readlines()

        counter = int(lines[0].strip()) + 1
        record = f"P{counter:04d}"

        lines[0] = f"{counter}\n"

        with open(filepath, 'w') as file:
            file.writelines(lines)

        return record

# def __init__(self, name: str, age: int, contact_number: str, email: str, blood_type: str, medical_history: list, registration_date: str, is_active: bool, patient_id=None, _loading=False):     
    @Person.name.getter
    def name(self) -> str:
        return Person.name.fget(self)
    
    @Person.age.getter
    def age(self):
        return Person.age.fget(self)
    
    @Person.contact_number.getter
    def contact_number(self) -> str:
        return Person.contact_number.fget(self)
    
    @Person.email.getter
    def email(self) -> str:
        return Person.email.fget(self)
    
    @Person.name.setter
    def name(self, value):
        if not isinstance(value, str) or value.strip() == '':
            raise ValueError("Name cannot be empty")
        self._Person__name = value
    
    @Person.age.setter
    def age(self, value):
        if not isinstance(value, int) or not (0 <= value <= 120):
            raise ValueError("Invalid age")
        self._Person__age = value
    
    @Person.contact_number.setter
    def contact_number(self, value):
        if not isinstance(value, str) or value.strip() == '':
            raise ValueError("Contact number cannot be empty")
        self._Person__contact_number = value
    
    @Person.email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise ValueError("Invalid email")
        self._Person__email = value

    #doesnt get setter
    @property
    def patient_id(self):
        return self.__patient_id
    
    @property
    def blood_type(self):
        return self.__blood_type
    
    @property
    def registration_date(self):
        return self.__registration_date
    
    @property
    def is_active(self):
        return self.__is_active
    
    @blood_type.setter
    def blood_type(self, value):
        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if (value.strip()).upper() not in blood_types:
            raise ValueError("Invalid blood types")
        self.__blood_type = (value.strip()).upper()

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("Invalid type")
        self.__is_active = value
        





