# Files
A simple python file explorer with PySimpleGUI and Tkinter interfaces. Features:
- copy, paste, delete to trash and rename (files, catalogs)
- copy/paste to/from another file manager (only Tkinter windows version)
- sorts by name (files, catalogs) and size (files)
- shows hidden files
- resizability
- open files by default program (only Tkinter version)

PySimpleGUI linux version (files.py):

<img src="https://github.com/lestec-al/files/raw/main/data/pic_1.png" width="541" height="366" />
<img src="https://github.com/lestec-al/files/raw/main/data/pic_31.png" width="541" height="366" />

Tkinter linux version (files_tk.py):

<img src="https://github.com/lestec-al/files/raw/main/data/pic_files_tk_1.png" width="541" height="366" />
<img src="https://github.com/lestec-al/files/raw/main/data/pic_files_tk_3.png" width="541" height="366" />

Tkinter windows version (files_tk_win.py):

<img src="https://github.com/lestec-al/files/raw/main/data/pic_files_tk_win.png" width="497" height="330" />

You need:
- install Python (v3.9 or higher)
- install PySimpleGUI (https://pysimplegui.readthedocs.io/en/latest/#installing-pysimplegui)
- install Tkinter (https://tkdocs.com/tutorial/install.html)
- install Send2Trash (https://pypi.org/project/Send2Trash/)
- download this project and extract
- launch via command line "python files.py" (or "files_tk.py" or "files_tk_win.py") in the project folder
- optional, you can make executable file for different OS, if use "pyinstaller" (https://pyinstaller.readthedocs.io/en/stable/installation.html)