from .person import Person #parent class
from storage import FileHandling
from abc import ABC, abstractmethod
import exceptions as excp
import os
import csv
import random

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # go up one level

from storage import FileHandling
# It was to import the module from another directory
# filepath = os.path.join("data", "doctors.csv") -> works on any OS 

    # def writing to csv():
    #     file_path = os.path.join('..', 'data', 'patients.csv') -> to get file path
    #     a need to pass in file_path as a parameter

#remember to auto-generate the IDs
class Doctor(Person, ABC):
    def __init__(self, name: str, age: int, contact_number: str, email: str, specialisation: str, available_days: list, is_available = True, doctor_id=None, _loading=False): #default
        Person.__init__(self, name, age, contact_number, email)
        self.__doctor_id = self.make_record() if not _loading and doctor_id is None else doctor_id
        self.__specialisation = specialisation
        self.__available_days = available_days
        self.__is_available = is_available
        if not _loading:
            self.save_to_csv()
        
    def get_info(self) -> str:
        info = f"""
======= DOCTOR DETAILS ========

Doctor ID: {self.__doctor_id}
Name: {self.name}
Age: {self.age}
Contact Number: {self.contact_number}
Email: {self.email}
Specialisation: {self.__specialisation}
Available Days: "{"; ".join(self.__available_days)}"
Availability: {self.__is_available}
"""
        return info

    def __str__(self):
        return f"\"Doctor[{self.__doctor_id} - {self.__specialisation}: {self.name}, Age: {self.age}]\""
    
    @abstractmethod
    def calculate_fee(self):
        pass

    @Person.name.getter
    def name(self) -> str:
        temp = Person.name.fget(self)
        return temp
    
    @Person.age.getter
    def age(self) -> str:
        temp = Person.age.fget(self)
        return temp
    
    @Person.contact_number.getter
    def contact_number(self) -> str:
        temp = Person.contact_number.fget(self)
        return temp
    
    @Person.email.getter
    def email(self) -> str:
        temp = Person.email.fget(self)
        return temp
    
    @property
    def doctor_id(self) -> str:
        return self.__doctor_id

    @property
    def specialisation(self) -> str:
        return self.__specialisation
    
    @property
    def available_days(self) -> str:
        return self.__available_days
    
    @property
    def is_available(self) -> str:
        return self.__is_available
    
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


# def __init__(self, name: str, age: int, contact_number: str, email: str, specialisation: str, available_days: list, is_available = True, doctor_id=None, _loading=False): #default
#         Person.__init__(self, name, age, contact_number, email)
    
    @is_available.setter
    def is_available(self, availability):
        if not isinstance(availability, bool):
            raise ValueError("Availability should be a boolean value.")
        self.__is_available = availability
    
    def make_record(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, '..', 'data', 'identification.txt')

        with open(filepath, 'r') as file:
            lines = file.readlines()

        counter = int(lines[0].strip()) + 1
        record = f"D{counter:04d}"

        lines[1] = f"{counter}\n"

        with open(filepath, 'w') as file:
            file.writelines(lines)

        return record
    
    def update_record(self):
        #ask record to update specifically for that class
        value_id = self.doctor_id
        if len(value_id) != 5 or value_id[0] != 'D':
            raise excp.InvalidDoctorIDError()

        filepath = self._filepath
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        for row in rows:
            if row['Doctor ID'] == value_id:
                row['Availability'] = self.is_available
                break
        else:
            raise excp.DoctorNotFoundError()
        
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


#GeneralPractitioner & Specialist sub-classes of Doctor
#Both override get_info() module
class GeneralPractitioner(Doctor, FileHandling):
    def __init__(self, name: str, age: int, contact_number: str, email: str, specialisation: str, available_days: list, is_available: bool, fee: float, home_visit: bool, doctor_id=None, _loading=False):
        Doctor.__init__(self, name, age, contact_number, email, specialisation, available_days, is_available, doctor_id, _loading)
        self.__fee = fee
        self.__home_visit = home_visit
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._filepath = os.path.join(base_dir, '..', 'data', 'gp.csv')

    def calculate_fee(self):
        return self.__fee
    
    def to_dict(self) -> dict:
        return {
"Doctor ID": self.doctor_id,
'Name': self.name,
'Age': self.age,
'Contact Number': self.contact_number,
'Email': self.email,
'Specialisation': self.specialisation,
'Available Days': "; ".join(self.available_days),
'Availability': self.is_available,
'Consultation Fee': self.__fee,
'Home Visit': self.__home_visit
                }
    
    @classmethod
    def from_dict(cls, data: dict): #creates a Patient class
        #def __init__(self, name: str, age: int, contact_number: str, email: str, patient_id: str, blood_type: str, medical_history: list, registration_date: str, is_active: bool):
        instance = cls(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data["Specialisation"], data['Available Days'].split('; '), data['Availability'], data['Consultation Fee'], data['Home Visit'], data['Doctor ID'], _loading=True)
        return instance
    
    @classmethod
    def load_from_csv(cls) -> list:
        """read all rows from CSV and return a list of objects"""
        instances = []
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'gp.csv')
        file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
        if file_is_empty:
            raise FileNotFoundError("File is Empty")
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = cls.from_dict(row)
                instances.append(instance)
        return instances

    def change_availability(self, value):
        self.is_available = value
        self.update_record()

    @Doctor.is_available.setter
    def is_available(self, availability):
        Doctor.is_available.fset(self, availability)
    
    @Doctor.name.setter
    def name(self, value):
        Doctor.name.fset(self, value)
    
    @Doctor.age.setter
    def age(self, value):
        Doctor.age.fset(self, value)
    
    @Doctor.contact_number.setter
    def contact_number(self, value):
        Doctor.contact_number.fset(self, value)
    
    @Doctor.email.setter
    def email(self, value):
        Doctor.email.fset(self, value)

    @property
    def fee(self):
        return self.__fee
    
    @fee.setter
    def fee(self, value):
        if value <= 0:
            raise ValueError("Invalid fee")
        self.__fee = value
    
    @property
    def home_visit(self):
        return self.__home_visit
    
    @home_visit.setter
    def home_visit(self, value):
        if not isinstance(value, bool):
            raise ValueError("Invalid value - Boolean required!")
        self.__home_visit = value

    @Doctor.name.getter
    def name(self):
        temp = Doctor.name.fget(self)
        return temp

    @Doctor.age.getter
    def age(self):
        temp = Doctor.age.fget(self)
        return temp
    
    @Doctor.email.getter
    def email(self):
        temp = Doctor.email.fget(self)
        return temp

    @Doctor.contact_number.getter
    def contact_number(self):
        temp = Doctor.contact_number.fget(self)
        return temp

    

