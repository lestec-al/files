import os, stat, re, sys, platform, subprocess, string, shutil, configparser, tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.messagebox import askyesno
from tkinter import filedialog
from pathlib import Path
from ftplib import FTP
from send2trash import send2trash

# Interface

def sort_name_reverse():
    global sort
    global reverse
    sort = "name"
    if reverse == False:
        reverse = True
        tree.heading("#0", text="   Name ↓")
    elif reverse == True:
        reverse = False
        tree.heading("#0", text="   Name ↑")
    tree.heading("#1", text="Size")
    update_files(entry.get())


def sort_size_reverse():
    global sort
    global reverse
    sort = "size"
    if reverse == False:
        reverse = True
        tree.heading("#1", text="Size ↓")
    elif reverse == True:
        reverse = False
        tree.heading("#1", text="Size ↑")
    tree.heading("#0", text="   Name")
    update_files(entry.get())


def move_up():
    global last_lower_folder
    up_path = entry.get().rsplit("/" if ftp != None else slash, 1)
    last_lower_folder = up_path[1]
    update_files(up_path[0])


def show_hide():
    global hidden
    if hidden_menu.get() == 1:
        hidden = True
    elif hidden_menu.get() == 0:
        hidden = False
    update_files(entry.get())


def open_right_menu(event):
    try:
        right_menu.tk_popup(event.x_root, event.y_root)
    finally:
        right_menu.grab_release()


def scan_disks_add_buttons():
    if sys.platform == "win32":
        letters = string.ascii_uppercase
        letter_c = 0
        column = 2
        for _ in range(26):
            disk = letters[letter_c]
            if os.path.exists(f"{disk}:{slash}"):
                tk.Button(frame_b, text=disk.lower(), font=("Arial", 14), relief="flat", bg="white", fg="black",
                    command=lambda disk=disk:update_files(f"{disk}:{slash}")).grid(column=column, row=1)
                column += 1
            letter_c += 1
    if sys.platform == "linux":
        column = 2
        os_user = home_path.rsplit(slash, 1)[1]
        if os.path.exists(f"/media/{os_user}/"):
            for l_disk in os.listdir(f"/media/{os_user}/"):
                tk.Button(frame_b, text=l_disk[0].lower(), font=("Arial", 14), relief="flat", bg="white", fg="black",
                    command=lambda l_disk=l_disk:update_files(f"/media/{os_user}/{l_disk}")).grid(column=column, row=1)
                column += 1


def up_down_focus():
    """Focus item on start"""
    if tree.focus() == "":
        try:
            item = tree.get_children()[0]
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
        except:pass


def select():
    """Enable some menu items"""
    if len(tree.selection()) > 0:
        right_menu.entryconfig("Open", state="normal")
        if ftp == None:
            right_menu.entryconfig("Copy", state="normal")
            right_menu.entryconfig("Rename", state="normal")
            right_menu.entryconfig("Delete in trash", state="normal")
        if ftp != None:
            right_menu.entryconfig("Copy to folder", state="normal")


def remove_selection(menu_only=False):
    """Remove selection + Disable some menu items"""
    if menu_only == False:
        tree.selection_remove(tree.focus())
    right_menu.entryconfig("Open", state="disabled")
    right_menu.entryconfig("Copy", state="disabled")
    right_menu.entryconfig("Rename", state="disabled")
    right_menu.entryconfig("Delete in trash", state="disabled")
    if ftp != None:
        right_menu.entryconfig("Copy to folder", state="disabled")


def click():
    stop = False
    for i in tree.selection():
        path = tree.item(i)["values"][1]
        if tree.item(i)["values"][0] == "dir":
            if stop == False:
                update_files(path)
                stop = True
        else:
            if ftp == None:
                if sys.platform == "win32":
                    os.startfile(path)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, path])

# Operations

