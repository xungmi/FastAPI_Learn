import pytest


class Student:
    def __init__(self, first_name, last_name, major, years):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 3)

def test_student_initialization(default_student):
    p = default_student
    assert p.first_name == "John", "First name should be John"
    assert p.last_name == "Doe"
    assert p.major == "Computer Science"
    assert p.years == 3