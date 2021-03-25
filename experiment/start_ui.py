import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from view.register import Register


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="user login")
        self.set_border_width(10)
        self.set_default_size(500, 300)

        glade_file = "login_register.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.window = self.builder.get_object("main_window")

        # register init
        register_button = self.builder.get_object("register_button")
        register_button.connect("clicked", self.register)

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def register(self, widget):
        register_glade_file = "register.glade"  # TODO
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
        choose_type_combo.set_active(0)  # TODO

        # button init
        confirm_button = self.builder.get_object("confirm_button")
        confirm_button.connect("clicked", self.confirm)

        cancel_button = self.builder.get_object("cancel_button")
        cancel_button.connect("clicked", Gtk.main_quit)  # TODO

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def confirm(self, widget):
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
