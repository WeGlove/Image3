import json
import os.path
import traceback
from typing import List
from strips.strip import Strip
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMenu
from renderer import Renderer
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from Nodes.value_property import ValueProperty
import torch
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs
from node_factory import NodeFactory
from node_widgets import NodeWidget, AnimatedPropertyNodeWidget, ValueNodeWidget
from Nodes.out import Out


class NodeEditor(QWidget):

    def __init__(self, factory: NodeFactory, strip, nodes=None):
        super().__init__()
        self.sockets = []
        self.node_widgets: List[NodeWidget] = []
        self.x = 0
        self.selected = None
        self.menu = QMenu(self)
        self.act_point_mapping_min = self.menu.addAction("PointMappingMin")
        self.act_animated_property = self.menu.addAction("AnimatedProperty")
        self.act_value_property = self.menu.addAction("ValueProperty")
        self.factory: NodeFactory = factory
        self.device = factory.device
        self.strip = strip

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
            print(f"Last Key Pressed: {key_text}", ord(key_text[0]))
            if ord(key_text) == 127:  # This is the delete button
                self.selected.cut()
                self.selected = None
            elif key_text[0] == "s":
                self.save("out.nmm")
            elif key_text[0] == "l":
                self.load("out.nmm")

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

    def save(self, path):
        widgets = []
        for node_widget in self.node_widgets:
            widgets.append(node_widget.to_dict())

        with open(os.path.join(path), "w+") as f:
            json.dump(widgets, f, indent=1)

    def load(self, path):
        with open(os.path.join(path), "r") as f:
            data = json.load(f)

        self.factory.reset()
        for node in self.node_widgets:
            node.cut()
        self.node_widgets = []

        for node_dict in data:
            node = node_dict["Node"]["properties"]
            name = node_dict["Node"]["name"]
            add_node = self.factory.node_from_dict(node, name)
            self.add_nodes([add_node])

        for k, node_dict in enumerate(data):
            socket_widgets = node_dict["Sockets"]
            for j, socket_widget in enumerate(socket_widgets):
                socket = socket_widget["Socket"]

                is_connected = socket["Connected"]
                if not is_connected:
                    continue

                connected_id = socket["ConnectedID"]
                for node_widget in self.node_widgets:
                    out_id = node_widget.node.node_id
                    if out_id == connected_id:
                        widget_to_connect = node_widget
                        break
                else:
                    ValueError()

                in_node_widget = self.node_widgets[k]
                in_node_widget.socket_labels[j].connect(widget_to_connect)

        for node_dict in data:
            position = node_dict["Position"]
            self.node_widgets[-1].move(position[0], position[1])

        for widget in self.node_widgets:
            if type(widget.node) == Out:
                self.strip.compositor = widget.node

    def contextMenuEvent(self, event):
        try:
            action = self.menu.exec()
            if action == self.act_point_mapping_min:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.pointMappingMin(LineConfigs.get_random(5, torch.tensor([0., 0.], device=self.device), 1., node_id=-1, device=self.device))
                self.add_nodes([node])
            elif action == self.act_animated_property:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.animated_poperty()
                self.add_nodes([node])
            elif action == self.act_value_property:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.value_property()
                self.add_nodes([node])
        except Exception:
            print(traceback.format_exc())

    def mousePressEvent(self, event):
        focused_widget = QGuiApplication.focusObject()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        super().mousePressEvent(event)


class RenderGui(QMainWindow):

    def __init__(self, frame_renderer: Renderer, node_factory, strip):
        super().__init__()
        self.frame_renderer = frame_renderer
        self.node_factory = node_factory

        self.strip = strip

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

        self.editor = NodeEditor(self.node_factory, strip)

    def run(self, app, strips: List[Strip], fps_wait=False):
        self.editor.add_nodes(strips[0].compositor.get_all_subnodes())
        self.frame_renderer.run(strips, fps_wait)
        self.show()
        self.editor.show()
        app.exec()
