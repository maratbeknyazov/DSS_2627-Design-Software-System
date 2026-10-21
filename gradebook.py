class Student:
    # atributes in object
    def __init__(self, name, score):
        self.name = name
        self.score = score  

    def grade(self):
        if self.score >= 90: 
            return "A"
        if self.score >= 75: 
            return "B"
        return "C" 


# class for control group of students
class Gradebook:
    def __init__(self, course):
        self.course = course  # save name of course
        self.students = []  # initial empty list of students 

    # Метод для добавления объекта Student в журнал
    
    def add(self, student):
        self.students.append(student)  # adding a student

    # Method for searching average score
    def average(self):
        if not self.students:  # Checking, is list empty or not
            return 0.0  #
        total = sum(
            s.score for s in self.students
        )  # Суммируем баллы всех студентов
        return total / len(self.students)  

    # Method for search best student
    def top(self):
        if not self.students: 
            return None  
        return max(
            self.students, key=lambda s: s.score
        )  


if __name__ == "__main__":
    gb = Gradebook("DSS") 
    gb.add(Student("Usmonjon", 88))
    gb.add(Student("Albert", 95)) 
    gb.add(Student("Bek", 61))  

    print("Average:", gb.average())  
    top_student = gb.top() 
    print(f"Top Student: {top_student.name} ({top_student.score})")