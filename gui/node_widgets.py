import traceback
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
import torch
from gui.node_socket_widget import NodeSocketWidget
from Nodes.interactables.node_edit import NodeEdit
from Nodes.interactables.node_button import NodeButton


class NodeWidget(QLabel):

    SOCKET_OFFSET = 20
    LINE_SIZE = 15

    def __init__(self, node, parent):
        super().__init__(node.get_node_name(), parent=parent)

        self.font = QFont()
        self.font.setBold(True)
        self.setFont(self.font)
        self.show()

        self.node = node
        self.parent = parent
        self.socket_labels = [NodeSocketWidget(socket.get_socket_name(), self.parent, socket) for socket in node.subnode_sockets]
        self.setToolTip(self.node.get_description())

        def get_on_edit(k):
            def on_edit(_):
                self.node.get_interactable(k).set(self.edit_fields[k].text())

            return on_edit

        def get_on_button_press(k):
            def on_press(_):
                self.node.get_interactable(k).toggle()

            return on_press

        self.connected_sockets = []

        for k, socket in enumerate(self.socket_labels):
            pos = self.pos()
            socket.move(pos.x(), pos.y() + self.SOCKET_OFFSET + k*self.LINE_SIZE)

        #self.edit_fields = [QLineEdit(parent=self.parent) for _ in range(self.node.get_interactable_count())]
        #for k, edit_field in enumerate(self.edit_fields):
        #    edit_field.textEdited.connect(get_on_edit(k))
        #    edit_field.show()

        self.edit_fields = []
        for j in range(self.node.get_interactable_count()):
            interactable = self.node.get_interactable(j)
            if type(interactable) == NodeEdit:
                edit_field = QLineEdit(parent=self.parent)
                self.edit_fields.append(edit_field)
                edit_field.textEdited.connect(get_on_edit(j))
                edit_field.show()

                try:
                    pos = self.pos()
                    edit_field.move(pos.x(), pos.y() + self.SOCKET_OFFSET + j*self.LINE_SIZE + len(self.socket_labels)*self.LINE_SIZE)
                    value = self.node.get_interactable(j).get()
                    if type(value) == torch.Tensor:
                        value = value.tolist()
                    edit_field.setText(str(value))
                except Exception:
                    print(traceback.format_exc())
            elif type(interactable) == NodeButton:
                edit_field = QPushButton(parent=self.parent)
                self.edit_fields.append(edit_field)
                edit_field.clicked.connect(get_on_button_press(j))
                edit_field.show()

                pos = self.pos()
                edit_field.move(pos.x(), pos.y() + self.SOCKET_OFFSET + j*self.LINE_SIZE + len(self.socket_labels)*self.LINE_SIZE)

    def cut(self):
        for connected_socket in self.connected_sockets:
            connected_socket.cut()
        for socket_label in self.socket_labels:
            socket_label.setParent(None)
        for edit in self.edit_fields:
            edit.setParent(None)
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

    def select(self):
        self.setStyleSheet("color:red")

    def deselect(self):
        self.setStyleSheet("color:black")

    def move(self, *a0):
        super().move(*a0)
        for connected_socket in self.connected_sockets:
            connected_socket.move(connected_socket.pos())
        for k, edit_field in enumerate(self.edit_fields):
            edit_field.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + k*self.LINE_SIZE + len(self.socket_labels)*self.LINE_SIZE)
        for k, label in enumerate(self.socket_labels):
            label.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + k*self.LINE_SIZE)

    def to_dict(self):
        return {"Node": self.node.to_dict(), "Sockets": [socket.to_dict() for socket in self.socket_labels], "Position": [self.pos().x(), self.pos().y()]}

"""
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
            except Exception:
                print(traceback.format_exc())

        self.edit.textEdited.connect(on_edit)
        self.edit.setText(str([(frame, value.tolist() if type(value) == torch.Tensor else value) for (frame, value) in self.node.keyframes]))

    def cut(self):
        super().cut()
        self.edit.setParent(None)

    def move(self, *a0):
        super().move(*a0)
        self.edit.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + len(self.socket_labels) * self.LINE_SIZE)
"""