class Specialist(Doctor, FileHandling):
    def __init__(self, name: str, age: int, contact_number: str, email: str, specialisation: str, available_days: list, is_available: bool, specialisation_area: str, fee: float, min_referral_required: bool, doctor_id=None, _loading=False):
        Doctor.__init__(self, name, age, contact_number, email, specialisation, available_days, is_available, doctor_id, _loading)
        self.__specialisation_area = specialisation_area
        self.__fee = fee
        self.__min_referral_required = min_referral_required
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._filepath = os.path.join(base_dir, '..', 'data', 'specialist.csv')

    def calculate_fee(self):
        return self.__fee
    
    def to_dict(self) -> dict:
        return {
"Doctor ID": self.doctor_id,
'Name': self.name,
'Age': self.age,
'Contact Number': self.contact_number,
'Email': self.email,
'Specialisation': self.specialisation,
'Available Days': "; ".join(self.available_days),
'Availability': self.is_available,
'Specialisation Area': self.__specialisation_area,
'Procedure Fee': self.__fee,
'Min Referral': self.__min_referral_required
                }
    
    @classmethod
    def from_dict(cls, data: dict): #creates a Doctor class
        instance = cls(data['Name'], int(data['Age']), data['Contact Number'], data['Email'], data["Specialisation"], data['Available Days'].split('; '), data['Availability'], data['Specialisation Area'], data['Procedure Fee'], data['Min Referral'], data['Doctor ID'], _loading=True)
        return instance
    
    @classmethod
    def load_from_csv(cls) -> list:
        """read all rows from CSV and return a list of objects"""
        instances = []
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'specialist.csv')
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
        value_id = self.doctor_id
        if len(value_id) != 5 or value_id[0] != 'D':
            raise excp.InvalidDoctorIDError()

        filepath = self._filepath
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        for row in rows:
            if row['Doctor ID'] == value_id:
                row['Availability'] = self.is_available
                break
        else:
            raise excp.DoctorNotFoundError()
        
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    
    def change_availability(self, value):
        self.is_available = value
        self.update_record()

    @Doctor.is_available.setter
    def is_available(self, availability):
        Doctor.is_available.fset(self, availability)
    
    @Doctor.name.setter
    def name(self, value):
        Doctor.name.fset(self, value)
    
    @Doctor.age.setter
    def name(self, value):
        Doctor.age.fset(self, value)
    
    @Doctor.contact_number.setter
    def name(self, value):
        Doctor.contact_number.fset(self, value)
    
    @Doctor.email.setter
    def name(self, value):
        Doctor.email.fset(self, value)

    @property
    def fee(self):
        return self.__fee
    
    @fee.setter
    def fee(self, value):
        if value <= 0:
            raise ValueError("Invalid fee")
        self.__fee = value

    @property
    def specialisation_area(self):
        return self.__specialisation_area
    
    @specialisation_area.setter
    def specialisation_area(self, value):
        specializations = ["General Surgery", "Neurosurgery", "Orthopedic Surgery", "Plastic Surgery", "Cardiology", "Gastroenterology", "Nephrology", "Rheumatology","Family Medicine", "Pediatrics", "Internal Medicine"]
        if value not in specializations:
            raise ValueError("Invalid specialisation")
        self.__specialisation_area = value
    
    @property
    def min_referral_required(self):
        return self.__min_referral_required
    
    @min_referral_required.setter
    def min_referral_required(self, value):
        if not isinstance(value, bool):
            raise ValueError("Invalid value - Boolean required!")
        self.__min_referral_required = value
    
    