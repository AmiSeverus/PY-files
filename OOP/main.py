class Student:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_grade = 0
        
    def __str__(self):
        self.count_average_grade()
        return(f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.average_grade}\nКурсы в процессе изучения: {self.courses_in_progress}\nЗавершенные курсы: {self.finished_courses}\n')

    def __lt__(self, other_student):
        if not isinstance(other_student, Student):
            return 'Нельзя сравнить'
        self.count_average_grade()
        other_student.count_average_grade()
        return self.average_grade > other_student.average_grade

    def add_finished_courses(self, course_name):
        self.finished_course.append(course_name)
        
    def add_courses_in_progress(self, course):
        if course not in self.courses_in_progress:
            self.courses_in_progress.append(course)
    
    def count_average_grade(self):
        average_grades = []
        for course, grades_list in self.grades.items():
            average_grades.append(sum(grades_list)/len(grades_list))
        self.average_grade = sum(average_grades)/len(average_grades)
    
    # def compare_students_by_average_grade(self, other_student):
    #     if isinstance(other_student, Student):
    #         self.count_average_grade()
    #         other_student.count_average_grade()
    #         if self.average_grade > other_student.average_grade:
    #             print(f'{self.name} лучше {other_student.name}')
    #         elif self.average_grade < other_student.average_grade:
    #             print(f'{self.name} хуже {other_student.name}')
    #         else:
    #             print(f'{self.name} равен {other_student.name}')
    
    def rate_Lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress and grade > 0 and grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            print('Ошибка')

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
    def add_course(self, course):
        if course not in self.courses_attached:
            self.courses_attached.append(course)    
        
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.average_grade = 0
    
    def __str__(self):
        self.count_average_grade()
        return(f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average_grade}\n')
    
    def __lt__(self, other_lecturer):
        if not isinstance(other_lecturer, Lecturer):
            return 'Нельзя сравнить'
        self.count_average_grade()
        other_lecturer.count_average_grade()
        return self.average_grade > other_lecturer.average_grade
    
    def count_average_grade(self):
        average_grades = []
        for course, grades_list in self.grades.items():
            average_grades.append(sum(grades_list)/len(grades_list))
        self.average_grade = sum(average_grades)/len(average_grades)
        
    # def compare_lecturers_by_average_grade(self, other_lecturer):
    #     if isinstance(other_lecturer, Lecturer):
    #         self.count_average_grade()
    #         other_lecturer.count_average_grade()
    #         if self.average_grade > other_lecturer.average_grade:
    #             print(f'{self.name} лучше {other_lecturer.name}')
    #         elif self.average_grade < other_lecturer.average_grade:
    #             print(f'{self.name} хуже {other_lecturer.name}')
    #         else:
    #             print(f'{self.name} равен {other_lecturer.name}')
        
class Reviewer(Mentor):
    def __str__(self):
        return(f'Имя: {self.name}\nФамилия: {self.surname}\n')
        
    def rate_hw(self, student, course, grade):        
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
    
first_student = Student('Mary', 'Jane')
second_student = Student('Rob', 'Smith')

first_student.courses_in_progress += ['PHP']
second_student.courses_in_progress += ['Python']
first_student.courses_in_progress += ['Git']
second_student.courses_in_progress += ['Git']

first_lecturer = Lecturer('Rob', 'Williams')
second_lecturer = Lecturer('Margo', 'Robby')

first_lecturer.add_course('PHP')
first_lecturer.add_course('Git')
second_lecturer.add_course('Python')
second_lecturer.add_course('Git')

first_student.rate_Lecturer(first_lecturer, 'Git', 9)
second_student.rate_Lecturer(first_lecturer, 'Git', 6)
first_student.rate_Lecturer(first_lecturer, 'PHP', 8)
second_student.rate_Lecturer(second_lecturer, 'Python', 7)
first_student.rate_Lecturer(second_lecturer, 'Git', 4)
second_student.rate_Lecturer(second_lecturer, 'Git', 3)

first_reviewer = Reviewer('Peter', 'Parker')
second_reviewer = Reviewer('Seline', 'Cyle')

first_reviewer.add_course('PHP')
first_reviewer.add_course('Git')
second_reviewer.add_course('Python')
second_reviewer.add_course('Git')

# сравнение лекторов
# first_lecturer.compare_lecturers_by_average_grade(second_lecturer)
# second_lecturer.compare_lecturers_by_average_grade(first_lecturer)
# print(first_lecturer.average_grade)
# print(second_lecturer.average_grade)
# print(first_lecturer < second_lecturer)
# print(second_lecturer < first_lecturer)

first_reviewer.rate_hw(first_student, 'Git', 5)
second_reviewer.rate_hw(first_student, 'Git', 7)
first_reviewer.rate_hw(second_student, 'Git', 9)
second_reviewer.rate_hw(second_student, 'Git', 8)
# сравнение студентов
# first_student.compare_students_by_average_grade(second_student)
# second_student.compare_students_by_average_grade(first_student)
# print(first_student.average_grade)
# print(second_student.average_grade)
# print(first_student < second_student)
# print(second_student < first_student)

# перегружение __str__
# print(first_student)
# print(first_lecturer)
# print(first_reviewer)

def count_average_hw_by_course(student_list, course_name):
    average_grade = 0
    average_grades = []
    for student in student_list:
        if isinstance(student, Student):
            for course, grades in student.grades.items():
                if course == course_name:
                    average_grades.append(sum(grades)/len(grades))
    if len(average_grades) > 0:
        average_grade = sum(average_grades)/len(average_grades)
        return(average_grade)
    else:
        return('Какая-то ошибка')

# print(count_average_hw_by_course([first_student, second_student], 'Git'))        
        
def count_average_lctr_by_course(lecturer_list, course_name):
    average_grade = 0
    average_grades = []
    for lecturer in lecturer_list:
        if isinstance(lecturer, Lecturer):
            for course, grades in lecturer.grades.items():
                if course == course_name:
                    average_grades.append(sum(grades)/len(grades))
    if len(average_grades) > 0:
        average_grade = sum(average_grades)/len(average_grades)
        return(average_grade)
    else:
        return('Какая-то ошибка')

# print(count_average_lctr_by_course([first_lecturer, second_lecturer], 'Git'))