import logging
import traceback
from PyQt6.QtWidgets import QLabel
from src.Nodes.node import NodeSocket


class NodeSocketWidget(QLabel):

    def __init__(self, name, parent, socket):
        super().__init__(name, parent=parent)
        self.logger = logging.getLogger(__name__)

        self.parent = parent
        self.socket: NodeSocket = socket
        self.connected_node_widget = None

        self.connection_label = QLabel("", parent=self.parent)
        self.setStyleSheet("background-color:rgb(230, 230, 230)")

        self.move(parent.pos())
        self.connection_label.move(parent.pos())
        self.connection_label.hide()
        self.show()

    def mousePressEvent(self, event):
        ...

    def mouseReleaseEvent(self, event):
        try:
            for node_widget in [node.gui_ref for node in self.parent.patch.get_nodes()]:
                hit = node_widget.geometry().contains(self.pos()+event.pos())
                if hit:
                    self.connect(node_widget)
                    break
            else:
                connected = self.socket.is_connected()
                if connected:
                    self.connected_node_widget.disconnect_socket(self)
                self.socket.disconnect()
                self.connection_label.hide()

            self.parent.redraw_lines()

        except Exception:
            self.logger.error(traceback.format_exc())

    def connect(self, node_widget):
        connected = self.socket.is_connected()
        if connected:
            self.connected_node_widget.disconnect_socket(self)
        self.socket.disconnect()

        self.socket.connect(node_widget.node)
        self.connected_node_widget = node_widget
        self.connected_node_widget.connect_socket(self)
        self.connection_label.show()

    def cut(self):
        if self.socket.is_connected():
            self.connected_node_widget.disconnect_socket(self)
        self.socket.disconnect()

        self.connection_label.setParent(None)

    def move(self, *a0):
        super().move(*a0)
        self.parent.redraw_lines()

    def to_dict(self):
        return {"Socket": self.socket.to_dict()}
