from src.Nodes.node import Node
from src.Nodes.node import NodeSocket
from playsound import playsound
from threading import Thread


class LivePlayer(Node):

    def __init__(self):
        self.compositor = NodeSocket("Compositor")
        self.data = NodeSocket("Path", default=".")

        # for playing wav file
        self.song = None

        super().__init__([self.compositor, self.data], [], "Live Player")

    def play_thread(self):
        playsound(self.data.get().produce(), block=True)

    def produce(self):
        if self.frame_counter.was_set:
            self.thrd = Thread(target=self.play_thread)
            self.thrd.start()

        return self.compositor.get().produce()