def new(goal: str):
    try:
        test = False
        cancel = False
        if goal == "dir":
            info_text = "Enter catalog name"
        elif goal == "file":
            info_text = "Enter file name"
        while test == False and cancel == False:
            name_dir = simpledialog.askstring(title="Files", prompt=info_text, parent=tree_frame)
            if name_dir is not None:
                test = True
                for f in os.listdir(last_path):
                    if f.lower() == name_dir.lower():
                        test = False
                        info_text = "Name is taken"
            else:
                cancel = True
        if test == True:
            path = os.path.join(last_path, name_dir)
            if goal == "dir":
                os.mkdir(path)
            elif goal == "file":
                Path(path).touch()
            update_files(last_path)

    except Exception as e:
        tk.messagebox.showerror(title="Error", message=str(e))


def copy():
    list_i = []
    for i in tree.selection():
        path = tree.item(i)["values"][1]
        if "\\" in path:
            path = path.replace("\\", "/")
        list_i.append(f"'{path}'")

    if len(list_i) > 1:
        items = ",".join(list_i)
    else:
        items = list_i[0]

    if sys.platform == "win32":
        os.system(f"powershell.exe Set-Clipboard -path {items}")
        right_menu.entryconfig("Paste", state="normal")
    else:
        global non_win_clipboard
        non_win_clipboard = items
        right_menu.entryconfig("Paste", state="normal")


def paste():
    if sys.platform == "win32":
        clipboard = window.selection_get(selection="CLIPBOARD").replace("/", slash).split("\n")
    else:
        clipboard = non_win_clipboard.replace("'", "").split(",")

    for source in clipboard:
        edit = source.rsplit(slash, 1)
        # Search copies, create destination path
        file_copies = 1
        for f in os.listdir(entry.get()):
            if f.lower() == edit[1].lower():
                file_copies += 1
        if file_copies > 1:
            while True:
                for f in os.listdir(entry.get()):
                    if f.lower() == f"({file_copies}){edit[1]}".lower():
                        file_copies += 1
                        continue
                break
            destination = entry.get() + slash + f"({file_copies})" + edit[1]
        else:
            destination = entry.get() + slash + edit[1]
        # Paste
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    update_files(entry.get())


def delete():
    try:
        del_list = []
        for i in tree.selection():
            del_path = tree.item(i)["values"][1]
            if os.path.exists(del_path):
                del_list.append(del_path)
        answer = askyesno(title="Files", message=f"Delete {len(tree.selection())} objects in trash?")
        if answer:
            for di in del_list:
                send2trash(di)
    except:pass
    update_files(entry.get())


def rename():
    for i in tree.selection():
        r_path = tree.item(i)["values"][1]
        e_path = r_path.rsplit(slash, 1)
        if os.path.exists(r_path):
            info_text = f"Rename '{e_path[1]}'"
            test = False
            while test == False:
                test = True
                new_name = simpledialog.askstring(title="Files", prompt=info_text, parent=tree_frame, initialvalue=e_path[1])
                if new_name is not None:
                    for f in os.listdir(entry.get()):
                        if f.lower() == new_name.lower() and new_name.lower() != e_path[1].lower():
                            test = False
                            info_text = "Name is taken"
            if new_name is not None and new_name.lower() != e_path[1].lower():
                n_path = e_path[0] + slash + new_name
                os.rename(r_path, n_path)
    update_files(entry.get())


