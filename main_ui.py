import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from usecase.manager import ManagerPeoples
from view.register_ui import RegisterUI
from view.users_ui import TeacherUI
from view.users_ui import StudentUI


class MainWindow(Gtk.Window):
    def __init__(self):
        glade_file = "ui/login_register.glade"
        image_file = "image/school.jpg"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.window = self.builder.get_object("main_window")
        self.window.set_title("教学管理系统")
        self.window.set_icon_from_file(image_file)
        self.window.set_border_width(10)
        self.window.set_default_size(300, 100)

        # register button init
        register_button = self.builder.get_object("register_button")
        register_button.connect("clicked", self.register)

        # login button init
        login_button = self.builder.get_object("login_button")
        login_button.connect("clicked", self.login)

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show()

    def check(self, id_number, password):
        manage_persons = ManagerPeoples()
        try:
            id_number = int(id_number)
            if not manage_persons.check_people_in(id_number) and manage_persons.check_password(id_number, password):
                person = manage_persons.find_person_by_id(id_number)
                return person
            else:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("用户不存在或密码错误")
                dialog.run()
                dialog.destroy()
                return None
        except ValueError:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("用户不存在")  # 当输入id不是数字时显示用户不存在
            dialog.run()
            dialog.destroy()
            return None

    def register(self, widget):
        ui = RegisterUI()
        self.window.show()
        ui.register_window.show()

    def login(self, widget):
        id_number_entry = self.builder.get_object("id_entry")
        id_number = id_number_entry.get_text()
        password_entry = self.builder.get_object("password_entry")
        password = password_entry.get_text()

        person = self.check(id_number, password)

        try:
            if person.people_type == "Teacher":
                ui = TeacherUI(person)
                self.window.hide()
                ui.window.show_all()  # show_all(),show()不会显示后加入的treeview中内容
            if person.people_type == "Student":
                ui = StudentUI(person)
                self.window.hide()
                ui.window.show_all()
        except AttributeError:
            pass


if __name__ == '__main__':
    main_window = MainWindow()
    Gtk.main()
