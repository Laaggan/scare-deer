import os
from time import sleep, time
import torch
import json
import shutil
from common.scare_deer_utils import OperatingMode, ipc_data_from_path

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
            # return (inference["name"] in deer_proxies.values(), results) # return results for convenience
    else:
        print("No object detected. Setting operating mode to slow")
        return (False, None)


def analysis_loop():
    inferences_path = os.getenv("INFERENCES_PATH")
    latest_image_path = os.getenv("LATEST_IMAGE_PATH")
    print("latest_image_path:", latest_image_path)
    ipc_path = os.getenv("IPC_PATH")
    ipc_obj = ipc_data_from_path(ipc_path)
    time_format = "%Y%m%d-%H%M%S"
    long_sleep = 1
    short_sleep = 1

    real_image_path = os.path.realpath(latest_image_path)
    model = load_model()
    deer_proxies = load_deer_proxies()

    while 1:
        is_deer, inferences = do_inference(model, latest_image_path, deer_proxies)
        
        if is_deer:
            print("Detected deer. Setting operating mode to fast and saving inference")
            ipc_obj.set_operating_mode(OperatingMode.Fast)
            save_inference(real_image_path, inferences_path, inferences)
        else:
            print("Found no deer in image. Setting operating mode to slow")
            ipc_obj.set_operating_mode(OperatingMode.Slow)
        
        print(f"Sleep for {short_sleep} seconds...")
        sleep(short_sleep)

def save_inference(real_image_path, inferences_path, inferences):
    image_name = real_image_path.split("/")[-1].split(".")[0]
    file_name = image_name = real_image_path.split("/")[-1]
    #TODO: I should probably have some mechanism for movie capture start and stop
    shutil.copyfile(real_image_path, f"{inferences_path}/{file_name}")
    inferences.to_pickle(f"{inferences_path}/{image_name}.pkl")

if __name__ == "__main__":
    analysis_loop()