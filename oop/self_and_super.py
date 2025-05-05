# self tham chiếu đến đối tượng hiện tại (instance) của lớp đang được tạo hoặc thao tác.
    # và Phân biệt giữa các biến instance (thuộc tính của đối tượng) và tham số có cùng tên trong phương thức.
# super gọi các phương thức hoặc constructor của lớp cha (parent class) từ lớp con (child class).

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, degree):
        super().__init__(name, age)  # Gọi constructor của Person
        self.degree = degree         # Gán thuộc tính riêng của Student

if __name__ == "__main__":
    student = Student("John", 20, "Bachelor")
    print(student.name)
    print(student.age)
    print(student.degree)