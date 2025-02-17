import psutil, ctypes, mouse, keyboard, time, threading, datetime, os
from ctypes import wintypes

#OnClickDeath
class ocd():
    def __init__(self, time_callback, time_refresh):
        self.time_callback = time_callback
        self.time_refresh = time_refresh
        self.__terminate_list = ["default", "test_", "thread_test"]
        self.__terminate = None
        self.log_path = "./ocd_log"
        self.__mode_logs = []
        self.enabled_list = []
        self.trigger_path = "./ocd_trigger.txt"
        self.__trigger_list = ("left", "middle", "right") #mouse
        self._ocd__trigger_import_set()

        self._mode_watcher()
        self._ocd__log_init()

        '''
            time_callback - the time in seconds used for the "pause" required to complete a process in a program without errors
            time_refresh - the time in seconds used for update parameters required for adjust loops "while"
            __terminate_list - the list containing names of mode subject to termination
            __terminate - variable containing the value for the "terminator" configuration module
            log_path - the path of the log dir
            __mode_logs - the list containing logs of terminated programs
            enabled_list - the list containing enabled modes
            trigger_path - the path of trigger (mouse)
            __trigger_list - the list of available triggers (mouse)
            
            __terminate - takes on value containing in __terminate_list. this is a flag, which shows mode subhect to removal
        '''

    #test function
    def test(self):
        return threading.enumerate()

    #log functions
        #protected
    def __mode_log_create(self, name, mode_name, pid, path, success, time_at): #creates log of closed program
        dir_name = self.log_path + "/" + os.path.splitext(name)[0]
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        mode_dict = {}
        mode_dict["process_name"] = name
        mode_dict["mode_name"] = mode_name
        mode_dict["process_obj"] = pid
        mode_dict["process_path"] = path
        mode_dict["successfull_terminate"] = success
        mode_dict["time_at"] = time_at

        self.__mode_logs.append(mode_dict)

        save_name = mode_dict["process_name"] + "_" + mode_dict["time_at"]
        for symbol in ":-,":
            save_name = save_name.replace(symbol, "_")
        with open(dir_name + "/" + save_name + ".txt", "w") as file:
            file.write("{\n")
            for key in mode_dict:
                file.write("    " + str(key) + ": " + str(mode_dict[key]) + ",\n")
            file.write("}")

    def mode_logs(self): #method returns list with logs
        return self.__mode_logs

        #protected
    def __log_init(self): #every time when program starts check up directory for logs (./ocd_log)
        if not os.path.isdir(self.log_path):
            os.makedirs(self.log_path)

    #enabled mode list
    def enabled(self): #method returns all enabled modes
        return self.enabled_list

    #callback functions
        #protected
    def __callback(self): #code execution hangs in a special thread
        time.sleep(self.time_callback)

    def callback_time(self): #method returns callback time
        return self.time_callback

    def callback_test(self): # :)
        self._ocd__callback()
        print("callback")

    #terminator
        #protected
    def __terminator(self, name): #terminator module manage threads. this protected method, which directly adjust thread
        if self.__terminate:
            for l in self.__terminate_list:
                if l == name == self.__terminate or self.__terminate == "all":
                    return True
    #if you want to see it in action, look down (default mode)

    #!
    def terminator(self, name): #external method returns
        if name == "all":
            self.__terminate = "all"
            self._ocd__callback()
            self.__terminate = None
        elif name in self.__terminate_list:
            self.__terminate = name
            self._ocd__callback()
            self.__terminate = None

    def terminate_value(self):
        return self.__terminate

    #refresh_time functions
    def __refresh(self):
        time.sleep(self.time_refresh)

    def refresh_time(self):
        return self.time_refresh

    def refresh_test(self):
        for i in range(10):
            print(i)
            self._ocd__refresh()

    # trigger functions
    def trigger_set(self, new_trigger):
        if new_trigger in self.__trigger_list:
            try:
                with open(self.trigger_path, "w") as file:
                    file.write(new_trigger)
            except:
                return "trigger_set cant write file"
            self.trigger = new_trigger
            return "trigger successfully installed"
        else:
            return "trigger name not found"

    def trigger_key(self):
        return self.trigger

    def __trigger_import_set(self):
        if os.path.exists(self.trigger_path):
            try:
                with open(self.trigger_path, "r") as file:
                    line = file.read()
                    if line in self.__trigger_list:
                        self.trigger = line
                    else:
                        self.trigger = "middle"
            except:
                return "__trigger_import_set err"
        else:
            self.trigger = "middle"

    #determine active window function
        #protected
    def __active_window(self):
        pid = wintypes.DWORD()
        active = ctypes.windll.user32.GetForegroundWindow()
        active_window = ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
        pid = pid.value

        for process in psutil.process_iter():
            if process.pid == pid:
                return process

    #kill process function
        #protected
    def __kill_process(self, process):
        try:
            process.kill()
            return True
        except Exception as err:
            return err

    #click death functions
    #!
    def mode_default(self):
        mode_name = "default"
        def default():
            while True:
                if self._ocd__terminator(mode_name):
                    break

                if mouse.is_pressed(self.trigger):
                    process = self._ocd__active_window()
                    process_name = process.name()
                    process_exe = process.exe()

                    status = self._ocd__kill_process(process)

                    self._ocd__mode_log_create(process_name, mode_name, process, process_exe.replace("\\", "/"), status, str(datetime.datetime.now()))
                    self._ocd__callback()

                self._ocd__refresh()
        thread = threading.Thread(target=default)
        thread.start()

    def _mode_watcher(self):
        def _mode_watcher_():
            threads_count = 0
            while True:
                if not threading.main_thread().is_alive():
                    self.__terminate = "all"
                    break
                else:
                    try:
                        if threads_count != threading.active_count():
                            threads_count = threading.active_count()
                            self.enabled_list.clear()
                            for thread in threading.enumerate(): #идея: не преобразовывать имя потока, а подогонать название режима под шаблон имени потока
                                splited_name = thread.name.split(" ")
                                if len(splited_name) > 1:
                                    thread_name = splited_name[1].strip("()")
                                    if thread_name in self.__terminate_list:
                                        self.enabled_list.append(thread_name)
                    except Exception as err:
                        print(err)

                self._ocd__refresh()

        thread = threading.Thread(target=_mode_watcher_)
        thread.start()

    def test_(self):
        def test_():
            while True:
                if self._ocd__terminator("test_"):
                    break

                print(1)

                time.sleep(1)

        thread = threading.Thread(target=test_)
        thread.start()

    def mode_thread_test(self):
        def thread_test():
            while True:
                if self._ocd__terminator("thread_test"):
                    break
                self._ocd__refresh()

        thread = threading.Thread(target=thread_test)
        thread.start()