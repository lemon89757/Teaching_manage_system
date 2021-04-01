import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from usecase.manager import ManagerPeoples
from usecase.manager import ManagerLessons

image_file = "image/school.jpg"


class BeforeLogin(Gtk.Window):
    def __init__(self, id_number, password):
        Gtk.Window.__init__(self, title="用户提示")
        self.id_number = id_number
        self.password = password
        self.set_border_width(10)
        self.set_default_size(200, 100)

    def check(self):
        manage_persons = ManagerPeoples()
        try:
            id_number = int(self.id_number)
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("用户不存在")  # 当输入id不是数字时显示用户不存在
            dialog.run()
            dialog.destroy()
            return None
        else:
            if not manage_persons.check_people_in(id_number) and manage_persons.check_password(id_number, self.password):
                person = manage_persons.find_person_by_id(id_number)
                return person
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("用户不存在或密码错误")
                dialog.run()
                dialog.destroy()
                return None


class TeacherUI(Gtk.Window):
    def __init__(self, person):
        teacher_ui_glade_file = "ui/user_teachers.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(teacher_ui_glade_file)
        self.window = self.builder.get_object("teacher_main_window")  # 控件名字不正确后面会报错
        self.window.set_icon_from_file(image_file)
        self.window.set_title("教师界面")
        self.window.set_border_width(10)
        self.window.set_default_size(500, 300)

        self.teacher_lessons_tree_view = None
        self.activate_row = None
        self._person = person
        self.add_lessons_ui = AddLessonUI(self._person)
        self.change_password_ui = ChangePasswordUI(self._person)
        self.manage_lessons = ManagerLessons(self._person)

        # label init
        welcome_label = self.builder.get_object("welcome_label")
        welcome_label.set_text("欢迎您，{}".format(self._person.name))

        # button init
        change_password_button = self.builder.get_object("change_password_button")
        change_password_button.connect("clicked", self.change_password)

        add_lesson_button = self.builder.get_object("add_lessons_button")
        add_lesson_button.connect("clicked", self.add_lesson)

        exit_button = self.builder.get_object("exit_button")
        exit_button.connect("clicked", Gtk.main_quit)

        cancel_lesson_button = self.builder.get_object("cancel_lesson_button")
        cancel_lesson_button.connect("clicked", self.cancel_lessons)

        confirm_add_lessons_button = self.add_lessons_ui.builder.get_object('confirm_button')
        confirm_add_lessons_button.connect("clicked", self.add_lesson_to_tree_view)

        self.load_tree_view()
        self.window.connect("delete-event", Gtk.main_quit)

    def load_tree_view(self):  # TODO listbox方法
        teach_lessons_scrolled_window = self.builder.get_object("teach_lessons_scrolled_window")
        model = self.create_model()
        self.teacher_lessons_tree_view = Gtk.TreeView()   # TODO 改成self.teacher_lessons_tree_view也不能同步显示
        self.teacher_lessons_tree_view.set_model(model)   # TODO
        self.teacher_lessons_tree_view.connect("row-activated", self.on_activated)  # 双击才能选中目标; 注释，用单击代替
        self.teacher_lessons_tree_view.set_rules_hint(True)

        self.create_columns(self.teacher_lessons_tree_view)
        teach_lessons_scrolled_window.add(self.teacher_lessons_tree_view)

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
        lessons = self.manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
        model = Gtk.ListStore(str, int, int)
        for lesson in lessons:
            model.append([lesson[0], lesson[1], lesson[3]])
        return model

    def on_activated(self, widget, row, col):  # 双击时的方法
        model = widget.get_model()
        self.activate_row = model[row]

    def cancel_lessons(self, widget):
        try:
            lesson_name = self.activate_row[0]
            self.manage_lessons.cancel_lesson(lesson_name, self._person.id_number)
            self.manage_lessons.save_lessons()
            tree_view_model = self.teacher_lessons_tree_view.get_model()
            tree_view_model.remove(self.activate_row.iter)
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("取消成功")
            dialog.run()
            dialog.destroy()
        except ValueError:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("未找到此课程")
            dialog.run()
            dialog.destroy()
        except TypeError:
            pass

    def change_password(self, widget):
        if not self.change_password_ui.window_state:
            self.change_password_ui.window.show_all()
            self.change_password_ui.window_state = True
        else:
            self.change_password_ui.window.hide()
            self.change_password_ui.window_state = False

