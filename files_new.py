import os
import stat
import pygit2
import re
import sys
import platform
import subprocess
import string
import shutil
import configparser
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.messagebox import askyesno
from tkinter import filedialog
from pathlib import Path
from ftplib import FTP
from send2trash import send2trash

# git status dictionary
git_status_dict = {
    -1: "NOT_GIT_REPOSITORY",
    0: "UNMODIFIED",
    1: "STAGED",
    2: "STAGED",
    4: "GIT_STATUS_INDEX_DELETED",
    8: "GIT_STATUS_INDEX_RENAMED",
    16: "GIT_STATUS_INDEX_TYPECHANGE",
    128: "UNTRACKED",
    132: "UNTRACKED",
    256: "UNSTAGED",
    257: "UNSTAGED-STAGED",
    258: "UNSTAGED-STAGED",
    512: "GIT_STATUS_WT_DELETED",
    1024: "GIT_STATUS_WT_RENAMED",
    2048: "GIT_STATUS_WT_TYPECHANGE",
    4096: "GIT_STATUS_WT_UNREADABLE",
    16384: "GIT_STATUS_IGNORED",
    32768: "GIT_STATUS_CONFLICTED"
}

# icons for status [default, unstaged, staged, both]
icon_status_dict = {
    -1: 0,
    0: 0,
    1: 2,
    2: 2,
    4: 0,
    8: 0,
    16: 0,
    128: 1,
    132: 1,
    256: 1,
    257: 3,
    258: 3,
    512: 0,
    1024: 0,
    2048: 0,
    4096: 0,
    16384: 0,
    32768: 0
}


# Interface
def git_restore():
    if check_git_repo(last_path):
        repo = pygit2.Repository(last_path)
        head_commit = repo.head.peel(pygit2.Commit)
        head_tree = head_commit.tree
        relative_path = get_relative_repo_path(
            last_path, repo) + g_current_item
        tree_entry = head_tree[relative_path]
        blob_oid = tree_entry.oid
        blob = repo[blob_oid]
        file_content = blob.data
        tmp_path = last_path + "/" + g_current_item
        with open(tmp_path, "wb") as f:
            f.write(file_content)
    update_files(last_path)


def git_restore_staged():
    if check_git_repo(last_path):
        repo = pygit2.Repository(last_path)
        index = repo.index
        index.read()
        relative_path = get_relative_repo_path(
            last_path, repo) + g_current_item
        index.remove(relative_path)
        try:
            obj = repo.revparse_single(
                'HEAD').tree[relative_path]  # Get object from db
            index.add(pygit2.IndexEntry(relative_path,
                                        obj.id, obj.filemode))  # Add to inde
            index.write()
        except KeyError:
            git_rm_cached()
    update_files(last_path)


def git_rm_cached():
    if check_git_repo(last_path):
        try:
            repo = pygit2.Repository(last_path)
            repo.index.remove(get_relative_repo_path(
                last_path, repo)+g_current_item)
            repo.index.write()
        except KeyError as e:
            print("Failed to remove file: ", e)
    update_files(last_path)


def git_rm():
    if check_git_repo(last_path):
        try:
            repo = pygit2.Repository(last_path)
            tmp_path = last_path + "/" + g_current_item
            git_rm_cached()
            os.remove(tmp_path)
            repo.index.write()
        except Exception as e:
            print("Failed to remove file: ", e)
    update_files(last_path)


def git_init():
    # non-bare repository init
    if not check_git_repo(last_path):
        pygit2.init_repository(f'{last_path}/.git', False)
    update_files(last_path)


def git_add():
    if check_git_repo(last_path):
        repository = pygit2.Repository(last_path)
    index = repository.index

    if g_current_item != None:
        path = get_relative_repo_path(last_path, repository) + g_current_item
    else:
        path = None

    if path != None:
        index.add(path)
    else:
        index.add_all()
    index.write()
    update_files(last_path)


def git_commit(commit_message):
    if check_git_repo(last_path):
        repository = pygit2.Repository(last_path)
    index = repository.index
    config = repository.config
    for name in config.get_multivar('user.name'):
        user_name = name
    for email in config.get_multivar('user.email'):
        user_email = email
    author = pygit2.Signature(user_name, user_email)
    committer = pygit2.Signature(user_name, user_email)
    tree = index.write_tree()
    ref = repository.head.name
    parents = [repository.head.target]

    repository.create_commit(
        ref,
        author, committer, commit_message,
        tree,
        parents
    )
    update_files(last_path)


