import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from entity.manager import ManagerPeoples
from entity.manager import ManagerLessons

student_ui_glade_file = "ui/user_students.glade"
teacher_ui_glade_file = "ui/user_teachers.glade"
image_file = "image/school.jpg"
correct_password = 1
error_password = 2


class LoginWindow(Gtk.Window):
    """它包括多个界面，学生界面和老师界面以及修改密码界面"""
    def __init__(self, id_number, password):
        Gtk.Window.__init__(self, title="用户登陆")   # 设置这个title好像也没什么用
        self._person = None   # 登陆人员
        self.student_window = None
        self.teacher_window = None
        self.change_password_window = None
        self.add_lesson_window = None
        self.teacher_ui_builder = None
        self.student_ui_builder = None
        self.change_password_builder = None
        self.add_lesson_builder = None
        self._lesson_name = ''
        self.manage_persons = ManagerPeoples()
        self.c_window_state = False

        # person = check_in(id, pwd)
        # init_manage_page(person)
        #
        # ui = get_check_ui()


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
        self.teacher_ui_builder = Gtk.Builder()
        self.teacher_ui_builder.add_from_file(teacher_ui_glade_file)
        self.teacher_window = self.teacher_ui_builder.get_object("teacher_main_window")  # 控件名字不正确后面会报错
        self.teacher_window.set_icon_from_file(image_file)
        self.teacher_window.set_title("老师界面")
        self.teacher_window.set_border_width(10)
        self.teacher_window.set_default_size(500, 300)

        # label init
        welcome_label = self.teacher_ui_builder.get_object("welcome_label")
        welcome_label.set_text("欢迎您，{}".format(self._person.name))

        # button init
        change_password_button = self.teacher_ui_builder.get_object("change_password_button")
        change_password_button.connect("clicked", self.change_password)

        add_lesson_button = self.teacher_ui_builder.get_object("add_lessons_button")
        add_lesson_button.connect("clicked", self.add_lesson)

        exit_button = self.teacher_ui_builder.get_object("exit_button")
        exit_button.connect("clicked", Gtk.main_quit)

        cancel_lesson_button = self.teacher_ui_builder.get_object("cancel_lesson_button")
        cancel_lesson_button.connect("clicked", self.cancel_lessons)

        # TODO listbox方法？
        # teach_lessons_listbox = self.teacher_ui_builder.get_object("teach_lessons_listbox")
        vbox = Gtk.VBox()  # TODO 还不能同步显示
        teach_lessons_scrolled_window = self.teacher_ui_builder.get_object("teach_lessons_scrolled_window")
        vbox.pack_start(teach_lessons_scrolled_window, True, True, 0)

        store = self.create_model()

        teach_lessons_tree_view = self.teacher_ui_builder.get_object("teach_lessons_tree_view")
        teach_lessons_tree_view.set_model(store)  # TODO
        teach_lessons_tree_view.connect("row-activated", self.on_activated)  # 双击才能选中目标
        teach_lessons_tree_view.set_rules_hint(True)

        self.create_columns(teach_lessons_tree_view)

        self.teacher_window.connect("delete-event", Gtk.main_quit)
        self.teacher_window.show()

    @staticmethod
    def create_columns(tree_view):
        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("课程名", renderer_text, text=0)
        column.set_sort_column_id(0)
        tree_view.append_column(column)

        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("限制人数", renderer_text, text=1)
        column.set_sort_column_id(1)
        tree_view.append_column(column)

        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("选课人数", renderer_text, text=2)
        column.set_sort_column_id(2)
        tree_view.append_column(column)

    def create_model(self):
        manage_lessons = ManagerLessons(self._person)
        lessons = manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
        store = Gtk.ListStore(str, int, int)
        for lesson in lessons:
            store.append([lesson[0], lesson[1], lesson[3]])
        return store

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        self._lesson_name = model[row][0]

    def cancel_lessons(self, widget):
        manage_lessons = ManagerLessons(self._person)
        try:
            manage_lessons.cancel_lesson(self._lesson_name, self._person.id_number)
            manage_lessons.save_lessons()
            dialog = Gtk.MessageDialog(self.teacher_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("取消成功")
            dialog.run()
            dialog.destroy()
        except ValueError:
            dialog = Gtk.MessageDialog(self.teacher_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("未找到此课程")
            dialog.run()
            dialog.destroy()

    def student_ui(self):
        self.student_ui_builder = Gtk.Builder()
        self.student_ui_builder.add_from_file(student_ui_glade_file)
        self.student_window = self.student_ui_builder.get_object("student_main_window")  # 控件名字不正确后面会报错
        self.student_window.set_icon_from_file(image_file)
        self.student_window.set_title("学生界面")
        self.student_window.set_border_width(10)
        self.student_window.set_default_size(500, 300)

        # label init
        welcome_label = self.student_ui_builder.get_object("welcome_label")
        welcome_label.set_text("欢迎您，{}".format(self._person.name))

        # button init
        change_password_button = self.student_ui_builder.get_object("change_password_button")
        change_password_button.connect("clicked", self.change_password)

        self.student_window.connect("delete-event", Gtk.main_quit)
        self.student_window.show()

    def add_lesson(self, widget):
        if not self.add_lesson_builder:
            add_lesson_glade_file = 'ui/add_lessons.glade'
            self.add_lesson_builder = Gtk.Builder()
            self.add_lesson_builder.add_from_file(add_lesson_glade_file)
            self.add_lesson_window = self.add_lesson_builder.get_object("add_lesson_main_window")
            self.add_lesson_window.set_icon_from_file(image_file)
            self.add_lesson_window.set_title("添加课程界面")
            self.add_lesson_window.set_border_width(10)
            self.add_lesson_window.set_default_size(500, 100)

            # label init
            welcome_label = self.add_lesson_builder.get_object("welcome_label")
            welcome_label.set_text("欢迎您，{}".format(self._person.name))

            # button init
            confirm_add_lesson_button = self.add_lesson_builder.get_object('confirm_button')
            confirm_add_lesson_button.connect("clicked", self.add_lesson_confirm)

            self.add_lesson_window.show()
        else:
            # TODO self.add_lesson_window = self.add_lesson_builder.get_object("add_lesson_main_window") 删除之后再点开却是空的
            # self.add_lesson_window.show()
            self.add_lesson_window.reshow_with_initial_size()

    def add_lesson_confirm(self, widget):
        manage_lessons = ManagerLessons(self._person)
        # entry init
        add_lesson_name_entry = self.add_lesson_builder.get_object("add_lesson_name_entry")
        add_lesson_name = add_lesson_name_entry.get_text()

        limit_number_entry = self.add_lesson_builder.get_object("limit_number_entry")
        try:
            limit_number = int(limit_number_entry.get_text())
        except ValueError:
            dialog = Gtk.MessageDialog(self.add_lesson_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("请输入阿拉伯数字")
            dialog.run()
            dialog.destroy()
        else:
            teach_lessons_name = []
            teach_lessons = manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
            for teach_lesson in teach_lessons:
                teach_lessons_name.append(teach_lesson[0])
            if add_lesson_name in teach_lessons_name:
                dialog = Gtk.MessageDialog(self.add_lesson_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("您已经添加了此课程")
                dialog.run()
                dialog.destroy()
            else:
                manage_lessons.add_lesson(add_lesson_name, self._person.id_number, limit_number)  # 此处将老师名字改成了老师id
                manage_lessons.save_lessons()
                dialog = Gtk.MessageDialog(self.add_lesson_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("添加课程成功")
                dialog.run()
                dialog.destroy()

    def change_password(self, widget):  # 感觉可以将这个界面单独做成一个类
        if not self.c_window_state:
            change_password_glade_file = "ui/change_password.glade"
            self.change_password_builder = Gtk.Builder()
            self.change_password_builder.add_from_file(change_password_glade_file)
            self.change_password_window = self.change_password_builder.get_object("change_password_main_window")
            self.change_password_window.set_icon_from_file(image_file)
            self.change_password_window.set_title("修改密码界面")
            self.change_password_window.set_border_width(10)
            self.change_password_window.set_default_size(500, 200)

            # label init
            welcome_label = self.change_password_builder.get_object("welcome_label")
            welcome_label.set_text("欢迎您，{}".format(self._person.name))

            # button init
            change_confirm_button = self.change_password_builder.get_object("confirm_button")
            change_confirm_button.connect("clicked", self.change_password_confirm)

            cancel_change_button = self.change_password_builder.get_object("cancel_button")
            cancel_change_button.connect("clicked", self.change_password_window_close)

            self.change_password_window.connect('delete-event', self.hide)

            self.change_password_window.show_all()
            self.c_window_state = True
        else:
            self.change_password_window.hide()
            self.c_window_state = False

    def hide(self, *args):
        self.change_password_window.hide()
        self.c_window_state = False

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
# TODO 刷新函数、做成不同的类、hide