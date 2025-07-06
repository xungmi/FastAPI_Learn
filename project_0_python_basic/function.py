def increment(number):
    return number + 1

def say_hi(name):
    print(f"Hi {name}")

color = "Red"
def print_local_color():
    color = "Blue"
    print(color)

def print_global_color():
    global color
    color = "Blue"
    print(color)

print_local_color()
print(color)

print_global_color()
print(color)









