# class A:
#     def __init__(self):
#         pass
#
#
# a = A()
# print(type(a) == A)
#
# B = []
# a, b = 1, 2
# B.append(a)
# print(B)
# B.append(b)
# print(B)
#
# # c = int('a')
#
# while True:
#     a = 0
#     if a < 10:
#         x = a + 1
#         a += 1
#         print(a)
#     else:
#         break

from entity.manager import ManagerPeoples
from entity.manager import ManagerLessons
from entity.people import People
from view.land import Land

# manager = ManagerPeoples()
# id_number = 123
# if not manager.check_people_in(id_number):
#     print("a")

# 测试查看可选课程：
# person_1 = People("name_1", 123, 123, "Student")
# test_1 = ManagerLessons(person_1)
# lessons = test_1.find_available_lessons()
# print(lessons)
# 测试选课
# test_1.choose_lesson("电路", 123, 456)
# test_1.save_lessons()
# 测试人员类型
# land = Land(456, 789)
# person = land.wait_input()
# print(person.people_type)
# 删除课程
# person_2 = People(1, "A", 11, "Teacher")
# test_2 = ManagerLessons(person_2)
# test_2.cancel_lesson("电路", 1)
# test_2.save_lessons()
