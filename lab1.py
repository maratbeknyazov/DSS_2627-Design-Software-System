# Exercise 7: Check type of an object
# Определить, к какому классу принадлежит объект School_bus с помощью встроенной функции type()

# class Vehicle:
#     def __init__(self, name, mileage, capacity):
#         self.name = name
#         self.mileage = mileage
#         self.capacity = capacity

# class Bus(Vehicle):
#     pass

# School_bus = Bus("School Volvo", 12, 50)

# print(type(School_bus))



# Exercise 8: Determine if School_bus is also an instance of the Vehicle class
# Проверить, является ли объект School_bus экземпляром класса Vehicle с помощью isinstance().

class Vehicle:
    def __init__(self, name, mileage, capacity):
        self.name = name
        self.mileage = mileage
        self.capacity = capacity

class Bus(Vehicle):
    pass

School_bus = Bus("School Volvo", 12, 50)

# Проверка наследования/принадлежности к экземпляру:
print(isinstance(School_bus, Vehicle))