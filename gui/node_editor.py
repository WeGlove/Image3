import json
import os.path
import traceback
from typing import Dict, List
from PyQt6.QtWidgets import QWidget, QLineEdit, QMenu
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from Nodes.system.value_property import ValueProperty
from Nodes.system.animated_property import AnimatedProperty
from node_factory import NodeFactory
from gui.node_widgets import NodeWidget, AnimatedPropertyNodeWidget
from Nodes.system.out import Out


class NodeEditor(QWidget):

    SAVE_KEY = "s"
    LOAD_KEY = "l"

    def __init__(self, factories: List[NodeFactory], strip, nodes=None):
        super().__init__()
        self.sockets = []
        self.node_widgets: Dict[int, NodeWidget] = dict()
        self.x = 0
        self.selected = None
        self.menu = QMenu(self)
        self.menu_acts = []
        self.factory_acts = []

        self.factory_menus = {}
        for factory in factories:
            factory_menu = QMenu(self.menu)
            self.factory_menus[factory.get_factory_name()] = factory_menu

            act = self.menu.addAction(factory.get_factory_name())
            self.menu_acts.append(act)

            for key in factory.in_dict.keys():
                act = factory_menu.addAction(key)
                self.factory_acts.append(act)
        self.factories: Dict[str, NodeFactory] = {factory.get_factory_name(): factory for factory in factories}
        self.device = factories[0].device
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
            if len(key_text) > 0:
                if ord(key_text[0]) == 127:  # This is the delete button
                    del self.node_widgets[self.selected.node.node_id]
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
            self.node_widgets[node.node_id] = label

    def save(self, path):
        widgets = dict()
        for k, node_widget in self.node_widgets.items():
             widgets[k] = node_widget.to_dict()

        with open(os.path.join(path), "w+") as f:
            json.dump(widgets, f, indent=1)

    def load(self, path):
        try:
            with open(os.path.join(path), "r") as f:
                data = json.load(f)

            self.factory.reset()
            for node in self.node_widgets.values():
                node.cut()

            self.node_widgets = dict()

            self.factory.set_next(1 + max([int(node_id) for node_id in data.keys()]))

            for k, node_dict in data.items():
                node = node_dict["Node"]["properties"]
                name = node_dict["Node"]["name"]
                add_node = self.factory.node_from_dict(node, name)
                self.add_nodes([add_node])

            for k, node_dict in data.items():
                socket_widgets = node_dict["Sockets"]
                for j, socket_widget in enumerate(socket_widgets):
                    socket = socket_widget["Socket"]

                    is_connected = socket["Connected"]
                    if not is_connected:
                        continue

                    connected_id = socket["ConnectedID"]
                    for node_widget in self.node_widgets.values():
                        out_id = node_widget.node.node_id
                        if out_id == connected_id:
                            widget_to_connect = node_widget
                            break
                    else:
                        ValueError()

                    in_node_widget = self.node_widgets[int(k)]
                    in_node_widget.socket_labels[j].connect(widget_to_connect)

            for k, node_dict in data.items():
                position = node_dict["Position"]
                self.node_widgets[int(k)].move(position[0], position[1])

            for widget in self.node_widgets.values():
                if type(widget.node) == Out:
                    self.strip.compositor = widget.node

        except Exception:
            print(traceback.format_exc())

    def contextMenuEvent(self, event):
        try:
            action = self.menu.exec()
            out_action = self.factory_menus[action.text()].exec()
            nodes = []

            self.menu.move(self.mapToGlobal(event.pos()))
            node = self.factories[action.text()].instantiate(out_action.text())
            nodes.append(node)

            self.add_nodes(nodes)
        except Exception:
            print(traceback.format_exc())

    def mousePressEvent(self, event):
        focused_widget = QGuiApplication.focusObject()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        super().mousePressEvent(event)

