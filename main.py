from core import *

def main():
    main = ocd(1, 0.1) #OnClickDeath
    print("JOXWORK\n")
    print("Нажми на среднюю кнопку мыши (по умолчанию), чтобы закрыть выбранную программу")
    print("Press middle mouse button (default) to close selected program")

    main.mode_default() #runs every time program start

    def logs():
        print(main.mode_logs())

    commands = {
        "mode_default": main.mode_default,
        "mode_test_": main.test_,
        "mode_thread_test": main.mode_thread_test,
        "test": lambda: print(main.test()),
        "refresh_test": main.refresh_test,
        "callback_test": main.callback_test,
        "terminate_value": lambda: print(main.terminate_value()),
        "enabled": lambda: print(main.enabled()),
        "refresh_time": lambda: print(main.refresh_time()),
        "callback_time": lambda: print(main.callback_time()),
        "trigger_key": lambda: print(main.trigger_key()),
        "logs": logs
    }

    help_list1 = [
        "enable default mode (click for kill)",
        "enable test mode (dev func)",
        "enable thread test (dev func)",
        "return enumerated threads",
        "update rate",
        "callback delay",
        "return terminate value (module terminaot) dev",
        "return enabled modes",
        "return refresh time",
        "return callback time",
        "return trigger key (left, middle, right)",
        "return logs",
        "help"
    ]

    commands_args = {
        "terminator": main.terminator,
        "trigger_set": main.trigger_set
    }

    help_list2 = [
        "terminator [mode name] - disables mods",
        "trigger_set [left, middle, right - changes mouse trigger"
    ]

    def command_help():
        for k, command in enumerate(commands):
            print(command, "-", help_list1[k])
        print("\n")
        for k, command in enumerate(commands_args):
            print(command, "-", help_list2[k])
    commands["help"] = command_help

    while True:
        cmd = input(">>")
        args_cmd = cmd.split(" ")
        command = args_cmd[0]

        if command in commands and len(args_cmd) == 1:
            try:
                commands[command]()
            except:
                print(commands[command])
        elif command in commands_args and len(args_cmd) > 1:
            try:
                if len(args_cmd) <= 2:
                    print(args_cmd)
                    commands_args[command](args_cmd[1])
            except Exception as err:
                print(err)
        elif cmd == "stop":
            main.terminator("all")
            break
        else:
            print("Commnad not found")


if __name__ == "__main__":
    main()