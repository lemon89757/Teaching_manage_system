from entity.read_writre import ReadWrite
# from usecase.persons import


class Land:
    def __init__(self, id_number, password, kind):
        self.id = id_number
        self._password = password
        self.kind = kind

    def get_kind_msg(self):
        get_msg = ReadWrite()
        if self.kind == "Teacher":
            data = get_msg.get_data().get("teachers")
            ways = ['查看选课学生', '查看任课信息', '添加课程', '删除课程', '修改密码']
            return data, ways
        if self.kind == "Student":
            data = get_msg.get_data().get("students")
            ways = ['查看可选课程', '选课', '修改密码']
            return data, ways
        if self.kind == "Administrator":
            data = get_msg.get_data().get("administrators")
            ways = ['初始化 ', '添加课程', '删除课程', '修改密码']
            return data, ways

    def check_id_password(self):
        msg = self.get_kind_msg()[0]
        id_numbers = []
        id_numbers_password = []
        for person in msg:
            id_numbers.append([person[1]["ID"]])
            id_numbers_password.append([person[1]["ID"], person[2]["password"]])
        if self.id not in id_numbers:
            return '未找到此用户'
        elif [self.id, self._password] not in id_numbers_password:
            return '用户密码错误'
        else:
            for name in msg:
                if self.id == name[0]["姓名"]:
                    welcome = "欢迎" + name[0]["姓名"]
                    return welcome

# if __name__ == '__main__':
#     A = Land(1, 1, "Teacher")
#     A.get_kind_msg()
