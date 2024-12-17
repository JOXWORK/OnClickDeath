# JOXWORK

> ## Контакты / Contacts
>>**GitHub** https://github.com/JOXWORK <br> **Discord** https://discord.gg/aENbZjuu3W

> ## Общее
>>### RU
>>Привет, меня зовут JOX (Джокс). Программа OnClickDeath (OCD) доступна для скачивания и редактирования совершенно бесплатно! Однако, не делай никаких криминальных вещей, нарушающих законы Российской Федерации и США. Если ты изменил программу и распространяешь её изменённую версию, то прошу указать меня как первоначального создателя. Не забывай скачивать программу с официального GitHub или Дискорд сервера!
>
>>### EN
>>Hello, I'm JOX. You can use this program for free! You can edit the program, but don't do anything criminal things please. If you edit or redact program and you distribute your version, then indicate me as the creator of the program. Don't forget to download program from oficial GitHub or Discord server!

> ## Описание программы
>>Программа называется OnClickDeath (OCD), она предназначена для прерывания процессов (закрытия) программ. OCD написана на `python3`, использует библиотеку `psutil` в качестве основного инструмента управления состоянием программ. OCD не умеет отличать условно неважный процесс операционной системы от условного важного процесса (paint.exe и explorer.exe например). По вышеуказанной причине, я советую быть осторожным при использовании программы и запускать её только по мере необходимости.

> ## Техническая часть
>>Программа использует библиотеки `psutil, time, ctypes, datetime, os`. Новая версия использует `psutil, ctypes, mouse, time, threading`. (Здесь указаны основные библиотеки). Информация о версиях библиотек и версии `python` смотрите выше в файле. Помимо библиотек OCD использует dll windows для индетификации приоритетного окна: `user32.dll`. 

> ## Совместимость
>>OCD создана для работы с операционной системой Windows 10 и выше. На Windows 7 программа не работает из-за отсутсвтия некоторых библиотек (возможно если их скачать, то всё будет работать). К сожелению нету возможности протестировать программу на операционных системах на базе ядра Linux.

> ## Исходный код первой версии / Source code of the first version
```python
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
```
