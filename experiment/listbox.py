# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk
#
# class ListBox(Gtk.Window):
#     def __init__(self):
#         Gtk.Window.__init__(self)
#         self.set_default_size(200, -1)
#         self.connect("destroy", Gtk.main_quit)
#
#         listbox = Gtk.ListBox()
#
#         self.add(listbox)
#
#         for count in range(0, 9):
#             label = Gtk.Label("Row %i" % (count))
#             listbox.add(label)
#
#         listbox.connect("row-activated", self.on_row_activated)
#
#     def on_row_activated(self, listbox, listboxrow):
#         print("Row %i activated" % (listboxrow.get_index()))
#
# window = ListBox()
# window.show_all()
# Gtk.main()


# import gi
#
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk
#
# # list of tuples for each software, containing the software name, initial release, and main programming languages used
# software_list = [
#     ("Firefox", 2002, "C++"),
#     ("Eclipse", 2004, "Java"),
#     ("Pitivi", 2004, "Python"),
#     ("Netbeans", 1996, "Java"),
#     ("Chrome", 2008, "C++"),
#     ("Filezilla", 2001, "C++"),
#     ("Bazaar", 2005, "Python"),
#     ("Git", 2005, "C"),
#     ("Linux Kernel", 1991, "C"),
#     ("GCC", 1987, "C"),
#     ("Frostwire", 2004, "Java"),
# ]
#
#
# class TreeViewFilterWindow(Gtk.Window):
#     def __init__(self):
#         Gtk.Window.__init__(self, title="Treeview Filter Demo")
#         self.set_border_width(10)
#
#         # Setting up the self.grid in which the elements are to be positionned
#         self.grid = Gtk.Grid()
#         self.grid.set_column_homogeneous(True)
#         self.grid.set_row_homogeneous(True)
#         self.add(self.grid)
#
#         # Creating the ListStore model
#         self.software_liststore = Gtk.ListStore(str, int, str)
#         for software_ref in software_list:
#             self.software_liststore.append(list(software_ref))
#         self.current_filter_language = None
#
#         # Creating the filter, feeding it with the liststore model
#         self.language_filter = self.software_liststore.filter_new()
#         # setting the filter function, note that we're not using the
#         self.language_filter.set_visible_func(self.language_filter_func)
#
#         # creating the treeview, making it use the filter as a model, and adding the columns
#         self.treeview = Gtk.TreeView(model=self.language_filter)
#         for i, column_title in enumerate(
#             ["Software", "Release Year", "Programming Language"]
#         ):
#             renderer = Gtk.CellRendererText()
#             column = Gtk.TreeViewColumn(column_title, renderer, text=i)
#             self.treeview.append_column(column)
#
#         # creating buttons to filter by programming language, and setting up their events
#         self.buttons = list()
#         for prog_language in ["Java", "C", "C++", "Python", "None"]:
#             button = Gtk.Button(label=prog_language)
#             self.buttons.append(button)
#             button.connect("clicked", self.on_selection_button_clicked)
#
#         # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
#         self.scrollable_treelist = Gtk.ScrolledWindow()
#         self.scrollable_treelist.set_vexpand(True)
#         self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
#         self.grid.attach_next_to(
#             self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1
#         )
#         for i, button in enumerate(self.buttons[1:]):
#             self.grid.attach_next_to(
#                 button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1
#             )
#         self.scrollable_treelist.add(self.treeview)
#
#         self.show_all()
#
#     def language_filter_func(self, model, iter, data):
#         """Tests if the language in the row is the one in the filter"""
#         if (
#                 self.current_filter_language is None
#                 or self.current_filter_language == "None"
#         ):
#             return True
#         else:
#             return model[iter][2] == self.current_filter_language
#
#     def on_selection_button_clicked(self, widget):
#         """Called on any of the button clicks"""
#         # we set the current language filter to the button's label
#         self.current_filter_language = widget.get_label()
#         print("%s language selected!" % self.current_filter_language)
#         # we update the filter, which updates in turn the view
#         self.language_filter.refilter()
#
#
# win = TreeViewFilterWindow()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))


class ListBoxWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ListBox Demo")
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        label1 = Gtk.Label(label="Automatic Date & Time", xalign=0)
        label2 = Gtk.Label(label="Requires internet access", xalign=0)
        vbox.pack_start(label1, True, True, 0)
        vbox.pack_start(label2, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        hbox.pack_start(switch, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Enable Automatic Update", xalign=0)
        check = Gtk.CheckButton()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(check, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Date Format", xalign=0)
        combo = Gtk.ComboBoxText()
        combo.insert(0, "0", "24-hour")
        combo.insert(1, "1", "AM/PM")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)

        listbox_2 = Gtk.ListBox()
        items = 'This is a sorted ListBox Fail'.split()

        for item in items:
            listbox_2.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == 'Fail' else True

        listbox_2.set_sort_func(sort_func, None, False)
        listbox_2.set_filter_func(filter_func, None, False)

        listbox_2.connect('row-activated', lambda widget, row: print(row.data))

        box_outer.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all()


def main():
    win = ListBoxWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()