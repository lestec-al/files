import os, stat, re, sys, subprocess, string, shutil, math
from pathlib import Path
from ftplib import FTP

# Interface functions

def print_interface(page=0):
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
        elif sys.platform == "linux":
            print(d[0], end=" ")
    print()
    size = os.get_terminal_size().columns.real-5
    line = "-"*size
    print(line)
    print(url_ftp if ftp != None else "", last_path)
    print(line)
    pages = math.ceil(len(last_dir) / 2000 if len(last_dir) / 2000 >= 1 else 1)
    page = int(page) - 1
    if page < 0:
        page = 0
    for io,f in enumerate(last_dir[page*2000:page*2000+2000]):
        io = io + 1 + page*2000
        i = io
        if len(str(i)) == 1:
            i = f"   {i}"
        elif len(str(i)) == 2:
            i = f"  {i}"
        elif len(str(i)) == 3:
            i = f" {i}"
        while True:
            main_line = f"{i} {f[3]}{f[0]}{f[1]}"
            if len(main_line) < len(line)-2:
                f[0] += " "
            else:
                break
        print(main_line)
    if pages > 1:
        print(line)
        print(f"{len(last_dir)} objects. {pages} pages")
    print(line)


def move_up():
    up_path = last_path.rsplit("/" if ftp != None else slash, 1)
    update_files(f"{url_ftp}{up_path[0]}" if ftp != None else up_path[0])


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

# Operations

def calc_show_size(item):
    def check_dir_size(path) -> int:
        size = 0
        try:
            for f in os.scandir(path):
                if f.is_dir():
                    size += check_dir_size(f.path)
                else:
                    size += convert_size(f.path)[1]
        except:pass
        return size

    def size_operations(item, size) -> list:
        name, type_size, path = item[0], item[1], item[2]
        if type_size == "dir":
            size.append(f"- {name.strip()}: {convert_size(check_dir_size(path))[0]}")
        else:
            size.append(f"- {name.strip()}: {convert_size(type_size)[0]}")
        return size

    size = []
    item_name, items_name = None, None
    item_index, items_index = None, None
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
    for i,f in enumerate(last_dir):
        i += 1
        if item_index != None and i == item_index or item_name != None and f[0].strip().lower() == item_name.lower():
            size = size_operations(f, size)
        elif items_index != None:
            for i1 in items_index:
                if i == i1:
                    size = size_operations(f, size)
        elif items_name != None:
            for n1 in items_name:
                if f[0].strip().lower() == n1.lower():
                    size = size_operations(f, size)
    for x in size:
        print(x)


def paste():
    if sys.platform == "win32":
        win_clipboard = subprocess.getoutput("powershell.exe -Command Get-Clipboard -Format FileDropList -Raw")
        clipboard = win_clipboard.replace("/", slash).split("\n")
    else:
        clipboard = non_win_clipboard.replace("'", "").split(",")

    for source in clipboard:
        edit = source.rsplit(slash, 1)
        # Search copies, create destination path
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
        # Paste
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)


def operations(item, operation):
    def delete_dir(d_path):
        for f in os.scandir(d_path):
            if f.is_dir():
                delete_dir(f.path)
            else:
                os.remove(f.path)
        try:
            os.rmdir(d_path)
        except:pass

    def do_operation(item, operation):
        name, type_size, path = item[0].strip(), item[1], item[2]
        if operation == "rename":
            e_path = path.rsplit(slash, 1)
            test = False
            while test == False:
                test = True
                new_name = input(f"Rename «{name}» or «..» for cancel > ")
                if new_name == "..":
                    break
                else:
                    try:
                        new_path = e_path[0] + slash + new_name
                        os.rename(path, new_path)
                    except Exception as e:
                        print(str(e))
                        test = False
        elif operation == "copy":
            if "\\" in path:
                path = path.replace("\\", "/")
            pathes.append(f"'{path}'")
        elif operation == "remove":
            pathes.append(path)
        elif operation == "delete":
            if type_size == "dir":
                delete_dir(path)
            else:
                os.remove(path)
        elif operation == "download":
            path_home = home_path.replace("\\", "/")
            with open(f"{path_home}/Downloads/{name}", "wb") as file:
                ftp.retrbinary(f"RETR {name}", file.write)
                file.close()

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
            do_operation(f, operation)
        elif items_index != None:
            for i1 in items_index:
                if i == i1:
                    do_operation(f, operation)
        elif items_name != None:
            for n1 in items_name:
                if f[0].strip().lower() == n1.lower():
                    do_operation(f, operation)
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
            update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)
        except:
            print("To remove in the trash, install Send2Trash") 
    else:
        update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)


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
            if f[1] == "dir":
                update_files(f[2])
            else:
                if sys.platform == "win32":
                    os.startfile(f[2])
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, f[2]])


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


