import abc
import decorator_pattern

class User(metaclass=abc.ABCMeta):
    def __init__(self,username,password):
        self.__username = username
        self._password = password
        self._pizza = None

    @abc.abstractmethod
    def get_username(self):
        pass
    @abc.abstractmethod
    def get_password(self):
        pass
    

class Customer():
    def __init__(self, username, password):
        self.__username = username
        self._password = password
        self._pizza = None

    def get_username(self):
        return self.__username
    def get_password(self):
        return self._password
  
    def set_pizza(self,pizza):
        self._pizza = pizza

