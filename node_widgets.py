import traceback
from PyQt6.QtWidgets import QLabel, QLineEdit
from PyQt6.QtGui import QFont
from Nodes.value_property import ValueProperty
import torch
from node_socket import NodeSocketWidget


class NodeWidget(QLabel):

    SOCKET_OFFSET = 20
    LINE_SIZE = 15

    def __init__(self, node, parent):
        super().__init__(node.node_name, parent=parent)

        self.font = QFont()
        self.font.setBold(True)
        self.setFont(self.font)
        self.show()

        self.node = node
        self.parent = parent
        self.socket_labels = [NodeSocketWidget(socket.get_socket_name(), self.parent, socket) for socket in node.subnode_sockets]
        self.connected_sockets = []

        for k, socket in enumerate(self.socket_labels):
            pos = self.pos()
            socket.move(pos.x(), pos.y() + self.SOCKET_OFFSET + k*self.LINE_SIZE)

    def cut(self):
        for connected_socket in self.connected_sockets:
            connected_socket.cut()
        for socket_label in self.socket_labels:
            socket_label.setParent(None)
        self.setParent(None)

    def mousePressEvent(self, event):
        ...

    def connect_socket(self, socket):
        self.connected_sockets.append(socket)

    def disconnect_socket(self, socket):
        for in_socket in self.connected_sockets:
            if in_socket is socket:
                out = in_socket
                self.connected_sockets.remove(out)
                break

    def mouseReleaseEvent(self, event):
        if self.geometry().contains(self.pos()+event.pos()):
            self.parent.select(self)
        else:
            offset = event.pos()
            pos = self.pos()
            self.move(pos.x() + offset.x(), pos.y() + offset.y())
            for label in self.socket_labels:
                label.move(label.pos().x() + offset.x(), label.pos().y() + offset.y())

    def select(self):
        self.setStyleSheet("color:red")

    def deselect(self):
        self.setStyleSheet("color:black")

    def move(self, *a0):
        super().move(*a0)
        for connected_socket in self.connected_sockets:
            connected_socket.move(connected_socket.pos())

    def to_dict(self):
        return {"Node": self.node.to_dict(), "Sockets": [socket.to_dict() for socket in self.socket_labels]}


class ValueNodeWidget(NodeWidget):

    def __init__(self, node: ValueProperty, parent):
        super().__init__(node, parent)
        self.edit = QLineEdit(parent=parent)
        self.edit.show()
        self.edit.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + len(self.socket_labels) * self.LINE_SIZE)
        self.edit.setText(str(self.node.initial_value))

        def on_edit(_):
            try:
                text = eval(self.edit.text())
                if type(text) is list:
                    self.node.set_value(torch.tensor(text, device=self.node.device))
                else:
                    self.node.set_value(text)
                print("valued")
            except Exception:
                print(traceback.format_exc())

        self.edit.textEdited.connect(on_edit)

    def cut(self):
        super().cut()
        self.edit.setParent(None)

    def move(self, *a0):
        super().move(*a0)
        self.edit.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + len(self.socket_labels) * self.LINE_SIZE)


class AnimatedPropertyNodeWidget(NodeWidget):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.edit = QLineEdit(parent=parent)
        self.edit.show()
        self.edit.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + len(self.socket_labels) * self.LINE_SIZE)

        def on_edit(_):
            text = self.edit.text()

            try:
                value = eval(text)
                self.node.clear_key_frames()
                for item in value:
                    frame = item[0]
                    object = item[1]
                    if type(object) == list:
                        object = torch.tensor(object, device=self.node.device)
                    self.node.set_key_frame(frame, object)
                print("pass, animated")
            except Exception:
                print(traceback.format_exc())

        self.edit.textEdited.connect(on_edit)

    def cut(self):
        super().cut()
        self.edit.setParent(None)

    def move(self, *a0):
        super().move(*a0)
        self.edit.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + len(self.socket_labels) * self.LINE_SIZE)
