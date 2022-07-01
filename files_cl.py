import os, stat, re, sys, subprocess, string, shutil, configparser
from pathlib import Path
# Interface functions
def print_interface():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    print()
    if len(disks) > 0:
        print("Files | disks: ", end="")
    else:
        print("Files")
    for d in disks:
        if sys.platform == "win32":
            print(d.upper(), end=" ")
        if sys.platform == "linux":
            print(d[0], end=" | ")
    print()
    line = "----------------------------------------------------"
    while len(line) < len(last_path):
        line += "-"
    print(line)
    print(last_path)
    print(line)
    for io,f in enumerate(last_dir):
        io += 1
        i = io
        if len(str(i)) == 1:
            i = f"  {i}"
        elif len(str(i)) == 2:
            i = f" {i}"
        f[0] += "  "
        while len(f[0]) < 40:
            f[0] += " "
        print(f"{i} {f[3]}{f[0]}{f[1]}")
    print(line)
def move_up():
    up_path = last_path.rsplit(slash, 1)
    if re.match(r"\w:$", up_path[0]) or up_path[0] == "":
        update_files_folders(up_path[0] + slash)
    else:
        update_files_folders(up_path[0])
def add_disks():
    disks = []
    if sys.platform == "win32":
        letters = string.ascii_uppercase
        letter_c = 0
        column = 2
        for _ in range(26):
            disk = letters[letter_c]
            if os.path.exists(f"{disk}:{slash}"):
                disks.append(disk.lower())
                column += 1
            letter_c += 1
    if sys.platform == "linux":
        column = 2
        os_user = home_path.rsplit(slash, 1)[1]
        if os.path.exists(f"/media/{os_user}/"):
            for l_disk in os.listdir(f"/media/{os_user}/"):
                disks.append((l_disk, os_user))
                column += 1
    return disks
# File operations
def paste():
    if sys.platform == "win32":
        win_clipboard = subprocess.getoutput("powershell.exe -Command Get-Clipboard -Format FileDropList -Raw")
        clipboard = win_clipboard.replace("/", slash).split("\n")
    else:
        clipboard = non_win_clipboard.replace("'", "").split(",")
    for source in clipboard:
        edit = source.rsplit(slash, 1)
        # Search file/folder copies
        file_copies = 1
        for f in os.listdir(last_path):
            if f.lower() == edit[1].lower():
                file_copies += 1
        if file_copies > 1:
            while True:
                for f in os.listdir(last_path):
                    if f.lower() == f"({file_copies}){edit[1]}".lower():
                        file_copies += 1
                        continue
                break
            destination = last_path + slash + f"({file_copies})" + edit[1]
        else:
            destination = last_path + slash + edit[1]
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    update_files_folders(last_path)
def copy_delete_rename(item, operation):
    def delete_dir(d_path):
        for f in os.listdir(d_path):
            f1 = os.path.join(d_path, f)
            if not os.path.isdir(f1):
                os.remove(f1)
            else:
                delete_dir(f1)
        os.rmdir(d_path)
    def operations(path):
        if os.path.exists(path):
            if operation == "rename":
                e_path = path.rsplit(slash, 1)
                test = False
                while test == False:
                    test = True
                    new_name = input(f"Rename '{e_path[1]}' or '..' for cancel > ")
                    if new_name is not None and new_name != '..':
                        for f in os.listdir(last_path):
                            if f.lower() == new_name.lower() and new_name.lower() != e_path[1].lower():
                                test = False
                        if test == False:
                            print("Name is taken")
                if new_name is not None and new_name.lower() != e_path[1].lower() and new_name != '..':
                    new_path = e_path[0] + slash + new_name
                    os.rename(path, new_path)
            elif operation == "copy":
                if "\\" in path:
                    path = path.replace("\\", "/")
                pathes.append(f"'{path}'")
            elif operation == "remove":
                pathes.append(path)
            elif operation == "delete":
                if os.path.isdir(path):
                    delete_dir(path)
                else:
                    os.remove(path)
    item_name = None
    items_name = None
    item_index = None
    items_index = None
    try:
        if "," in item:
            items_index = [int(i) for i in item.split(",")]
        else:
            item_index = int(item)
    except:
        if "," in item:
            items_name = item.split(",")
        else:
            item_name = item
    pathes = []
    for i,f in enumerate(last_dir):
        i += 1
        if item_index != None and i == item_index or item_name != None and f[0].strip().lower() == item_name.lower():
            operations(f[2])
        elif items_index != None:
            for i1 in items_index:
                if i == i1:
                    operations(f[2])
        elif items_name != None:
            for n1 in items_name:
                if f[0].strip().lower() == n1.lower():
                    operations(f[2])
    if operation == "copy":
        if len(pathes) > 1:
            items = ",".join(pathes)
        else:
            items = pathes[0]
        if sys.platform == "win32":
            os.system(f"powershell.exe Set-Clipboard -path {items}")
        else:
            global non_win_clipboard
            non_win_clipboard = items
    elif operation == "remove":
        try:
            from send2trash import send2trash
            for p in pathes:
                send2trash(p)
            update_files_folders(last_path)
        except:
            print("Remove to trash not supported") 
    else:
        update_files_folders(last_path)
