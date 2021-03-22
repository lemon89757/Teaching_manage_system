# {"lessons":[[{"lesson_name":''}, {"teacher_ID":''}, {"limit_number":0}, {"students":[学生的ID]}, {"number_students":0}]]}
# {"peoples":[[{"ID":0}, {"name":''}, {"password":None}, {"type":''}]]
# 左下角TODO标记
from view.register import Register
from view.land import Land

REG_FUNCTION = '0'
LOGIN_FUNCTION = '1'


def register_user():
    name = input("输入您的用户名")
    id_number = int(input("输入您的纯数字用户ID"))  # raise ValueError
    password = input("设置您的密码")
    register = Register(name, id_number, password)

    print("从以下类型中选择您的人员类型")     # 人员类型不应自己给出，应访问相应程序得到人员类型，避免后续需改中的麻烦
    print(register.view_people_type())
    register.check_people_type()  # raise TypeError

    register.registering()  # raise LookUpError
    print("欢迎您", name)


def login_user():
    id_number = int(input("输入您的纯数字用户ID"))  # raise ValueError
    password = input("输入您的密码")
    land = Land(id_number, password)

    msg = land.landing()  # raise LookUpError 登陆失败，用户不存在

    if msg[-1] == "yes":  # 登陆成功
        print("欢迎您,{}".format(land.get_name()))
        print("可进行的操作：{}".format(msg[:-1]))
        while True:
            try:
                land.wait_input()
                continue
            except ValueError:
                continue
            except TypeError:
                break

    if msg[-1] == "no":  # 登陆失败,密码错误
        print("登陆失败")
        print("原因：{}".format(str(msg[0])))


if __name__ == '__main__':
    tag = input("输入0进行注册，输入1进行登录")
    if tag == REG_FUNCTION:
        while True:
            try:
                register_user()
                print("注册成功")
                break
            except ValueError:
                print("请确认输入ID为纯数字")
                exit_register_tag = input("按Q退出注册，任意按键继续")
            except TypeError:
                print("请选择正确的人员类型")
                exit_register_tag = input("按Q退出注册，任意按键继续")
            except LookupError:
                print("用户ID已存在")
                exit_register_tag = input("按Q退出注册，任意按键继续")
            if exit_register_tag == 'Q':
                break
    elif tag == LOGIN_FUNCTION:
        while True:
            try:
                login_user()
                break
            except ValueError:
                print("请确认输入ID为纯数字")
                exit_land_tag = input("按Q退出登陆，任意按键继续")
            except LookupError:
                print("用户ID不存在")
                exit_land_tag = input("按Q退出登陆，任意按键继续")
            if exit_land_tag == 'Q':
                break
    else:
        print("请输入正确的选项")
