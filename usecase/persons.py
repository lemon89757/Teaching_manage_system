"""学生、老师、管理员类
   他们的密码设置和修改密码可直接调用entity中的setter
"""
from entity.people import People
from entity.manager import ManagerLesson
from entity.read_writre import ReadWrite


class Teacher(People):
    def __init__(self, name):
        super(Teacher, self).__init__(name)
        self._tag = 1

    def manage(self, lesson_name):
        manager = ManagerLesson(lesson_name, self.name, self._tag)
        return manager


class Student(People):
    def __init__(self, name):
        super(Student, self).__init__(name)
        self._tag = 2

    def manage(self, lesson_name):
        manager = ManagerLesson(lesson_name, self.name, self._tag)
        return manager


class Administrator(People):
    def __init__(self, name):
        super(Administrator, self).__init__(name)
        self._tag = 0

    @staticmethod
    def initialize():
        way = ReadWrite()
        way.to_json()

    def manage(self, lesson_name):
        manager = ManagerLesson(lesson_name, self.name, self._tag)
        return manager