def update_files(orig_dirname: str):
    def convert_size(var) -> tuple:
        if type(var) == type(1):
            byte_size = var
        else:
            byte_size = os.stat(var).st_size
        #
        if byte_size >= 1000000000000:
            size = str(round(byte_size/1000000000000, 2)) + " TB"
        elif byte_size >= 1000000000:
            size = str(round(byte_size/1000000000, 2)) + " GB"
        elif byte_size >= 1000000:
            size = str(round(byte_size/1000000, 2)) + " MB"
        elif byte_size >= 1000:
            size = str(round(byte_size/1000, 2)) + " KB"
        elif byte_size < 1000:
            size = str(byte_size) + " B"
        return size, byte_size

    try:
        global last_path
        global ftp
        global url_ftp
        dirname = orig_dirname
        # FTP
        if "ftp://" in dirname:
            x = dirname.split("//", 1)
            if "/" in x[1]:
                dirname = "/" + x[1].split("/", 1)[1]
            else:
                dirname = "/"
            #
            if ftp == None:
                ftp = FTP("")
                try:
                    if ":" in x[1]:
                        ftp_split = x[1].split(":", 1)
                        ftp.connect(ftp_split[0],int(ftp_split[1]))
                        url_ftp = f"ftp://{ftp_split[0]}:{ftp_split[1]}"
                    else:
                        ftp.connect(x[1])
                        url_ftp = f"ftp://{x[1]}"
                    ftp.login()
                    #
                    right_menu.add_command(label="Copy to folder", command=copy_from_ftp, state="disable")
                    right_menu.entryconfig("Show hidden files", state="disable")
                    right_menu.entryconfig("New file", state="disable")
                    right_menu.entryconfig("New catalog", state="disable")
                except:
                    ftp = None
                    url_ftp = None
        else:
            if ftp != None:
                ftp.quit()
                ftp = None
                url_ftp = None
                #
                right_menu.delete("Copy to folder")
                right_menu.entryconfig("Show hidden files", state="normal")
                right_menu.entryconfig("New file", state="normal")
                right_menu.entryconfig("New catalog", state="normal")
        # Check path
        if ftp == None and op_slash in dirname:
            dirname = dirname.replace(op_slash, slash)
        elif ftp != None and "\\" in dirname:
            dirname = dirname.replace("\\", "/")
        if re.match(r".+\\$", dirname) or re.match(r".+/$", dirname):
            dirname = dirname[0:-1]
        if re.match(r"\w:$", dirname) or dirname == "":
            if ftp == None:
                dirname = dirname + slash
            else:
                dirname = "/"
        # Scan
        files_list, dirs_list = [], []
        if ftp == None:
            files = os.scandir(dirname)
            for f in files:
                f_stat = f.stat()
                size = convert_size(f_stat.st_size)
                if f.is_dir():
                    if hidden == False:
                        if sys.platform == "win32":
                            if not f.is_symlink() and not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append([f.name, "dir", f.path, folder_icon])
                        else:
                            if not f.name.startswith("."):
                                dirs_list.append([f.name, "dir", f.path, folder_icon])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append([f.name, "dir", f.path, folder_hidden_icon])
                            else:
                                if f.is_symlink():
                                    dirs_list.append([f.name, "dir", f.path, folder_hidden_icon])
                                else:
                                    dirs_list.append([f.name, "dir", f.path, folder_icon])
                        else:
                            if f.name.startswith("."):
                                dirs_list.append([f.name, "dir", f.path, folder_hidden_icon])
                            else:
                                dirs_list.append([f.name, "dir", f.path, folder_icon])
                if f.is_file():
                    if hidden == False:
                        if sys.platform == "win32":
                            if not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append([f.name, size[0], f.path, file_icon, size[1]])
                        else:
                            if not f.name.startswith("."):
                                files_list.append([f.name, size[0], f.path, file_icon, size[1]])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append([f.name, size[0], f.path, file_hidden_icon, size[1]])
                            else:
                                files_list.append([f.name, size[0], f.path, file_icon, size[1]])
                        else:
                            if f.name.startswith("."):
                                files_list.append([f.name, size[0], f.path, file_hidden_icon, size[1]])
                            else:
                                files_list.append([f.name, size[0], f.path, file_icon, size[1]])
        # FTP
        else:
            ftp.cwd(dirname)
            try:
                for f in ftp.mlsd():
                    if f[1]["type"] == "dir":
                        dirs_list.append([f[0], "dir", f"{orig_dirname}/{f[0]}", folder_icon])
                    elif f[1]["type"] == "file":
                        size = convert_size(int(f[1]["size"]))
                        files_list.append([f[0], size[0], f"{orig_dirname}/{f[0]}", file_icon, size[1]])
            except:
                ftp.voidcmd('TYPE I')
                for f in ftp.nlst():
                    try:
                        if "." in f and not f.startswith("."):
                            size = convert_size(ftp.size(f))
                            files_list.append([f, size[0], f"{orig_dirname}/{f}", file_icon, size[1]])    
                        else:
                            dirs_list.append([f, "dir", f"{orig_dirname}/{f}", folder_icon])
                    except:
                        dirs_list.append([f, "dir", f"{orig_dirname}/{f}", folder_icon])
        # Sorting
        if sort == "size":
            if reverse == False:
                dirs_list.sort(key=lambda s: s[0])
                files_list.sort(key=lambda s: s[4])
            if reverse == True:
                dirs_list.sort(key=lambda s: s[0], reverse=True)
                files_list.sort(key=lambda s: s[4], reverse=True)
        elif sort == "name":
            if reverse == False:
                dirs_list.sort(key=lambda f: f[0])
                files_list.sort(key=lambda f: f[0])
            elif reverse == True:
                dirs_list.sort(key=lambda f: f[0], reverse=True)
                files_list.sort(key=lambda f: f[0], reverse=True)
        # Clean old data
        for item in tree.get_children():
            tree.delete(item)
        entry.delete(0, "end")
        # Add new data
        count = 0
        for i in dirs_list:
            tree.insert("", tk.END, text=i[0], values=[f"{i[1]}", i[2]], open=False, image=i[3])
            count += 1
        for i in files_list:
            tree.insert("", tk.END, text=i[0], values=[f"{i[1]}", i[2]], open=False, image=i[3])
            count += 1
        #
        if ftp == None:
            last_path = dirname
            entry.insert("end", dirname)
        else:
            last_path = ftp.pwd()
            entry.insert("end", f"{url_ftp}{ftp.pwd()}")
        #
        label["text"]=f"   {str(count)} objects"
        # Set title = folder name
        if ftp == None:
            if re.match(r"\w:\\$", dirname):
                window.title(f"Disk ({dirname[0:2]})")
            elif dirname == slash:
                window.title("Files")
            else:
                window.title(dirname.rsplit(slash, 1)[1])
        else:
            window.title(url_ftp)
        #
        remove_selection(menu_only=True)
        # If clipboard on windows has a path - change button
        if sys.platform == "win32" and ftp == None:
            try:
                if re.match(r"\w:", window.selection_get(selection="CLIPBOARD")):
                    right_menu.entryconfig("Paste", state="normal")
                else:
                    right_menu.entryconfig("Paste", state="disabled")
            except:
                right_menu.entryconfig("Paste", state="disabled")
        # Focus on the folder from which you returned
        if tree.focus() == "" and last_lower_folder != None:
            for item in tree.get_children():
                if tree.item(item)["text"] == last_lower_folder:
                    tree.selection_set(item)
                    tree.focus(item)
                    tree.see(item)
                    break

    except Exception as e:
        tk.messagebox.showerror(title="Error", message=str(e))


