import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from view.register import Register
from view.land import Land
from entity.manager import ManagerLessons
from entity.manager import ManagerPeoples


# class RegisterWindow(Gtk.Window):  # TODO  parent = ???  周五提到的那个？
#     def __init__(self):
#         Gtk.Window.__init__(self, title="register")
#         self.set_border_width(10)
#         self.set_default_size(500, 300)
#
#         register_glade_file = "../ui/register.glade"  # ..表示返回至上级目录
#         self.builder = Gtk.Builder()
#         self.builder.add_from_file(register_glade_file)
#         self.window = self.builder.get_object("main_window")
#
#         choose_type_combo = self.builder.get_object("choose_type_combobox")
#         person_type_model = Gtk.ListStore(int, str)
#         person_type_model.append([0, "老师"])
#         person_type_model.append([1, "学生"])
#         choose_type_combo.set_model(person_type_model)
#         person_cell = Gtk.CellRendererText()
#         choose_type_combo.pack_start(person_cell, True)
#         choose_type_combo.add_attribute(person_cell, 'text', 1)
#         choose_type_combo.set_active(0)  # TODO
#
#         # button init
#         # confirm_button = self.builder.get_object("confirm_button")
#         # confirm_button.connect("clicked", self.confirm)
#
#         cancel_button = self.builder.get_object("cancel_button")
#         cancel_button.connect("clicked", Gtk.main_quit)  # TODO 可以不可以只是关闭当前界面而不结束程序,hide,先判断该窗口在不在
#
#         # self.window.connect("delete-event", Gtk.main_quit)
#         self.window.show()


