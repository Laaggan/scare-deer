from enum import Enum
import os
from time import sleep
import torch
import json

# TODO: move to environment variables
latest_image_path = "/home/llag/repos/scare-deer/shared/images/latest.jpg"
ipc_path = "/home/llag/repos/scare-deer/shared/ipc.json"
dear_proxies_path = "/home/llag/repos/scare-deer/shared/dear_proxies.json"
time_format = "%Y%m%d-%H%M%S"
ipc_obj = None
long_sleep = 15
short_sleep = 1

# TODO: move to utils
class OperatingMode(Enum):
    Slow = "SLOW"
    Fast = "FAST"

def load_ipc():
    global ipc_obj
    with open(ipc_path, 'r') as ipc_file:
        ipc_obj = json.loads(ipc_file.read())

# TODO: move to utils
def get_operating_mode():
    global ipc_obj
    return ipc_obj["mode"]

def set_operating_mode(mode: OperatingMode):
    ipc_obj["mode"] = mode.value
    ipc_json = json.dumps(ipc_obj)
    with open(ipc_path, 'w+') as file:
        file.write(ipc_json)

with open(dear_proxies_path) as file:
    dear_proxies:dict = json.loads(file.read())

# Check CPU/GPU
print("PyTorch version:", torch.__version__)
print("Is CUDA available?", torch.cuda.is_available())

# Try loading YOLOv5 from Torch Hub
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
print("YOLO model loaded!")

while 1:
    load_ipc()
    real_image_path = os.path.realpath(latest_image_path)

    # Run inference on latest image
    results = model([real_image_path])
    print("Inference OK!")

    # print(results)
    inferences = results.pandas().xyxy[0]

    if len(inferences) > 0:
        for i, inference in inferences.iterrows():
            if inference["name"] in dear_proxies.values():
                # set operating mode to fast
                print("Detected animal. Setting operating mode to fast and saving inference")
                set_operating_mode(OperatingMode.Fast)
                image_name = real_image_path.split("/")[-1].split(".")[0]
                inferences.to_pickle(f"/home/llag/repos/scare-deer/shared/inferences/{image_name}.pkl")
                break
            else:
                print("Found no animal in detection. Setting operating mode to slow")
                set_operating_mode(OperatingMode.Slow)
    else:
        print("No object detected. Setting operating mode to slow")
        set_operating_mode(OperatingMode.Slow)
    
    load_ipc()
    mode = get_operating_mode()

    if mode == OperatingMode.Slow.value:
        sleep_time = long_sleep
    else:
        sleep_time = short_sleep
    
    print(f"Sleep for {sleep_time} seconds...")
    sleep(sleep_time)


