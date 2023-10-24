class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lect(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grades(self):
        for grades in self.grades.values():
            average_grade = round(sum(grades) / len(grades), 1)
        return average_grade

    def average_grades_for_course(students, course):
        grade = 0
        for student in students:
             if course not in student.courses_in_progress:
                 return 'This course is not finished'
             elif not isinstance (student, Student):
                 return (f'{student} is not student')
             else:
                grade +=  (sum(student.grades[course]) / len(student.grades[course]))  #Cкажите, пожалуйста
            # можно ли здесь было воспользоваться (если можно то как) уже имеющимся методом average_grades,
            # а не писать его логику заново?
                average_grade = round(grade / len(students), 1)
        return f'Средняя оценка студентов за курс {course}: {average_grade}'

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grades(self):
        for grades in self.grades.values():
            average_grade = round(sum(grades) / len(grades), 1)
        return average_grade

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСреднняя оценка: {self.average_grades()}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Lecturer!')
            return
        return self.average_grades() < other.average_grades()

    def average_grades_for_lecture(lecturers, course):
        grade = 0
        for lecturer in lecturers:
             if course not in lecturer.courses_attached:
                 return 'This lecturer is not attached for this course'
             elif not isinstance (lecturer, Lecturer):
                 return (f'{student} is not lecturer')
             else:
                grade +=  (sum(lecturer.grades[course]) / len(lecturer.grades[course]))  #Cкажите,
                # пожалуйста можно ли здесь было воспользоваться (если можно то как) уже имеющимся
                # методом average_grades, а не писать его логику заново?
                average_grade = round(grade / len(lecturers), 1)
        return f'Средняя оценка лекторов за курс {course}: {average_grade}'

class Revicewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student,
                      Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res


best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student2 = Student('Bill', 'Epman', 'your_gender')
best_student2.courses_in_progress += ['Python']

cool_lecturer = Lecturer('Some', 'Buddy')
cool_lecturer.courses_attached += ['Python']
cool_lecturer1 = Lecturer('Bob', 'Black')
cool_lecturer1.courses_attached += ['Python']

cool_revicewer = Revicewer('Mike', 'Tyson')
cool_revicewer.courses_attached += ['Python']

cool_revicewer.rate_hw(best_student, 'Python', 1)
cool_revicewer.rate_hw(best_student, 'Python', 10)
cool_revicewer.rate_hw(best_student, 'Python', 10)
cool_revicewer.rate_hw(best_student2, 'Python', 10)
cool_revicewer.rate_hw(best_student2, 'Python', 10)
cool_revicewer.rate_hw(best_student2, 'Python', 10)

best_student.rate_lect(cool_lecturer, 'Python', 10)
best_student.rate_lect(cool_lecturer, 'Python', 10)
best_student.rate_lect(cool_lecturer, 'Python', 10)
best_student.rate_lect(cool_lecturer1, 'Python', 10)
best_student.rate_lect(cool_lecturer1, 'Python', 10)
best_student.rate_lect(cool_lecturer1, 'Python', 10)

print(best_student.grades)
print(cool_lecturer.grades)
print(cool_revicewer)
print(cool_lecturer.average_grades())
print(best_student.average_grades())
print(cool_lecturer1.average_grades())
print(cool_lecturer1)
print(cool_lecturer1 < cool_lecturer)
print(Student.average_grades_for_course([best_student, best_student2], 'Python'))
print(Lecturer.average_grades_for_lecture([cool_lecturer, cool_lecturer1], 'Python'))