def click(item):
    item_name = None
    item_index = None
    try:
        item_index = int(item)
    except:
        item_name = item
    for i,f in enumerate(last_dir):
        i += 1
        if item_index != None and i == item_index or item_name != None and f[0].strip().lower() == item_name.lower():
            if os.path.isdir(f[2]):
                update_files_folders(f[2])
            else:
                if sys.platform == "win32":
                    os.startfile(f[2])
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, f[2]])
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
    last_dir.clear()# Clear old 
    size_list = []
    # Check path
    if op_slash in dirname:
        dirname = dirname.replace(op_slash, slash)
    if re.match(r".+\\$", dirname) or re.match(r".+/$", dirname):
        dirname = dirname[0:-1]
    if re.match(r"\w:$", dirname):
        dirname = dirname + slash
    try:
        files = os.listdir(dirname)
    except Exception as e:
        if "Access is denied" in str(e):
            print("Access is denied")
        dirname = home_path
        if last_path != None:
            dirname = last_path
        files = os.listdir(dirname)
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
                        last_dir.append([f, "<dir>", fullname, "▓"])# folder_icon
                else:continue
            else:
                if f.startswith("  ."):
                    continue
                elif os.path.isdir(fullname):
                    last_dir.append([f, "<dir>", fullname, "▓"])# folder_icon
                else:continue
        elif os.path.isdir(fullname):
            if sys.platform == "win32":
                if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                    last_dir.append([f, "<dir>", fullname, "░"])# folder_hidden_icon
                else:
                    try:
                        if os.readlink(fullname):
                            last_dir.append([f, "<dir>", fullname, "░"])# folder_hidden_icon
                    except:
                        last_dir.append([f, "<dir>", fullname, "▓"])# folder_icon
            else:
                if f.startswith("  ."):
                    last_dir.append([f, "<dir>", fullname, "░"])# folder_hidden_icon
                else:
                    last_dir.append([f, "<dir>", fullname, "▓"])# folder_icon
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
                if sys.platform == "win32":
                    if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                        size_list_ml = [size[1], fullname, f, size[0], "hidden"]
                        size_list.append(size_list_ml)
                    else:
                        size_list_ml = [size[1], fullname, f, size[0]]
                        size_list.append(size_list_ml)
                else:
                    if f.startswith("  ."):
                        size_list_ml = [size[1], fullname, f, size[0], "hidden"]
                        size_list.append(size_list_ml)
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
                            last_dir.append([f, f"{size[0]}", fullname, "▓"])# file_icon
                    else:
                        if f.startswith("  ."):
                            continue
                        else:
                            last_dir.append([f, f"{size[0]}", fullname, "▓"])# file_icon
            elif os.path.isdir(fullname):
                continue
            else:
                if sys.platform == "win32":
                    if bool(os.stat(fullname).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                        last_dir.append([f, f"{size[0]}", fullname, "░"])# file_hidden_icon
                    else:
                        last_dir.append([f, f"{size[0]}", fullname, "▓"])# file_icon
                else:
                    if f.startswith("  ."):
                        last_dir.append([f, f"{size[0]}", fullname, "░"])# file_hidden_icon
                    else:
                        last_dir.append([f, f"{size[0]}", fullname, "▓"])# file_icon
    # Sorting
    if sort_size == True:
        if reverse == False:
            size_list.sort(key=lambda size_list: size_list[0], reverse=True)
        if reverse == True:
            size_list.sort(key=lambda size_list: size_list[0])
        for s in size_list:
            if len(s) == 4:
                last_dir.append([s[2], f"{s[3]}", s[1], "▓"])# file_icon
            elif len(s) == 5:
                last_dir.append([s[2], f"{s[3]}", s[1], "░"])# file_hidden_icon
        size_list.clear()
    last_path = dirname
    print_interface()
# Ini config home path, showing hidden files + other variables
try:
    config = configparser.ConfigParser()
    config.read("files.ini")
    home_path_config = config["USER SETTINGS"]["home_path"]
    hidden_config = config["USER SETTINGS"]["show_hidden_files"]
except:
    home_path_config = ""
    hidden_config = ""
home_path = str(Path.home()) if home_path_config == "" else home_path_config
hidden = True if hidden_config == "True" else False
reverse, sort_size = False, False
last_path, non_win_clipboard = None, None
slash = "\\" if sys.platform == "win32" else "/"
op_slash = "/" if sys.platform == "win32" else "\\"
last_dir = []
disks = add_disks()
update_files_folders(home_path)
while True:
    input1 = input("'help' for FAQ > ").split(" ", 1)
    if len(input1) == 1:
        if slash in input1[0]:
            update_files_folders(input1[0])
        elif input1[0] == "exit":
            if sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
            break
        elif input1[0] == "..":
            move_up()
        elif input1[0] == "paste":
            paste()
        elif input1[0] == "home":
            update_files_folders(home_path)
        elif input1[0] == "hidden":
            if hidden == False:
                hidden = True
            elif hidden == True:
                hidden = False
            update_files_folders(last_path)
        elif input1[0] == "sort":
            if sort_size == True:
                sort_size = False
            elif sort_size == False:
                sort_size = True
            update_files_folders(last_path)
        elif input1[0] == "reverse":
            if reverse == True:
                reverse = False
            elif reverse == False:
                reverse = True
            update_files_folders(last_path)
        elif input1[0] == "help":
            print()
            print("- up: '..'")
            print("- open: '12' 'documents' 'c:\\users' '/home'")
            print("- copy/rename/remove/delete: 'copy 11' 'delete 2,10'")
            print("  remove (to trash, need Send2Trash), delete (permanently)")
            print("- disks: 'disk C' 'disk disk 2'")
            print("- create directory/file: 'dir Pictures' 'file readme.txt'")
            print("- other: 'paste' 'exit' 'home' 'hidden' 'sort' 'reverse'")
            print()
        else:
            click(input1[0])
    elif len(input1) == 2:
        if input1[0] == "copy":
            copy_delete_rename(input1[1], "copy")
        elif input1[0] == "delete":
            copy_delete_rename(input1[1], "delete")
        elif input1[0] == "remove":
            copy_delete_rename(input1[1], "remove")
        elif input1[0] == "rename":
            copy_delete_rename(input1[1], "rename")
        elif input1[0] == "dir" or input1[0] == "file":
            test = True
            for f in last_dir:
                if f[0].strip().lower() == input1[1].lower():
                    test = False
            if test == True:
                path = os.path.join(last_path, input1[1])
                if input1[0] == "dir":
                    os.mkdir(path)
                elif input1[0] == "file":
                    Path(path).touch()
                update_files_folders(last_path)
            else:
                print("Name is taken")
        elif input1[0] == "disk":
            if sys.platform == "win32":
                update_files_folders(f"{input1[1].upper()}:{slash}")
            if sys.platform == "linux":
                for d in disks:
                    if input1[1].lower() in d[0].lower():
                        update_files_folders(f"/media/{d[1]}/{d[0]}")