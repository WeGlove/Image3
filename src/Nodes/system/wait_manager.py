import time
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from threading import Thread
from threading import RLock


class WaitManager(Node):

    def __init__(self, node_id, factory_id, device, initial_value=""):
        self.wait_for = NodeSocket(False, "Wait For", default=None, description="")
        self.last = None
        self.last_frame = -1
        self.production_thread = None
        self.is_running = False
        self.production_lock = RLock()
        super().__init__(node_id, factory_id, "Returns the given value.", [self.wait_for], device, [])

    def _waiting_production(self):
        while self.is_running:
            if self.last_frame == self.frame_counter.get():
                time.sleep(1)
                continue

            last_frame = self.frame_counter.get()
            production = self.wait_for.get().produce()
            with self.production_lock:
                self.last_frame = last_frame
                self.last = production

    def produce(self):
        with self.production_lock:
            return self.last

    def initialize(self, width, height, excluded_nodes, *args):
        super().initialize(width, height, excluded_nodes, *args)
        self.last = self.wait_for.get().produce()
        self.last_frame = self.frame_counter.get()

        if self.is_running:
            self.is_running = False
            self.production_thread.join()

        self.production_thread = Thread(target=self._waiting_production)

        self.is_running = True
        self.production_thread.start()

    @staticmethod
    def get_node_name():
        return "Wait Manager"
