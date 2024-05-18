from ast import Dict
from lmao.graph.lmao_graph_node import LmaoGraphNode
from pathlib import Path
from datetime import datetime
import cv2

import dataclasses, json
import os


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class TimeMachineSaveNode(LmaoGraphNode):
    """
    Does what it says, capute now detect later
    """

    def __init__(self, save_path: str = "./timemachine"):
        self.__save_path = save_path
        current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        self.__img_save_dir = os.path.join(self.__save_path, current_time, "img")
        self.__telem_save_dir = os.path.join(self.__save_path, current_time, "telem")

        os.makedirs(self.__img_save_dir, exist_ok=True)
        os.makedirs(self.__telem_save_dir, exist_ok=True)
        self.__count = 0

    def process(self, signal: Dict):
        image = signal["image"]
        img_name = os.path.join(self.__img_save_dir, f"{self.__count}.png")
        cv2.imwrite(img_name, image)

        a = {key: value for key, value in signal.items() if key != "image"}

        with open(
            os.path.join(self.__telem_save_dir, f"{self.__count}.json"), "w"
        ) as out:
            json.dump(a, out, cls=EnhancedJSONEncoder)

        self.__count += 1

    def tear_down(self):
        pass
