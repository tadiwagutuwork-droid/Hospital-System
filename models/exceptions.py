class HospitalSystemError(Exception):
    def __init__(self, message='System Error'):
        super().__init__(message)

class PatientNotFoundError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Patient Not Found")

class AppointmentNotFoundError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Appointment Not Found")

class DoctorNotFoundError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Doctor Not Found")

class MedicalRecordNotFoundError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"MedicalRecord Not Found")

class InvalidPatientIDError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Invalid Patient ID entered!")

class InvalidDoctorIDError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Invalid Doctor ID entered!")

class InvalidAppointmentIDError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Invalid Appointment ID entered!")

class InvalidMedicalRecordIDError(HospitalSystemError):
    def __init__(self):
        super().__init__(f"Invalid Medical Record ID entered!")

class DuplicateID(HospitalSystemError):
    def __init__(self, message):
        super().__init__(f"No Duplicate {message.title()} IDs Allowed!")
