# Files
A simple python file explorer with PySimpleGUI and Tkinter interfaces. Features:
- copy, paste, delete to trash and rename (files, catalogs)
- sorts by name (files, catalogs) and size (files)
- shows hidden files
- resizability
- open files by default program (only Tkinter ver)
- disks buttons (only Tkinter ver)
- keyboard navigation (arrows, enter, backspace) support (only Tkinter ver)
- copy/paste to/from another file manager (only on Windows)

Tkinter ver (files_new.py) works only on Windows or Linux Ubuntu-based distros. Screenshots from Windows 10 and Linux Ubuntu 20.04:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_tk_win_1.png" width="541" height="366"/>
<img src="https://github.com/lestec-al/files/raw/main/data/pic_tk_linux_1.png" width="541" height="366"/>

PySimpleGUI ver (files_old.py) works only on Linux Ubuntu-based distros. Screenshot from Linux Ubuntu 20.04:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_psg_linux_1.png" width="541" height="366"/>

You need:
- install Python (v3.9 or higher)
- install Tkinter (https://tkdocs.com/tutorial/install.html) or PySimpleGUI (https://pysimplegui.readthedocs.io/en/latest/#installing-pysimplegui)
- install Send2Trash (https://pypi.org/project/Send2Trash/)
- download (and extract) or clone this repo
- launch via command line "python files_new.py" in the project folder
- optional, you can make executable file for different OS, if use "pyinstaller" (https://pyinstaller.readthedocs.io/en/stable/installation.html)