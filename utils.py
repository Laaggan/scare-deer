from dataclasses import dataclass
from enum import Enum
import json

class OperatingMode(Enum):
        Slow = "SLOW"
        Fast = "FAST"

@dataclass
class IpcData():
    operating_mode: OperatingMode
    file_path: str

    def __post_init__(self):
        if not isinstance(self.operating_mode, OperatingMode):
            self.operating_mode = OperatingMode(self.operating_mode)

    def set_operating_mode(self, mode: OperatingMode):
            self.operating_mode = mode

            ipc_json = json.dumps({'operating_mode': self.operating_mode.value})
            with open(self.file_path, 'w+') as file:
                file.write(ipc_json)

def ipc_data_from_path(path):
    with open(path, 'r') as f:
        j = json.loads(f.read())
    return IpcData(**j, file_path=path)