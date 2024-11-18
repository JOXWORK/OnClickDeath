import psutil, time, ctypes, datetime
from ctypes import wintypes
from os import makedirs

def main():
    wait_time = 10
    close_time = 4

    def kill_process(process):
        print("Process found, trying to kill...\n")
        try:
            process.kill()
        except:
            print("Failed")
        time.sleep(1)
        if psutil.pid_exists(process.pid) == False:
            print("Successful process kill :)")
            print("Closing by {} second(s)".format(close_time))
            print("Программа закроется через {} секунд(у/ы)".format(close_time))

            return True
        else:
            print("Sorry, failed to kill the process :(")
            print("Closing by {} second(s)".format(close_time))
            print("Программа закроется через {} секунд(у/ы)".format(close_time))

            return False

    def create_log(process, process_name, process_exe, status):
        makedirs("./ocd_log", exist_ok=True)

        time_at = str(datetime.datetime.now())
        file_name = process_name + "_" + time_at
        symbols_to_remove = ":-."
        symbols_replace = "_"
        for symbol in symbols_to_remove:
            file_name = file_name.replace(symbol, symbols_replace)

        with open("./ocd_log/" + file_name + ".txt", "w") as file:
            file.write(file_name + "\n")
            file.write(str(process) + "\n")
            file.write("Path: " + process_exe + "\n")
            file.write("Successful: {}".format(str(status)) + "\n")
            file.write("wait_time: {}".format(str(wait_time)) + "\n")
            file.write("close_time: {}".format(str(close_time)) + "\n")

    print("JOXWORK")
    print("Press on the window and wait {} second(s)".format(wait_time))
    print("Нажми на окно и подожди {} секунд(у/ы) \n".format(wait_time))
    time.sleep(wait_time)

    pid = wintypes.DWORD()
    active = ctypes.windll.user32.GetForegroundWindow()
    print("Window descriptor:", active)
    active_window = ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
    pid = pid.value
    print("Thread id:", active_window)
    print("Process id:", pid, "\n")

    for process in psutil.process_iter():
        if process.pid == pid:
            process_name = process.name()
            process_exe = process.exe()
            status = kill_process(process)
            create_log(process, process_name, process_exe, status)
            time.sleep(close_time)

if __name__ == "__main__":
    main()