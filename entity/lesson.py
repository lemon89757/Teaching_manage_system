class Lesson(object):
    def __init__(self, lesson_name, teacher_id, limit_number):
        self._name = lesson_name
        self._teacher_id = teacher_id
        self._students = []
        self._number_students = 0
        self._limit_number = limit_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def teacher_id(self):
        return self._teacher_id

    @teacher_id.setter
    def teacher_id(self, teacher_id):
        self._teacher_id = teacher_id

    @property
    def students(self):
        return self._students

    @students.setter
    def students(self, students):
        self._students = students

    # # 添加是学生id
    # def add_student(self, student_id):
    #     self._students.append(student_id)

    @property
    def number_students(self):
        self._number_students = len(self._students)
        return self._number_students

    @property
    def limit_number(self):
        return self._limit_number

    @limit_number.setter
    def limit_number(self, limit_number):
        self._limit_number = limit_number

