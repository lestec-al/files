# Python file explorer

Tkinter version (files_new.py) works on Windows, Linux (should work on MacOS).
For Windows 10, available in "Releases" (download "files.zip", unpack and run files.exe)

<img title="Screenshot from Windows 10" src="https://github.com/lestec-al/files/raw/main/data/pic_new_win.png" width="541" height="366"/>
<img title="Screenshot from Linux Ubuntu" src="https://github.com/lestec-al/files/raw/main/data/pic_new_linux.png" width="541" height="366"/>

Command line version (files_cl.py) works on Windows, Linux (should work on MacOS)

<img title="Screenshot from Windows 10" src="https://github.com/lestec-al/files/raw/main/data/pic_cl_win.png" width="541" height="366"/>
<img title="Screenshot from Linux Ubuntu" src="https://github.com/lestec-al/files/raw/main/data/pic_cl_linux.png" width="541" height="366"/>

# Other versions

Test Kivy version (files_kivy.py) works on Windows, Linux (should work on MacOS), Android (after compilation via buildozer).
For Android, available in "Releases" (download "files.apk" and install on device)

<img title="Screenshot from Windows 10" src="https://github.com/lestec-al/files/raw/main/data/pic_kivy_win.png" width="541" height="366"/>

Obsolete PySimpleGUI version (files_old.py) works on Linux (should work on MacOS).

<img title="Screenshot from Linux Ubuntu" src="https://github.com/lestec-al/files/raw/main/data/pic_old_linux.png" width="541" height="366"/>


# Install and run as Python script
- install: Python (v3.9 or higher)
- depending on the version install: Tkinter or Kivy (+KivyMD) or PySimpleGUI
- install Send2Trash (needed for Tkinter, PySimpleGUI versions)
- download or clone this repo and in the project folder run via command line "python files_new.py" (files_cl.py, files_kivy.py, files_old.py)


# Features
- connect to ftp servers (e.g. ftp://ftp.us.debian.org) and download files from there (tkinter, command line)
- copy/paste to/from another file manager (windows, tkinter, command line)
- catalog, files creation (tkinter, kivy, command line)
- open files by default program (tkinter, command line)
- local disks buttons (tkinter)
- keyboard navigation, copy/paste support (arrows, enter, backspace, ctrl-c/ctrl-v, tkinter)
- select multiple files/catalogs by holding Ctrl and clicking with the mouse (tkinter)
- copy, paste, rename, delete to trash (in command line ver: remove to trash, delete permanently)
- sorts by name and size
- shows hidden files
- resizability
- the command line version has navigation by typing short commands