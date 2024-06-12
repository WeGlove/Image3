from typing import List
from strips.strip import Strip
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from renderer import Renderer


class NodeEditor(QWidget):

    def __init__(self, nodes=None):
        super().__init__()
        self.nodes = []
        self.labels = []
        self.x = 0

        if nodes is not None:
            self.add_nodes(nodes)

    def add_nodes(self, nodes):
        self.nodes.extend(nodes)
        self.labels = []
        for node in self.nodes:
            self.labels.append(QLabel(node.node_name, parent=self))
            self.labels[self.x].move(self.x * 110, 10)
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
