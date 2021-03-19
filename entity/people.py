class People(object):
    def __init__(self, name, id_number, password, people_type):
        self._id_number = id_number
        self._name = name
        self._password = password
        self._type = people_type

    @property
    def id_number(self):
        return self._id_number

    @id_number.setter
    def id_number(self, id_number):
        self._id_number = id_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        # 初始设置和修改密码
        self._password = password

    @property
    def people_type(self):
        return self._type

    @people_type.setter
    def people_type(self, people_type):
        self._type = people_type


