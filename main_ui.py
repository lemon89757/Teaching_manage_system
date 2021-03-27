import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from view.register_ui import RegisterWindow
from view.login_ui import LoginWindow


class MainWindow(Gtk.Window):
    def __init__(self):
        glade_file = "ui/login_register.glade"
        image_file = "image/school.jpg"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.window = self.builder.get_object("main_window")
        self.window.set_title("教学管理系统")
        self.window.set_icon_from_file(image_file)
        self.person = None  # 这个是登陆用户
        self.register_ui = None
        self.login_ui = None

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

    def register(self, widget):
        if self.register_ui:
            self.register_ui.register_window.reshow_with_initial_size()
        else:
            self.register_ui = RegisterWindow()
            # self.register_ui.show()  , object at 0x000001fc1b376340 of type RegisterWindow is not initialized
            # 改正：self.register_ui.register_window.show()

    def login(self, widget):
        # entry init
        id_number_entry = self.builder.get_object("id_entry")
        id_number = id_number_entry.get_text()
        password_entry = self.builder.get_object("password_entry")
        password = password_entry.get_text()
        if self.login_ui:
            pass   # 限制只能同时登陆一个用户
        else:
            self.login_ui = LoginWindow(id_number, password)


if __name__ == '__main__':
    main_window = MainWindow()
    Gtk.main()