def git_mv(new_file_name):
    if check_git_repo(last_path):
        repository = pygit2.Repository(last_path)
        index = repository.index
        old_file_name = g_current_item
        old_path = f'{last_path}/{old_file_name}'
        new_path = f'{last_path}/{new_file_name}'
        index.remove(old_file_name)
        os.rename(old_path, new_path)
        index.add(new_file_name)
        index.write()

        update_files(last_path)


def update_file_git_status(path, file_name):
    if check_git_repo(path):
        repository = pygit2.Repository(path)
        status = repository.status_file(file_name)
    else:
        return 0
    return status


# cur_directory_path 현재 접근한 디렉토리정보(아마 last_path), repo 객체를 넣으면 하위폴더에 대한
# 상대 경로를 반환함. 만약 .git 폴더가 있는 폴더면 반환값은 '' 이며 하위 폴더의 경우 상대경로 + '/'를 반환
# 전달 받은 relative_path와 파일명을 결합하여 사용
def get_relative_repo_path(cur_directory_path, repo):
    repo_dir = cur_directory_path
    repo_dir = repo_dir[(len(repo.path) - 5):]
    if not repo_dir:
        return ''
    else:
        return repo_dir + '/'


def check_git_repo(path):
    try:
        # 디렉토리가 Git 저장소인지 확인 레포가 만들어지면 init 불가능
        repo = pygit2.Repository(path)
    except pygit2.GitError:
        return False
    return True


def update_git_repo(path):
    try:
        # 디렉토리가 Git 저장소인지 확인 레포가 만들어지면 init 불가능
        repo = pygit2.Repository(path)

    except pygit2.GitError:
        return False, pygit2.Repository()

    return True, repo


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
                          command=lambda disk=disk: update_files(f"{disk}:{slash}")).grid(column=column, row=1)
                column += 1
            letter_c += 1
    if sys.platform == "linux":
        column = 2
        os_user = home_path.rsplit(slash, 1)[1]
        if os.path.exists(f"/media/{os_user}/"):
            for l_disk in os.listdir(f"/media/{os_user}/"):
                tk.Button(frame_b, text=l_disk[0].lower(), font=("Arial", 14), relief="flat", bg="white", fg="black",
                          command=lambda l_disk=l_disk: update_files(f"/media/{os_user}/{l_disk}")).grid(column=column,
                                                                                                         row=1)
                column += 1


def up_down_focus():
    """Focus item on start"""
    if tree.focus() == "":
        try:
            item = tree.get_children()[0]
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
        except:
            pass


