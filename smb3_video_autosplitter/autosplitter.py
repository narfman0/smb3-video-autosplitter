"""
video based autosplitter for smb3
"""

import logging
import time

import cv2
import win32file, win32pipe

from smb3_video_autosplitter.util import locate_all_opencv, settings

LOGGER = logging.getLogger(__name__)
SPLIT_DEDUPE_WAIT_S = settings.get_int("split_dedupe_wait_s", fallback=5.0)
SPLIT_OFFSET_FRAMES = settings.get_int("split_offset_frames", fallback=40)
SPLIT_OFFSET_S = (SPLIT_OFFSET_FRAMES * 16.64) / 1000


class LivesplitConnectFailedException(Exception):
    pass


class Autosplitter:
    def __init__(self):
        self.region = settings.get_config_region("autosplitter_region")
        self.template = cv2.imread(
            settings.get(
                "autosplitter_path",
                fallback="data/trigger.png",
            )
        )
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
        self.earliest_next_trigger_time = 0

    def tick(self, frame):
        if frame is None or self.earliest_next_trigger_time >= time.time():
            return
        if list(locate_all_opencv(self.template, frame, region=self.region)):
            time.sleep(SPLIT_OFFSET_S)
            self.earliest_next_trigger_time = time.time() + SPLIT_DEDUPE_WAIT_S
            win32file.WriteFile(self.handle, b"split\r\n")
            LOGGER.info(f"Livesplit autosplit")
