from kivy.config import Config
Config.set('graphics', 'maxfps', '60')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
import kivy, os, stat, re, sys, shutil, time
from pathlib import Path
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineIconListItem, OneLineIconListItem
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
if kivy.platform == "android":
    from kivymd.utils.set_bars_colors import set_bars_colors
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path


kivy_str = """
#:import images_path kivymd.images_path
#:import path os.path

<ListLabel>:

    IconLeftWidget:
        icon: root.icon
        on_release: app.screen.update_with_timer(root.path) if path.isdir(root.path) else None
        ripple_scale: 0
        md_bg_color: app.theme_cls.bg_normal

<FilesScreen>:

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: "arrow-up"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release: root.move_up(self)
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal

            MDIconButton:
                icon: "home"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release: root.update_files(root.home_path)
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal

            MDIconButton:
                icon: "dots-vertical"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release: root.controls_menu(self)
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal

            MDTextField:
                id: text_input
                text: root.last_path
                on_text_validate: root.update_files(self.text)

        RecycleView:
            id: rv
            key_viewclass: "viewclass"
            key_size: "height"
            size_hint: 1.0,1.0
            bar_width: dp(10)
            scroll_type: ["bars", "content"]
            effect_cls: "ScrollEffect"
            on_scroll_move: root.scroll_timer(True)

            RecycleBoxLayout:
                default_size: None, dp(60)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"
"""


class ListLabel(TwoLineIconListItem):
    icon = StringProperty()
    divider = None
    ripple_scale = 0

    def on_release(self):
        if app.screen.timer() and app.screen.scroll_timer():
            app.screen.controls_menu(item=self)
        return super().on_release()


class MenuItem(OneLineIconListItem):
    def __init__(self, icon=None, item=None, **kwargs):
        super().__init__(**kwargs)
        self.divider = None
        self.item = item

    def on_release(self):
        if app.screen.timer():
            try:
                if self.text == "Hidden":
                    if app.screen.hidden == False:
                        app.screen.hidden = True
                    elif app.screen.hidden == True:
                        app.screen.hidden = False
                    app.screen.update_files(app.screen.last_path)

                elif self.text == "Paste":
                    app.screen.paste()
                    app.screen.update_files(app.screen.last_path)

                elif self.text == "Copy":
                    app.screen.non_win_clipboard = f"'{self.item.path}'"

                elif self.text == "Delete":
                    path = self.item.path
                    popup = MDDialog(
                        text=f"Delete '{self.item.text}' ?", buttons=[
                            MDFlatButton(text="NO", text_color=self.theme_cls.primary_color,
                                on_press=lambda button: popup.dismiss(force=True)),
                            MDFlatButton(text="YES", text_color=self.theme_cls.primary_color,
                                on_press=lambda button: app.screen.delete(popup, path)),
                        ],)
                    popup.open()
                    app.screen.update_files(app.screen.last_path)

                elif self.text == "Rename":
                    r_path = self.item.path
                    e_path = r_path.rsplit(app.screen.slash, 1)
                    if os.path.exists(r_path):
                        popup = MDDialog()
                        text_input = MDTextField(text=e_path[1], pos_hint={"center_y": .5},
                            on_text_validate=lambda value: app.screen.rename(value.text, r_path, e_path[1], e_path[0], popup))
                        popup.add_widget(text_input)
                        popup.open()
                        app.screen.update_files(app.screen.last_path)

                elif self.text == "New file" or self.text == "New catalog":
                    if self.text == "New catalog":
                        goal = "dir"
                        info_text = "Enter catalog name"
                    elif self.text == "New file":
                        goal = "file"
                        info_text = "Enter file name"
                    popup = MDDialog()
                    text_input = MDTextField(hint_text=info_text, on_text_validate=lambda value: app.screen.new(value.text, popup, goal))
                    popup.add_widget(text_input)
                    popup.open()
                    app.screen.update_files(app.screen.last_path)

                elif self.text == "Name sort":
                    app.screen.sort = "name"
                    app.screen.update_files(app.screen.last_path)

                elif self.text == "Size sort":
                    app.screen.sort = "size"
                    app.screen.update_files(app.screen.last_path)

                elif self.text == "Open":##########
                    path = self.item.path
                    if os.path.isdir(path):
                        app.screen.update_files(path)

                elif self.text == "Size":##########
                    path = self.item.path
                    if os.path.isdir(path):
                        size = app.screen.convert_size(app.screen.check_dir_size(path))[0]
                    else:
                        size = app.screen.convert_size(path)[0]
                    popup = MDDialog()
                    popup.add_widget(MDLabel(text=size, halign="center"))
                    popup.open()

                app.screen.right_menu.dismiss(force=True)

            except Exception as e:
                MDDialog(text=f"Menu - {e}").open()
        return super().on_release()


