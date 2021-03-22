from entity.manager import ManagerPeoples

manager = ManagerPeoples()


class Register:
    def __init__(self, name, id_number, password):
        self._name = name
        self._id = id_number
        self._password = password
        self._type = None

    @staticmethod
    def view_people_type():
        return ["Teacher", "Student"]  # 注意类型的来源

    def check_people_type(self):
        people_type = input("请选择人员类型")
        if people_type not in ["Teacher", "Student"]:
            raise TypeError
        else:
            self._type = people_type

    def registering(self):
        if manager.check_people_in(self._id):
            manager.add_people(self._name, self._id, self._password, self._type)
        else:
            raise LookupError