def copy_from_ftp():
    path = filedialog.askdirectory()
    print(path)
    for i in tree.selection():
        text = tree.item(i)["text"]
        with open(f"{path}/{text}", "wb") as file:
            ftp.retrbinary(f"RETR {text}", file.write)
            file.close()


# Fix graphic on Win 10
if sys.platform == "win32"and platform.release() == "10":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# Ini config home path, showing hidden files + other variables
config = configparser.ConfigParser()
config.read("files.ini")
home_path = str(Path.home()) if config["USER SETTINGS"]["home_path"] == "" else config["USER SETTINGS"]["home_path"]
hidden = True if config["USER SETTINGS"]["show_hidden_files"] == "True" else False
sort = "size" if config["USER SETTINGS"]["sort"] == "size" else "name"
reverse = False
last_lower_folder = None
last_path = None
non_win_clipboard = None
slash = "\\" if sys.platform == "win32" else "/"
op_slash = "/" if sys.platform == "win32" else "\\"
ftp = None
url_ftp = None

# Window
window = tk.Tk()
window.resizable(True, True)
window.iconphoto(True, tk.PhotoImage(file="data/icon.png"))
window.minsize(width=800, height=500)
frame_up = tk.Frame(window, border=1, bg="white")
frame_up.pack(fill="x", side="top")

