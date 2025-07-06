from src.Nodes.node import Node
from src.interactables.node_edit import NodeEdit
import wave


class SoundReader(Node):

    def __init__(self):
        self.initial_value = NodeEdit(".")
        self.w = None
        self.w_frame = None
        super().__init__([], [self.initial_value], "Sound Reader")

    def produce(self):
        frame = self.w.readframes(self.frame_counter.get() % self.w_frame)
        return frame

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.w = wave.open('/usr/share/sounds/ekiga/voicemail.wav', 'r') # TODO wtf xD?
        self.w_frame = self.w.getnframes()