class ArrowButton(MDRectangleFlatIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = 'Custom'
        self.text_color = 1, 0, 0, 1
        self.line_color = 1, 0, 0, 1
        self.icon_color = 1, 0, 0, 1
        if app.screen.reverse == True:
            self.icon = "arrow-down"
        elif app.screen.reverse == False:
            self.icon = "arrow-up"
        self.pos_hint = {"center_x": .5, "center_y": .5}
        if app.screen.sort == "name":
            self.text = "Name"
        elif app.screen.sort == "size":
            self.text = "Size"

    def on_release(self):
        if app.screen.timer():
            if app.screen.reverse == True:
                self.icon = "arrow-up"
                app.screen.reverse = False
            elif app.screen.reverse == False:
                self.icon = "arrow-down"
                app.screen.reverse = True
            if app.screen.sort == "name":
                self.text = "Name"
            elif app.screen.sort == "size":
                self.text = "Size"
            app.screen.update_files(app.screen.last_path)
        return super().on_release()


class FilesScreen(Screen):
    if kivy.platform == "android":
        home_path = primary_external_storage_path()
    else:
        home_path = str(Path.home())
    hidden = False
    reverse = False
    sort = "name"
    last_path = home_path
    non_win_clipboard = None
    slash = "\\" if sys.platform == "win32" else "/"
    button_pressed_time = None
    scroll_end_time = None

    # Operations methods

    def update_files(self, dirname):
        def add_item(text, secondary_text, path, icon):
            self.ids.rv.data.append({
                "viewclass": "ListLabel",
                "icon": icon,
                "text": text,
                "secondary_text": secondary_text,
                "path": path,})

        try:
            # Check path
            if re.match(r".+\\$", dirname) or re.match(r".+/$", dirname):
                dirname = dirname[0:-1]
            if re.match(r"\w:$", dirname) or dirname == "":
                dirname = dirname + self.slash
            # Scan
            if kivy.platform == "android":
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            files = os.scandir(dirname)
            files_list, dirs_list = [], []
            for f in files:
                f_stat = f.stat()
                size = self.convert_size(f_stat.st_size)
                if f.is_dir():
                    if self.hidden == False:
                        if sys.platform == "win32":
                            if not f.is_symlink() and not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append([f.name, "dir", f.path, "folder"])
                        else:
                            if not f.name.startswith("."):
                                dirs_list.append([f.name, "dir", f.path, "folder"])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append([f.name, "dir", f.path, "folder-outline"])
                            else:
                                if f.is_symlink():
                                    dirs_list.append([f.name, "dir", f.path, "folder-outline"])
                                else:
                                    dirs_list.append([f.name, "dir", f.path, "folder"])
                        else:
                            if f.name.startswith("."):
                                dirs_list.append([f.name, "dir", f.path, "folder-outline"])
                            else:
                                dirs_list.append([f.name, "dir", f.path, "folder"])
                if f.is_file():
                    if self.hidden == False:
                        if sys.platform == "win32":
                            if not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append([f.name, size[0], f.path, "file", size[1]])
                        else:
                            if not f.name.startswith("."):
                                files_list.append([f.name, size[0], f.path, "file", size[1]])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append([f.name, size[0], f.path, "file-alert-outline", size[1]])
                            else:
                                files_list.append([f.name, size[0], f.path, "file", size[1]])
                        else:
                            if f.name.startswith("."):
                                files_list.append([f.name, size[0], f.path, "file-alert-outline", size[1]])
                            else:
                                files_list.append([f.name, size[0], f.path, "file", size[1]])
            # Sorting
            if self.sort == "size":
                if self.reverse == False:
                    dirs_list.sort(key=lambda s: s[0])
                    files_list.sort(key=lambda s: s[4])
                if self.reverse == True:
                    dirs_list.sort(key=lambda s: s[0], reverse=True)
                    files_list.sort(key=lambda s: s[4], reverse=True)
            else:
                if self.reverse == False:
                    dirs_list.sort(key=lambda f: f[0])
                    files_list.sort(key=lambda f: f[0])
                elif self.reverse == True:
                    dirs_list.sort(key=lambda f: f[0], reverse=True)
                    files_list.sort(key=lambda f: f[0], reverse=True)
            # Clear old & Add new
            self.ids.rv.data = []
            for i in dirs_list:
                add_item(text=i[0], secondary_text=f"{i[1]}", path=i[2], icon=i[3])
            for i in files_list:
                add_item(text=i[0], secondary_text=f"{i[1]}", path=i[2], icon=i[3])
            self.last_path = dirname
            self.ids.text_input.text = dirname
            self.ids.rv.scroll_y = 1# return scroll to up

        except Exception as e:
            MDDialog(text=f"Update - {e}").open()

    def delete(self, popup, p):
        def delete_dir(d_path):
            for f in os.listdir(d_path):
                f1 = os.path.join(d_path, f)
                if not os.path.isdir(f1):
                    os.remove(f1)
                else:
                    delete_dir(f1)
            try:os.rmdir(d_path)
            except:pass

        if self.timer():
            try:
                if os.path.exists(p):
                    if os.path.isdir(p):
                        delete_dir(p)
                    else:
                        os.remove(p)
                popup.dismiss(force=True)
                self.update_files(self.last_path)
            except Exception as e:
                MDDialog(text=f"Delete - {e}").open()

    def paste(self):
        if self.timer():
            try:
                clipboard = self.non_win_clipboard.replace("'", "").split(",")
                for source in clipboard:
                    edit = source.rsplit(self.slash, 1)
                    # Search file/folder copies
                    file_copies = 1
                    for f in os.listdir(self.last_path):
                        if f.lower() == edit[1].lower():
                            file_copies += 1
                    if file_copies > 1:
                        while True:
                            for f in os.listdir(self.last_path):
                                if f.lower() == f"({file_copies}){edit[1]}".lower():
                                    file_copies += 1
                                    continue
                            break
                        destination = self.last_path + self.slash + f"({file_copies})" + edit[1]
                    else:
                        destination = self.last_path + self.slash + edit[1]
                    if os.path.isdir(source):
                        shutil.copytree(source, destination)
                    else:
                        shutil.copy2(source, destination)
                self.update_files(self.last_path)
            except Exception as e:
                MDDialog(text=f"Paste - {e}").open()

    def rename(self, new_name, r_path, old_name, old_path, popup):
        if self.timer():
            try:
                if new_name is not None:
                    test = True
                    for f in os.listdir(self.last_path):
                        if f.lower() == new_name.lower() and new_name.lower() != old_name.lower():
                            test = False
                    if test == True and r_path.lower() != old_name.lower():
                        n_path = old_path + self.slash + new_name
                        os.rename(r_path, n_path)
                        popup.dismiss(force=True)
                        self.update_files(self.last_path)
            except Exception as e:
                MDDialog(text=f"Rename - {e}").open()

    def new(self, name, popup, goal):
        if self.timer():
            try:
                test = True
                for f in os.listdir(self.last_path):
                    if f.lower() == name.lower():
                        test = False
                if test == True:
                    path = os.path.join(self.last_path, name)
                    if goal == "dir":
                        os.mkdir(path)
                    elif goal == "file":
                        Path(path).touch()
                    popup.dismiss(force=True)
                    self.update_files(self.last_path)
            except Exception as e:
                MDDialog(text=f"New - {e}").open()

    # Interface methods

    def controls_menu(self, button=None, item=None):
        if item:
            self.right_menu = MDDialog(type="simple", items=[
                MenuItem(text="Open", item=item) if os.path.isdir(item.path) else None,
                MenuItem(text="Copy", item=item),
                MenuItem(text="Delete", item=item),
                MenuItem(text="Rename", item=item),
                MenuItem(text="Size", item=item),
            ],)
        elif button:
            self.right_menu = MDDialog(type="simple", items=[
                MenuItem(text="Hidden"),
                MenuItem(text="New catalog"),
                MenuItem(text="New file"),
                MenuItem(text='Name sort'),
                MenuItem(text='Size sort'),
                MenuItem(text="Paste") if self.non_win_clipboard != None else None,
            ], buttons=[
                ArrowButton(size_hint_x=None, width=100),
            ])
        self.right_menu.open()

    def move_up(self, button):
        if self.timer():
            up_path = self.last_path.rsplit(self.slash, 1)
            self.update_files(up_path[0])

    def scroll_timer(self, var=None):
        if var == True:
            self.scroll_end_time = time.time()
        elif var == None:
            if self.scroll_end_time == None or time.time() - self.scroll_end_time > 1.0:
                return True
            else:
                return False

    def timer(self):
        if self.button_pressed_time == None or time.time() - self.button_pressed_time > 0.5:
            self.button_pressed_time = time.time()
            return True
        else:
            return False

    # Helping methods

    def update_with_timer(self, dirname):
        if self.timer():
            self.update_files(dirname)

    def check_dir_size(self, path) -> int:
        size = 0
        try:
            for f in os.listdir(path):
                f1 = os.path.join(path, f)
                if os.path.isdir(f1):
                    size += self.check_dir_size(f1)
                else:
                    size += self.convert_size(f1)[1]
        except:pass
        return size

    def convert_size(self, var):
        if type(var) == type(1):
            s = var
        else:
            s = os.stat(var).st_size
        if s < 1000:
            size = str(s) + " B"
        if s >= 1000:
            size = str(round(s/1000, 2)) + " KB"
        if s >= 1000000:
            size = str(round(s/1000000, 2)) + " MB"
        if s >= 1000000000:
            size = str(round(s/1000000000, 2)) + " GB"
        if s >= 1000000000000:
            size = str(round(s/1000000000000, 2)) + " TB"
        return [size, s]


class FilesApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(kivy_str)
        self.screen = FilesScreen()

    def build(self):
        if kivy.platform == "android":
            self.set_bars_colors_s()
        else:
            self.icon = "data/icon.png"
        return self.screen

    def set_bars_colors_s(self):
            set_bars_colors(app.theme_cls.bg_normal, app.theme_cls.bg_normal, "Dark")

    def on_start(self):
        self.screen.update_files(self.screen.home_path)

app = FilesApp()
app.run()