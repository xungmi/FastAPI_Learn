class Person:
    def __init__(self, name, age):
        self.__name = name # private attribute
        self.__age = age
        self._gender = gender # protected attribute

    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age
    
if __name__ == "__main__":
    person = Person("John", 20)

    print(person.get_name())
    print(person.get_age())

