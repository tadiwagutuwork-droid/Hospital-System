#__init__ file acts as package file of all modules to be used in other modules
from .patient import Patient
from .doctor import GeneralPractitioner, Specialist
from .appointments import Appointments
from .medical_records import Medical_Records
from . import exceptions
