import logging
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QApplication
from src.renderer import Renderer
from src.gui.node_editor import NodeEditor
from src.factories import get_system_factory
from src.patch import Patch


class RenderGui(QMainWindow):

    def __init__(self, frame_renderer: Renderer, node_factories):
        self.app = QApplication([])
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.frame_renderer = frame_renderer
        system_factory = get_system_factory(frame_renderer.device)
        self.node_factories = [system_factory] + node_factories

        out = system_factory.instantiate("Output")
        self.patch = Patch(out)

        self.setWindowTitle("NightmareMachine")

        self.pause_button = QPushButton("Pause", self)

        def on_pause():
            self.logger.info("Pause")
            self.frame_renderer.pause_unpause()
        self.pause_button.clicked.connect(on_pause)
        self.pause_button.setCheckable(True)

        self.reset_button = QPushButton("Reset", self)

        def on_reset():
            self.logger.info("Reset")
            self.frame_renderer.reset()
            self.text_widget.setText(self._get_frame_text(0))
        self.reset_button.clicked.connect(on_reset)

        self.render_button = QPushButton("Render", self)

        def on_render():
            self.logger.info("Render")
            self.frame_renderer.render()
        self.render_button.clicked.connect(on_render)
        self.render_button.setCheckable(True)

        self.forward_button = QPushButton("Backwards", self)

        self.repeat_button = QPushButton("Don't Repeat", self)
        self.repeat_button.setCheckable(True)

        def on_repeat():
            self.logger.info("Repeat")
            self.frame_renderer.repeat_unrepeat()

        self.repeat_button.clicked.connect(on_repeat)

        def on_forward():
            self.logger.info("Forward")
            self.frame_renderer.forwads_backwards()

        self.forward_button.clicked.connect(on_forward)
        self.forward_button.setCheckable(True)

        self.line_edit = QLineEdit("", parent=self)

        self.set_frame_button = QPushButton("Set Frame", self)

        def on_set_frame():
            self.logger.info("Set Frame")
            text = self.line_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_frame(int(float(text)))
                self.text_widget.setText(self._get_frame_text(int(float(text))))
        self.set_frame_button.clicked.connect(on_set_frame)

        self.stopframe_edit = QLineEdit("", parent=self)

        self.stopframe_button = QPushButton("Set Stop Frame", self)

        def on_set_stop_frame():
            self.logger.info("Set Stop Frame")
            text = self.stopframe_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_stopframe(int(float(text)))
        self.stopframe_button.clicked.connect(on_set_stop_frame)

        self.text_widget = QLabel("0")
        self.frame_renderer.on_frame = lambda frame: self.text_widget.setText(self._get_frame_text(frame))

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

        self.editor = NodeEditor(self.node_factories, self.patch)

    def run(self, fps_wait=False):
        self.editor.add_nodes(self.patch.get_root().get_all_subnodes())
        self.frame_renderer.run(self.patch, fps_wait)
        self.show()
        self.editor.show()
        self.app.exec()

    def _get_frame_text(self, frame):
        return f"frame: {frame} / {self.frame_renderer.stop_frame}, {frame/self.frame_renderer.fps:.2f}"
