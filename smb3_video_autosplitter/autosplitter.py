"""
video based autosplitter for smb3
"""
from dataclasses import dataclass
import logging
import time

import cv2

from smb3_video_autosplitter.livesplit import Livesplit
from smb3_video_autosplitter.util import locate_all_opencv, settings

LOGGER = logging.getLogger(__name__)
SPLIT_DEDUPE_WAIT_S = settings.get("split_dedupe_wait_s", 5.0)
SPLIT_OFFSET_FRAMES = settings.get("split_offset_frames", 40)
SPLIT_OFFSET_S = (SPLIT_OFFSET_FRAMES * 16.64) / 1000


@dataclass
class Split:
    path: str
    image: any
    region: list[int, int, int, int]


class Autosplitter:
    def __init__(self):
        self.initialize_splits()
        self.earliest_next_trigger_time = 0
        self.livesplit = Livesplit()

    def tick(self, frame):
        if frame is None or self.earliest_next_trigger_time >= time.time():
            return
        for split in self.splits:
            results = list(locate_all_opencv(split.image, frame, region=split.region))
            if results:
                time.sleep(SPLIT_OFFSET_S)
                self.earliest_next_trigger_time = time.time() + SPLIT_DEDUPE_WAIT_S
                LOGGER.info(
                    f"Splitting after {split.path} observed {len(results)} times at {list(map(str, results))}"
                )
                self.livesplit.send("split")

    def initialize_splits(self):
        self.splits: list[Split] = []
        for split in settings.get("splits"):
            path = split["path"]
            image = cv2.imread(path)
            region = [split["x"], split["y"], split["width"], split["height"]]
            self.splits.append(Split(path, image, region))
