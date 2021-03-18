class Lesson(object):
    def __init__(self, lesson_name, teacher):
        self._name = lesson_name
        self._teacher = teacher
        self._student = []
        self._number_student = 0
        self._limit_number = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, teacher):
        self._teacher = teacher

    @property
    def student(self):
        return self._student

    # 添加学生id
    def add_student(self, student_id):
        self._student.append(student_id)

    @property
    def number_student(self):
        self._number_student = len(self._student)
        return self._number_student

    @property
    def limit_number(self):
        return self._limit_number

    @limit_number.setter
    def limit_number(self, limit_number):
        self._limit_number = limit_number