# TODO
    def add_lesson(self, widget):
        if not self.add_lessons_ui.window_state:
            self.add_lessons_ui.window.show_all()
            self.add_lessons_ui.window_state = True
        else:
            self.add_lessons_ui.window.hide()
            self.add_lessons_ui.window_state = False

    def add_lesson_to_tree_view(self, widget):
        teach_lessons_name = []
        teach_lessons = self.manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
        for teach_lesson in teach_lessons:
            teach_lessons_name.append(teach_lesson[0])

        add_lesson_name = self.add_lessons_ui.add_lesson_name
        limit_number = self.add_lessons_ui.limit_number
        try:
            limit_number = int(limit_number)
        except ValueError:
            pass
        else:
            if add_lesson_name in teach_lessons_name:
                pass
            else:
                teacher_model = self.teacher_lessons_tree_view.get_model()
                _iter = teacher_model.append()
                teacher_model.set_value(_iter, 0, add_lesson_name)
                teacher_model.set_value(_iter, 1, limit_number)
                teacher_model.set_value(_iter, 2, 0)


class StudentUI(Gtk.Window):
    def __init__(self, person):
        student_ui_glade_file = 'ui/user_students.glade'
        self.builder = Gtk.Builder()
        self.builder.add_from_file(student_ui_glade_file)
        self.window = self.builder.get_object("student_main_window")  # 控件名字不正确后面会报错
        self.window.set_icon_from_file(image_file)
        self.window.set_title("学生界面")
        self.window.set_border_width(10)
        self.window.set_default_size(500, 300)

        self.already_lessons_tree_view = None
        self.available_lessons_tree_view = None
        self.activate_row_available = None
        self.activate_row_already = None
        self._person = person
        self.change_password_ui = ChangePasswordUI(self._person)
        self.manage_lessons = ManagerLessons(self._person)

        # label init
        welcome_label = self.builder.get_object("welcome_label")
        welcome_label.set_text("欢迎您，{}".format(self._person.name))

        # button init
        change_password_button = self.builder.get_object("change_password_button")
        change_password_button.connect("clicked", self.change_password)

        confirm_choose_lesson_button = self.builder.get_object("confirm_choose_lessons_button")
        confirm_choose_lesson_button.connect("clicked", self.confirm_choose_lesson)

        cancel_choose_lesson_button = self.builder.get_object("cancel_choose_lesson_button")
        cancel_choose_lesson_button.connect("clicked", self.cancel_choose_lesson)

        exit_button = self.builder.get_object("exit_button")
        exit_button.connect('clicked', Gtk.main_quit)

        self.load_already_tree_view()
        self.load_available_tree_view()
        self.window.connect("delete-event", Gtk.main_quit)

    def load_already_tree_view(self):
        already_choose_scrolled_window = self.builder.get_object("already_choose_scrolled_window")
        model = self.create_model_already()
        self.already_lessons_tree_view = Gtk.TreeView()
        self.already_lessons_tree_view.set_model(model)
        self.already_lessons_tree_view.connect("row-activated", self.on_already_activated)
        self.already_lessons_tree_view.set_rules_hint(True)

        self.create_columns(self.already_lessons_tree_view)
        already_choose_scrolled_window.add(self.already_lessons_tree_view)

    def load_available_tree_view(self):
        available_lessons_msg_scrolled_window = self.builder.get_object("available_lessons_msg_scrolled_window")
        model = self.create_model_available()
        self.available_lessons_tree_view = Gtk.TreeView()
        self.available_lessons_tree_view.set_model(model)
        self.available_lessons_tree_view.connect("row-activated", self.on_available_activated)
        self.available_lessons_tree_view.set_rules_hint(True)

        self.create_columns(self.available_lessons_tree_view)
        available_lessons_msg_scrolled_window.add(self.available_lessons_tree_view)

    @staticmethod
    def create_columns(tree_view):
        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("课程名", renderer_text, text=0)
        column.set_sort_column_id(0)
        tree_view.append_column(column)

        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("任课老师", renderer_text, text=1)
        column.set_sort_column_id(1)
        tree_view.append_column(column)

        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("限制人数", renderer_text, text=2)
        column.set_sort_column_id(2)
        tree_view.append_column(column)

        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("选课人数", renderer_text, text=3)
        column.set_sort_column_id(3)
        tree_view.append_column(column)

    def create_model_available(self):
        lessons = self.manage_lessons.find_available_lessons()
        # for lesson in lessons:
        #     lesson[1] = self.manage_lessons.find_name_by_id(lesson[1])
        model = Gtk.ListStore(str, int, int, int)
        for lesson in lessons:
            model.append([lesson[0], lesson[1], lesson[2], lesson[3]])
        return model

    def create_model_already(self):
        self.manage_lessons = ManagerLessons(self._person)
        lessons = self.manage_lessons.find_choose_lessons_by_student_id(self._person.id_number)
        # for lesson in lessons:
        #     lesson[1] = self.manage_lessons.find_name_by_id(lesson[1])  # TODO 改成显示老师名字
        model = Gtk.ListStore(str, int, int, int)
        for lesson in lessons:
            model.append([lesson[0], lesson[1], lesson[2], lesson[3]])
        return model

    def on_already_activated(self, widget, row, col):
        model = widget.get_model()
        self.activate_row_already = model[row]
        # self._manage_lesson_name = model[row][0]
        # self._manage_lesson_teacher_id = model[row][1]  # TODO

    def on_available_activated(self, widget, row, col):
        model = widget.get_model()
        self.activate_row_available = model[row]

    def cancel_choose_lesson(self, widget):
        try:
            lesson_name = self.activate_row_already[0]
            teacher_id = self.activate_row_already[1]
            self.manage_lessons.check_choose_lesson(lesson_name, teacher_id, self._person.id_number)
        except TypeError:
            pass
        except AttributeError:
            lesson_name = self.activate_row_already[0]
            teacher_id = self.activate_row_already[1]
            lesson = self.manage_lessons.find_lesson_by_lesson_name_and_teacher_id(lesson_name, teacher_id)
            self.manage_lessons.cancel_choose_lesson(lesson_name, teacher_id, self._person.id_number)
            self.manage_lessons.save_lessons()

            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("取消成功")
            dialog.run()
            dialog.destroy()

            already_model = self.already_lessons_tree_view.get_model()
            already_model.remove(self.activate_row_already.iter)

            available_model = self.available_lessons_tree_view.get_model()
            _iter = available_model.append()
            available_model.set_value(_iter, 0, lesson_name)
            available_model.set_value(_iter, 1, teacher_id)
            available_model.set_value(_iter, 2, lesson.limit_number)  # TODO 有时候这样写会报错
            available_model.set_value(_iter, 3, lesson.number_students)
        else:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("您还未选择此课程")
            dialog.run()
            dialog.destroy()

    def confirm_choose_lesson(self, widget):
        try:
            lesson_name = self.activate_row_available[0]
            teacher_id = self.activate_row_available[1]
            self.manage_lessons.check_choose_lesson(lesson_name, teacher_id, self._person.id_number)
        except TypeError:
            pass
        except AttributeError:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("您已经选择了此课程")
            dialog.run()
            dialog.destroy()
        else:
            lesson = self.manage_lessons.find_lesson_by_lesson_name_and_teacher_id(lesson_name, teacher_id)
            self.manage_lessons.choose_lesson(lesson_name, teacher_id, self._person.id_number)
            self.manage_lessons.save_lessons()
            available_model = self.available_lessons_tree_view.get_model()
            available_model.remove(self.activate_row_available.iter)

            already_model = self.already_lessons_tree_view.get_model()
            _iter = already_model.append()
            already_model.set_value(_iter, 0, lesson_name)
            already_model.set_value(_iter, 1, teacher_id)
            already_model.set_value(_iter, 2, lesson.limit_number)  # TODO self.activate_row_available[2]有时候这样写会报错
            already_model.set_value(_iter, 3, lesson.number_students)

            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("选课成功")
            dialog.run()
            dialog.destroy()

    def change_password(self, widget):
        if not self.change_password_ui.window_state:
            self.change_password_ui.window.show_all()
            self.change_password_ui.window_state = True
        else:
            self.change_password_ui.window.hide()
            self.change_password_ui.window_state = False


