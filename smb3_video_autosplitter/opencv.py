from pygrabber.dshow_graph import FilterGraph

from smb3_video_autosplitter.util import locate_all_opencv, settings


class OpenCV:
    def __init__(self):
        self.graph = FilterGraph()
        self.graph.add_video_input_device(settings.get_int("video_capture_source"))
        self.graph.add_sample_grabber(self.on_frame_received)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()
        self.frame = None

    def tick(self):
        self.graph.grab_frame()

    def on_frame_received(self, frame):
        self.frame = frame
