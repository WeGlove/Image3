from typing import List
from strips.strip import Strip
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from alpha_comp.renderer import Renderer


class RenderGui(QMainWindow):

    def __init__(self, frame_renderer: Renderer):
        super().__init__()
        self.frame_renderer = frame_renderer

        self.setWindowTitle("NightmareMachine")

        self.pause_button = QPushButton("Pause", self)

        def on_pause():
            self.frame_renderer.pause_unpause()
        self.pause_button.clicked.connect(on_pause)

        self.reset_button = QPushButton("Reset", self)

        def on_reset():
            self.frame_renderer.reset()
        self.reset_button.clicked.connect(on_reset)

        self.render_button = QPushButton("Render", self)

        def on_render():
            self.frame_renderer.render()
        self.render_button.clicked.connect(on_render)

        self.forward_button = QPushButton("Forward", self)

        def on_forward():
            self.frame_renderer.forwads_backwards()

        self.forward_button.clicked.connect(on_forward)

        self.text_widget = QLabel("0")
        self.frame_renderer.on_frame = lambda frame:  self.text_widget.setText(f"frame: {frame}")

        layout = QVBoxLayout()
        layout.addWidget(self.reset_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.render_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.text_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setFixedSize(QSize(400, 300))

    def run(self, app, strips: List[Strip], fps_wait=False):
        self.frame_renderer.run(strips, fps_wait)
        self.show()
        app.exec()