def update_files(orig_dirname: str):
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
                except:
                    ftp = None
                    url_ftp = None
        else:
            if ftp != None:
                ftp.quit()
                ftp = None
                url_ftp = None
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
                                dirs_list.append([f.name, "dir", f.path, "▓ "])
                        else:
                            if not f.name.startswith("."):
                                dirs_list.append([f.name, "dir", f.path, "▓ "])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append([f.name, "dir", f.path, "░ "])
                            else:
                                if f.is_symlink():
                                    dirs_list.append([f.name, "dir", f.path, "░ "])
                                else:
                                    dirs_list.append([f.name, "dir", f.path, "▓ "])
                        else:
                            if f.name.startswith("."):
                                dirs_list.append([f.name, "dir", f.path, "░ "])
                            else:
                                dirs_list.append([f.name, "dir", f.path, "▓ "])
                if f.is_file():
                    if hidden == False:
                        if sys.platform == "win32":
                            if not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append([f.name, size[0], f.path, "▓ ", size[1]])
                        else:
                            if not f.name.startswith("."):
                                files_list.append([f.name, size[0], f.path, "▓ ", size[1]])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append([f.name, size[0], f.path, "░ ", size[1]])
                            else:
                                files_list.append([f.name, size[0], f.path, "▓ ", size[1]])
                        else:
                            if f.name.startswith("."):
                                files_list.append([f.name, size[0], f.path, "░ ", size[1]])
                            else:
                                files_list.append([f.name, size[0], f.path, "▓ ", size[1]])
        # FTP
        else:
            ftp.cwd(dirname)
            try:
                for f in ftp.mlsd():
                    if f[1]["type"] == "dir":
                        dirs_list.append([f[0], "dir", f"{orig_dirname}/{f[0]}", "▓ "])
                    elif f[1]["type"] == "file":
                        size = convert_size(int(f[1]["size"]))
                        files_list.append([f[0], size[0], f"{orig_dirname}/{f[0]}", "▓ ", size[1]])
            except:
                ftp.voidcmd('TYPE I')
                for f in ftp.nlst():
                    try:
                        if "." in f and not f.startswith("."):
                            size = convert_size(ftp.size(f))
                            files_list.append([f, size[0], f"{orig_dirname}/{f}", "▓ ", size[1]])    
                        else:
                            dirs_list.append([f, "dir", f"{orig_dirname}/{f}", "▓ "])
                    except:
                        dirs_list.append([f, "dir", f"{orig_dirname}/{f}", "▓ "])
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
        last_dir.clear()
        # Add new data
        count = 0
        for i in dirs_list:
            last_dir.append([i[0], f"{i[1]}", i[2], i[3]])
            count += 1
        for i in files_list:
            last_dir.append([i[0], f"{i[1]}", i[2], i[3]])
            count += 1
        #
        if ftp == None:
            last_path = dirname
        else:
            last_path = ftp.pwd()
        print_interface()

    except Exception as e:
        print(str(e))


# Variables
home_path = str(Path.home())
hidden = False
sort = "name"
reverse = False
last_path, non_win_clipboard = None, None
slash = "\\" if sys.platform == "win32" else "/"
op_slash = "/" if sys.platform == "win32" else "\\"
last_dir = []
ftp = None
url_ftp = None


# Start app
disks = add_disks()
update_files(home_path)


# Main loop
while True:
    input1 = input("«help» for FAQ > ").split(" ", 1)

    if len(input1) == 1:
        if slash in input1[0] or op_slash in input1[0]:
            update_files(input1[0])
        elif input1[0] == "exit":
            if sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
            break
        elif input1[0] == "..":
            move_up()
        elif input1[0] == "paste" and ftp == None:
            paste()
        elif input1[0] == ".":
            update_files(home_path)
        elif input1[0] == "hidden":
            if hidden == False:
                hidden = True
            elif hidden == True:
                hidden = False
            update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)
        elif input1[0] == "sort":
            if reverse == True:
                reverse = False
            elif reverse == False:
                reverse = True
            update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)
        elif input1[0] == "help":
            print()
            print("- up: «..»")
            print("- open: «12» «documents» «c:\\users» «/home» «ftp://ftp.us.debian.org»")
            print("- home path: «.»")
            print("- copy,rename,remove(to trash),delete(permanently): «copy 11» «delete 2,10»")
            print("- ftp download: «download 11» «download 12,14»")
            print("- show size: «size 9»")
            print("- select page: «page 3»")
            print("- disks: «disk C» «disk disk 2»")
            print("- create: «dir Pictures» «file readme.txt»")
            print("- sorting: «sort»(for ↑↓) «sort name» «sort size»")
            print("- exercute cl command: «code dir» «code ls»")
            print("- «exit» «paste» «hidden»")
            print()
        else:
            click(input1[0])

    elif len(input1) == 2:
        if input1[0] == "disk":
            if sys.platform == "win32":
                update_files(f"{input1[1].upper()}:{slash}")
            elif sys.platform == "linux":
                for d in disks:
                    if input1[1].lower() in d[0].lower():
                        update_files(f"/media/{d[1]}/{d[0]}")
        elif input1[0] == "sort":
            sort = "size" if input1[1] == "size" else "name"
            update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)
        elif input1[0] == "page":
            print_interface(input1[1])

        elif ftp == None:
            if input1[0] == "copy":
                operations(input1[1], "copy")
            elif input1[0] == "delete":
                operations(input1[1], "delete")
            elif input1[0] == "remove":
                operations(input1[1], "remove")
            elif input1[0] == "rename":
                operations(input1[1], "rename")
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
                    update_files(f"{url_ftp}{last_path}" if ftp != None else last_path)
                else:
                    print("Name is taken")
            elif input1[0] == "size":
                calc_show_size(input1[1])
            # Test CL commands support
            elif input1[0] == "code":
                os.chdir(last_path)
                try:
                    msg = subprocess.getoutput(input1[1])
                    print()
                    print(msg)
                    print()
                except:
                    subprocess.call(input1[1], creationflags=subprocess.CREATE_NEW_CONSOLE)

        elif ftp != None:
            if input1[0] == "download":
                operations(input1[1], "download")