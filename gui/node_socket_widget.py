import traceback
from PyQt6.QtWidgets import QLabel
from Nodes.node import NodeSocket


class NodeSocketWidget(QLabel):

    def __init__(self, name, parent, socket):
        super().__init__(name, parent=parent)
        self.parent = parent
        self.socket: NodeSocket = socket
        self.connected_node_widget = None

        self.connection_label = QLabel("===Wire===", parent=self.parent)
        self.move(parent.pos())
        self.connection_label.move(parent.pos())
        self.connection_label.hide()
        self.show()

    def mousePressEvent(self, event):
        ...

    def mouseReleaseEvent(self, event):
        try:
            for k, node_widget in self.parent.node_widgets.items():
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
        except Exception:
            print(traceback.format_exc())

    def connect(self, node_widget):
        connected = self.socket.is_connected()
        if connected:
            self.connected_node_widget.disconnect_socket(self)
        self.socket.disconnect()

        self.socket.connect(node_widget.node)
        self.connection_label.move((self.pos() + node_widget.pos()) / 2)
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
        if self.connected_node_widget is not None:
            self.connection_label.move((self.pos() + self.connected_node_widget.pos()) / 2)

    def to_dict(self):
        return {"Socket": self.socket.to_dict()}