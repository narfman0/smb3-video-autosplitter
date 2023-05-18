from pygrabber.dshow_graph import FilterGraph
import cv2
from smb3_video_autosplitter.settings import settings


class OpenCV:
    def __init__(self):
        self.graph = FilterGraph()
        self.graph.add_video_input_device(settings.video_capture_source)
        self.graph.add_sample_grabber(self.on_frame_received)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()
        self.frame = None

    def tick(self):
        self.graph.grab_frame()
        if settings.show_capture_video and self.frame is not None:
            cv2.imshow("capture", self.frame)
            _ = cv2.waitKey(1)

    def on_frame_received(self, frame):
        self.frame = frame
