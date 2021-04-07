import json
from entity.lesson import Lesson
from entity.people import People

file_path = r'C:\Users\helloTt\Desktop\tt\2021上半学期（电科）\learning_project\Teaching_manage_system\data.json'


def load_lessons():
    #  将json文件中"lessons"的内容对应到相应对象
    lessons = []
    try:
        with open(file_path) as file:
            data_json = json.load(file)
            # peoples = data_json["peoples"]
        for data in data_json["lessons"]:
            lesson = Lesson(data[0]["lesson_name"], data[1]["teacher_ID"], data[2]["limit_number"])
            lesson.students = data[3]["students"]
            lessons.append(lesson)
        return lessons
    except json.decoder.JSONDecodeError:
        # peoples = []
        return lessons


def load_lessons_dict():
    try:
        with open(file_path) as file:
            data_json = json.load(file)
            lessons = data_json["lessons"]
            return lessons
    except json.decoder.JSONDecodeError:
        lessons = []
        return lessons


def load_peoples():
    #  将json文件中"peoples"的内容对应到相应对象
    peoples = []
    try:
        with open(file_path) as file:
            data_json = json.load(file)
            # lessons = data_json["lessons"]
        for data in data_json["peoples"]:
            people = People(data[1]["name"], data[0]["ID"], data[2]["password"], data[3]["type"])
            peoples.append(people)
        return peoples
    except json.decoder.JSONDecodeError:
        # lessons = []
        return peoples


def load_peoples_dict():
    try:
        with open(file_path) as file:
            data_json = json.load(file)
            peoples = data_json["peoples"]
            return peoples
    except json.decoder.JSONDecodeError:
        peoples = []
        return peoples


