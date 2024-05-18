
from lmao.detection.detector import Detection, Detector
from typing import List

import logging as log

class NullDetector(Detector):
    """
    Detector implementation that does nothing. This is used as a placeholder to avoid doing null checks.
    """

    def __init__(self):
        log.warning('Using NullDetector. This implementation is a placeholder and does not detect anything')

    def detect(self, image) -> List[Detection]:
        return []