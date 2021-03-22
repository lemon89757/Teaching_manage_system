from entity.manager import ManagerLessons
from entity.manager import ManagerPeoples

manage_peoples = ManagerPeoples()


class Land:
    def __init__(self, id_number, password):
        self._id_number = id_number
        self._password = password

    def landing(self):
        if not manage_peoples.check_people_in(self._id_number):
            tag = manage_peoples.check_password(self._id_number, self._password)
            if tag == 1:
                person = manage_peoples.find_person_by_id(self._id_number)
                if person.people_type == "Teacher":
                    land_msg = ["0修改密码", "1添加课程", "2取消课程", "3查看选课学生", "4查看任教课程信息", "Q退出系统", "yes"]
                    return land_msg
                if person.people_type == "Student":
                    land_msg = ["0修改密码", "5查看可选课程", "6选课", "7查看所选课程", "Q退出系统", "yes"]
                    return land_msg
            if tag == 2:
                land_msg = ["密码错误", "no"]
                return land_msg
        else:
            raise LookupError

    def get_name(self):
        if not manage_peoples.check_people_in(self._id_number):
            person = manage_peoples.find_person_by_id(self._id_number)
            return person.name

    def wait_input(self):  # 当弹出错误时重新等待输入
        person = manage_peoples.find_person_by_id(self._id_number)
        manage_lessons = ManagerLessons(person)
        ways = ["0", "1", "2", "3", "4", "5", "6", "7", "Q"]
        choose_way = input("输入您要进行的操作的对应数字")
        if choose_way in ways:
            if choose_way == "0":
                new_password = input("请输入新的密码")
                person.password = new_password
                msg = input("输入s以确定操作，其他输入则取消")
                if msg == 's':
                    manage_peoples.save_peoples()
                    print("操作成功")
                else:
                    raise ValueError
            if choose_way == "1":
                try:
                    lesson_name = input("请输入课程名")
                    lesson_teacher = person.id_number
                    lesson_limit = int(input("请输入限制人数，请输入阿拉伯数字"))
                except ValueError:
                    print("请输入限制人数，请输入阿拉伯数字")
                else:
                    manage_lessons.add_lesson(lesson_name, lesson_teacher, lesson_limit)
                    msg = input("输入s以确定操作，其他输入则取消")
                    if msg == 's':
                        manage_lessons.save_lessons()
                        print("操作成功")
                    else:
                        raise ValueError
            if choose_way == "2":
                lesson_name = input("请输入课程名")
                try:
                    manage_lessons.cancel_lesson(lesson_name, person.id_number)
                except ValueError:
                    print("未找到相应课程")
                else:
                    msg = input("输入s以确定操作，其他输入则取消")
                    if msg == 's':
                        manage_lessons.save_lessons()
                        print("操作成功")
                    else:
                        raise ValueError
            if choose_way == "3":
                lesson_name = input("请输入课程名")
                lesson_teacher_id = person.id_number
                students = manage_lessons.find_students_by_teacher_lesson(lesson_name, lesson_teacher_id)
                print(students)
            if choose_way == "4":
                lessons = manage_lessons.find_teach_lessons_by_teacher_id(person.id_number)
                print(lessons)
            if choose_way == "5":
                lessons = manage_lessons.find_available_lessons()
                print(lessons)
            if choose_way == "6":
                lesson_name = input("请输入选择的课程名")
                lesson_teacher_id = int(input("请输入老师的ID"))
                try:
                    manage_lessons.check_choose_lesson(lesson_name, lesson_teacher_id, person.id_number)
                    manage_lessons.choose_lesson(lesson_name, lesson_teacher_id, person.id_number)
                except ValueError:
                    print("未找到此课程")
                except TypeError:
                    print("您已经选择此课程了")
                else:
                    msg = input("输入s以确定操作，其他输入则取消")
                    if msg == 's':
                        manage_lessons.save_lessons()
                        print("操作成功")
                    else:
                        raise ValueError
            if choose_way == "7":
                choose_lessons = manage_lessons.find_choose_lessons_by_student_id(person.id_number)
                print(choose_lessons)
            if choose_way == "Q":
                print("完成退出")
                raise TypeError
        else:
            print("请输入正确的操作格式")