class ChangePasswordUI(Gtk.Window):
    def __init__(self, person):
        change_password_glade_file = 'ui/change_password.glade'
        self.builder = Gtk.Builder()
        self.builder.add_from_file(change_password_glade_file)
        self.window = self.builder.get_object("change_password_main_window")
        self.window.set_icon_from_file(image_file)
        self.window.set_title("修改密码界面")
        self.window.set_border_width(10)
        self.window.set_default_size(300, 100)

        self.window_state = False
        self._person = person
        self.manage_persons = ManagerPeoples()

        # label init
        welcome_label = self.builder.get_object("welcome_label")
        welcome_label.set_text("欢迎您，{}".format(self._person.name))

        # button init
        change_confirm_button = self.builder.get_object("confirm_button")
        change_confirm_button.connect("clicked", self.change_password_confirm)

        cancel_change_button = self.builder.get_object("cancel_button")
        cancel_change_button.connect("clicked", self.hide)

        # self.window.connect("delete-event", self.hide)  # TODO

    def hide(self, widget, *args):
        self.window.hide()
        self.window_state = False

    # def window_close(self, widget, *args):
    #     self.window.close()

    def change_password_confirm(self, widget):
        #  注：假如将不将builder放进初始化中，通过在该函数中直接复制相关语句，get_text()不能得到相应读数。
        #   可能是这样做使上个函数直接将空字符通过get_text()传入了，即使get_text()在这个函数中
        # entry init
        old_password_entry = self.builder.get_object("old_password_entry")
        old_password = old_password_entry.get_text()

        new_password_entry = self.builder.get_object("new_password_entry")
        new_password = new_password_entry.get_text()

        new_password_confirm_entry = self.builder.get_object("new_password_confirm_entry")
        new_password_confirm = new_password_confirm_entry.get_text()

        if old_password != self._person.password:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("原密码错误")
            dialog.run()
            dialog.destroy()
        elif new_password != new_password_confirm:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("两次输入的新密码不一致")
            dialog.run()
            dialog.destroy()
        else:
            person = self.manage_persons.find_person_by_id(self._person.id_number)  # TODO ??? 返回的实例化人只能在本文件里得到有效保存？
            person.password = new_password
            self.manage_persons.save_peoples()
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("修改成功")
            dialog.run()
            dialog.destroy()


