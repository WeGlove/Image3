from Nodes.node import Node
from Nodes.node_socket import NodeSocket
from strips.frame_counter import FrameCounter


class FromFile(Node):

    def __init__(self, node_id, device, frame_counter: FrameCounter):
        self.file_name = NodeSocket(True, "File", None)
        super().__init__(node_id, "FromFile", frame_counter, [self.file_name], device, [])
        self.f = None
        self.x = 0

    def produce(self, *args):
        frame = self.frame_counter.get()
        self.f.seek(frame)
        if self.frame_counter.was_reversed:
            self.f.seek(frame-1)

        return int.from_bytes(self.f.read(1), "big") / 255

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.f = open(self.file_name.get().produce(), "rb")
