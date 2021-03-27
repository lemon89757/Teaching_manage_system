import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from entity.manager import ManagerPeoples

student_ui_glade_file = "ui/user_students.glade"
teacher_ui_glade_file = "ui/user_teachers.glade"
image_file = "image/school.jpg"
correct_password = 1
error_password = 2


class LoginWindow(Gtk.Window):
    """它包括两个界面，学生界面和老师界面以及修改密码界面"""
    def __init__(self, id_number, password):
        Gtk.Window.__init__(self, title="用户登陆")   # 设置这个title好像也没什么用
        self._person = None   # 登陆人员
        self.student_window = None
        self.teacher_window = None
        self.change_password_window = None
        self.change_password_builder = None
        self.manage_persons = ManagerPeoples()
        try:
            id_number = int(id_number)
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("用户不存在")  # 当输入id不是数字时显示用户不存在
            dialog.run()
            dialog.destroy()
        else:
            if not self.manage_persons.check_people_in(id_number):
                tag = self.manage_persons.check_password(id_number, password)
                if tag == correct_password:
                    self._person = self.manage_persons.find_person_by_id(id_number)
                    if self._person.people_type == "Teacher":
                        self.teacher_ui()
                    if self._person.people_type == "Student":
                        self.student_ui()
                if tag == error_password:
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                    dialog.format_secondary_text("密码错误")
                    dialog.run()
                    dialog.destroy()
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("用户不存在")
                dialog.run()
                dialog.destroy()

    def teacher_ui(self):   # TODO 注：没传入小控件就不需要widget？
        teacher_ui_builder = Gtk.Builder()
        teacher_ui_builder.add_from_file(teacher_ui_glade_file)
        self.teacher_window = teacher_ui_builder.get_object("teacher_main_window")  # 控件名字不正确后面会报错
        self.teacher_window.set_icon_from_file(image_file)
        self.teacher_window.set_title("老师界面")
        self.teacher_window.set_border_width(10)
        self.teacher_window.set_default_size(500, 300)

        # button init
        change_password_button = teacher_ui_builder.get_object("change_password_button")
        change_password_button.connect("clicked", self.change_password)

        self.teacher_window.connect("delete-event", Gtk.main_quit)
        self.teacher_window.show()

    def student_ui(self):
        student_ui_builder = Gtk.Builder()
        student_ui_builder.add_from_file(student_ui_glade_file)
        self.student_window = student_ui_builder.get_object("student_main_window")  # 控件名字不正确后面会报错
        self.student_window.set_icon_from_file(image_file)
        self.student_window.set_title("学生界面")
        self.student_window.set_border_width(10)
        self.student_window.set_default_size(500, 300)

        # button init
        change_password_button = student_ui_builder.get_object("change_password_button")
        change_password_button.connect("clicked", self.change_password)

        self.student_window.connect("delete-event", Gtk.main_quit)
        self.student_window.show()

    def change_password(self, widget):  # 感觉可以将这个界面单独做成一个类
        if not self.change_password_builder:
            change_password_glade_file = "ui/change_password.glade"
            self.change_password_builder = Gtk.Builder()
            self.change_password_builder.add_from_file(change_password_glade_file)
            self.change_password_window = self.change_password_builder.get_object("change_password_main_window")
            self.change_password_window.set_icon_from_file(image_file)
            self.change_password_window.set_title("修改密码界面")
            self.change_password_window.set_border_width(10)
            self.change_password_window.set_default_size(500, 200)

            # button init
            change_confirm_button = self.change_password_builder.get_object("confirm_button")
            change_confirm_button.connect("clicked", self.change_password_confirm)

            cancel_change_button = self.change_password_builder.get_object("cancel_button")
            cancel_change_button.connect("clicked", self.change_password_window_close)

            self.change_password_window.show()
        else:
            self.change_password_window.reshow_with_initial_size()

    def change_password_window_close(self, widget):
        self.change_password_window.close()

    def change_password_confirm(self, widget):
        # TODO 注：假如将不将change_password_builder放进初始化中，通过在该函数中直接复制相关语句，get_text()不能得到相应读数。
        #   可能是这样做使上个函数直接将空字符通过get_text()传入了，即使get_text()在这个函数中
        # entry init
        old_password_entry = self.change_password_builder.get_object("old_password_entry")
        old_password = old_password_entry.get_text()

        new_password_entry = self.change_password_builder.get_object("new_password_entry")
        new_password = new_password_entry.get_text()

        new_password_confirm_entry = self.change_password_builder.get_object("new_password_confirm_entry")
        new_password_confirm = new_password_confirm_entry.get_text()

        if old_password != self._person.password:
            dialog = Gtk.MessageDialog(self.change_password_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("原密码错误")
            dialog.run()
            dialog.destroy()
        elif new_password != new_password_confirm:
            dialog = Gtk.MessageDialog(self.change_password_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("两次输入的新密码不一致")
            dialog.run()
            dialog.destroy()
        else:
            self._person.password = new_password
            self.manage_persons.save_peoples()
            dialog = Gtk.MessageDialog(self.change_password_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("修改成功")
            dialog.run()
            dialog.destroy()
