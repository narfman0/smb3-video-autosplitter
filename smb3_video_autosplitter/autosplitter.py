"""
video based autosplitter for smb3
"""
from dataclasses import dataclass
import logging
import time

import cv2

from smb3_video_autosplitter.livesplit import Livesplit
from smb3_video_autosplitter.settings import Settings
from smb3_video_autosplitter.util import locate_all_opencv

LOGGER = logging.getLogger(__name__)


@dataclass
class Split:
    path: str
    image: any
    region: list[int, int, int, int]


class Autosplitter:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.initialize_splits()
        self.earliest_next_trigger_time = 0
        self.livesplit = Livesplit()
        self.split_offset_s = (settings.split_offset_frames * 16.64) / 1000

    def tick(self, frame):
        if frame is None or self.earliest_next_trigger_time >= time.time():
            return
        for split in self.splits:
            results = list(locate_all_opencv(split.image, frame, region=split.region))
            if results:
                time.sleep(self.split_offset_s)
                self.earliest_next_trigger_time = (
                    time.time() + self.settings.split_dedupe_wait_s
                )
                LOGGER.info(
                    f"Splitting after {split.path} observed {len(results)} times at {list(map(str, results))}"
                )
                self.livesplit.send("split")

    def initialize_splits(self):
        self.splits: list[Split] = []
        for split in self.settings.splits:
            image = cv2.imread(split.path)
            region = [split.x, split.y, split.width, split.height]
            self.splits.append(Split(split.path, image, region))
