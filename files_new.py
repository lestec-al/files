import os, stat, re, sys, subprocess
import string
import shutil
import configparser
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import simpledialog
from pathlib import Path
from send2trash import send2trash
# Interface functions
def sort_name_reverse():
    global reverse
    global sort_size
    if sort_size == True:
        sort_size = False
    elif sort_size == False:
        if reverse == False:
            reverse = True
        elif reverse == True:
            reverse = False
    update_files_folders(entry.get())
def sort_size_reverse():
    global reverse
    global sort_size
    if sort_size == False:
        sort_size = True
    elif sort_size == True:
        if reverse == False:
            reverse = True
        elif reverse == True:
            reverse = False
    update_files_folders(entry.get())
def move_up():
    global last_lower_folder
    up_path = entry.get().rsplit(slash, 1)
    last_lower_folder = up_path[1]
    if re.match(r"\w:$", up_path[0]) or up_path[0] == "":
        update_files_folders(up_path[0] + slash)
    else:
        update_files_folders(up_path[0])
def show_hide():
    global hidden
    if hidden_menu.get() == 1:
        hidden = True
    elif hidden_menu.get() == 0:
        hidden = False
    update_files_folders(entry.get())
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
                tk.Button(frame_b, text=disk, font=("Arial", 14), relief="flat", bg="white", fg="black",
                    command=lambda disk=disk:update_files_folders(f"{disk}:{slash}")).grid(column=column, row=1)
                column += 1
            letter_c += 1
    if sys.platform == "linux":
        column = 2
        os_user = home_path.rsplit(slash, 1)[1]
        if os.path.exists(f"/media/{os_user}/"):
            for l_disk in os.listdir(f"/media/{os_user}/"):
                tk.Button(frame_b, text=l_disk[0], font=("Arial", 14), relief="flat", bg="white", fg="black",
                    command=lambda l_disk=l_disk:update_files_folders(f"/media/{os_user}/{l_disk}")).grid(column=column, row=1)
                column += 1
# File operations
def copy():
    list_i = []
    for i in tree.selection():
        path = tree.item(i)["values"][1]
        if slash in path:
            path = path.replace(slash, "/")
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
        # Search file/folder copies
        file_copies = 1
        for f in os.listdir(entry.get()):
            if f == edit[1]:
                file_copies += 1
        if file_copies > 1:
            while True:
                for f in os.listdir(entry.get()):
                    if f == f"({file_copies})" + edit[1]:
                        file_copies += 1
                        continue
                break
            destination = entry.get() + slash + f"({file_copies})" + edit[1]
        else:
            destination = entry.get() + slash + edit[1]
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    update_files_folders(entry.get())
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
    update_files_folders(entry.get())
def rename():
    for i in tree.selection():
        r_path = tree.item(i)["values"][1]
        e_path = r_path.rsplit(slash, 1)
        if os.path.exists(r_path):
            answer = simpledialog.askstring(title="Files", prompt=f"Rename '{e_path[1]}'", parent=tree_frame, initialvalue=e_path[1])
            if answer is not None:
                rename_str = e_path[0] + slash + answer
                os.rename(r_path, rename_str)
    update_files_folders(entry.get())
