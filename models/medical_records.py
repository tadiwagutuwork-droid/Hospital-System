from storage import FileHandling
import os
import csv
import random
import exceptions as excp


class Medical_Records(FileHandling):
    def __init__(self, patient_id, doctor_id, appointment_id, diagnosis, prescription, date_created, record_id=None, _loading=False):
        self.__record_id = self.make_record() if not _loading and record_id is None else record_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__appointment_id = appointment_id
        self.__diagnosis = diagnosis
        self.__prescription = prescription
        self.__date_created = date_created
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._filepath = os.path.join(base_dir, '..', 'data', 'medical_records.csv')
        if not _loading:
            self.save_to_csv()

    def to_dict(self) -> dict:
        """return all attributes as a flat dictionary for CSV writing"""
        return {
                'Record ID': self.__record_id,
                'Patient ID': self.__patient_id,
                'Doctor ID': self.__doctor_id,
                'Appointment ID': self.__appointment_id,
                'Diagnosis': self.__diagnosis,
                'Prescription': self.__prescription, 
                'Date Created': self.__date_created
                }
        
    @classmethod
    def from_dict(cls, data: dict): #creates a Patient class
        #def __init__(self, name: str, age: int, contact_number: str, email: str, patient_id: str, blood_type: str, medical_history: list, registration_date: str, is_active: bool):
        instance = cls(data['Patient ID'], data['Doctor ID'], data['Appointment ID'], data['Diagnosis'], data['Prescription'], data['Date Created'], data['Record ID'], _loading=True)
        return instance
    

    @classmethod
    def load_from_csv(cls) -> list:
        """read all rows from CSV and return a list of objects"""
        #This is all the patients in the hospital system
        instances = []
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'medical_records.csv')
        file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
        if file_is_empty:
            raise FileNotFoundError("File is Empty")
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = cls.from_dict(row)
                instances.append(instance)
        return instances
    
    def make_record(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, '..', 'data', 'identification.txt')
        record = f"M{random.randint(1, 9999):04d}"
        if os.path.getsize(filepath) == 0:
            with open(filepath, 'w') as file:
                writer = file.writelines(['0\n', '0\n', '0\n', record + '\n'])
            return record
        else:
            with open(filepath, 'r', newline='') as file:
                lines = file.readlines()
            while lines[-1].strip() == record:
                record = f"M{random.randint(1, 9999):04d}"
            lines[-1] = record + '\n'
            with open(filepath, 'w') as file:
                file.writelines(lines)
            return record
        
    def __str__(self):
        return f"""
======== MEDICAL RECORD =========
Record ID: {self.__record_id}
Patient ID: {self.__patient_id}
Doctor ID: {self.__doctor_id}
Appointment ID: {self.__appointment_id}
Diagnosis: {self.__diagnosis}
Prescription: {self.__prescription}
Date Created: {self.__date_created}
=================================
"""