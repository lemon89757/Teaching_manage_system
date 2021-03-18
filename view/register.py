from usecase.persons import Teacher
from usecase.persons import Student
from usecase.persons import Administrator
from entity.read_writre import ReadWrite


class Register:
    def __init__(self, name, id_number, password, kind):
        self._name = name
        self._id_number = id_number
        self._kind = kind
        self._person = None
        self._password = password

    # def choose_kind(self):
    #     if self._kind == "Teacher":
    #         self._person = Teacher(self._name)
    #         self._person.password = self._password
    #         self._person.id_number = self._id_number
    #     if self._kind == "Student":
    #         self._person = Student(self._name)
    #         self._person.password = self._password
    #         self._person.id_number = self._id_number
    #     if self._kind == "Administrator":
    #         self._person = Administrator(self._name)
    #         self._person.password = self._password
    #         self._person.id_number = self._id_number

    def check_exist(self):
        check = []
        get_msg = ReadWrite()
        data = get_msg.get_data().get(self._kind)
        for person_msg in data:
            check.append([person_msg[1]["ID"]])
        if self._id_number in check:
            raise ValueError

    def register(self):
        try:
            self.check_exist()
        except ValueError:
            print("用户已存在")
        else:
            get_msg = ReadWrite()
            data = get_msg.get_data().get(self._kind)
            if self._kind == "Teacher":
                self._person = Teacher(self._name)
                self._person.password = self._password
                self._person.id_number = self._id_number
                data.append([[{"姓名": self._person.name}, {"ID": self._person.id_number},
                              {"password": self._person.password}, {"所教课程相关信息": [[{'课程名': ''}, {"选课人数上限": 0},
                                                                                  {'选课学生': []}, {"选课学生人数": 0}]]}]])
            if self._kind == "Student":
                self._person = Student(self._name)
                self._person.password = self._password
                self._person.id_number = self._id_number
                data.append([{"姓名": self._person.name}, {"ID": self._person.id_number},
                             {"password": self._person.password}, {"所选课程相关信息": [[{'课程名': ''}, {"任课老师": ''},
                                                                                 {"选课人数上限": 0}, {"选课学生人数": 0}]]}])
            if self._kind == "Administrator":
                self._person = Administrator(self._name)
                self._person.password = self._password
                self._person.id_number = self._id_number
                data.append([{"姓名": self._person.name}, {"ID": self._person.id_number},
                             {"password": self._person.password}])
            get_msg.save()
