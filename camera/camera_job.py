# import schedule
import time
import datetime
import json
import os
from picamera2 import Picamera2, Preview
from scare_deer_utils import IpcData, OperatingMode, ipc_data_from_path

picam2 = Picamera2()
time_format = "%Y%m%d-%H%M%S"
ipc_path = os.getenv("IPC_PATH")
ipc_obj = ipc_data_from_path(ipc_path)

images_path = os.getenv("IMAGES_PATH")
long_sleep = 1
short_sleep = 0.1
start_time = datetime.datetime.now()
cleanup_interval = datetime.timedelta(seconds=30)
cleanup_rate = 10

def cleanup(clean_until_time):
    print(clean_until_time)
    files = os.listdir(images_path)
    
    for file in files:
        if "latest" in file:
            print("We don't clean the latest")
            continue

        time_str = file.split("/")[-1][:-4]
        time = datetime.datetime.strptime(time_str, time_format)
        
        if time < clean_until_time:
            file_path = os.path.join(images_path, file)
            # TODO: Add different log levels
            # print(f"Remove {file_path}")
            os.remove(file_path)


def job():
    global time_format
    timestr = time.strftime(time_format)
    file_name = f"{timestr}.jpg"
    file_path = f"{images_path}/{file_name}"
    
    print("Taking snapshot")
    picam2.start_and_capture_file(file_path, show_preview=False)
    latest_path = f"{images_path}/latest.jpg"
    
    if os.path.lexists(latest_path):
        os.remove(latest_path)
    
    os.symlink(os.path.abspath(file_path), latest_path)

while 1:
    if ipc_obj.operating_mode == OperatingMode.Slow:
        job()
        time.sleep(long_sleep)
    else:
        job()
        time.sleep(short_sleep)

    loop_time = datetime.datetime.now()
    
    if loop_time > (start_time + cleanup_interval):
        cleanup(start_time)
        start_time = datetime.datetime.now()