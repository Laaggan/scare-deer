# import schedule
import time
import json
import os
from picamera2 import Picamera2

picam2 = Picamera2()
# TODO: take in from env
time_format = "%Y%m%d-%H%M%S"
ipc_path = "/home/llag/repos/scare-deer/shared/ipc.json"
long_sleep = 15
short_sleep = 0.1

# TODO: move to utils
def get_operating_mode():
    global ipc_path
    with open(ipc_path, 'r') as ipc_file:
        ipc_obj = json.loads(ipc_file.read())
    
    return ipc_obj["mode"]

def job():
    global time_format
    base_path = "/home/llag/repos/scare-deer/shared/images"
    timestr = time.strftime(time_format)
    file_name = f"{timestr}.jpg"
    file_path = f"{base_path}/{file_name}"
    
    print("Taking snapshot")
    picam2.start_and_capture_file(file_path, show_preview=False)
    latest_path = f"{base_path}/latest.jpg"
    
    if os.path.exists(latest_path):
        os.remove(latest_path)
    
    os.symlink(file_path, latest_path)

# schedule.every(2).seconds.do(job)
#schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    mode = get_operating_mode()
    if mode == "SLOW":
        job()
        time.sleep(long_sleep)
    else:
        job()
        time.sleep(short_sleep)

# while 1:
#     n = schedule.idle_seconds()
#     if n is None:
#         # no more jobs
#         break
#     elif n > 0:
#         # sleep exactly the right amount of time
#         time.sleep(n)
#     schedule.run_pending()