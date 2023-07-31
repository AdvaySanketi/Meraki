from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt
from os import system
from time import sleep

parallel_tasks = [["Server.bat", 1], ["Meraki.bat", 3]]

def DatTijd():
    Nu = dt.datetime.now()
    return Nu

def GetStartTime(Nu, seconds):
    StartTime = (Nu + dt.timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")
    return StartTime

len_li = len(parallel_tasks)
sleepTime = parallel_tasks[len_li - 1][1] + 3
Nu = DatTijd()
for x in range(0, len_li):
    parallel_tasks[x][0] = 'start cmd /C ' + parallel_tasks[x][0]
    # if you want the command window stay open after the tasks are finished use: cmd /k in the line above
    delta = parallel_tasks[x][1]
    parallel_tasks[x][1] = GetStartTime(Nu, delta)

JobShedul = BackgroundScheduler()
JobShedul.start()

for x in range(0, len_li):
    JobShedul.add_job(system, 'date', run_date=parallel_tasks[x][1], misfire_grace_time=3, args=[parallel_tasks[x][0]])

sleep(sleepTime)
JobShedul.shutdown()
exit()