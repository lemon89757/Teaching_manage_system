from lesson import Lesson
from read_writre import ReadWrite


class ManagerLesson:
    def __init__(self, lesson_name, teacher, tag):
        self._read_write = ReadWrite()
        self._lessons = self._read_write.get_data().get("lessons")
        self._teachers = self._read_write.get_data().get("teachers")
        self._students = self._read_write.get_data().get("students")
        self._administrator = self._read_write.get_data().get("administrators")
        self.lesson = Lesson(lesson_name, teacher)
        self._tag = tag

    def add_lesson(self, limit_number):
        if self._tag == 0 or self._tag == 1:
            self.lesson.limit_number = limit_number
            # 课程信息中添加课程
            self._lessons.append([{"课程名": self.lesson.name}, {"任课老师": self.lesson.teacher},
                                  {"选课人数上限": self.lesson.limit_number}, {"选课学生": self.lesson.student},
                                  {"选课学生人数": self.lesson.number_student}])
            # 老师信息中添加课程
            for teacher in self._teachers:
                if self.lesson.teacher == teacher[0]['姓名']:
                    msg = self._teachers[3].get("所教课程相关信息")
                    msg.append([{'课程名': self.lesson.name}, {"选课人数上限": self.lesson.limit_number},
                                {'选课学生': self.lesson.student}, {"选课学生人数": self.lesson.number_student}])
                    self._teachers[3].update({"所教课程相关信息": msg})
            self._read_write.save()  # 保存至文件
        else:
            pass

    def check_teacher_lesson(self):
        # 检查老师是否任教某节课,没有则引起错误
        check = []
        for teacher_msg in self._teachers:
            for teacher_lesson in teacher_msg[3].values():
                check.append([teacher_msg[0]["姓名"], teacher_lesson[0]['课程名']])
        if [self.lesson.teacher, self.lesson.name] not in check:
            raise ValueError

    def delete_lesson(self):
        if self._tag == 0 or self._tag == 1:
            try:
                self.check_teacher_lesson()
            except ValueError:
                return "未找到此课程"
            else:
                for teacher in self._teachers:  # 删除self._teachers中相关信息
                    if self.lesson.teacher == teacher[0]['姓名']:
                        msg = self._teachers[3].get("所教课程相关信息")
                        for teacher_lesson in msg:
                            if self.lesson.name == teacher_lesson[0]['课程名']:
                                msg.remove(teacher_lesson)
                for teacher_lesson in self._lessons:  # 删除self._lessons中相关信息
                    if [self.lesson.name, self.lesson.teacher] == [teacher_lesson[0]['课程名'], teacher_lesson[1]['任课老师']]:
                        self._lessons.remove(teacher_lesson)
                for student_lesson in self._students:  # 删除self._students中相关信息
                    msg = student_lesson[3].get("所选课程相关信息")
                    for lesson in msg:
                        if self.lesson.name == lesson[0]['课程名'] and self.lesson.teacher == lesson[1]["任课老师"]:
                            msg.remove(lesson)
            self._read_write.save()
        else:
            pass

    def teacher_view_lessons(self):
        # 感觉这个方法不应改放在课程管理类里，可以直接给老师这个类型
        if self._tag == 1 or self._tag == 0:
            for teacher in self._teachers:
                if self.lesson.teacher == teacher[0]['姓名']:
                    teacher_lessons = teacher[3].get("所教课程相关信息")
                    return teacher_lessons
                else:
                    return "未找到相关信息"
        else:
            pass

    def view_students_by_teacher_lesson(self):
        if self._tag == 1 or self._tag == 0:
            try:
                self.check_teacher_lesson()
            except ValueError:
                return "未找到此课程"
            else:
                for teacher_lesson in self._lessons:
                    if [self.lesson.name, self.lesson.teacher] == [teacher_lesson[0]['课程名'], teacher_lesson[1]['任课老师']]:
                        return teacher_lesson[3]['选课学生']
        else:
            pass

    def view_available_lesson(self):
        if self._tag == 0 or self._tag == 2:
            available_lesson = []
            for student_lesson in self._lessons:
                if student_lesson[4]["选课学生人数"] < student_lesson[2]["选课人数上限"]:
                    student_lesson.pop(3)
                    available_lesson.append(student_lesson)
            return available_lesson
        else:
            pass

    def check_choose_lesson(self):
        available_lesson = self.view_available_lesson()
        check = []
        for student_lesson in available_lesson:
            msg = [student_lesson[0]["课程名"], student_lesson[1]["任课老师"]]
            check.append(msg)
        if [self.lesson.name, self.lesson.teacher] not in check:
            raise ValueError

    def choose_lesson(self, student_id, student_name):
        if self._tag == 2:
            try:
                self.check_choose_lesson()
            except ValueError:
                return "请选择可选课程"
            else:
                for student in self._students:  # 学生信息添加选课
                    if student_id == student[1]["ID"]:
                        lesson_msg = student[3].get("所选课程相关信息")
                        self.lesson.add_student(student_name)
                        lesson_msg.append([{'课程名': self.lesson.name}, {"任课老师": self.lesson.teacher},
                                           {"选课人数上限": self.lesson.limit_number}, {"选课学生人数": self.lesson.number_student}])
                        self._students[3].update({"所选课程相关信息": lesson_msg})
                for teacher in self._teachers:  # 老师信息添加选课
                    if self.lesson.teacher == teacher[0]["姓名"]:
                        msg = teacher[3].get("所教课程相关信息")
                        for lesson_name in msg:
                            if self.lesson.name == lesson_name[0]['课程名']:
                                lesson_name[2]['选课学生'].append(student_name)
                                lesson_name[3]["选课学生人数"] = self.lesson.number_student
                for lessons_data in self._lessons:  # 课程信息添加选课
                    if self.lesson.name == lessons_data[0]["课程名"] and self.lesson.teacher == lessons_data[1]["任课老师"]:
                        lessons_data[3]["选课学生"].append(student_name)
                        lessons_data[4]["选课学生人数"] = self.lesson.number_student
            self._read_write.save()
        else:
            pass

