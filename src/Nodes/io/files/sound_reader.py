import torch
from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
import wave


class SoundReader(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.initial_value = NodeEdit(initial_value)
        self.w = None
        self.w_frame = None
        super().__init__(node_id, factory_id, "Sound Reader", frame_counter, [], device, [self.initial_value])

    def produce(self):
        frame = self.w.readframes(self.frame_counter.get() % self.w_frame)
        return frame

    def to_dict(self):
        property_dict = super().to_dict()
        value = self.initial_value.get()

        if type(value) == torch.Tensor:
            value = value.tolist()

        property_dict["properties"]["initial_value"] = value
        return property_dict

    def initialize(self, width, height, *args):
        self.w = wave.open('/usr/share/sounds/ekiga/voicemail.wav', 'r')
        self.w_frame = self.w.getnframes()

    @staticmethod
    def get_node_name():
        return "Sound Reader"
