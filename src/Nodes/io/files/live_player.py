from src.Nodes.node import Node
from src.Nodes.node import NodeSocket
from playsound import playsound
from threading import Thread


class LivePlayer(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.compositor = NodeSocket(False, "Compositor", None)
        self.data = NodeSocket(False, "Path", None)

        # for playing wav file
        self.song = None

        super().__init__(node_id, factory_id, "Live Player", frame_counter,
                         [self.compositor, self.data], device, [])

    def play_thread(self):
        playsound(self.data.get().produce(), block=True)

    def produce(self):
        if self.frame_counter.was_set:
            self.thrd = Thread(target=self.play_thread)
            self.thrd.start()

        return self.compositor.get().produce()

    @staticmethod
    def get_node_name():
        return "Live Player"
