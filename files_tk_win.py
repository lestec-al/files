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
    global last_lower_path
    up_path = entry.get().rsplit("\\", 1)
    last_lower_path = up_path[1]
    if re.match(r"\w:$", up_path[0]):
        update_files_folders(up_path[0] + "\\")
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
    letters = string.ascii_uppercase
    letter_c = 0
    column = 2
    for _ in range(26):
        disk = letters[letter_c]
        if os.path.exists(f"{disk}:\\"):
            tk.Button(frame_b, text=f"{disk}:", width=2, font=("Arial", 14), relief="flat", bg="white", fg="black",
                command=lambda disk=disk:update_files_folders(f"{disk}:\\")).grid(column=column, row=1)
            column += 1
        letter_c += 1
# File operations
def copy():
    global select_path
    if "\\" in select_path:
        select_path = select_path.replace("\\", "/")
    os.system(f"powershell.exe Set-Clipboard -path '{select_path}'")
    right_menu.entryconfig("Paste", state="normal")
def paste():
    source = window.selection_get(selection="CLIPBOARD")
    if "/" in source:
        source = source.replace("/", "\\")
    source_edit = source.rsplit("\\", 1)
    # Search file/folder copies
    file_copies = 1
    for f in os.listdir(entry.get()):
        if f == source_edit[1]:
            file_copies += 1
    if file_copies > 1:
        while True:
            for f in os.listdir(entry.get()):
                if f == f"({file_copies})" + source_edit[1]:
                    file_copies += 1
                    continue
            break
        destination = entry.get() + "\\" + f"({file_copies})" + source_edit[1]
    else:
        destination = entry.get() + "\\" + source_edit[1]
    if os.path.isdir(source):
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)
    update_files_folders(entry.get())
def delete():
    try:
        del_path = select_path
        del_edit = del_path.rsplit("\\", 1)
        answer = askyesno(title="confirmation", message=f"Delete '{del_edit[1]}' in trash?")
        if answer:
            if os.path.exists(del_path):
                send2trash(del_path)
                update_files_folders(entry.get())
    except:pass
