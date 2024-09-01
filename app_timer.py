import psutil
import time
import datetime
import logging
import scheduler
import atexit

vscode_start_time = None
pycharm_start_time = None
sublime_start_time = None
steam_start_time = None
GameUP_start_time = None

# Create and configure logger
logging.basicConfig(filename="coding_timer.csv",
                    format='%(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

with open("coding_timer.csv", "r") as x:
    if len(x.readline()) < 1:
        logger.info("date,clock,app,stime,etime,timer,reason")


def csv_write(*, appname, stime, etime, reason):
    logger.info(
        f"{datetime.datetime.now().date()},{datetime.datetime.now().time()},{appname},{stime},{etime},{etime-stime},{reason}")


# set app priority on realtime
processes = set(process for process in psutil.process_iter())
for process in processes:
    if process.name() == "python.exe":
        process.nice(psutil.REALTIME_PRIORITY_CLASS)


def reason_selector(app_name):
    option = int(
        input(f"{app_name} usage reason:\n1-compony\n2-job\n3-onmyway\n4-game\t"))
    if option == 1:
        reason = "compony"
    elif option == 2:
        reason = "job"
    elif option == 3:
        reason = "onmyway"
    elif option == 4:
        reason = "game"
    else:
        reason = "test"
    return reason


def main():
    global vscode_start_time, pycharm_start_time, sublime_start_time, GameUP_start_time, steam_start_time, counter
    names = set(process.name() for process in psutil.process_iter())

    # vscode usage
    if 'Code.exe' in names and vscode_start_time == None:
        vscode_start_time = int(time.time())

    if 'Code.exe' not in names and vscode_start_time != None:
        vscode_end_time = int(time.time())
        reason = reason_selector("VsCode")
        csv_write(appname="Vscode", stime=vscode_start_time,
                  etime=vscode_end_time, reason=reason)
        vscode_start_time = None

    # pycharm usage
    if 'pycharm64.exe' in names and pycharm_start_time == None:
        pycharm_start_time = int(time.time())

    if 'pycharm64.exe' not in names and pycharm_start_time != None:
        pycharm_end_time = int(time.time())
        reason = reason_selector("Pycharm")
        csv_write(appname="Pycharm", stime=pycharm_start_time,
                  etime=pycharm_end_time, reason=reason)
        pycharm_start_time = None

    # sublime usage
    if 'sublime_text.exe' in names and sublime_start_time == None:
        sublime_start_time = int(time.time())

    if 'sublime_text.exe' not in names and sublime_start_time != None:
        sublime_end_time = int(time.time())
        reason = reason_selector("Sublime")
        csv_write(appname="Sublime", stime=sublime_start_time,
                  etime=sublime_end_time, reason=reason)
        sublime_start_time = None

    # steam usage
    if 'steam.exe' in names and steam_start_time == None:
        steam_start_time = int(time.time())

    if 'steam.exe' not in names and steam_start_time != None:
        steam_end_time = int(time.time())
        # reason = reason_selector("Steam")
        csv_write(appname="Steam", stime=steam_start_time,
                  etime=steam_end_time, reason="game")
        steam_start_time = None

    # GameUP usage
    if 'GameUP.exe' in names and GameUP_start_time == None:
        GameUP_start_time = int(time.time())

    if 'GameUP.exe' not in names and GameUP_start_time != None:
        GameUP_end_time = int(time.time())
        # reason = reason_selector("GameUp")
        csv_write(appname="Gameup", stime=GameUP_start_time,
                  etime=GameUP_end_time, reason="game")
        GameUP_start_time = None
    print(f"round :{counter: >3}")
    counter += 1

@atexit.register
def exit_manager():
    if GameUP_start_time:
        GameUP_end_time = int(time.time())
        # reason = reason_selector("GameUp")
        csv_write(appname="Gameup", stime=GameUP_start_time,
                  etime=GameUP_end_time, reason="game")
    if steam_start_time:
        steam_end_time = int(time.time())
        # reason = reason_selector("Steam")
        csv_write(appname="Steam", stime=steam_start_time,
                  etime=steam_end_time, reason="game")

    if sublime_start_time:
        sublime_end_time = int(time.time())
        # reason = reason_selector("Sublime")
        csv_write(appname="Sublime", stime=sublime_start_time,
                  etime=sublime_end_time, reason="shutdown")

    if pycharm_start_time:
        pycharm_end_time = int(time.time())
        # reason = reason_selector("Pycharm")
        csv_write(appname="Pycharm", stime=pycharm_start_time,
                  etime=pycharm_end_time, reason="shutdown")

    if vscode_start_time:
        vscode_end_time = int(time.time())
        # reason = reason_selector("VsCode")
        csv_write(appname="Vscode", stime=vscode_start_time,
                  etime=vscode_end_time, reason="shutdown")

if __name__ == "__main__":
    schedule = scheduler.Scheduler()
    schedule.cyclic(datetime.timedelta(seconds=10), main)
    counter = 0
    
    while True:
        schedule.exec_jobs()
        time.sleep(5)