def select():
    global g_current_item
    for x in buttons:
        x.config(state="normal")
    try:
        select_row = tree.focus()
        row_data = tree.item(select_row)
        g_current_item = row_data["text"]
        if not tree.selection():
            g_current_item = ''
            for x in buttons:
                if check_git_repo(last_path):
                    if x == add_button:
                        continue
                    else:
                        x.config(state="disabled")
                else:
                    if x == init_button:
                        continue
                    else:
                        x.config(state="disabled")

        current_git_status = row_data["values"][1]
        folder_status = row_data["values"][0]
        if check_git_repo(last_path):
            if folder_status == 'dir':
                for x in buttons:
                    if x != add_button:
                        x.config(state="disabled")
            else:
                try:
                    if current_git_status == "STAGED":
                        for x in buttons:
                            if x == commit_button or x == restore_staged_button or x == rm_cached_button or x == mv_button:
                                continue
                            else:
                                x.config(state="disabled")

                    elif current_git_status == "UNMODIFIED":
                        for x in buttons:
                            if x == rm_button or x == rm_cached_button or x == mv_button or x == commit_button:
                                continue
                            else:
                                x.config(state="disabled")
                    elif current_git_status == "UNSTAGED":
                        for x in buttons:
                            if x == add_button or x == rm_button or x == rm_cached_button or x == mv_button or x == restore_button or x == commit_button:
                                continue
                            else:
                                x.config(state="disabled")

                    elif current_git_status == "UNTRACKED":
                        for x in buttons:
                            if x == add_button:
                                continue
                            else:
                                x.config(state="disabled")
                    elif current_git_status == "UNSTAGED-STAGED":
                        init_button.config(state="disabled")
                    else:
                        print(None)
                except:
                    print("Invalid Git status code:", current_git_status)
        else:
            for x in buttons:
                if x == init_button:
                    continue
                else:
                    x.config(state="disabled")

    except IndexError:
        g_current_item = None
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
        path = tree.item(i)["values"][2]
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
            name_dir = simpledialog.askstring(
                title="Files", prompt=info_text, parent=tree_frame)
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
        clipboard = window.selection_get(
            selection="CLIPBOARD").replace("/", slash).split("\n")
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
        answer = askyesno(
            title="Files", message=f"Delete {len(tree.selection())} objects in trash?")
        if answer:
            for di in del_list:
                send2trash(di)
    except:
        pass
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
                new_name = simpledialog.askstring(
                    title="Files", prompt=info_text, parent=tree_frame, initialvalue=e_path[1])
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
        if byte_size >= 1000000000000:
            size = str(round(byte_size / 1000000000000, 2)) + " TB"
        elif byte_size >= 1000000000:
            size = str(round(byte_size / 1000000000, 2)) + " GB"
        elif byte_size >= 1000000:
            size = str(round(byte_size / 1000000, 2)) + " MB"
        elif byte_size >= 1000:
            size = str(round(byte_size / 1000, 2)) + " KB"
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
                        ftp.connect(ftp_split[0], int(ftp_split[1]))
                        url_ftp = f"ftp://{ftp_split[0]}:{ftp_split[1]}"
                    else:
                        ftp.connect(x[1])
                        url_ftp = f"ftp://{x[1]}"
                    ftp.login()
                    #
                    right_menu.add_command(
                        label="Copy to folder", command=copy_from_ftp, state="disable")
                    right_menu.entryconfig(
                        "Show hidden files", state="disable")
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
            git_repo = pygit2.Repository()
            is_repo_exist, git_repo = update_git_repo(dirname)

            for f in files:
                f_stat = f.stat()
                size = convert_size(f_stat.st_size)

                if f.is_dir():
                    # 오브젝트가 폴더이면 다음과 같은 정보들을 삽입
                    if is_repo_exist:  # if true -> cant init
                        git_status = 0  # status 0 of file is current state
                    else:  # if not exist -> can init, and flag is -1
                        git_status = -1

                    if hidden == False:
                        if sys.platform == "win32":
                            if not f.is_symlink() and not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append(
                                    [f.name, "dir", f.path, folder_icon_list[icon_status_dict[git_status]], 0,
                                     git_status_dict[git_status]])
                        else:
                            if not f.name.startswith("."):
                                dirs_list.append(
                                    [f.name, "dir", f.path, folder_icon_list[icon_status_dict[git_status]], 0,
                                     git_status_dict[git_status]])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                dirs_list.append(
                                    [f.name, "dir", f.path, folder_hidden_icon, 0, git_status_dict[git_status]])
                            else:
                                if f.is_symlink():
                                    dirs_list.append(
                                        [f.name, "dir", f.path, folder_hidden_icon, 0, git_status_dict[git_status]])
                                else:
                                    dirs_list.append(
                                        [f.name, "dir", f.path, folder_icon_list[icon_status_dict[git_status]], 0,
                                         git_status_dict[git_status]])
                        else:
                            if f.name.startswith("."):
                                dirs_list.append(
                                    [f.name, "dir", f.path, folder_hidden_icon, 0, git_status_dict[git_status]])
                            else:
                                dirs_list.append(
                                    [f.name, "dir", f.path, folder_icon_list[icon_status_dict[git_status]], 0,
                                     git_status_dict[git_status]])
                if f.is_file():
                    # 오브젝트가 파일이면 아래와 같은 정보들을 삽입
                    if is_repo_exist:  # if true -> cant init
                        repo_dir = dirname
                        repo_dir = repo_dir[(len(git_repo.path) - 5):]
                        if not repo_dir:
                            git_status = git_repo.status_file(f.name)
                        else:
                            git_status = git_repo.status_file(
                                repo_dir + '/' + f.name)

                    else:  # if not exist -> can init, and flag is
                        git_status = -1

                    if hidden == False:
                        if sys.platform == "win32":
                            if not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append(
                                    [f.name, size[0], f.path, file_icon, size[1], git_status_dict[git_status]])
                        else:
                            if not f.name.startswith("."):
                                files_list.append(
                                    [f.name, size[0], f.path, file_icon_list[icon_status_dict[git_status]], size[1],
                                     git_status_dict[git_status]])
                    else:
                        if sys.platform == "win32":
                            if bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                                files_list.append(
                                    [f.name, size[0], f.path, file_hidden_icon, size[1], git_status_dict[git_status]])
                            else:
                                files_list.append(
                                    [f.name, size[0], f.path, file_icon_list[icon_status_dict[git_status]], size[1],
                                     git_status_dict[git_status]])
                        else:
                            if f.name.startswith("."):
                                files_list.append(
                                    [f.name, size[0], f.path, file_hidden_icon, size[1], git_status_dict[git_status]])
                            else:
                                files_list.append(
                                    [f.name, size[0], f.path, file_icon_list[icon_status_dict[git_status]], size[1],
                                     git_status_dict[git_status]])
        # FTP
        else:
            ftp.cwd(dirname)
            try:
                for f in ftp.mlsd():
                    if f[1]["type"] == "dir":
                        dirs_list.append(
                            [f[0], "dir", f"{orig_dirname}/{f[0]}", folder_icon])
                    elif f[1]["type"] == "file":
                        size = convert_size(int(f[1]["size"]))
                        files_list.append(
                            [f[0], size[0], f"{orig_dirname}/{f[0]}", file_icon, size[1]])
            except:
                ftp.voidcmd('TYPE I')
                for f in ftp.nlst():
                    try:
                        if "." in f and not f.startswith("."):
                            size = convert_size(ftp.size(f))
                            files_list.append(
                                [f, size[0], f"{orig_dirname}/{f}", file_icon, size[1]])
                        else:
                            dirs_list.append(
                                [f, "dir", f"{orig_dirname}/{f}", folder_icon])
                    except:
                        dirs_list.append(
                            [f, "dir", f"{orig_dirname}/{f}", folder_icon])
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

        # [f.name, "dir", f.path, folder_icon, git_status])
        for i in dirs_list:
            tree.insert("", tk.END, text=i[0], values=[
                f"{i[1]}", i[5], i[2]], open=False, image=i[3])
            count += 1
        for i in files_list:
            tree.insert("", tk.END, text=i[0], values=[
                f"{i[1]}", i[5], i[2]], open=False, image=i[3])
            count += 1
        #
        if ftp == None:
            last_path = dirname
            entry.insert("end", dirname)
        else:
            last_path = ftp.pwd()
            entry.insert("end", f"{url_ftp}{ftp.pwd()}")
        #
        label["text"] = f"   {str(count)} objects"
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
if sys.platform == "win32" and platform.release() == "10":
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

