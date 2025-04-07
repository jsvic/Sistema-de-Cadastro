from cx_Freeze import setup, Executable
  

executables = [Executable("main.py", base= 'Win32GUI', icon= 'img/logo.ico')]

packages = ["tkinter","tkinter.filedialog","tkinter.messagebox", "PIL", "tkcalendar", "datetime", "sqlite3", "shutil", "os", "user"]
include_files = ["img/", "database.db","newBD.py", "root.py", "user.py"]

options = {
    'build_exe': {

        'packages':packages,
        'include_files' : include_files,
    },

}

setup(
    name = "Sistema de Cadastro",
    options = options,
    version = "1.0",
    description = 'Software para auxiliar no gerenciamento de agência',
    executables = executables
)