class MainWindow(Gtk.Window):  # TODO 可以将界面做成不同的类？ 一个界面弹出时怎么在保证程序继续运行的情况下，删除之前界面，同一账户成功登陆后还能继续登录生成新的界面，或者点开注册
    def __init__(self):
        # Gtk.Window.__init__(self, title="login or register")

        glade_file = "login_register.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.window = self.builder.get_object("main_window")
        self.person = None  # 这个是登陆用户

        self.window.set_border_width(10)
        self.window.set_default_size(900, 300)

        # register button init
        register_button = self.builder.get_object("register_button")
        register_button.connect("clicked", self.register)

        # login button init
        login_button = self.builder.get_object("login_button")
        login_button.connect("clicked", self.login)  # view.Land    # TODO 尺寸设置不起作用？

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()
        # self.show()

    # @staticmethod
    # def register_window(self):
    #     a = RegisterWindow()

    def login(self, widget):
        id_number_entry = self.builder.get_object("id_entry")
        id_number = int(id_number_entry.get_text())

        password_entry = self.builder.get_object("password_entry")
        password = password_entry.get_text()

        land = Land(id_number, password)
        try:
            self.person = land.landing()   # 实例化该登陆用户
            if self.person.people_type == "Teacher":
                self.teacher_ui()  # TODO 上面不需要加括号？ 未直接调用
            if self.person.people_type == "Student":
                self.student_ui()
        except LookupError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("用户不存在")
            dialog.run()
            dialog.destroy()
        except AssertionError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("密码错误")
            dialog.run()
            dialog.destroy()

    def teacher_ui(self):
        teacher_glade_file = "user_teachers.glade"
        self.builder.add_from_file(teacher_glade_file)
        self.window = self.builder.get_object("main_window")

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def student_ui(self):
        student_glade_file = "user_students.glade"
        self.builder.add_from_file(student_glade_file)
        self.window = self.builder.get_object("main_window")
        # self.window_2
        # button init
        manager_lessons = ManagerLessons(self.person)
        confirm_choose_lessons_button = self.builder.get_object("confirm_choose_lessons_button")  # 确认选课,并非调用land中方法
        # confirm_choose_lessons_button.connect("clicked", manager_lessons.save_lessons())

        change_password_button = self.builder.get_object("change_password_button")  # 修改密码
        change_password_button.connect("clicked", self.change_password)

        exit_button = self.builder.get_object("exit_button")  # 退出系统
        exit_button.connect("clicked", Gtk.main_quit)

        cancel_choose_lessons_button = self.builder.get_object("cancel_choose_lesson_button")
        cancel_choose_lessons_button.connect("clicked", self.cancel_choose_lessons)  # TODO 按键弹不出取消课程界面

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def cancel_choose_lessons(self, widget):  # 需要传入widget
        cancel_choose_lessons_glade_file = "cancel_lessons.glade"
        self.builder.add_from_file(cancel_choose_lessons_glade_file)
        self.window = self.builder.get_object("main_window")

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def change_password(self, widget):
        change_password_glade_file = "change_password.glade"
        self.builder.add_from_file(change_password_glade_file)
        self.window = self.builder.get_object("main_window")

        # cancel button
        cancel_button = self.builder.get_object("cancel_button")
        cancel_button.connect("clicked", Gtk.main_quit)
        # confirm button
        confirm_button = self.builder.get_object("confirm_button")
        confirm_button.connect("clicked", self.change_password_confirm)

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def change_password_confirm(self, widget):
        # entry init
        old_password_entry = self.builder.get_object("old_password_entry")
        old_password = old_password_entry.get_text()
        new_password_entry = self.builder.get_object("new_password_entry")
        new_password = new_password_entry.get_text()
        new_password_confirm_entry = self.builder.get_object("new_password_confirm_entry")
        new_password_confirm = new_password_confirm_entry.get_text()

        if self.person.password == old_password:
            if new_password == new_password_confirm:
                self.person.password = new_password
                manager_persons = ManagerPeoples()
                manager_persons.save_peoples()  # TODO 修改密码保存不了
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("密码修改成功")
                dialog.run()
                dialog.destroy()
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("两次新密码输入不同")
                dialog.run()
                dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("原密码不正确")
            dialog.run()
            dialog.destroy()

    def register(self, widget):
        register_glade_file = "register.glade"  # TODO 需要用到小部件时才给函数传入widget？
        self.builder.add_from_file(register_glade_file)
        self.window = self.builder.get_object("main_window")

        choose_type_combo = self.builder.get_object("choose_type_combobox")
        person_type_model = Gtk.ListStore(int, str)
        person_type_model.append([0, "老师"])
        person_type_model.append([1, "学生"])
        choose_type_combo.set_model(person_type_model)
        person_cell = Gtk.CellRendererText()
        choose_type_combo.pack_start(person_cell, True)
        choose_type_combo.add_attribute(person_cell, 'text', 1)
        choose_type_combo.set_active(0)

        # button init
        confirm_button = self.builder.get_object("confirm_button")
        confirm_button.connect("clicked", self.confirm_register)

        cancel_button = self.builder.get_object("cancel_button")
        cancel_button.connect("clicked", Gtk.main_quit)

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def confirm_register(self, widget):
        try:
            name_entry = self.builder.get_object("user_name_entry")
            name = name_entry.get_text()

            id_number_entry = self.builder.get_object("id_entry")
            id_number = int(id_number_entry.get_text())

            password_entry = self.builder.get_object("password_entry")
            password = password_entry.get_text()

            choose_type_combo = self.builder.get_object("choose_type_combobox")
            type_index = choose_type_combo.get_active()
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("输入为空或ID不是纯数字")
            dialog.run()
            dialog.destroy()
        else:
            if name == '' or password == '':
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("输入不能为空")
                dialog.run()
                dialog.destroy()
            else:
                register = Register(name, id_number, password)
                if type_index == 0:
                    register.check_people_type("Teacher")
                if type_index == 1:
                    register.check_people_type("Student")
                try:
                    register.registering()
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                    dialog.format_secondary_text("注册成功。欢迎您,{}".format(name))
                    dialog.run()
                    dialog.destroy()
                except LookupError:
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                    dialog.format_secondary_text("用户已存在")
                    dialog.run()
                    dialog.destroy()


if __name__ == '__main__':
    main_window = MainWindow()
    Gtk.main()
