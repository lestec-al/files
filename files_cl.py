import os, stat, re, sys, subprocess, string, shutil, math
from pathlib import Path
from ftplib import FTP

# INTERFACE

def print_interface(page=0):
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    print()
    if len(DISKS) > 0:
        print("Files | disks: ", end="")
        for d in DISKS:
            if sys.platform == "win32":
                print(d.upper(), end=" ")
            elif sys.platform == "linux":
                print(d[0], end=" ")
    else:
        print("Files", end="")
    print()
    line = "-"*(os.get_terminal_size().columns.real-5)
    print(line)
    print(URL_FTP if FTP_VAR != None else "", LAST_PATH)
    print(line)
    page = int(page) - 1
    if page < 0:
        page = 0
    for idx,f in enumerate(LAST_DIR[page*2000:page*2000+2000]):
        idx = idx + 1 + page*2000
        i = idx
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
    pages = math.ceil(len(LAST_DIR) / 2000 if len(LAST_DIR) / 2000 >= 1 else 1)
    if pages > 1:
        print(line)
        print(f"{len(LAST_DIR)} objects. Page {page+1}/{pages}")
    print(line)


def move_up():
    up_path = LAST_PATH.rsplit("/" if FTP_VAR != None else SLASH, 1)
    update_files(f"{URL_FTP}{up_path[0]}" if FTP_VAR != None else up_path[0])

# OPERATIONS

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
            size.append(f"- {name.strip()}: {type_size}")
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
    for i,f in enumerate(LAST_DIR):
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
    try:
        if sys.platform == "win32":
            win_clipboard = subprocess.getoutput("powershell.exe -Command Get-Clipboard -Format FileDropList -Raw")
            clipboard = win_clipboard.replace("/", SLASH).split("\n")
        else:
            clipboard = NON_WIN_CLIPBOARD.replace("'", "").split(",")

        for source in clipboard:
            edit = source.rsplit(SLASH, 1)
            # Search copies, create destination path
            file_copies = 1
            for f in os.listdir(LAST_PATH):
                if f.lower() == edit[1].lower():
                    file_copies += 1
            if file_copies > 1:
                while True:
                    for f in os.listdir(LAST_PATH):
                        if f.lower() == f"({file_copies}){edit[1]}".lower():
                            file_copies += 1
                            continue
                    break
                destination = LAST_PATH + SLASH + f"({file_copies})" + edit[1]
            else:
                destination = LAST_PATH + SLASH + edit[1]
            # Paste
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
    except Exception as e:
        pass

    update_files(f"{URL_FTP}{LAST_PATH}" if FTP_VAR != None else LAST_PATH)


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
            e_path = path.rsplit(SLASH, 1)
            test = False
            while test == False:
                test = True
                new_name = input(f"Rename «{name}» or «..» for cancel > ")
                if new_name == "..":
                    break
                else:
                    try:
                        new_path = e_path[0] + SLASH + new_name
                        os.rename(path, new_path)
                    except Exception as e:
                        print(str(e))
                        test = False
        elif operation == "copy":
            if "\\" in path:
                path = path.replace("\\", "/")
            pathes.append(f"'{path}'")
        elif operation == "delete":
            if type_size == "dir":
                delete_dir(path)
            else:
                os.remove(path)
        elif operation == "download":
            path_home = HOME_PATH.replace("\\", "/")
            with open(f"{path_home}/Downloads/{name}", "wb") as file:
                FTP_VAR.retrbinary(f"RETR {name}", file.write)
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
    for i,f in enumerate(LAST_DIR):
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
            global NON_WIN_CLIPBOARD
            NON_WIN_CLIPBOARD = items
    else:
        update_files(f"{URL_FTP}{LAST_PATH}" if FTP_VAR != None else LAST_PATH)


def click(item):
    item_name = None
    item_index = None
    try:
        item_index = int(item)
    except:
        item_name = item
    for i,f in enumerate(LAST_DIR):
        i += 1
        if item_index != None and i == item_index or item_name != None and f[0].strip().lower() == item_name.lower():
            if f[4] == "dir":
                update_files(f[2])
            else:
                if sys.platform == "win32":
                    os.startfile(f[2])
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, f[2]])


def convert_size(var):
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
    else:
        size = str(byte_size) + " B"
    return size, byte_size

# MAIN

