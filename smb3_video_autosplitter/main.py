"""
video based autosplitter for smb3
"""

from smb3_video_autosplitter.autosplitter import Autosplitter
from smb3_video_autosplitter.opencv import OpenCV


def main():
    opencv = OpenCV()
    autosplitter = Autosplitter()
    while True:
        opencv.tick()
        autosplitter.tick(opencv.frame)


if __name__ == "__main__":
    main()
