import psutil
import time
import datetime
import logging
import schedule
import atexit

class Timer:
    def __init__(self) -> None:
        self.app_dict: dict = {
            "code": [None, None],
            "pycharm64": [None, None],
            "steam": [None, None],
            "gameup": [None, None],
            "sublime_text": [None, None],
            "chrome": [None, None],
        }


    def app_list_checker(self):
        self.app_list = psutil.pids()
        print(self.app_list[0])

    def reason(self, app):
        pass


if __name__ == "__main__":
    timer = Timer()
    timer.app_list_checker()