def update_files(orig_dirname: str, show_all_size=False):
    try:
        global LAST_PATH
        global FTP_VAR
        global URL_FTP
        dirname = orig_dirname
        # FTP
        if "ftp://" in dirname:
            x = dirname.split("//", 1)
            if "/" in x[1]:
                dirname = "/" + x[1].split("/", 1)[1]
            else:
                dirname = "/"
            #
            if FTP_VAR == None:
                FTP_VAR = FTP("")
                try:
                    if ":" in x[1]:
                        ftp_split = x[1].split(":", 1)
                        FTP_VAR.connect(ftp_split[0],int(ftp_split[1]))
                        URL_FTP = f"ftp://{ftp_split[0]}:{ftp_split[1]}"
                    else:
                        FTP_VAR.connect(x[1])
                        URL_FTP = f"ftp://{x[1]}"
                    FTP_VAR.login()
                except:
                    FTP_VAR = None
                    URL_FTP = None
        else:
            if FTP_VAR != None:
                FTP_VAR.quit()
                FTP_VAR = None
                URL_FTP = None
        # Check path
        if FTP_VAR == None and OP_SLASH in dirname:
            dirname = dirname.replace(OP_SLASH, SLASH)
        elif FTP_VAR != None and "\\" in dirname:
            dirname = dirname.replace("\\", "/")
        if re.match(r".+\\$", dirname) or re.match(r".+/$", dirname):
            dirname = dirname[0:-1]
        if re.match(r"\w:$", dirname) or dirname == "":
            if FTP_VAR == None:
                dirname = dirname + SLASH
            else:
                dirname = "/"
        # Scan
        files_list, dirs_list = [], []
        if FTP_VAR == None:
            files = os.scandir(dirname)
            for f in files:
                f_stat = f.stat()
                size = convert_size(f_stat.st_size)
                if f.is_dir():
                    if HIDDEN == False:
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
                    if HIDDEN == False:
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
            FTP_VAR.cwd(dirname)
            try:
                for f in FTP_VAR.mlsd():
                    if f[1]["type"] == "dir":
                        dirs_list.append([f[0], "dir", f"{orig_dirname}/{f[0]}", "▓ "])
                    elif f[1]["type"] == "file":
                        size = convert_size(int(f[1]["size"]))
                        files_list.append([f[0], size[0], f"{orig_dirname}/{f[0]}", "▓ ", size[1]])
            except:
                FTP_VAR.voidcmd('TYPE I')
                for f in FTP_VAR.nlst():
                    try:
                        if "." in f and not f.startswith("."):
                            size = convert_size(FTP_VAR.size(f))
                            files_list.append([f, size[0], f"{orig_dirname}/{f}", "▓ ", size[1]])    
                        else:
                            dirs_list.append([f, "dir", f"{orig_dirname}/{f}", "▓ "])
                    except:
                        dirs_list.append([f, "dir", f"{orig_dirname}/{f}", "▓ "])
        # Sorting
        dirs_list.sort(key=lambda f: f[0], reverse=REVERSE)
        files_list.sort(key=lambda f: f[4] if SORT == "size" else f[0], reverse=REVERSE)
        # Add new data
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
        LAST_DIR.clear()
        count = 0
        for i in dirs_list:
            if show_all_size:
                size = convert_size(check_dir_size(i[2]))
                LAST_DIR.append([i[0], f"{size[0]}", i[2], i[3], "dir"])
            else:
                LAST_DIR.append([i[0], "dir", i[2], i[3], "dir"]) # name, size, path, icon, type
            count += 1
        for i in files_list:
            LAST_DIR.append([i[0], f"{i[1]}", i[2], i[3], "file"])
            count += 1
        #
        LAST_PATH = dirname if FTP_VAR == None else FTP_VAR.pwd()
        print_interface()
    except Exception as e:
        print(str(e))