def rename():
    r_path = select_path
    r_edit = r_path.rsplit("\\", 1)
    if os.path.exists(r_path):
        answer_str = simpledialog.askstring(f"Rename '{r_edit[1]}'", "Enter new name:", parent=tree_frame, initialvalue=r_edit[1])
        if answer_str is not None:
            rename_str = r_edit[0] + "\\" + answer_str
            os.rename(r_path, rename_str)
            update_files_folders(entry.get())
        else:None
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
    global select_path
    global reverse
    global sort_size
    size_list = []
    count = 0
    # If access to folder is denied
    try:
        files = os.listdir(dirname)
    except PermissionError as e:
        tk.messagebox.showerror(title="Permission Error", message=e)
        dirname = dirname.rsplit("\\", 1)
        dirname = dirname[0]
        if re.match(r"\w:$", dirname):
            dirname = dirname + "\\"
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
                    if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
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
                    if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                        continue
                    else:
                        tree.insert("", tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                        count += 1
            elif os.path.isdir(fullname):
                continue
            else:
                tree.insert("", tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                count += 1
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
    # Set title = folder name
    try:
        dirname_edit = dirname.rsplit("\\", 1)
        window.title(dirname_edit[1])
    except:pass
    # Clean selection + menu to default
    select_path = None
    right_menu.entryconfig("Open", command=None, state="disabled")
    right_menu.entryconfig("Copy", state="disabled")
    right_menu.entryconfig("Rename", state="disabled")
    right_menu.entryconfig("Delete in trash", state="disabled")
    # If clipboard has a path change button
    try:
        if "/" in window.selection_get(selection="CLIPBOARD"):
            right_menu.entryconfig("Paste", state="normal")
        else:
            right_menu.entryconfig("Paste", state="disabled")
    except:
        right_menu.entryconfig("Paste", state="disabled")
    # Focus on the folder from which you returned
    if tree.focus() == "" and last_lower_path != None:
        for item in tree.get_children():
            if tree.item(item)["text"] == f"  {last_lower_path}":
                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)
                break
# Press UP, DOWN - focus item in start
def up_down_item_focus():
    if tree.focus() == "":
        try:
            item = tree.get_children()[0]
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
        except:pass
# Select, click tree item
def item_selected(event):    
    global select_path
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        select_path = item["values"][1]
        # Change menu when select item
        right_menu.entryconfig("Open", command=lambda:item_clicked(event), state="normal")
        right_menu.entryconfig("Copy", state="normal")
        right_menu.entryconfig("Rename", state="normal")
        right_menu.entryconfig("Delete in trash", state="normal")
        # Click on empty - remove selection + change menu
        if "<ButtonPress" in str(event):
            tree.selection_remove(tree.focus())
            select_path = None
            right_menu.entryconfig("Open", command=None, state="disabled")
            right_menu.entryconfig("Copy", state="disabled")
            right_menu.entryconfig("Rename", state="disabled")
            right_menu.entryconfig("Delete in trash", state="disabled")
# Open folders/files
def item_clicked(event):
    global select_path
    if select_path is not None:
        if os.path.isdir(select_path):
            update_files_folders(select_path)
        else:
            os.startfile(select_path)
# Ini config home path, hidden files + variables
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
select_path = None
reverse = False
sort_size = False
last_lower_path = None
# Window
window = tk.Tk()
window.resizable(True, True)
window.iconphoto(True, tk.PhotoImage(file="data/files.png"))
window.minsize(width=800, height=500)
frame_up = tk.Frame(window, border=1, bg="white")
frame_up.pack(fill="x", side="top")
folder_icon = tk.PhotoImage(file="data/files_c.png")
file_icon = tk.PhotoImage(file="data/files_f.png")
# Top of window
frame_b = tk.Frame(frame_up, border=2, relief="groove", bg="white")
frame_b.pack(side="left")
tk.Button(frame_b, text="↑", width=2, font=("Arial", 14), relief="flat", bg="white", fg="black", command=move_up).grid(column=0, row=1)
tk.Button(frame_b, text="🏠", width=2, font=("Arial", 14), relief="flat", bg="white", fg="black", command=lambda:update_files_folders(home_path)).grid(column=1, row=1)
entry = tk.Entry(frame_up, font=("Arial", 12), justify="left", highlightcolor="white", highlightthickness=0, relief="groove", border=2)
entry.pack(side="right",fill="both", expand=1)
label = tk.Label(window, font=("Arial", 12), anchor="w", bg="white", foreground="grey", border=2)
label.pack(side="bottom",fill="both")
# Tree view
tree_frame = tk.Frame(window, border=1, relief="flat", bg="white")
tree_frame.pack(expand=1, fill="both")
tree = ttk.Treeview(tree_frame, columns=("#1"), selectmode="browse", show="tree headings", style="mystyle.Treeview")
tree.heading("#0", text="   Name", anchor="w", command=sort_name_reverse)
tree.heading("#1", text="Size", anchor="w", command=sort_size_reverse)
tree.column("#0", anchor="w")
tree.column("#1", anchor="e", stretch=False, width=120)
tree.pack(side="left", expand=1, fill="both")
style = ttk.Style()
style.configure("Treeview", rowheight=40, font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 12), foreground="grey")
style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right",fill="y")
# On/off for checkbutton when start app
hidden_menu = tk.IntVar()
if hidden == False:
    hidden_menu.set(0)
if hidden == True:
    hidden_menu.set(1)
# Right click menu
right_menu = tk.Menu(tree_frame, tearoff=0, font=("Arial", 12))
right_menu.add_command(label="Open", command=None, state="disabled")
right_menu.add_command(label="Copy", command=copy, state="disabled")
right_menu.add_command(label="Rename", command=rename, state="disabled")
right_menu.add_command(label="Delete in trash", command=delete, state="disabled")
right_menu.add_separator()
right_menu.add_command(label="Paste", command=paste, state="disabled")
right_menu.add_separator()
right_menu.add_checkbutton(label="Show hidden files", onvalue=1, offvalue=0, variable=hidden_menu, command=show_hide)
# Click elsewhere - close right click menu
right_menu.bind("<FocusOut>", lambda event:right_menu.unpost())
scan_disks_add_buttons()
update_files_folders(home_path)
tree.focus_set()
# Keyboard, mouse buttons
tree.bind("<<TreeviewSelect>>", item_selected)
tree.bind("<Double-Button-1>", item_clicked)
tree.bind("<Button-1>", item_selected)
tree.bind("<Return>", item_clicked)
tree.bind("<BackSpace>", lambda event:move_up())
tree.bind("<Button-3>", open_right_menu)
tree.bind("<Up>", lambda event:up_down_item_focus())
tree.bind("<Down>", lambda event:up_down_item_focus())
tree.bind("<Delete>", lambda event:delete())
entry.bind("<Return>", lambda event:update_files_folders(entry.get()))
entry.bind("<KP_Enter>", lambda event:update_files_folders(entry.get()))
window.mainloop()