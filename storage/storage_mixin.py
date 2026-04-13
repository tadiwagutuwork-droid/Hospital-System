from abc import ABC, abstractmethod

class StorageMixin(ABC):
#docstring
    """Any class that inherits from this class should implement these two methods"""
    
    @abstractmethod
    def save_to_csv(self, filepath: str) -> None:
        """save this object's data to a CSV file"""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """return all attributes as a flat dictionary for CSV writing"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """creating an instance of this class from a CSV row dictionary"""
        pass

    #Deleting with key-value pairs
    #delete_record('data/appointments.csv', 'Appointment ID', 'APT001')
    @abstractmethod
    def delete_record(self, key, value):
        pass


