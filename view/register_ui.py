import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from usecase.manager import ManagerPeoples


class RegisterUI(Gtk.Window):  # TODO  parent = ???  周五提到的那个？
    def __init__(self):
        register_glade_file = "ui/register.glade"  # ..表示返回至上级目录  未加..是表示该地址是相对于运行文件的相对地址(加会报错)，若单独运行则需要加..
        image_file = "image/school.jpg"
        self.register_builder = Gtk.Builder()
        self.register_builder.add_from_file(register_glade_file)
        self.register_window = self.register_builder.get_object("register_main_window")  # 名字不正确报错
        self.register_window.set_icon_from_file(image_file)
        self.register_window.set_title("用户注册")
        self.register_window.set_border_width(10)
        self.register_window.set_default_size(300, 100)

        # combobox init
        choose_type_combo = self.register_builder.get_object("choose_type_combobox")
        person_type_model = Gtk.ListStore(int, str)
        person_type_model.append([0, "老师"])
        person_type_model.append([1, "学生"])
        choose_type_combo.set_model(person_type_model)
        person_cell = Gtk.CellRendererText()
        choose_type_combo.pack_start(person_cell, True)
        choose_type_combo.add_attribute(person_cell, 'text', 1)
        choose_type_combo.set_active(0)  # TODO

        # button init
        confirm_button = self.register_builder.get_object("confirm_button")
        confirm_button.connect("clicked", self.confirm_register)

        cancel_button = self.register_builder.get_object("cancel_button")
        cancel_button.connect("clicked", self.close)

    def close(self, widget):
        self.register_window.close()

    def confirm_register(self, widget):
        try:
            name_entry = self.register_builder.get_object("user_name_entry")
            name = name_entry.get_text()

            id_number_entry = self.register_builder.get_object("id_entry")
            id_number = int(id_number_entry.get_text())

            password_entry = self.register_builder.get_object("password_entry")
            password = password_entry.get_text()

            choose_type_combo = self.register_builder.get_object("choose_type_combobox")
            type_index = choose_type_combo.get_active()
        except ValueError:
            dialog = Gtk.MessageDialog(self.register_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            # TODO 传入参数改成self会报错
            dialog.format_secondary_text("ID只能为纯数字，也不能为空")
            dialog.run()
            dialog.destroy()
        else:
            if name == '' or password == '':
                dialog = Gtk.MessageDialog(self.register_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("输入不能为空")
                dialog.run()
                dialog.destroy()
            else:
                manage_persons = ManagerPeoples()
                if not manage_persons.check_people_in(id_number):
                    dialog = Gtk.MessageDialog(self.register_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                    dialog.format_secondary_text("用户已存在")
                    dialog.run()
                    dialog.destroy()
                else:
                    if type_index == 0:
                        manage_persons.add_people(name, id_number, password, "Teacher")
                    if type_index == 1:
                        manage_persons.add_people(name, id_number, password, "Student")
                    dialog = Gtk.MessageDialog(self.register_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                    dialog.format_secondary_text("注册成功。欢迎您,{}".format(name))
                    dialog.run()
                    dialog.destroy()


# if __name__ == '__main__':
#     main_window = RegisterWindow()
#     Gtk.main()