# Update files/dirs + convert size
def convert_size(name):
    s = os.stat(name).st_size
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
def update_files_folders(dirname):
    global last_path
    size_list = []
    count = 0
    # Check path
    try:
        files = os.listdir(dirname)
    except PermissionError as e:
        tk.messagebox.showerror(title="Error", message=e)
        dirname = dirname.rsplit(slash, 1)
        dirname = dirname[0]
        if re.match(r"\w:$", dirname) or dirname == "":
            dirname = dirname + slash
        files = os.listdir(dirname)
    except:
        tk.messagebox.showerror(title="Error", message="Incorrect path")
        dirname = home_path
        if last_path != None:
            dirname = last_path
        files = os.listdir(dirname)
    # Clean old
    for item in tree.get_children():
        tree.delete(item)
    entry.delete(0, "end")
    # Reverse sorting
    if reverse == False:
        files.sort(key=str.lower)
    elif reverse == True:
        files.sort(key=str.lower, reverse=True)
    # Scan folders
    for f in files:
        fullname = os.path.join(dirname, f)
        f = f"  {f}"
        size = convert_size(fullname)
        if hidden == False:
            if sys.platform == "win32":
                try:
                    if os.readlink(fullname):
                        continue
                except:pass
                if os.path.isdir(fullname):
                    if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                        continue
                    else:
                        tree.insert("", tk.END, text=f, values=["<dir>", fullname], open=False, image=folder_icon)
                        count += 1
                else:continue
            else:
                if f.startswith("  ."):
                    continue
                elif os.path.isdir(fullname):
                    tree.insert("", tk.END, text=f, values=["<dir>", fullname], open=False, image=folder_icon)
                    count += 1
                else:continue
        elif os.path.isdir(fullname):
            tree.insert("", tk.END, text=f, values=["<dir>", fullname], open=False, image=folder_icon)
            count += 1
        else:continue
    # Scan files
    for f in files:
        fullname = os.path.join(dirname, f)
        f = f"  {f}"
        size = convert_size(fullname)  
        if sort_size == True:
            if hidden == False:
                if os.path.isdir(fullname):
                    continue
                else:
                    if sys.platform == "win32":
                        if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                            continue
                        else:
                            size_list_ml = [size[1], fullname, f, size[0]]
                            size_list.append(size_list_ml)
                    else:
                        if f.startswith("  ."):
                            continue
                        else:
                            size_list_ml = [size[1], fullname, f, size[0]]
                            size_list.append(size_list_ml)
            elif os.path.isdir(fullname):
                continue
            else:
                size_list_ml = [size[1], fullname, f, size[0]]
                size_list.append(size_list_ml)
        else:
            if hidden == False:
                if os.path.isdir(fullname):
                    continue
                else:
                    if sys.platform == "win32":
                        if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                            continue
                        else:
                            tree.insert("", tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                            count += 1
                    else:
                        if f.startswith("  ."):
                            continue
                        else:
                            tree.insert("", tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                            count += 1
            elif os.path.isdir(fullname):
                continue
            else:
                tree.insert("", tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                count += 1
    # Sorting
    if sort_size == True:
        if reverse == False:
            size_list.sort(key=lambda size_list: size_list[0], reverse=True)
        if reverse == True:
            size_list.sort(key=lambda size_list: size_list[0])
        for s in size_list:
            tree.insert("", tk.END, text=s[2], values=[s[3], s[1]], open=False, image=file_icon)
            count += 1
        size_list.clear()
    entry.insert("end", dirname)
    label["text"]=f"   {str(count)} objects"
    last_path = dirname
    # Set title = folder name
    dirname_edit = dirname.rsplit(slash, 1)
    if re.match(r"\w:\\$", dirname):
        dirname_edit[1] = f"Disk ({dirname[0:2]})"
    elif dirname_edit[1] == "":
        dirname_edit[1] = "Computer"
    window.title(dirname_edit[1])
    # Clean selection + menu to default
    right_menu.entryconfig("Open", state="disabled")
    right_menu.entryconfig("Copy", state="disabled")
    right_menu.entryconfig("Rename", state="disabled")
    right_menu.entryconfig("Delete in trash", state="disabled")
    # If clipboard on windows has a path - change button
    if sys.platform == "win32":
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
            if tree.item(item)["text"] == f"  {last_lower_folder}":
                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)
                break
# Press UP, DOWN - focus item in start
def up_down_focus():
    if tree.focus() == "":
        try:
            item = tree.get_children()[0]
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
        except:pass
# Select, click tree item + when select change menu
def select():
    if len(tree.selection()) > 0:
        right_menu.entryconfig("Open", state="normal")
        right_menu.entryconfig("Copy", state="normal")
        right_menu.entryconfig("Rename", state="normal")
        right_menu.entryconfig("Delete in trash", state="normal")
# Click on empty - remove selection + change menu
def remove_selection():
    tree.selection_remove(tree.focus())
    right_menu.entryconfig("Open", state="disabled")
    right_menu.entryconfig("Copy", state="disabled")
    right_menu.entryconfig("Rename", state="disabled")
    right_menu.entryconfig("Delete in trash", state="disabled")
# Open folders/files
def click():
    for selected_item in tree.selection():
        select_path = tree.item(selected_item)["values"][1]
        if os.path.isdir(select_path):
            update_files_folders(select_path)
        else:
            if sys.platform == "win32":
                os.startfile(select_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, select_path])
# Ini config home path, hidden files + others variables
config = configparser.ConfigParser()
config.read("data/files.ini")
home_path = config["USER"]["home_path"]
if home_path == "":
    home_path = config["DEFAULT"]["home_path"]
home_path = eval(home_path)
hidden = config["USER"]["show_hidden"]
if hidden == "":
    hidden = config["DEFAULT"]["show_hidden"]
hidden = eval(hidden)
reverse = False
sort_size = False
last_lower_folder = None
last_path = None
non_win_clipboard = None
# Slash for OS
if sys.platform == "win32":
    slash = "\\"
else:
    slash = "/"
# Window
window = tk.Tk()
window.resizable(True, True)
window.iconphoto(True, tk.PhotoImage(file="data/files.png"))
window.minsize(width=800, height=500)
frame_up = tk.Frame(window, border=1, bg="white")
frame_up.pack(fill="x", side="top")
# Top of window
folder_icon = tk.PhotoImage(file="data/files_c.png")
file_icon = tk.PhotoImage(file="data/files_f.png")
home_icon = tk.PhotoImage(file="data/files_h.png")
up_icon = tk.PhotoImage(file="data/files_up.png")
frame_b = tk.Frame(frame_up, border=2, relief="groove", bg="white")
frame_b.pack(side="left")
tk.Button(frame_b, image=up_icon, width=25, height=32, relief="flat", bg="white", fg="black", command=move_up).grid(column=0, row=1)
tk.Button(frame_b, image=home_icon, width=25, height=32, relief="flat", bg="white", fg="black", command=lambda:update_files_folders(home_path)).grid(column=1, row=1)
entry = tk.Entry(frame_up, font=("Arial", 12), justify="left", highlightcolor="white", highlightthickness=0, relief="groove", border=2)
entry.pack(side="right",fill="both", expand=1)
label = tk.Label(window, font=("Arial", 12), anchor="w", bg="white", foreground="grey", border=2)
label.pack(side="bottom",fill="both")
# Tree view
tree_frame = tk.Frame(window, border=1, relief="flat", bg="white")
tree_frame.pack(expand=1, fill="both")
tree = ttk.Treeview(tree_frame, columns=("#1"), selectmode="extended", show="tree headings", style="mystyle.Treeview")
tree.heading("#0", text="   Name", anchor="w", command=sort_name_reverse)
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
right_menu.add_checkbutton(label="Show hidden files", onvalue=1, offvalue=0, variable=hidden_menu, command=show_hide)
right_menu.bind("<FocusOut>", lambda event:right_menu.unpost())# Click elsewhere - close right click menu
scan_disks_add_buttons()
update_files_folders(home_path)
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
entry.bind("<Return>", lambda event:update_files_folders(entry.get()))
entry.bind("<KP_Enter>", lambda event:update_files_folders(entry.get()))
window.mainloop()