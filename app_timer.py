import psutil
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import schedule

import time
import datetime
import logging
import atexit


class Timer:
    def __init__(self) -> None:
        self.app_dict: dict = {
            "Code.exe": [None, None],
            "pycharm64.exe": [None, None],
            "steam.exe": [None, None],
            "gameup.exe": [None, None],
            "sublime_text.exe": [None, None],
            "chrome.exe": [None, None],
        }
        self.counter = 0

        self.file_setup()
        self.app_list_cretor()
        self.python_priority_changer()

    def file_setup(self):
        with open("timerlog.csv", "a") as f:
            pass
        with open("timerlog.csv", "r") as f1:
            first_line = f1.readline()
            if first_line != "app,shamsi,miladi,sclock,eclock,stime,etime,timer,reason\n":
                lines = f1.readlines()
                lines.insert(
                    0, "app,shamsi,miladi,sclock,eclock,stime,etime,timer,reason\n")
                with open("timerlog.csv", "w") as f2:
                    for line in lines:
                        f2.write(f"{line}")

    def app_list_cretor(self):
        self.app_list = set(app for app in psutil.process_iter())
        self.app_name_list = []
        for app in self.app_list:
            self.app_name_list.append(f"{app.name()}")

    def app_list_checker(self):
        for app in self.app_dict.keys():
            if app in self.app_name_list and self.app_dict[app][0] == None:
                self.app_dict[app][0] = time.time()
            elif app not in self.app_name_list and self.app_dict[app][0] != None:
                self.app_dict[app][1] = time.time()
                self.app_exit(app=app)

    def app_exit(self, app: str):
        reason = self.reason_collector(app)
        with open("timerlog.csv", "a") as f:
            print(
                f"{app},{JalaliDate.today().isoformat()},{datetime.date.today().isoformat()},{datetime.datetime.fromtimestamp(self.app_dict[app][0]).strftime('%H:%M:%S.%f')},{datetime.datetime.fromtimestamp(self.app_dict[app][1]).strftime('%H:%M:%S.%f')},{self.app_dict[app][0]},{self.app_dict[app][1]},{int(self.app_dict[app][1]-self.app_dict[app][0])},{reason}",
                file=f
            )
        self.app_dict[app][0] = None
        self.app_dict[app][1] = None

    def python_priority_changer(self):
        for app in self.app_list:
            if app.name() == "python.exe":
                app.nice(psutil.REALTIME_PRIORITY_CLASS)

    def run(self):
        print(f"{self.counter}")
        self.app_list_cretor()
        self.app_list_checker()
        self.counter += 1

    def reason_collector(self, app):
        if app not in ["chrome.exe", "steam.exe", "gameup.exe"]:
            choice = int(
                input(f"reason for {app} :\n1- Compony\n2- MySelf\n3- Job\n4- Misc\n???"))
        elif app in ["steam.exe", "gameup.exe"]:
            choice = 5
        else:
            choice = 4

        optinos = ["Compony", "MySelf", "Job", "Misc", "Game"]
        return optinos[choice-1]


if __name__ == "__main__":
    timer = Timer()
    schedule.every(5).seconds.do(timer.run)
    
    while True:
        schedule.run_pending()
        time.sleep(1)