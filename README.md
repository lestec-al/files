# Files
Python file explorer.

Tkinter ver (files_new.py) works on Windows, Linux (should work on MacOS). For Windows 10, version available in "Releases" (download "files.zip", unpack and run files.exe). Screenshots from Windows 10 and Linux Ubuntu:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_new_win.png" width="541" height="366"/>
<img src="https://github.com/lestec-al/files/raw/main/data/pic_new_linux.png" width="541" height="366"/>

Command line ver (files_cl.py) works on Windows, Linux (should work on MacOS). Screenshots from Windows 10 and Linux Ubuntu:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_cl_win.png" width="541" height="366"/>
<img src="https://github.com/lestec-al/files/raw/main/data/pic_cl_linux.png" width="541" height="366"/>

Kivy ver (files_kivy.py) works on Windows, Linux (should work on MacOS), Android (after compilation via buildozer). For Android, version available in "Releases" (download "files.apk" and install on device). Screenshot from Windows 10:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_kivy_win.png" width="541" height="366"/>

PySimpleGUI ver (files_old.py) works on Linux (should work on MacOS). Screenshot from Linux Ubuntu:

<img src="https://github.com/lestec-al/files/raw/main/data/pic_old_linux.png" width="541" height="366"/>


# Install and run as Python script
- install: Python (v3.9 or higher); Tkinter or Kivy and KivyMD or PySimpleGUI (depending on version); Send2Trash (needed for Tkinter, PySimpleGUI versions)
- download or clone this repo and in the project folder run via command line "python files_new.py" (files_cl.py, files_kivy.py, files_old.py)


# Features
- copy, paste, rename, delete to trash (files, catalogs) + in command line ver remove (to trash), delete (permanently)
- sorts by name (files, catalogs) and size (files)
- shows hidden files
- resizability
- catalog, files creation (only Tkinter and Command line)
- open files by default program (only Tkinter and Command line)
- local disks buttons (only Tkinter)
- keyboard navigation, copy/paste support (arrows, enter, backspace, ctrl-c/ctrl-v, only Tkinter)
- select multiple files/catalogs by holding Ctrl and clicking with the mouse (bugs, only Tkinter)
- copy/paste to/from another file manager (only Windows and Tkinter)
- the command line ver has navigation by typing short commands