# Ini config home path, showing hidden files + other variables
config = configparser.ConfigParser()
config.read("files.ini")
home_path = str(Path.home(
)) if config["USER SETTINGS"]["home_path"] == "" else config["USER SETTINGS"]["home_path"]
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

frame_left = tk.Frame(window, border=1, bg="white")
frame_left.pack(fill="both", side="left", expand=True)

frame_right = tk.Frame(window,  bg="white")
frame_right.pack(fill="both", side="right")


frame_up = tk.Frame(frame_left, border=1, bg="white")
frame_up.pack(fill="x", side="top")

frame_right_branch = tk.Frame(frame_right, border=1, bg="white")
frame_right_branch.pack(fill="both", side="left")
frame_right_history = tk.Frame(frame_right, border=1, bg="white")
frame_right_history.pack(fill="both", side="right")

frame_right_branch_list = tk.Frame(
    frame_right_branch, border=1, bg="red", width=300, height=500)
frame_right_branch_list.pack(side="top")
frame_right_branch_button = tk.Frame(
    frame_right_branch, border=1, bg="white", width=300, height=100)
frame_right_branch_button.pack(side="bottom")
frame_right_history_graph = tk.Frame(
    frame_right_history, border=1, bg="green", width=300, height=500)
frame_right_history_graph.grid(column=0, row=0)
frame_right_history_detail = tk.Frame(
    frame_right_history, border=1, bg="blue", width=300, height=200)
frame_right_history_detail.grid(column=0, row=1)

frame_right_branch_list