class ManagerLessons:
    def __init__(self, person):
        self._lessons = load_lessons()
        self._peoples = load_peoples_dict()
        self._person = person

    def add_lesson(self, lesson_name, teacher_name, limit_number):  # 需要保存
        if self._person.people_type == "Teacher":
            lesson = Lesson(lesson_name, teacher_name, limit_number)
            self._lessons.append(lesson)
        else:
            pass

    def cancel_lesson(self, lesson_name, teacher_id):  # 需要保存
        if self._person.people_type == "Teacher":
            reference = len(self._lessons)
            through_lessons_number = 0
            for lesson in self._lessons:  # lesson为实例化的Lesson
                if lesson.name == lesson_name and lesson.teacher_id == teacher_id:
                    # == 条件
                    self._lessons.remove(lesson)
                else:
                    through_lessons_number += 1
            if reference == through_lessons_number:
                raise ValueError
        else:
            pass

    def find_name_by_id(self, id_number):
        #  通过id找名字
        for person in self._peoples:
            if id_number == person[0]["ID"]:
                name = person[1]["name"]
                return name

    def find_students_by_teacher_lesson(self, lesson_name, teacher_id):
        #  当任课老师没有此课程时返回值是None，有课程但没人选时返回[]
        if self._person.people_type == "Teacher":
            students_name = []
            for lesson in self._lessons:
                if lesson.name == lesson_name and lesson.teacher_id == teacher_id:
                    for student in lesson.students:
                        student_name = self.find_name_by_id(student)
                        students_name.append(student_name)
                    return students_name
        else:
            pass

    def find_available_lessons(self):
        if self._person.people_type == "Student":
            available_lessons = []
            for lesson in self._lessons:
                if lesson.number_students < lesson.limit_number and self._person.id_number not in lesson.students:
                    available_lesson = [lesson.name, lesson.teacher_id, lesson.limit_number, lesson.number_students]
                    available_lessons.append(available_lesson)
            return available_lessons
        else:
            pass

    def check_choose_lesson(self, lesson_name, teacher_id, student_id):
        for lesson in self._lessons:
            if lesson.name == lesson_name and lesson.teacher_id == teacher_id:
                if student_id in lesson.students:
                    raise AttributeError

    def choose_lesson(self, lesson_name, teacher_id, student_id):  # 需要保存
        if self._person.people_type == "Student":
            lessons_number = 0
            for lesson in self._lessons:
                if lesson.name == lesson_name and lesson.teacher_id == teacher_id:
                    lesson.students.append(student_id)
                else:
                    lessons_number += 1
            if lessons_number == len(self._lessons):
                raise ValueError
        else:
            pass

    def cancel_choose_lesson(self, lesson_name, teacher_id, student_id):  # 需要保存
        if self._person.people_type == "Student":
            for lesson in self._lessons:
                if teacher_id == lesson.teacher_id and lesson_name == lesson.name:
                    if student_id in lesson.students:
                        lesson.students.remove(student_id)
        else:
            pass

    def find_teach_lessons_by_teacher_id(self, id_number):
        if self._person.people_type == "Teacher":
            #  通过id查找其所教课程
            teach_lessons = []
            for lesson in self._lessons:
                if lesson.teacher_id == id_number:
                    students_name = []
                    for student in lesson.students:
                        student_name = self.find_name_by_id(student)
                        students_name.append(student_name)
                    teach_lesson = [lesson.name, lesson.limit_number, students_name, lesson.number_students]
                    teach_lessons.append(teach_lesson)
            return teach_lessons
        else:
            pass

    def find_choose_lessons_by_student_id(self, id_number):
        if self._person.people_type == "Student":
            #  通过id查找其所选课程
            choose_lessons = []
            for lesson in self._lessons:
                if id_number in lesson.students:
                    choose_lesson = [lesson.name, lesson.teacher_id, lesson.limit_number, lesson.number_students]
                    choose_lessons.append(choose_lesson)
            return choose_lessons
        else:
            pass

    def find_lesson_by_lesson_name_and_teacher_id(self, lesson_name, teacher_id):
        count = 0
        for lesson in self._lessons:
            if lesson_name == lesson.name and teacher_id == lesson.teacher_id:
                return lesson
            else:
                count += 1
        if count == len(self._lessons):
            raise ValueError

    def save_lessons(self):
        #  将对象转换为json文件中的相应格式
        peoples = self._peoples
        lessons = []
        for lesson in self._lessons:
            a_lesson = [{"lesson_name": lesson.name}, {"teacher_ID": lesson.teacher_id},
                        {"limit_number": lesson.limit_number}, {"students": lesson.students},
                        {"number_students": lesson.number_students}]
            lessons.append(a_lesson)
        data = dict()
        data["lessons"] = lessons
        data["peoples"] = peoples
        data_json = json.dumps(data)
        with open(file_path, 'w') as file:
            file.write(data_json)


class ManagerPeoples:
    def __init__(self):
        self._peoples = load_peoples()
        self._lessons = load_lessons_dict()

    def add_people(self, name, id_number, password, people_type):  # 需要保存
        people = People(name, id_number, password, people_type)
        self._peoples.append(people)
        self.save_peoples()

    def check_people_in(self, id_number):
        peoples_id_number = []
        for people in self._peoples:
            peoples_id_number.append(people.id_number)
        if id_number in peoples_id_number:
            return False
        else:
            return True

    def check_password(self, id_number, password):
        for people in self._peoples:
            if people.id_number == id_number:
                if people.password == password:
                    return True
                else:
                    return False
    #  改之前（命令行实现）True对应1，False对应2

    def find_person_by_id(self, id_number):
        #  通过id找人
        for person in self._peoples:
            if id_number == person.id_number:
                return person

    def update_modification(self, modify_person):
        for person in self._peoples:
            if person.id_number == modify_person.id_number:
                person.password = modify_person.password
        self.save_peoples()

    def save_peoples(self):
        #  将对象转换为json文件中的相应格式
        peoples = []
        for people in self._peoples:
            a_people = [{"ID": people.id_number}, {"name": people.name},
                        {"password": people.password}, {"type": people.people_type}]
            peoples.append(a_people)
        data = dict()
        data["lessons"] = self._lessons
        data["peoples"] = peoples
        data_json = json.dumps(data)
        with open(file_path, 'w') as file:
            file.write(data_json)

# TODO  更新修改、copy、deepcopy
