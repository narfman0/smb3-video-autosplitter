"""
video based autosplitter for smb3
"""
import logging

from pygrabber.dshow_graph import FilterGraph

from smb3_video_autosplitter.settings import settings
from smb3_video_autosplitter.autosplitter import Autosplitter
from smb3_video_autosplitter.livesplit import LivesplitConnectFailedException
from smb3_video_autosplitter.opencv import OpenCV

from smb3_video_autosplitter.logging import initialize_logging

LOGGER = logging.getLogger(__name__)


def print_camera_info():
    graph = FilterGraph()
    input_devices = graph.get_input_devices()
    video_capture_source = settings.video_capture_source
    if (
        video_capture_source == None
        or video_capture_source == -1
        or video_capture_source >= len(input_devices)
    ):
        LOGGER.warning(
            "No camera selected or invalid, please update to one of the below:"
        )
        LOGGER.warning(input_devices)
        exit()
    LOGGER.info(f"Selected video source: {input_devices[video_capture_source]}")


def main():
    initialize_logging()
    print_camera_info()
    opencv = OpenCV()
    try:
        autosplitter = Autosplitter(settings)
    except LivesplitConnectFailedException:
        LOGGER.warning("Failed to connect to livesplit, is it running?")
        exit()
    while True:
        opencv.tick()
        autosplitter.tick(opencv.frame)


if __name__ == "__main__":
    main()