def checkout_branch():
    if check_git_repo(last_path):
        repo = pygit2.Repository(last_path)
        # TODO : 사용자에게 입력받은 브랜치로 checkout 구현 예정
        # branch = repo.branches.get('testBranch')
        # repo.checkout(branch)
        # 전환된 브랜치 확인
        # current_branch = repo.head.shorthand
        # update_files(last_path)
        branches_list = list(repo.branches)
        print(branches_list)


def get_selected_branch(listbox):
    items = listbox.curselection()
    if items:
        return listbox.get(items)
    else:
        print("not selected")


def create_branch():
    if check_git_repo(last_path):
        repo = pygit2.Repository(last_path)
        current_commit_id = repo.head.target
        print(repo.get(current_commit_id))
        branches = list(repo.branches.local)
        listbox = tk.Listbox(frame_right_branch_list)
        listbox.pack()
        for branch in branches:
            listbox.insert(tk.END, branch)

        # TODO : 사용자에게 입력받은 브랜치로 create 구현 예정
        # new_branch_name = 'new-branch'
        # new_branch = repo.create_branch(
        #     new_branch_name, repo.get(current_commit_id))
        # print(new_branch)


def delete_branch():
    if check_git_repo(last_path):
        repo = pygit2.Repository(last_path)
        # TODO : 사용자에게 입력받은 브랜치로 delete 구현 예정
        # repo.branches.delete('new-branch')
        # print('삭제')


def rename_branch():
    if check_git_repo(last_path):
        repo = pygit2.Repository(last_path)
        # TODO : 사용자에게 선택한 브랜치 rename 구현 예정
        # TODO : 사용자가 선택한 브랜치 input
        # TODO : 사용자가 변경할 브랜치 이름 input

        # selected_branch_name = 'testBranch'
        # new_name = 'rename-branch'
        # selected_branch = repo.branches[selected_branch_name]
        # selected_branch.rename(new_name)


# Frame_right_branch_butoon
branch_buttons = []
create_button = tk.Button(frame_right_branch_button, text='create', width=4, height=1, relief="flat", bg="black",
                          fg="black", command=lambda: create_branch())
create_button.grid(column=0, row=0)
branch_buttons.append(create_button)
delete_button = tk.Button(frame_right_branch_button, text='delete', width=4, height=1, relief="flat", bg="black",
                          fg="black", command=lambda: delete_branch())
delete_button.grid(column=1, row=0)
branch_buttons.append(delete_button)
rename_button = tk.Button(frame_right_branch_button, text='rename', width=4, height=1, relief="flat", bg="black",
                          fg="black", command=lambda: rename_branch())
rename_button.grid(column=2, row=0)
branch_buttons.append(rename_button)
checkout_button = tk.Button(frame_right_branch_button, text='checkout', width=4, height=1, relief="flat", bg="black",
                            fg="black", command=lambda: checkout_branch())
checkout_button.grid(column=3, row=0)
branch_buttons.append(checkout_button)
merge_button = tk.Button(frame_right_branch_button, text='merge', width=4, height=1, relief="flat", bg="black",
                         fg="black", command=lambda: update_files(last_path))
merge_button.grid(column=4, row=0)
branch_buttons.append(merge_button)

# Top of window
folder_icon_list = [tk.PhotoImage(file="data/icon_folder.png"), tk.PhotoImage(file="data/icon_folder_unstaged.png"),
                    tk.PhotoImage(file="data/icon_folder_staged.png"), tk.PhotoImage(file="data/icon_folder_both.png")]
file_icon_list = [tk.PhotoImage(file="data/icon_file.png"), tk.PhotoImage(file="data/icon_file_unstaged.png"),
                  tk.PhotoImage(file="data/icon_file_staged.png"), tk.PhotoImage(file="data/icon_file_both.png")]
file_icon = tk.PhotoImage(file="data/icon_file.png")
folder_icon = tk.PhotoImage(file="data/icon_folder.png")
folder_hidden_icon = tk.PhotoImage(file="data/icon_folder_hidden.png")
file_hidden_icon = tk.PhotoImage(file="data/icon_file_hidden.png")
home_icon = tk.PhotoImage(file="data/icon_home.png")
up_icon = tk.PhotoImage(file="data/icon_up.png")
frame_b = tk.Frame(frame_up, border=2, relief="groove", bg="white")
frame_b.pack(side="left")
tk.Button(frame_b, image=up_icon, width=25, height=32, relief="flat",
          bg="white", fg="black", command=move_up).grid(column=0, row=1)