# Top of window
folder_icon = tk.PhotoImage(file="data/icon_folder.png")
file_icon = tk.PhotoImage(file="data/icon_file.png")
folder_hidden_icon = tk.PhotoImage(file="data/icon_folder_hidden.png")
file_hidden_icon = tk.PhotoImage(file="data/icon_file_hidden.png")
home_icon = tk.PhotoImage(file="data/icon_home.png")
up_icon = tk.PhotoImage(file="data/icon_up.png")
frame_b = tk.Frame(frame_up, border=2, relief="groove", bg="white")
frame_b.pack(side="left")
tk.Button(frame_b, image=up_icon, width=25, height=32, relief="flat", bg="white", fg="black", command=move_up).grid(column=0, row=1)
tk.Button(frame_b, image=home_icon, width=25, height=32, relief="flat", bg="white", fg="black", command=lambda:update_files(home_path)).grid(column=1, row=1)
entry = tk.Entry(frame_up, font=("Arial", 12), justify="left", highlightcolor="white", highlightthickness=0, relief="groove", border=2)
entry.pack(side="right",fill="both", expand=1)
label = tk.Label(window, font=("Arial", 12), anchor="w", bg="white", foreground="grey", border=2)
label.pack(side="bottom",fill="both")

# Tree view
tree_frame = tk.Frame(window, border=1, relief="flat", bg="white")
tree_frame.pack(expand=1, fill="both")
tree = ttk.Treeview(tree_frame, columns=(["#1"]), selectmode="extended", show="tree headings", style="mystyle.Treeview")
tree.heading("#0", text="   Name ↑", anchor="w", command=sort_name_reverse)
tree.heading("#1", text="Size", anchor="w", command=sort_size_reverse)
tree.column("#0", anchor="w")
tree.column("#1", anchor="e", stretch=False, width=120)
tree.pack(side="left", expand=1, fill="both")
style = ttk.Style()
style.configure("Treeview", rowheight=40, font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 12), foreground="grey")
style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky":"nswe"})])
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right",fill="y")

# On/off hidden files checkbutton on start
hidden_menu = tk.IntVar()
if hidden == False:
    hidden_menu.set(0)
if hidden == True:
    hidden_menu.set(1)

# Right click menu
right_menu = tk.Menu(tree_frame, tearoff=0, font=("Arial", 12))
right_menu.add_command(label="Open", command=click, state="disabled")
right_menu.add_command(label="Copy", command=copy, state="disabled")
right_menu.add_command(label="Rename", command=rename, state="disabled")
right_menu.add_command(label="Delete in trash", command=delete, state="disabled")
right_menu.add_separator()
right_menu.add_command(label="Paste", command=paste, state="disabled")
right_menu.add_separator()
right_menu.add_command(label="New file", command=lambda:new("file"), state="normal")
right_menu.add_command(label="New catalog", command=lambda:new("dir"), state="normal")
right_menu.add_separator()
right_menu.add_checkbutton(label="Show hidden files", onvalue=1, offvalue=0, variable=hidden_menu, command=show_hide)
right_menu.bind("<FocusOut>", lambda event:right_menu.unpost())# Click elsewhere - close right click menu
scan_disks_add_buttons()
update_files(home_path)
tree.focus_set()

# Keyboard, mouse buttons
tree.bind("<<TreeviewSelect>>", lambda event:select())
tree.bind("<Double-Button-1>", lambda event:click())
tree.bind("<Button-1>", lambda event:remove_selection())
tree.bind("<Return>", lambda event:click())
tree.bind("<BackSpace>", lambda event:move_up())
tree.bind("<Button-3>", open_right_menu)
tree.bind("<Up>", lambda event:up_down_focus())
tree.bind("<Down>", lambda event:up_down_focus())
tree.bind("<Delete>", lambda event:delete())
tree.bind("<Control-c>", lambda event: copy())
tree.bind("<Control-v>", lambda event: paste() if right_menu.entrycget(index=5, option="state") == "normal" else None)
entry.bind("<Return>", lambda event:update_files(entry.get()))
entry.bind("<KP_Enter>", lambda event:update_files(entry.get()))

window.mainloop()