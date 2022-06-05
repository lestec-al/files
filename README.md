# Files
A simple python file explorer with Tkinter and PySimpleGUI interfaces. Features:
- copy, paste, delete to trash and rename (files, catalogs)
- sorts by name (files, catalogs) and size (files)
- shows hidden files
- resizability
- open files by default program (only Tkinter)
- local disks buttons (only Tkinter)
- keyboard navigation, copy/paste support (arrows, enter, backspace, ctrl-c/ctrl-v, only Tkinter)
- select multiple files/catalogs by holding Ctrl and clicking with the mouse (works with bugs, only Tkinter)
- copy/paste to/from another file manager (only on Windows)

Tkinter ver (files_new.py) works on Windows, Linux (should work on MacOS, but not tested). Screenshots from Windows 10 and Linux Ubuntu 20.04:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_new_win.png" width="541" height="366"/>
<img src="https://github.com/lestec-al/files/raw/main/data/pic_new_linux.png" width="541" height="366"/>

PySimpleGUI ver (files_old.py) works on Linux (should work on MacOS, but not tested). Screenshot from Linux Ubuntu 20.04:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_old_linux.png" width="541" height="366"/>

If you on Windows 10, download "files.7z" from "Releases", unpack and lanch files.exe from catalog, should work. For others:
- install Python (v3.9 or higher)
- install Tkinter (https://tkdocs.com/tutorial/install.html) or PySimpleGUI (https://pysimplegui.readthedocs.io/en/latest/#installing-pysimplegui)
- install Send2Trash (https://pypi.org/project/Send2Trash/)
- download (and extract) or clone this repo
- launch via command line "python files_new.py" in the project folder
- optional, you can make executable file for different OS, if use "pyinstaller" (https://pyinstaller.readthedocs.io/en/stable/installation.html)