tk.Button(frame_b, image=home_icon, width=25, height=32, relief="flat", bg="white",
          fg="black", command=lambda: update_files(home_path)).grid(column=1, row=1)


# error type을 파라미터로 받고 type에 따라 error_text 띄우기
def open_error_window(error_type):
    error_window = tk.Toplevel(window)
    error_window.title('error')
    error_window.geometry("500x50")
    error_window.geometry("+100+200")

    error_text = {
        'init': 'git init 할 수 없는 디렉토리입니다',
        'add': '추가할 파일이 없습니다',
        'commit': 'commit 할 수 있는 파일이 없습니다'
    }
    label = tk.Label(
        error_window, text=error_text[error_type])
    label.pack()
    button = tk.Button(error_window, text="확인",
                       command=lambda: (error_window.destroy()))
    button.pack()


def confirm_staged_files():
    if check_git_repo(last_path):
        repository = pygit2.Repository(last_path)
    status = repository.status()
    staged_list = []
    for file_name, flag in status.items():
        if git_status_dict[flag] == "STAGED" or git_status_dict[flag] == "UNSTAGED-STAGED":
            staged_list.append(file_name)

    if not staged_list:
        open_error_window('commit')
        return

    confirm_window = tk.Toplevel(window)
    confirm_window.title('staging files')
    confirm_window.geometry("500x200")
    confirm_window.geometry("+100+100")

    label = tk.Label(
        confirm_window, text="commit할 파일을 확인해 주세요 !")
    label.pack()

    confirm_frame = tk.Frame(confirm_window)
    confirm_frame.pack()

    listNodes = tk.Listbox(confirm_frame, width=30,
                           height=8, font=("Helvetica", 15))
    listNodes.pack(side="left", fill="y")

    scrollbar = tk.Scrollbar(confirm_frame, orient="vertical")
    scrollbar.config(command=listNodes.yview)
    scrollbar.pack(side="right", fill="y")

    listNodes.config(yscrollcommand=scrollbar.set)
    for file in staged_list:
        listNodes.insert(tk.END, file)

    button = tk.Button(confirm_window, text="확인 완료",
                       command=lambda: (open_git_commit_window(), confirm_window.destroy()))
    button.pack()


def open_git_commit_window():
    input_window = tk.Toplevel(window)
    input_window.title('commit message')
    input_window.geometry("500x100")
    input_window.geometry("+100+200")

    label = tk.Label(
        input_window, text="commit message를 입력해주세요 !")
    label.pack()
    input_entry = tk.Entry(input_window, width=30)
    input_entry.pack()
    input_entry.focus_set()
    button = tk.Button(input_window, text="commit",
                       command=lambda: (git_commit(input_entry.get()), input_window.destroy()))
    button.pack()


def open_git_mv_window():
    input_window = tk.Toplevel(window)
    input_window.title('파일명 변경')
    input_window.geometry("500x100")
    input_window.geometry("+100+200")

    label = tk.Label(
        input_window, text="변경할 이름을 입력해주세요 !")
    label.pack()
    input_entry = tk.Entry(input_window, width=30)
    input_entry.pack()
    input_entry.focus_set()
    button = tk.Button(input_window, text="rename",
                       command=lambda: (git_mv(input_entry.get()), input_window.destroy()))
    button.pack()


# git buttons
frame_down = tk.Frame(frame_left, border=1)
frame_down.pack(fill="x", side="bottom")
frame_c = tk.Frame(frame_down, relief="groove", bg="white")
frame_c.pack(side="bottom")
buttons = []
# init button
init_button = tk.Button(frame_c, text='init', width=5, height=1, relief="flat", bg="black",
                        fg="black", command=lambda: git_init())
init_button.grid(column=1, row=0)
buttons.append(init_button)
# add button
add_button = tk.Button(frame_c, text='add', width=5, height=1, relief="flat", bg="black",
                       fg="black", command=lambda: git_add())
add_button.grid(column=2, row=0)
buttons.append(add_button)
# commit button
commit_button = tk.Button(frame_c, text='commit', width=5, height=1, relief="flat", bg="black",
                          fg="black", command=lambda: confirm_staged_files())
commit_button.grid(column=3, row=0)
buttons.append(commit_button)
# git_rm button
rm_button = tk.Button(frame_c, text='rm', width=5, height=1, relief="flat", bg="black",
                      fg="black", command=lambda: git_rm())
