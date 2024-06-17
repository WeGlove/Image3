import traceback
from typing import List
from strips.strip import Strip
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from renderer import Renderer
from Nodes.Node import NodeSocket
from PyQt6.QtGui import QFont, QKeyEvent
from Nodes.value_property import ValueProperty
import torch
from Nodes.animated_property import AnimatedProperty


class NodeSocketWidget(QLabel):

    def __init__(self, name, parent, socket):
        super().__init__(name, parent=parent)
        self.parent = parent
        self.socket: NodeSocket = socket
        self.connected_node_widget: NodeWidget = None

        self.connection_label = QLabel("===Wire===", parent=self.parent)

    def mousePressEvent(self, event):
        ...

    def mouseReleaseEvent(self, event):
        for k, node_widget in enumerate(self.parent.node_widgets):
            hit = node_widget.geometry().contains(self.pos()+event.pos())
            if hit:
                connected = self.socket.is_connected()
                if connected:
                    self.connected_node_widget.disconnect_socket(self)
                self.socket.disconnect()

                self.socket.connect(node_widget.node)
                self.connection_label.move((self.pos() + node_widget.pos()) / 2)
                self.connected_node_widget = node_widget
                self.connected_node_widget.connect_socket(self)

                break

    def cut(self):
        if self.socket.is_connected():
            self.connected_node_widget.disconnect_socket(self)
        self.socket.disconnect()

        self.connection_label.setParent(None)

    def move(self, *a0):
        super().move(*a0)
        if self.connected_node_widget is not None:
            self.connection_label.move((self.pos() + self.connected_node_widget.pos()) / 2)


class NodeWidget(QLabel):

    SOCKET_OFFSET = 20
    LINE_SIZE = 15

    def __init__(self, node, parent):
        super().__init__(node.node_name, parent=parent)

        self.font = QFont()
        self.font.setBold(True)
        self.setFont(self.font)

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


class ValueNodeWidget(NodeWidget):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.edit = QLineEdit(parent=parent)
        self.edit.move(self.pos().x(), self.pos().y() + self.SOCKET_OFFSET + len(self.socket_labels) * self.LINE_SIZE)

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


class NodeEditor(QWidget):

    def __init__(self, nodes=None):
        super().__init__()
        self.sockets = []
        self.node_widgets = []
        self.x = 0
        self.selected = None

        if nodes is not None:
            self.add_nodes(nodes)

        self.setWindowTitle("Node Editor")

    def select(self, selection):
        if self.selected is not None:
            self.selected.deselect()
        self.selected = selection
        self.selected.select()

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent):
            key_text = event.text()
            print(f"Last Key Pressed: {key_text}")
            if key_text in ["\n", "\r"]:
                self.selected.cut()
                self.selected.setParent(None)
                self.selected = None

    def add_nodes(self, nodes):
        for node in nodes:
            if type(node) == ValueProperty:
                label = ValueNodeWidget(node, parent=self)
            elif type(node) == AnimatedProperty:
                label = AnimatedPropertyNodeWidget(node, parent=self)
            else:
                label = NodeWidget(node, parent=self)
            self.node_widgets.append(label)
            self.x += 1


class RenderGui(QMainWindow):

    def __init__(self, frame_renderer: Renderer):
        super().__init__()
        self.frame_renderer = frame_renderer

        self.setWindowTitle("NightmareMachine")

        self.pause_button = QPushButton("Pause", self)

        def on_pause():
            self.frame_renderer.pause_unpause()
        self.pause_button.clicked.connect(on_pause)
        self.pause_button.setCheckable(True)

        self.reset_button = QPushButton("Reset", self)

        def on_reset():
            self.frame_renderer.reset()
            self.text_widget.setText(f"frame: 0 / {self.frame_renderer.stop_frame}")
        self.reset_button.clicked.connect(on_reset)

        self.render_button = QPushButton("Render", self)

        def on_render():
            self.frame_renderer.render()
        self.render_button.clicked.connect(on_render)
        self.render_button.setCheckable(True)

        self.forward_button = QPushButton("Backwards", self)

        self.repeat_button = QPushButton("Don't Repeat", self)
        self.repeat_button.setCheckable(True)

        def on_repeat():
            self.frame_renderer.repeat_unrepeat()

        self.repeat_button.clicked.connect(on_repeat)

        def on_forward():
            self.frame_renderer.forwads_backwards()

        self.forward_button.clicked.connect(on_forward)
        self.forward_button.setCheckable(True)

        self.line_edit = QLineEdit("", parent=self)

        self.set_frame_button = QPushButton("Set Frame", self)

        def on_set_frame():
            text = self.line_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_frame(int(float(text)))
                self.text_widget.setText(f"frame: {int(float(text))} / {self.frame_renderer.stop_frame}")
        self.set_frame_button.clicked.connect(on_set_frame)

        self.stopframe_edit = QLineEdit("", parent=self)

        self.stopframe_button = QPushButton("Set Stop Frame", self)

        def on_set_stop_frame():
            text = self.stopframe_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_stopframe(int(float(text)))
        self.stopframe_button.clicked.connect(on_set_stop_frame)

        self.text_widget = QLabel("0")
        self.frame_renderer.on_frame = lambda frame:  self.text_widget.setText(f"frame: {frame} / {self.frame_renderer.stop_frame}")

        layout = QVBoxLayout()
        layout.addWidget(self.reset_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.render_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.repeat_button)
        layout.addWidget(self.set_frame_button)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.stopframe_button)
        layout.addWidget(self.stopframe_edit)
        layout.addWidget(self.text_widget)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setFixedSize(QSize(400, 300))

        self.editor = NodeEditor()

    def run(self, app, strips: List[Strip], fps_wait=False):
        self.editor.add_nodes(strips[0].compositor.get_all_subnodes())
        self.frame_renderer.run(strips, fps_wait)
        self.show()
        self.editor.show()
        app.exec()
