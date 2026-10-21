# Lab #1 - Python Classes and Objects
# Student: Albert Muratbaev
# Exercises 1-8. Each exercise is a small self-contained program.

# ==============================================================================
# Exercise 1: Create a Class with instance attributes
# ==============================================================================
def exercise1():
    print("=== Exercise 1 ===")

    class Vehicle:
        def __init__(self, max_speed, mileage):
            self.max_speed = max_speed
            self.mileage = mileage

    car = Vehicle(180, 12)
    print("Max speed:", car.max_speed)
    print("Mileage:", car.mileage)


# ==============================================================================
# Exercise 2: Class without any variables and methods
# ==============================================================================
def exercise2():
    print("=== Exercise 2 ===")

    class Vehicle:
        pass

    v = Vehicle()
    print(v)


# ==============================================================================
# Exercise 3: Child class Bus inherits all variables and methods of Vehicle
# ==============================================================================
def exercise3():
    print("=== Exercise 3 ===")

    class Vehicle:
        def __init__(self, name, max_speed, mileage):
            self.name = name
            self.max_speed = max_speed
            self.mileage = mileage

    class Bus(Vehicle):
        pass

    bus = Bus("School Volvo", 180, 12)
    print("Vehicle Name:", bus.name, "Speed:", bus.max_speed, "Mileage:", bus.mileage)


# ==============================================================================
# Exercise 4: Bus with a default seating capacity of 50
# ==============================================================================
def exercise4():
    print("=== Exercise 4 ===")

    class Vehicle:
        def __init__(self, name, max_speed, mileage):
            self.name = name
            self.max_speed = max_speed
            self.mileage = mileage

        def seating_capacity(self, capacity):
            return f"The seating capacity of a {self.name} is {capacity} passengers"

    class Bus(Vehicle):
        def seating_capacity(self, capacity=50):
            return super().seating_capacity(capacity)

    print(Bus("bus", 180, 12).seating_capacity())


# ==============================================================================
# Exercise 5: Class attribute "color" with default value White
# ==============================================================================
def exercise5():
    print("=== Exercise 5 ===")

    class Vehicle:
        color = "White"  # one value shared by every instance

        def __init__(self, name, max_speed, mileage):
            self.name = name
            self.max_speed = max_speed
            self.mileage = mileage

    class Bus(Vehicle):
        pass

    class Car(Vehicle):
        pass

    bus = Bus("School Volvo", 180, 12)
    car = Car("Audi Q5", 240, 18)
    print(f"Color: {bus.color}, Vehicle name: {bus.name}, Speed: {bus.max_speed}, Mileage: {bus.mileage}")
    print(f"Color: {car.color}, Vehicle name: {car.name}, Speed: {car.max_speed}, Mileage: {car.mileage}")


# ==============================================================================
# Exercise 6: Override fare() - 10% maintenance charge for Bus (expected 5500.0)
# ==============================================================================
def exercise6():
    print("=== Exercise 6 ===")

    class Vehicle:
        def __init__(self, name, mileage, capacity):
            self.name = name
            self.mileage = mileage
            self.capacity = capacity

        def fare(self):
            return self.capacity * 100

    class Bus(Vehicle):
        def fare(self):
            return super().fare() * 1.10

    school_bus = Bus("School Volvo", 12, 50)
    print("Total Bus fare is:", school_bus.fare())


# ==============================================================================
# Exercise 7: Which class does the object belong to?
# ==============================================================================
def exercise7():
    print("=== Exercise 7 ===")

    class Vehicle:
        def __init__(self, name, mileage, capacity):
            self.name = name
            self.mileage = mileage
            self.capacity = capacity

    class Bus(Vehicle):
        pass

    school_bus = Bus("School Volvo", 12, 50)
    print(type(school_bus))
    print(type(school_bus).__name__)


# ==============================================================================
# Exercise 8: Is school_bus also an instance of Vehicle?
# ==============================================================================
def exercise8():
    print("=== Exercise 8 ===")

    class Vehicle:
        def __init__(self, name, mileage, capacity):
            self.name = name
            self.mileage = mileage
            self.capacity = capacity

    class Bus(Vehicle):
        pass

    school_bus = Bus("School Volvo", 12, 50)
    print(isinstance(school_bus, Vehicle))


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
    exercise5()
    exercise6()
    exercise7()
    exercise8()