rm_button.grid(column=4, row=0)
buttons.append(rm_button)
# git_rm_cached button
rm_cached_button = tk.Button(frame_c, text='rm --cached', width=8, height=1, relief="flat", bg="black",
                             fg="black", command=lambda: git_rm_cached())
rm_cached_button.grid(column=5, row=0)
buttons.append(rm_cached_button)
# git_restore button
restore_button = tk.Button(frame_c, text='restore', width=6, height=1, relief="flat", bg="black",
                           fg="black", command=lambda: git_restore())
restore_button.grid(column=6, row=0)
buttons.append(restore_button)
# git_restore --staged button
restore_staged_button = tk.Button(frame_c, text='restore --staged', width=10, height=1, relief="flat", bg="black",
                                  fg="black", command=lambda: git_restore_staged())
restore_staged_button.grid(column=7, row=0)
buttons.append(restore_staged_button)
# git_mv button
mv_button = tk.Button(frame_c, text='mv', width=6, height=1, relief="flat", bg="black",
                      fg="black", command=lambda: open_git_mv_window())
mv_button.grid(column=8, row=0)
buttons.append(mv_button)

entry = tk.Entry(frame_up, font=("Arial", 12), justify="left",
                 highlightcolor="white", highlightthickness=0, relief="groove", border=2)
entry.pack(side="right", fill="both", expand=1)
label = tk.Label(frame_left, font=("Arial", 12), anchor="w",
                 bg="white", foreground="grey", border=2)
label.pack(side="bottom", fill="both")

# Git Status Icon file
git_temp_icon = tk.PhotoImage(file="data/git_logo.png")

# Tree view
tree_frame = tk.Frame(frame_left, border=1, relief="flat", bg="white")
tree_frame.pack(expand=1, fill="both")
tree = ttk.Treeview(tree_frame, columns=(
    ["#1", "#2"]), selectmode="extended", show="tree headings", style="mystyle.Treeview")
tree.heading("#0", text="   Name ↑", anchor="w", command=sort_name_reverse)
tree.heading("#1", text="Size", anchor="w", command=sort_size_reverse)
tree.heading("#2", text="Git_status", anchor="w")  # 새로운 git status 칼럼 헤더 추가
tree.column("#0", anchor="w")
tree.column("#1", anchor="e", stretch=False, width=120)
tree.column("#2", anchor="center", width=80)  # 새로운 git status 칼럼
tree.pack(side="left", expand=1, fill="both")
style = ttk.Style()
style.configure("Treeview", rowheight=40, font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 12), foreground="grey")
style.layout("mystyle.Treeview", [
    ("mystyle.Treeview.treearea", {"sticky": "nswe"})])
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

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
right_menu.add_command(label="Delete in trash",
                       command=delete, state="disabled")
right_menu.add_separator()
right_menu.add_command(label="Paste", command=paste, state="disabled")
right_menu.add_separator()
right_menu.add_command(
    label="New file", command=lambda: new("file"), state="normal")
right_menu.add_command(label="New catalog",
                       command=lambda: new("dir"), state="normal")
right_menu.add_separator()
right_menu.add_checkbutton(label="Show hidden files", onvalue=1,
                           offvalue=0, variable=hidden_menu, command=show_hide)
# Click elsewhere - close right click menu
right_menu.bind("<FocusOut>", lambda event: right_menu.unpost())
scan_disks_add_buttons()
update_files(home_path)
tree.focus_set()

# Keyboard, mouse buttons
tree.bind("<<TreeviewSelect>>", lambda event: select())
tree.bind("<Double-Button-1>", lambda event: click())
tree.bind("<Button-1>", lambda event: remove_selection())
tree.bind("<Return>", lambda event: click())
tree.bind("<BackSpace>", lambda event: move_up())
tree.bind("<Button-3>", open_right_menu)
tree.bind("<Up>", lambda event: up_down_focus())
tree.bind("<Down>", lambda event: up_down_focus())
tree.bind("<Delete>", lambda event: delete())
tree.bind("<Control-c>", lambda event: copy())
tree.bind("<Control-v>", lambda event: paste()
          if right_menu.entrycget(index=5, option="state") == "normal" else None)
entry.bind("<Return>", lambda event: update_files(entry.get()))
entry.bind("<KP_Enter>", lambda event: update_files(entry.get()))
window.mainloop()
