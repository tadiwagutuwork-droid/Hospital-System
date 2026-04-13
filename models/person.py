from abc import ABC, abstractmethod
#So the child classes should inherit the CSV Handler module to access FileHandling class
class Person(ABC):
    """This is a parent class for the entire system (for all people)"""

    def __init__(self, name: str, age: int, contact_number: str, email: str):
        #private attributes
        self.__name = name
        self.__age = age
        self.__contact_number = contact_number
        self.__email = email

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def age(self) -> str:
        return self.__age
    
    @property
    def contact_number(self) -> str:
        return self.__contact_number
    
    @property
    def email(self) -> str:
        return self.__email

    @abstractmethod
    def get_info(self) -> str:
        #to return a string of information
        pass

    @abstractmethod
    def __str__(self):
        #implement its own information
        pass



    
    
    