import json
import logging
import os.path
import traceback
from typing import Dict, List
from src.node_factory import NodeFactory
from src.gui.node_widget import NodeWidget
from src.Nodes.system.out import Out
from PyQt6.QtWidgets import QWidget, QLineEdit
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from PyQt6.QtWidgets import QLabel
from PyQt6 import QtGui
from src.patch import Patch
from src.gui.context_menu_hierarchy import ContextMenuHierarchy


class NodeEditor(QWidget):

    SAVE_KEY = "s"
    LOAD_KEY = "l"
    DELETE_KEY = 127

    WHITE = 0xffffff

    def __init__(self, factories: List[NodeFactory], patch):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.patch = patch
        self.selected = None
        self.factories: Dict[str, NodeFactory] = {factory.get_factory_name(): factory for factory in factories}

        self.context_menu_hierarchy = ContextMenuHierarchy(
            [(factory.factory_name, factory.hierarchy) for factory in factories], self)

        self.label_canvas = QLabel(parent=self)
        self.canvas = QtGui.QPixmap(1920, 1080)
        self.line_pen = QtGui.QPen()
        self.line_pen.setWidth(1)
        self.line_pen.setColor(QtGui.QColor('black'))

        self.setWindowTitle("Node Editor")
        self.resize(192, 108)

        for node in self.patch.get_nodes():
            node_widget = NodeWidget(node, parent=self)
            node.set_gui_ref(node_widget)
        self.redraw_lines()

    def redraw_lines(self):
        self.canvas.fill(self.WHITE)
        self.label_canvas.setPixmap(self.canvas)

        painter = QtGui.QPainter(self.canvas)
        painter.setPen(self.line_pen)

        for node in self.patch.get_nodes():
            node_widget = node.get_gui_ref()
            for node_socket_widget in node_widget.connected_sockets:
                a = node_widget.pos()
                a.setY(a.y() + node_widget.height() / 2)
                b = node_socket_widget.pos()
                b.setY(b.y() + node_socket_widget.height() / 2)

                if a.x() <= b.x():
                    a.setX(a.x() + node_widget.width())
                else:
                    b.setX(b.x() + node_socket_widget.width())
                painter.drawLine(a, b)

        painter.end()
        self.label_canvas.setPixmap(self.canvas)

    def select(self, selection):
        if self.selected is not None:
            self.selected.deselect()
        self.selected = selection
        self.selected.select()

    def delete_selected_node(self):
        try:
            self.logger.info(f"Deleting Node {self.selected.node.node_id}")
            self.patch.remove_node(self.selected.node.node_id)
            self.selected.cut()
            self.selected = None
        except Exception:
            self.logger.error(traceback.format_exc())

    def add_nodes(self, nodes):
        for node in nodes:
            node_widget = NodeWidget(node, parent=self)
            node_widget.move(*node.position.tolist())

    def save(self, path):
        self.logger.info(f"Saving patch to {path}")
        try:
            widgets = {k: v.get_gui_ref().to_dict() for k, v in self.patch.nodes.items()}

            file_dump = {
                "factories": {factory.get_factory_name(): factory.next_id for factory in self.factories.values()},
                "node_widgets": widgets
            }

            with open(os.path.join(path), "w+") as f:
                json.dump(file_dump, f, indent=1)
        except Exception:
            self.logger.error(traceback.format_exc())

    def load(self, path):
        self.logger.info(f"Loading patch from {path}")
        try:
            with open(os.path.join(path), "r") as f:
                data = json.load(f)

            factories = data["factories"]
            data = data["node_widgets"]

            for factory in self.factories.values():
                factory.reset()

            for node in self.patch.get_nodes():
                node.get_gui_ref().cut()

            self.patch = Patch()

            for factory_name, next_id in factories.items():
                self.factories[factory_name].set_next(next_id)

            for k, node_dict in data.items():
                factory_id = node_dict["Node"]["factory_id"]
                add_node = self.factories[factory_id].node_from_dict(node_dict["Node"])
                if add_node is None:
                    continue
                self.add_nodes([add_node])

            for k, node_dict in data.items():
                socket_widgets = node_dict["Sockets"]
                for j, socket_widget in enumerate(socket_widgets):
                    socket = socket_widget["Socket"]

                    is_connected = socket["Connected"]
                    if not is_connected:
                        continue

                    connected_id = socket["ConnectedID"]
                    for node in self.patch.get_nodes():
                        node_widget = node.get_gui_ref()
                        out_id = node_widget.node.node_id
                        if out_id == connected_id:
                            widget_to_connect = node_widget
                            break
                    else:
                        raise ValueError()

                    if node_dict["Node"]["node_id"] not in self.patch.get_node_ids():
                        continue
                    in_node_widget = self.patch.get_node(node_dict["Node"]["node_id"])
                    in_node_widget.socket_labels[j].connect(widget_to_connect) # TODO this is probably broken

            for k, node_dict in data.items():
                position = node_dict["Node"]["position"]
                if k in self.patch.get_node_ids():
                    self.patch.get_node(k).move(position[0], position[1])

            for node in self.patch.get_nodes():
                node_widget = node.get_gui_ref()
                if type(node_widget.node) == Out: # TODO this should be done by the patch itself
                    self.patch.set_root(node)
                    self.logger.info(self.patch.get_root().node_id)

        except Exception:
            self.logger.error(traceback.format_exc())

    """Events"""

    def contextMenuEvent(self, event):
        try:
            try:
                action_trace = self.context_menu_hierarchy.exec(event)
            except ValueError:
                return

            factory_name = action_trace[0]
            node_name = action_trace[-1]
            factory = self.factories[factory_name]

            node = factory.instantiate(node_name)
            node.set_position((event.pos().x(), event.pos().y()))
            self.patch.add_node(node)
            self.add_nodes([node])
        except Exception:
            self.logger.error(traceback.format_exc())

    def mousePressEvent(self, event):
        focused_widget = QGuiApplication.focusObject()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent):
            key_text = event.text()
            if len(key_text) > 0:
                if ord(key_text[0]) == self.DELETE_KEY:
                    self.delete_selected_node()
                elif key_text[0] == self.SAVE_KEY:
                    self.logger.info("Saving Patch")
                    self.save("out.nmm")
                elif key_text[0] == self.LOAD_KEY:
                    self.logger.info("Loading Patch")
                    self.load("out.nmm")
