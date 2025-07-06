from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from src.gui.node_socket_widget import NodeSocketWidget
from src.interactables.node_edit import NodeEdit
from src.interactables.node_button import NodeButton
from src.interactables.node_display import NodeDisplay
from src.interactables.node_table import NodeTable
from src.gui.interactable_widgets.ButtonWidget import ButtonWidget
from src.gui.interactable_widgets.EditWidget import EditWidget
from src.gui.interactable_widgets.TableWidget import TableWidget


class NodeWidget(QLabel):

    SOCKET_OFFSET = 20
    LINE_SIZE = 15

    def __init__(self, node, parent):
        super().__init__(node.get_node_name(), parent=parent)

        self.font = QFont()
        self.font.setBold(True)
        self.setStyleSheet("background-color:rgb(230, 230, 230)")
        self.setFont(self.font)
        self.show()

        self.node = node
        self.node.set_gui_ref(self)
        self.parent = parent
        self.setToolTip(self.node.get_description())

        self.connected_sockets = []

        self.socket_labels = [NodeSocketWidget(socket.get_socket_name(), self.parent, socket) for socket in node.subnode_sockets]

        for k, socket in enumerate(self.socket_labels):
            pos = self.pos()
            socket.move(pos.x(), pos.y() + self.SOCKET_OFFSET + k*self.LINE_SIZE)

        self.edit_fields = []
        for j in range(self.node.get_interactable_count()):
            interactable = self.node.get_interactable(j)
            if type(interactable) == NodeEdit:
                edit_field = EditWidget(self.parent, node, j, j)
                self.edit_fields.append(edit_field)
            elif type(interactable) == NodeButton:
                edit_field = ButtonWidget(self.parent, node, j, j)
                self.edit_fields.append(edit_field)
            elif type(interactable) == NodeDisplay:
                edit_field = EditWidget(self.parent, node, j, j)
                self.edit_fields.append(edit_field)
            elif type(interactable) == NodeTable:
                edit_field = TableWidget(self.parent, node, j, j)
                self.edit_fields.append(edit_field)
            else:
                raise ValueError(f"Unknown edit field {type(interactable)}")

            edit_field.update()

    def cut(self):
        for connected_socket in self.connected_sockets:
            connected_socket.cut()
        for socket_label in self.socket_labels:
            socket_label.setParent(None)
        for edit in self.edit_fields:
            edit.cut()
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
            self.move(pos.x() - self.parent.global_position[0] + offset.x(),
                      pos.y() - self.parent.global_position[1] + offset.y())

    def select(self):
        self.setStyleSheet("color:red")

    def deselect(self):
        self.setStyleSheet("color:black")

    def update_position(self):
        self.move(*self.node.position.tolist())

    def move(self, *a0):
        super().move(a0[0] + self.parent.global_position[0], a0[1] + self.parent.global_position[1])
        self.node.set_position(a0)

        for connected_socket in self.connected_sockets:
            connected_socket.move(connected_socket.pos())
        for k, edit_field in enumerate(self.edit_fields):
            edit_field.move(self.pos().x(),
                            self.pos().y() + self.SOCKET_OFFSET + k*self.LINE_SIZE + len(self.socket_labels)*self.LINE_SIZE)
        for k, label in enumerate(self.socket_labels):
            label.move(self.pos().x(),
                       self.pos().y() + self.SOCKET_OFFSET + k*self.LINE_SIZE)

    def to_dict(self):
        return {"Node": self.node.to_dict(), "Sockets": [socket.to_dict() for socket in self.socket_labels]}
