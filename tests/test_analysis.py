import pytest
import os
from analysis.main import load_model, load_deer_proxies, do_inference

BASE_IMAGE_PATH="./tests/example_images"

# Manually Define Env Variables in Test
os.environ["LATEST_IMAGE_PATH"] = f"{BASE_IMAGE_PATH}/deer1.jpg"
os.environ["DEER_PROXIES"]="shared/deer_proxies.json"
os.environ["IPC_PATH"]="shared/ipc.json"

model = load_model()
deer_proxies = load_deer_proxies()

def test_load_env_vars():
    assert os.environ["LATEST_IMAGE_PATH"] == f"{BASE_IMAGE_PATH}/deer1.jpg"
    assert os.environ["DEER_PROXIES"] == "shared/deer_proxies.json"
    assert os.environ["IPC_PATH"] == "shared/ipc.json"

@pytest.mark.parametrize("image_path", [f"{BASE_IMAGE_PATH}/deer1.jpg", f"{BASE_IMAGE_PATH}/deer2.jpg", f"{BASE_IMAGE_PATH}/deer3.jpg"])
def test_detect_deer(image_path):
    os.environ["LATEST_IMAGE_PATH"] = image_path
    is_deer, inferences = do_inference(model, os.environ["LATEST_IMAGE_PATH"], deer_proxies)
    assert is_deer

@pytest.mark.parametrize("image_path", [f"{BASE_IMAGE_PATH}/linus_siri.jpg", f"{BASE_IMAGE_PATH}/empty_field.jpg"])
def test_detect_no_deer(image_path):
    os.environ["LATEST_IMAGE_PATH"] = image_path
    is_deer, _ = do_inference(model, os.environ["LATEST_IMAGE_PATH"], deer_proxies)

    assert not is_deer