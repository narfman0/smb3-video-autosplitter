from pygrabber.dshow_graph import FilterGraph
import cv2


class OpenCV:
    def __init__(self, video_capture_source, show_capture_video=False):
        self.show_capture_video = show_capture_video
        self.graph = FilterGraph()
        self.graph.add_video_input_device(video_capture_source)
        self.graph.add_sample_grabber(self.on_frame_received)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()
        self.frame = None

    def tick(self):
        self.graph.grab_frame()
        if self.show_capture_video and self.frame is not None:
            cv2.imshow("capture", self.frame)
            _ = cv2.waitKey(1)

    def on_frame_received(self, frame):
        self.frame = frame
