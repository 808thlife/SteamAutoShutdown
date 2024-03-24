from sys import platform

def shutdown_machine(platform):
    if platform == "darwin" or platform =="posix":
        os.system('sudo shutdown now')
    elif platform == "win32" or platform == "win64":
        os.system('shutdown /s /t 0')

