"""
video based autosplitter for smb3
"""
from dataclasses import dataclass
import logging
import time

import cv2
import win32file, win32pipe

from smb3_video_autosplitter.util import locate_all_opencv, settings

LOGGER = logging.getLogger(__name__)
SPLIT_DEDUPE_WAIT_S = settings.get("split_dedupe_wait_s", 5.0)
SPLIT_OFFSET_FRAMES = settings.get("split_offset_frames", 40)
SPLIT_OFFSET_S = (SPLIT_OFFSET_FRAMES * 16.64) / 1000


class LivesplitConnectFailedException(Exception):
    pass


@dataclass
class Split:
    path: str
    image: any
    region: list[int, int, int, int]


class Autosplitter:
    def __init__(self):
        self.initialize_splits()
        self.initialize_livesplit()
        self.earliest_next_trigger_time = 0

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
                win32file.WriteFile(self.handle, b"split\r\n")

    def initialize_livesplit(self):
        try:
            self.handle = win32file.CreateFile(
                r"\\.\pipe\LiveSplit",
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                win32file.FILE_ATTRIBUTE_NORMAL,
                None,
            )
        except:
            raise LivesplitConnectFailedException()
        res = win32pipe.SetNamedPipeHandleState(
            self.handle, win32pipe.PIPE_READMODE_BYTE, None, None
        )
        if res == 0:
            print(f"SetNamedPipeHandleState return code: {res}")

    def initialize_splits(self):
        self.splits: list[Split] = []
        for split in settings.get("splits"):
            path = split["path"]
            image = cv2.imread(path)
            region = [split["x"], split["y"], split["width"], split["height"]]
            self.splits.append(Split(path, image, region))