class AddLessonUI(Gtk.Window):
    def __init__(self, person):
        add_lessons_glade_file = 'ui/add_lessons.glade'
        self.builder = Gtk.Builder()
        self.builder.add_from_file(add_lessons_glade_file)
        self.window = self.builder.get_object("add_lesson_main_window")
        self.window.set_icon_from_file(image_file)
        self.window.set_title("添加课程界面")
        self.window.set_border_width(10)
        self.window.set_default_size(300, 100)

        self.window_state = False
        self.add_lesson_name = ''
        self.limit_number = 0
        self._person = person
        self.manage_lessons = ManagerLessons(self._person)

        # label init
        welcome_label = self.builder.get_object("welcome_label")
        welcome_label.set_text("欢迎您，{}".format(self._person.name))

        # button init
        confirm_add_lesson_button = self.builder.get_object('confirm_button')
        confirm_add_lesson_button.connect("clicked", self.add_lesson_confirm)

    def add_lesson_confirm(self, widget):
        # entry init
        add_lesson_name_entry = self.builder.get_object("add_lesson_name_entry")
        self.add_lesson_name = add_lesson_name_entry.get_text()

        limit_number_entry = self.builder.get_object("limit_number_entry")
        self.limit_number = limit_number_entry.get_text()

        try:
            limit_number = int(self.limit_number)
        except ValueError:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
            dialog.format_secondary_text("请输入阿拉伯数字")
            dialog.run()
            dialog.destroy()
        else:
            teach_lessons_name = []
            teach_lessons = self.manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
            for teach_lesson in teach_lessons:
                teach_lessons_name.append(teach_lesson[0])
            if self.add_lesson_name in teach_lessons_name:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("您已经添加了此课程")
                dialog.run()
                dialog.destroy()
            else:
                self.manage_lessons.add_lesson(self.add_lesson_name, self._person.id_number, limit_number)  # 此处将老师名字改成了老师id
                self.manage_lessons.save_lessons()
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
                dialog.format_secondary_text("添加课程成功")
                dialog.run()
                dialog.destroy()
