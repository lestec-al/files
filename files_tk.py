import tkinter as tk
import os, sys, subprocess
import shutil
from pathlib import Path
from send2trash import send2trash
import configparser
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import simpledialog
# ini config main path, hidden files + variables
config = configparser.ConfigParser()
config.read('files.ini')
main_path = config['USER']['main_path']
if main_path == "":
    main_path = config['DEFAULT']['main_path']
main_path = eval(main_path)
hidden = config['USER']['hidden']
if hidden == "":
    hidden = config['DEFAULT']['hidden']
hidden = eval(hidden)
select_path = None
reverse = False
sort_size = False
source = None
def name_f(): # sort by name + reverse
    global reverse
    global sort_size
    if sort_size == True:
        sort_size = False
    elif sort_size == False:
        if reverse == False:
            reverse = True
        elif reverse == True:
            reverse = False
    add_files_and_folders("", entry.get())
def size_f(): # sort by size + reverse
    global reverse
    global sort_size
    if sort_size == False:
        sort_size = True
    elif sort_size == True:
        if reverse == False:
            reverse = True
        elif reverse == True:
            reverse = False
    add_files_and_folders("", entry.get())
def to_home(): # button 🏠
    add_files_and_folders("", main_path)
def to_up(): # button ↑
    up_path = entry.get().rsplit("/", 1)
    if up_path[0] == "":
        add_files_and_folders("", "/")
    else:
        add_files_and_folders("", up_path[0])
# window settings
window = tk.Tk()
window.resizable(True, True)
window.iconphoto(False, tk.PhotoImage(file="images/files.png"))
window.minsize(width=800, height=500)
frame = tk.Frame(window)
frame.pack(fill="x", side='top')
folder_icon = tk.PhotoImage(file="images/files_c_24.png")
file_icon = tk.PhotoImage(file="images/files_f_24.png")
# the staff inside window
frame_b = tk.Frame(frame)
frame_b.pack(side="left")
button = tk.Button(frame_b, text="↑", height=1, width=3, font=("Helvetica", 14), command=to_up)
button.grid(column=0, row=1)
button = tk.Button(frame_b, text="🏠", height=1, width=3, font=("Helvetica", 14), command=to_home)
button.grid(column=1, row=1)
entry = tk.Entry(frame, font="size= 14", justify="left", highlightcolor="white", highlightthickness=0)
entry.pack(side="right",fill="both", expand=1)
label = tk.Label(window, font="size= 14", anchor="w")
label.pack(side='bottom',fill="both")
# the tree settings (inside window)
tree_frame = tk.Frame(window)
tree_frame.pack(expand=1, fill="both")
tree = ttk.Treeview(tree_frame, columns=('#1'), selectmode="browse", show='tree headings')
tree.heading('#0', text='Name', anchor='w', command=name_f)
tree.heading('#1', text='Size', anchor='w', command=size_f)
tree.column("#0", anchor='w')
tree.column("#1", anchor='e', stretch=False, width=120)
tree.pack(side="left", expand=1, fill="both")
style = ttk.Style()
style.configure("Treeview", rowheight=35, highlightthickness=0, bd=0, font=("Helvetica", 14)) # body font
style.configure("Treeview.Heading", font=("Helvetica", 14,'bold')) # headings font
scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right",fill="y")
# file operations
def copy():
    global source
    try:
        source = select_path
        m.entryconfig("▣ Paste", state="normal")
    except:None
def paste():
    global source
    source_edit = source.rsplit("/", 1)
    if source != "":
        if os.path.isdir(source):
            if source_edit[0] == entry.get():
                destination = entry.get() + "/" + source_edit[1] + " (copy)"
            else:
                destination = entry.get() + "/" + source_edit[1]
            shutil.copytree(source, destination)
            destination = ""
        else:
            if source_edit[0] == entry.get():
                destination = entry.get() + "/" + source_edit[1] + " (copy)"
            else:
                destination = entry.get() + "/"
            shutil.copy2(source, destination)
            destination = ""
        add_files_and_folders("", entry.get())
def delete():
    try:
        del_path = select_path
        del_edit = del_path.rsplit("/", 1)
        answer = askyesno(title='confirmation', message=f"Delete '{del_edit[1]}' in trash?")
        if answer:
            if os.path.exists(del_path):
                send2trash(del_path)
                add_files_and_folders("", entry.get())
    except:None
def rename():
    r_path = select_path
    r_edit = r_path.rsplit("/", 1)
    if os.path.exists(r_path):
        answer_str = simpledialog.askstring(f"Rename '{r_edit[1]}'", "Enter new name:", parent=tree_frame, initialvalue=r_edit[1])
        if answer_str is not None:
            rename_str = r_edit[0] + "/" + answer_str
            os.rename(r_path, rename_str)
            add_files_and_folders("", entry.get())
        else:None
# on/off for checkbutton when start app
h = tk.IntVar()
if hidden == False:
    h.set(0)
