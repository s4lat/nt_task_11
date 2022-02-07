from functools import total_ordering

# Декоратор @total_ordering позволяет не расписывать все методы сравнения(lt, gt, le, ge, eq),
# а только два из них: eq и любой из оставшихся.
@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.avg_grade = 0.0

    def rate_lector(self, lector, course, grade):
        if (isinstance(lector, Lector) and course in lector.courses_attached
            and course in self.courses_in_progress):
            if course in lector.grades:
                lector.grades[course] += [grade]
            else:
                lector.grades[course] = [grade]
        else:
            return "Ошибка"

        lector.recalculate_avg_grade()

    def recalculate_avg_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        self.avg_grade = sum(all_grades) / len(all_grades)

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.avg_grade == other.avg_grade
        else:
            return "Ошибка"

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.avg_grade < other.avg_grade
        else:
            return "Ошибка"

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n" +
            f"Средняя оценка за домашние задания: {self.avg_grade:.2f}\n" + 
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" +
            f"Завершенные курсы: {', '.join(self.finished_courses)}\n")

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        # Вы не уточнили в условии дз(или я не нашёл), должен ли Reviewer 
        # быть закреплен за курсом, по которому выставляет оценку, 
        # я решил что должен быть
        if (isinstance(student, Student) and course in self.courses_attached 
            and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

        student.recalculate_avg_grade()

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\n"

@total_ordering
class Lector(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.avg_grade = 0.0

    def recalculate_avg_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        self.avg_grade = sum(all_grades) / len(all_grades)

    def __eq__(self, other):
        if isinstance(other, Lector):
            return self.avg_grade == other.avg_grade
        else:
            return "Ошибка"

    def __lt__(self, other):
        if isinstance(other, Lector):
            return self.avg_grade < other.avg_grade
        else:
            return "Ошибка"

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n" +
            f"Средняя оценка за лекции: {self.avg_grade:.2f}\n")

# У меня обе функции получились одинаковыми и их можно объединить в одну
# функцию course_avg, но так-как в условии было сказано про 2 отдельных функции,
# я их оставил как есть
def hw_course_avg(students, course):
    all_grades = []
    for st in students:
        if course in st.grades:
            all_grades += st.grades[course]

    return sum(all_grades) / len(all_grades)

def lectures_course_avg(lectors, course):
    all_grades = []
    for lc in lectors:
        if course in lc.grades:
            all_grades += lc.grades[course]

    return sum(all_grades) / len(all_grades)


st1 = Student("Maxim", "Pavlov", "male")
st1.courses_in_progress += ["Python", "JS"]
st1.finished_courses += ["Git"]
st2 = Student("Sasha", "Volya", "female")
st2.courses_in_progress += ["Git", "JS"]

lc1 = Lector("Kirill", "Posov")
lc1.courses_attached += ["Python", "JS"]
lc2 = Lector("Katya", "Bosova")
lc2.courses_attached += ["Git", "JS"]

rv1 = Reviewer("Gosha", "Rubchinsky")
rv1.courses_attached += ["Python", "JS"]
rv2 = Reviewer("Masha", "Pupchynsky")
rv2.courses_attached += ["Git", "JS"]

# Вывод оценщиков
print("% ОБЪЕКТЫ КЛАССА Reviewer %")
print(rv1)
print(rv2)

# Оценка дз студентов
rv1.rate_hw(st1, "Python", 4)
rv1.rate_hw(st1, "Python", 3)
rv1.rate_hw(st1, "JS", 5)
rv1.rate_hw(st1, "JS", 3)
rv2.rate_hw(st2, "Git", 3)
rv2.rate_hw(st2, "Git", 1)
rv2.rate_hw(st2, "JS", 2)
rv2.rate_hw(st2, "JS", 5)

# Вывод студентов и их сравнение
print("% ОБЪЕКТЫ КЛАССА Student %")
print(st1)
print(st2)
print("Результат st1 > st2: ", st1 > st2)
print("Результат st1 <= st2: ", st1 <= st2, "\n")

# Оценка лекции
st1.rate_lector(lc1, "Python", 5)
st1.rate_lector(lc1, "JS", 8)
st2.rate_lector(lc2, "Git", 8)
st2.rate_lector(lc2, "JS", 5)

# Вывод лекторов и их сравнение
print("% ОБЪЕКТЫ КЛАССА Lector %")
print(lc1)
print(lc2)
print("Результат lc1 > lc2: ", lc1 > lc2)
print("Результат lc1 <= lc2: ", lc1 <= lc2, "\n")

# Проверка функций hw_course_avg и lectures_course_avg
print("Средняя оценка за дз по курсу 'JS': ", hw_course_avg([st1, st2], "JS"))
print("Средняя оценка лекций по курсу 'JS': ", lectures_course_avg([lc1, lc2], "JS"))


