# {"lessons":[[{"lesson_name":''}, {"teacher_ID":''}, {"limit_number":0}, {"students":[学生的ID]}, {"number_students":0}]]}
# {"peoples":[[{"ID":0}, {"name":''}, {"password":None}, {"type":''}]]
from view.register import Register


if __name__ == '__main__':
    tag = input("输入0进行注册，输入1进行登录")
    if tag == '0':
        while True:
            try:
                name = input("输入您的用户名")
                id_number = int(input("输入您的用户ID，纯数字"))
                password = input("设置您的密码")
            except ValueError:
                print("请设置ID为纯数字")
                continue
            else:
                register = Register(name, id_number, password)
                print("从以下类型中选择您的人员类型")
                print(register.view_people_type())
                try:
                    register.get_people_type()
                except ValueError:
                    print("请输入正确格式的人员类型")
                    continue
                else:
                    try:
                        register.registering()
                        print("欢迎您", name)
                        break
                    except ValueError:
                        print("用户ID已存在")
                        tag = input("输入2结束，其他继续注册")
                        if tag == '2':
                            break
                        else:
                            continue
    if tag == '1':
        while True:
            id_number = input("请输入您的ID")
            password = input("请输入您的用户密码")