if hidden == True:
    h.set(1)
def hidden_f(): # show/hide files
    global hidden
    if h.get() == 1:
        hidden = True
    elif h.get() == 0:
        hidden = False
    add_files_and_folders("", entry.get())
# right click menu
m = tk.Menu(tree_frame, tearoff=0, font=("Helvetica", 14))
m.add_command(label="➲ Open", command=None, state="disabled")
m.add_separator()
m.add_command(label="❐ Copy", command=copy, state="disabled")
m.add_command(label="▣ Paste", command=paste, state="disabled")
m.add_command(label="✎ Rename", command=rename, state="disabled")
m.add_command(label="✘ Delete in trash", command=delete, state="disabled")
m.add_separator()
m.add_checkbutton(label="Show hidden files", onvalue=1, offvalue=0, variable=h, command=hidden_f)
def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
tree.bind("<Button-3>", do_popup)
# click elsewhere - close menu
def popupFocusOut(event=None):
        m.unpost()
m.bind("<FocusOut>",popupFocusOut)
# convert size in updating files
def add_size(name):
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
def takeFirst(elem): # for sort in updating files
    return elem[0]
# updating files + sort
def add_files_and_folders(parent, dirname):
    global select_path
    size_list = []
    count = 0
    files = os.listdir(dirname)
    # clean old
    for item in tree.get_children():
        tree.delete(item)
    entry.delete(0, "end")

    if reverse == False:
        files.sort(key=str.lower)
    elif reverse == True:
        files.sort(key=str.lower, reverse=True)

    for f in files:
        fullname = os.path.join(dirname, f)
        size = add_size(fullname)
        if hidden == False:
            if f.startswith("."):
                continue
            elif os.path.isdir(fullname):
                tree.insert(parent, tk.END, text=f, values=[size[0], fullname], open=False, image=folder_icon)
                count += 1
            else:continue
        elif os.path.isdir(fullname):
            tree.insert(parent, tk.END, text=f, values=[size[0], fullname], open=False, image=folder_icon)
            count += 1
        else:continue
    for f in files:
        fullname = os.path.join(dirname, f)
        size = add_size(fullname)
        if sort_size == True:
            if hidden == False:
                if f.startswith("."):
                    continue
                elif os.path.isdir(fullname):
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
                if f.startswith("."):
                    continue
                elif os.path.isdir(fullname):
                    continue
                else:
                    tree.insert(parent, tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                    count += 1
            elif os.path.isdir(fullname):
                continue
            else:
                tree.insert(parent, tk.END, text=f, values=[size[0], fullname], open=False, image=file_icon)
                count += 1
    if sort_size == True:
        if reverse == False:
            size_list.sort(key=takeFirst, reverse=True)
        if reverse == True:
            size_list.sort(key=takeFirst)
        for s in size_list:
            tree.insert(parent, tk.END, text=s[2], values=[s[3], s[1]], open=False, image=file_icon)
            count += 1
        size_list.clear()
    entry.insert("end", dirname)
    label["text"]=str(count) + " objects"
    # set title = catalog name
    dirname_edit = dirname.rsplit("/", 1)
    window.title(dirname_edit[1] + " - Files")
    # clean selection + menu to default
    select_path = None
    m.entryconfig("➲ Open", command=None, state="disabled")
    m.entryconfig("❐ Copy", state="disabled")
    m.entryconfig("✎ Rename", state="disabled")
    m.entryconfig("✘ Delete in trash", state="disabled")
add_files_and_folders("", main_path)
# select, click tree item + open files
def item_selected(event):    
    global select_path
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        select_path = item['values'][1]
        # change menu when select item
        m.entryconfig("➲ Open", command=lambda:item_clicked(event), state="normal")
        m.entryconfig("❐ Copy", state="normal")
        m.entryconfig("✎ Rename", state="normal")
        m.entryconfig("✘ Delete in trash", state="normal")
        if "<ButtonPress" in str(event): # click on empty - remove selection + change menu
            tree.selection_remove(tree.focus())
            select_path = None
            m.entryconfig("➲ Open", command=None, state="disabled")
            m.entryconfig("❐ Copy", state="disabled")
            m.entryconfig("✎ Rename", state="disabled")
            m.entryconfig("✘ Delete in trash", state="disabled")
def item_clicked(event):
    if select_path is not None:
        if os.path.isdir(select_path): # open catalog
            add_files_and_folders("", select_path)
        else: # open file
            if sys.platform == "win32":
                os.startfile(select_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, select_path])
tree.bind('<<TreeviewSelect>>', item_selected)
tree.bind('<Double-Button-1>', item_clicked)
tree.bind('<Button-1>', item_selected)
# change dir from input
def entry_op():
    add_files_and_folders("", entry.get())
entry.bind("<Return>", lambda event:entry_op())
entry.bind("<KP_Enter>", lambda event:entry_op())
window.mainloop()