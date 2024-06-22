import json
import os.path
import traceback
from typing import List
from PyQt6.QtWidgets import QWidget, QLineEdit, QMenu
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from Nodes.value_property import ValueProperty
import torch
from Nodes.animated_property import AnimatedProperty
from Nodes.alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs
from node_factory import NodeFactory
from gui.node_widgets import NodeWidget, AnimatedPropertyNodeWidget
from Nodes.out import Out


class NodeEditor(QWidget):

    SAVE_KEY = "s"
    LOAD_KEY = "l"

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
        self.act_line = self.menu.addAction("Line")
        self.act_pointMapComb = self.menu.addAction("PointMapComb")
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
            if ord(key_text) == 127:  # This is the delete button
                self.selected.cut()
                self.selected = None
            elif key_text[0] == self.SAVE_KEY:
                self.save("out.nmm")
            elif key_text[0] == self.LOAD_KEY:
                self.load("out.nmm")

    def add_nodes(self, nodes):
        for node in nodes:
            if type(node) == ValueProperty:
                label = NodeWidget(node, parent=self)
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
            nodes = []
            if action == self.act_point_mapping_min:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.pointMappingMin()
                nodes.append(node)
            elif action == self.act_animated_property:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.animated_property()
                nodes.append(node)
            elif action == self.act_value_property:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.value_property()
                nodes.append(node)
            elif action == self.act_line:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.line()
                nodes.append(node)
            elif action == self.act_pointMapComb:
                self.menu.move(self.mapToGlobal(event.pos()))
                node = self.factory.pointMapComb()
                nodes.append(node)

            self.add_nodes(nodes)
        except Exception:
            print(traceback.format_exc())

    def mousePressEvent(self, event):
        focused_widget = QGuiApplication.focusObject()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        super().mousePressEvent(event)

