from enum import Enum
import os
from time import sleep, time
import torch
import json
import shutil

def load_deer_proxies():
    path = os.getenv("DEER_PROXIES")
    real_path = os.path.realpath(path)
    with open(real_path) as file:
        return json.loads(file.read())


def load_model():
    # Check CPU/GPU
    print("PyTorch version:", torch.__version__)
    print("Is CUDA available?", torch.cuda.is_available())

    # Try loading YOLOv5 from Torch Hub
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    print("YOLO model loaded!")
    return model

def do_inference(model, image_path, deer_proxies):
    real_image_path = os.path.realpath(image_path)

    start = time()
    # Run inference on latest image
    results = model([real_image_path])
    print("Inference OK!")
    end = time()
    print(f"Inference took {end - start} seconds")

    inferences = results.pandas().xyxy[0]

    if len(inferences) > 0:
        for i, inference in inferences.iterrows():
            print("Detected object:", inference["name"])
            
            return (inference["name"] in deer_proxies.values(), inferences)
    else:
        print("No object detected. Setting operating mode to slow")
        return (False, None)


def analysis_loop():
    latest_image_path = os.getenv("LATEST_IMAGE_PATH")
    print("latest_image_path:", latest_image_path)
    ipc_path = os.getenv("IPC_PATH")
    time_format = "%Y%m%d-%H%M%S"
    ipc_obj = None
    long_sleep = 1
    short_sleep = 1

    # TODO: move to utils
    class OperatingMode(Enum):
        Slow = "SLOW"
        Fast = "FAST"

    def load_ipc():
        global ipc_obj
        print(ipc_path)
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

    
    load_ipc()
    real_image_path = os.path.realpath(latest_image_path)
    model = load_model()
    deer_proxies = load_deer_proxies()

    while 1:
        is_deer, inferences = do_inference(model, latest_image_path, deer_proxies)
        
        if is_deer:
            print("Detected deer. Setting operating mode to fast and saving inference")
            set_operating_mode(OperatingMode.Fast)
            image_name = real_image_path.split("/")[-1].split(".")[0]
            file_name = image_name = real_image_path.split("/")[-1]
            #TODO: I should probably have some mechanism for movie capture start and stop
            shutil.copyfile(real_image_path, f"../shared/inferences/{file_name}")
            inferences.to_pickle(f"../shared/inferences/{image_name}.pkl")
            break
        else:
            print("Found no deer in image. Setting operating mode to slow")
            set_operating_mode(OperatingMode.Slow)
        
        # load_ipc()
        # mode = get_operating_mode()

        # if mode == OperatingMode.Slow.value:
        #     sleep_time = long_sleep
        # else:
        #     sleep_time = short_sleep
        
        # print(f"Sleep for {sleep_time} seconds...")
        # sleep(sleep_time)
        print(f"Sleep for {short_sleep} seconds...")
        sleep(short_sleep)

# analysis_loop()