def run_app():
    global SORT
    global REVERSE
    global HIDDEN
    # Add disks
    global DISKS
    DISKS.clear()
    if sys.platform == "win32":
        letters = string.ascii_uppercase
        letter_c = 0
        column = 2
        for _ in range(26):
            disk = letters[letter_c]
            if os.path.exists(f"{disk}:{SLASH}"):
                DISKS.append(disk.lower())
                column += 1
            letter_c += 1
    if sys.platform == "linux":
        column = 2
        os_user = HOME_PATH.rsplit(SLASH, 1)[1]
        if os.path.exists(f"/media/{os_user}/"):
            for l_disk in os.listdir(f"/media/{os_user}/"):
                DISKS.append((l_disk, os_user))
                column += 1
    #
    update_files(HOME_PATH)

    # Main loop
    while True:
        input1 = input("«help» for FAQ > ").split(" ", 1)

        if len(input1) == 1:
            if SLASH in input1[0] or OP_SLASH in input1[0]:
                update_files(input1[0])
            elif input1[0] == "exit":
                if sys.platform == "win32":
                    os.system("cls")
                else:
                    os.system("clear")
                break
            elif input1[0] == "..":
                move_up()
            elif input1[0] == "paste" and FTP_VAR == None:
                paste()
            elif input1[0] == ".":
                update_files(HOME_PATH)
            elif input1[0] == "hidden":
                HIDDEN = True if HIDDEN == False else False
                update_files(f"{URL_FTP}{LAST_PATH}" if FTP_VAR != None else LAST_PATH)
            elif input1[0] == "sort":
                REVERSE = False if REVERSE == True else True
                update_files(f"{URL_FTP}{LAST_PATH}" if FTP_VAR != None else LAST_PATH)
            elif input1[0] == "help":
                print()
                print("- up: «..»")
                print("- open: «12», «documents», «c:\\users», «/home», «ftp://ftp.us.debian.org»")
                print("- home path: «.»")
                print("- copy,rename,delete: «copy 11», «delete 2,10»")
                print("- ftp download: «download 11», «download 12,14»")
                print("- show size: «size 9», «size»")
                print("- select page: «page 3»")
                print("- disks: «disk C», «disk disk 2»")
                print("- create: «dir Pictures», «file readme.txt»")
                print("- sorting: «sort»(for ↑↓), «sort name», «sort size»")
                print("- exercute cli command: «code dir», «code ls»")
                print("- «exit», «paste», «hidden»")
                print()
            elif input1[0] == "size":
                if FTP_VAR == None:
                    print(f"This action calculates the sizes for all folders.")
                    new_input = input(f"This may take a long time. Proceed (y/n)? > ")
                    if new_input == "y":
                        update_files(LAST_PATH, True)
            else:
                click(input1[0])

        elif len(input1) == 2:
            if input1[0] == "disk":
                if sys.platform == "win32":
                    update_files(f"{input1[1].upper()}:{SLASH}")
                elif sys.platform == "linux":
                    for d in DISKS:
                        if input1[1].lower() in d[0].lower():
                            update_files(f"/media/{d[1]}/{d[0]}")
            elif input1[0] == "sort":
                SORT = "size" if input1[1] == "size" else "name"
                update_files(f"{URL_FTP}{LAST_PATH}" if FTP_VAR != None else LAST_PATH)
            elif input1[0] == "page":
                print_interface(input1[1])

            elif FTP_VAR == None:
                if input1[0] == "copy":
                    operations(input1[1], "copy")
                elif input1[0] == "delete":
                    operations(input1[1], "delete")
                elif input1[0] == "rename":
                    operations(input1[1], "rename")
                elif input1[0] == "dir" or input1[0] == "file":
                    test = True
                    for f in LAST_DIR:
                        if f[0].strip().lower() == input1[1].lower():
                            test = False
                    if test == True:
                        path = os.path.join(LAST_PATH, input1[1])
                        if input1[0] == "dir":
                            os.mkdir(path)
                        elif input1[0] == "file":
                            Path(path).touch()
                        update_files(f"{URL_FTP}{LAST_PATH}" if FTP_VAR != None else LAST_PATH)
                    else:
                        print("Name is taken")
                elif input1[0] == "size":
                    calc_show_size(input1[1])
                # Test CL commands support
                elif input1[0] == "code":
                    os.chdir(LAST_PATH)
                    try:
                        msg = subprocess.getoutput(input1[1])
                        print()
                        print(msg)
                        print()
                    except:
                        subprocess.call(input1[1], creationflags=subprocess.CREATE_NEW_CONSOLE)

            elif FTP_VAR != None:
                if input1[0] == "download":
                    operations(input1[1], "download")


# VARIABLES
HOME_PATH = str(Path.home())
HIDDEN = False
SORT = "name"
REVERSE = False
LAST_PATH = None
NON_WIN_CLIPBOARD = None
SLASH = "\\" if sys.platform == "win32" else "/"
OP_SLASH = "/" if sys.platform == "win32" else "\\"
LAST_DIR = []
FTP_VAR = None
URL_FTP = None
DISKS = []


# START
if __name__=="__main__":
    run_app()