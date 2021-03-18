class People(object):
    def __init__(self, name):
        self._id_number = 0
        self._name = name
        self._password = None

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
        self.password = password

