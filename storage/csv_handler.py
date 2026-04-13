#This is where I record everything in the csv files
#we are importing the module's class to inherit it here
from .storage_mixin import StorageMixin
from abc import ABC, abstractmethod
import csv
import os #The Operating System module will be used to check if the file is empty to avoid writing a header

#The other modules need to inherit this class

class FileHandling(StorageMixin, ABC):
    def save_to_csv(self) -> None:
        """save this object's data to a CSV file"""
        #filepath - stored in data remember
        filepath = self._filepath

        row = self.to_dict() #return dictionary for writing
        file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0

        with open(filepath, "a", newline='') as csvfile:
            fieldnames = list(row.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if file_is_empty: #avoid writing another header
                writer.writeheader()
            writer.writerow(row)

    #Will an error be raised here? if Yes, then fix it not to be an abstract method
    @abstractmethod
    def to_dict(self) -> dict:
        """return all attributes as a flat dictionary for CSV writing"""
        #these are also for the fieldnames and information
        #check specifications
        pass
        # the classes should implement it themselves 
    
    @classmethod
    def from_dict(cls, data: dict):
        """creating an instance of this class from a CSV row dictionary"""
        # instance = cls(data) -> depending on which cls, it is the class itself
        # from_dict(data: dict) -> Patient class method, creates Patient from CSV row
        pass

    def clear_csv_file(self):
        filepath = self._filepath
        with open(filepath, 'w') as file:
            pass
    
    #Deleting with key-value pairs
    #delete_record('data/appointments.csv', 'Appointment ID', 'APT001')
    def delete_record(self, key, value):
        filepath = self._filepath
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            rows = list(reader)
            
        match = [row for row in rows if row[key] == value]
        if not match: #nothing is found
            raise ValueError(f"{value} not Found")
        to_write = [i for i in rows if i[key] != value]
            
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(to_write)
    
    @abstractmethod
    def update_record(self, key_id, value_id, key, value, other=None, other2=None):
        pass

    @abstractmethod
    def make_record(self):
        pass

        

