import json
import os
import shutil

from utils import IpcData, OperatingMode, ipc_data_from_path

test_ipc_path = "./tests/test_data/ipc.json"
shutil.copyfile("./shared/ipc.json", "./tests/test_data/ipc.json")

def test_ipc_obj():
    ipcData = ipc_data_from_path(test_ipc_path)
    assert ipcData.operating_mode == OperatingMode.Slow

def test_set_operating_mode():
    ipcData = ipc_data_from_path(test_ipc_path)
    assert ipcData.operating_mode == OperatingMode.Slow

    ipcData.set_operating_mode(OperatingMode.Fast)
    # Object in memory should have value
    assert ipcData.operating_mode == OperatingMode.Fast
    # As well as file on disk
    with open(test_ipc_path) as f:
        assert json.loads(f.read())["operating_mode"] == OperatingMode.Fast.value