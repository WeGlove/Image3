import time
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from threading import Thread
from threading import RLock


class WaitManager(Node):

    def __init__(self):
        self.wait_for = NodeSocket("Wait For")
        self.last = None
        self.last_frame = -1
        self.production_thread = None
        self.is_running = False
        self.production_lock = RLock()
        super().__init__([self.wait_for], [], "Returns the given value.")

    def _waiting_production(self):
        while self.is_running:
            if self.last_frame == self.frame_counter.get():
                time.sleep(1) # TODO this number shouldn't be magic
                continue

            last_frame = self.frame_counter.get()
            production = self.wait_for.get().produce()
            with self.production_lock:
                self.last_frame = last_frame
                self.last = production

    def produce(self):
        with self.production_lock:
            return self.last

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.last = self.wait_for.get().produce()
        self.last_frame = self.frame_counter.get()

        if self.is_running:
            self.is_running = False
            self.production_thread.join()

        self.production_thread = Thread(target=self._waiting_production)

        self.is_running = True
        self.production_thread.start()