# TODO 添加课程需要保存

# class LoginWindow(Gtk.Window):
#     """它包括多个界面，学生界面和老师界面以及修改密码界面"""
#     def __init__(self, id_number, password):
#         Gtk.Window.__init__(self, title="用户登陆")   # 设置这个title好像也没什么用
#         self._person = None   # 登陆人员
#         self.window = None
#         self.window = None
#         self.window = None
#         self.add_lesson_window = None
#         self.builder = None
#         self.builder = None
#         self.builder = None
#         self.add_lesson_builder = None
#         self._lesson_name = ''
#         self.manage_persons = ManagerPeoples()
#         self.c_window_state = False
#
#         # person = check_in(id, pwd)
#         # init_manage_page(person)
#         #
#         # ui = get_check_ui()
#
#     def teacher_ui(self):   #  注：没传入小控件就不需要widget
#         self.builder = Gtk.Builder()
#         self.builder.add_from_file(teacher_ui_glade_file)
#         self.window = self.builder.get_object("teacher_main_window")  # 控件名字不正确后面会报错
#         self.window.set_icon_from_file(image_file)
#         self.window.set_title("老师界面")
#         self.window.set_border_width(10)
#         self.window.set_default_size(500, 300)
#
#         # label init
#         welcome_label = self.builder.get_object("welcome_label")
#         welcome_label.set_text("欢迎您，{}".format(self._person.name))
#
#         # button init
#         change_password_button = self.builder.get_object("change_password_button")
#         change_password_button.connect("clicked", self.change_password)
#
#         add_lesson_button = self.builder.get_object("add_lessons_button")
#         add_lesson_button.connect("clicked", self.add_lesson)
#
#         exit_button = self.builder.get_object("exit_button")
#         exit_button.connect("clicked", Gtk.main_quit)
#
#         cancel_lesson_button = self.builder.get_object("cancel_lesson_button")
#         cancel_lesson_button.connect("clicked", self.cancel_lessons)
#
#         # TODO listbox方法？
#         # teach_lessons_listbox = self.builder.get_object("teach_lessons_listbox")
#         vbox = Gtk.VBox()  # TODO 还不能同步显示
#         teach_lessons_scrolled_window = self.builder.get_object("teach_lessons_scrolled_window")
#         vbox.pack_start(teach_lessons_scrolled_window, True, True, 0)
#
#         model = self.create_model()
#
#         teach_lessons_tree_view = self.builder.get_object("teach_lessons_tree_view")
#         teach_lessons_tree_view.set_model(model)
#         teach_lessons_tree_view.connect("row-activated", self.on_activated)  # 双击才能选中目标
#         teach_lessons_tree_view.set_rules_hint(True)
#
#         self.create_columns(teach_lessons_tree_view)
#
#         self.window.connect("delete-event", Gtk.main_quit)
#         self.window.show()
#
#     @staticmethod
#     def create_columns(tree_view):
#         renderer_text = Gtk.CellRendererText()
#         column = Gtk.TreeViewColumn("课程名", renderer_text, text=0)
#         column.set_sort_column_id(0)
#         tree_view.append_column(column)
#
#         renderer_text = Gtk.CellRendererText()
#         column = Gtk.TreeViewColumn("限制人数", renderer_text, text=1)
#         column.set_sort_column_id(1)
#         tree_view.append_column(column)
#
#         renderer_text = Gtk.CellRendererText()
#         column = Gtk.TreeViewColumn("选课人数", renderer_text, text=2)
#         column.set_sort_column_id(2)
#         tree_view.append_column(column)
#
#     def create_model(self):
#         self.manage_lessons = ManagerLessons(self._person)
#         lessons = self.manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
#         model = Gtk.Listmodel(str, int, int)
#         for lesson in lessons:
#             model.append([lesson[0], lesson[1], lesson[3]])
#         return model
#
#     def on_activated(self, widget, row, col):
#         model = widget.get_model()
#         self._lesson_name = model[row][0]
#
#     def cancel_lessons(self, widget):
#         self.manage_lessons = ManagerLessons(self._person)
#         try:
#             self.manage_lessons.cancel_lesson(self._lesson_name, self._person.id_number)
#             self.manage_lessons.save_lessons()
#             dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#             dialog.format_secondary_text("取消成功")
#             dialog.run()
#             dialog.destroy()
#         except ValueError:
#             dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#             dialog.format_secondary_text("未找到此课程")
#             dialog.run()
#             dialog.destroy()
#
#     def student_ui(self):
#         self.builder = Gtk.Builder()
#         self.builder.add_from_file(student_ui_glade_file)
#         self.window = self.builder.get_object("student_main_window")  # 控件名字不正确后面会报错
#         self.window.set_icon_from_file(image_file)
#         self.window.set_title("学生界面")
#         self.window.set_border_width(10)
#         self.window.set_default_size(500, 300)
#
#         # label init
#         welcome_label = self.builder.get_object("welcome_label")
#         welcome_label.set_text("欢迎您，{}".format(self._person.name))
#
#         # button init
#         change_password_button = self.builder.get_object("change_password_button")
#         change_password_button.connect("clicked", self.change_password)
#
#         self.window.connect("delete-event", Gtk.main_quit)
#         self.window.show()
#
#     def add_lesson(self, widget):
#         if not self.add_lesson_builder:
#             add_lesson_glade_file = 'ui/add_lessons.glade'
#             self.add_lesson_builder = Gtk.Builder()
#             self.add_lesson_builder.add_from_file(add_lesson_glade_file)
#             self.add_lesson_window = self.add_lesson_builder.get_object("add_lesson_main_window")
#             self.add_lesson_window.set_icon_from_file(image_file)
#             self.add_lesson_window.set_title("添加课程界面")
#             self.add_lesson_window.set_border_width(10)
#             self.add_lesson_window.set_default_size(500, 100)
#
#             # label init
#             welcome_label = self.add_lesson_builder.get_object("welcome_label")
#             welcome_label.set_text("欢迎您，{}".format(self._person.name))
#
#             # button init
#             confirm_add_lesson_button = self.add_lesson_builder.get_object('confirm_button')
#             confirm_add_lesson_button.connect("clicked", self.add_lesson_confirm)
#
#             self.add_lesson_window.show()
#         else:
#             # TODO self.add_lesson_window = self.add_lesson_builder.get_object("add_lesson_main_window") 删除之后再点开却是空的
#             # self.add_lesson_window.show()
#             self.add_lesson_window.reshow_with_initial_size()
#
#     def add_lesson_confirm(self, widget):
#         self.manage_lessons = ManagerLessons(self._person)
#         # entry init
#         add_lesson_name_entry = self.add_lesson_builder.get_object("add_lesson_name_entry")
#         add_lesson_name = add_lesson_name_entry.get_text()
#
#         limit_number_entry = self.add_lesson_builder.get_object("limit_number_entry")
#         try:
#             limit_number = int(limit_number_entry.get_text())
#         except ValueError:
#             dialog = Gtk.MessageDialog(self.add_lesson_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#             dialog.format_secondary_text("请输入阿拉伯数字")
#             dialog.run()
#             dialog.destroy()
#         else:
#             teach_lessons_name = []
#             teach_lessons = self.manage_lessons.find_teach_lessons_by_teacher_id(self._person.id_number)
#             for teach_lesson in teach_lessons:
#                 teach_lessons_name.append(teach_lesson[0])
#             if add_lesson_name in teach_lessons_name:
#                 dialog = Gtk.MessageDialog(self.add_lesson_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#                 dialog.format_secondary_text("您已经添加了此课程")
#                 dialog.run()
#                 dialog.destroy()
#             else:
#                 self.manage_lessons.add_lesson(add_lesson_name, self._person.id_number, limit_number)  # 此处将老师名字改成了老师id
#                 self.manage_lessons.save_lessons()
#                 dialog = Gtk.MessageDialog(self.add_lesson_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#                 dialog.format_secondary_text("添加课程成功")
#                 dialog.run()
#                 dialog.destroy()
#
#     def change_password(self, widget):  # 感觉可以将这个界面单独做成一个类
#         if not self.c_window_state:
#             change_password_glade_file = "ui/change_password.glade"
#             self.builder = Gtk.Builder()
#             self.builder.add_from_file(change_password_glade_file)
#             self.window = self.builder.get_object("change_password_main_window")
#             self.window.set_icon_from_file(image_file)
#             self.window.set_title("修改密码界面")
#             self.window.set_border_width(10)
#             self.window.set_default_size(500, 200)
#
#             # label init
#             welcome_label = self.builder.get_object("welcome_label")
#             welcome_label.set_text("欢迎您，{}".format(self._person.name))
#
#             # button init
#             change_confirm_button = self.builder.get_object("confirm_button")
#             change_confirm_button.connect("clicked", self.change_password_confirm)
#
#             cancel_change_button = self.builder.get_object("cancel_button")
#             cancel_change_button.connect("clicked", self.window_close)
#
#             self.window.connect('delete-event', self.hide)
#
#             self.window.show_all()
#             self.c_window_state = True
#         else:
#             self.window.hide()
#             self.c_window_state = False
#
#     def hide(self, *args):
#         self.window.hide()
#         self.c_window_state = False
#
#     def window_close(self, widget):
#         self.window.close()
#
#     def change_password_confirm(self, widget):
#         #  注：假如将不将builder放进初始化中，通过在该函数中直接复制相关语句，get_text()不能得到相应读数。
#         #   可能是这样做使上个函数直接将空字符通过get_text()传入了，即使get_text()在这个函数中
#         # entry init
#         old_password_entry = self.builder.get_object("old_password_entry")
#         old_password = old_password_entry.get_text()
#
#         new_password_entry = self.builder.get_object("new_password_entry")
#         new_password = new_password_entry.get_text()
#
#         new_password_confirm_entry = self.builder.get_object("new_password_confirm_entry")
#         new_password_confirm = new_password_confirm_entry.get_text()
#
#         if old_password != self._person.password:
#             dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#             dialog.format_secondary_text("原密码错误")
#             dialog.run()
#             dialog.destroy()
#         elif new_password != new_password_confirm:
#             dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#             dialog.format_secondary_text("两次输入的新密码不一致")
#             dialog.run()
#             dialog.destroy()
#         else:
#             self._person.password = new_password
#             self.manage_persons.save_peoples()
#             dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "提示")
#             dialog.format_secondary_text("修改成功")
#             dialog.run()
#             dialog.destroy()
# TODO 刷新函数、做成不同的类、hide
