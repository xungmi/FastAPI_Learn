from abc import ABC, abstractmethod
class Animal(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self, food):
        print(f"{self.name} is eating {food}")
    
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        print("Woof")

if __name__ == "__main__":
    dog = Dog("Dog", 10)
    dog.sound()
