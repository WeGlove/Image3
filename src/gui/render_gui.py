import logging
import numpy as np
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QApplication, QHBoxLayout, QFileDialog
from src.renderer import Renderer
from src.gui.node_editor import NodeEditor
from src.factories import get_system_factory
from src.Nodes.system.patch import Patch
from typing import List
from src.node_factory import NodeFactory


class RenderGui(QMainWindow): # Future TODO, set FPS Button

    OUT_ID = "Out"

    def __init__(self, frame_renderer: Renderer, node_factories: List[NodeFactory]):
        self.app = QApplication([])
        super().__init__()
        self.logger = logging.getLogger(__name__)

        # Render Variables
        self.frame_renderer = frame_renderer
        system_factory = get_system_factory()
        self.node_factories = [system_factory] + node_factories
        out = system_factory.instantiate(self.OUT_ID)
        out.set_node_name(self.OUT_ID)
        self.patch = Patch()
        self.patch.add_node(out)
        self.patch.set_root(out)

        # Metrics
        self.frame_times = []
        self.render_time = 0
        self.current_frame = 0

        """GUI Settings"""
        self.setWindowTitle("Nightmare Machine")

        def on_frame(frame, frame_time):
            """
            Feedback function from renderer
            :param frame:
            :param frame_time:
            :return:
            """
            self.frame_times.append(frame_time)
            self.frame_times = self.frame_times[int(-self.frame_renderer.fps):]
            if len(self.frame_times) > 1:
                self.render_time += self.frame_times[-1] - self.frame_times[-2]
            self.current_frame = frame
            self.update_fps_labels()
        self.frame_renderer.on_frame = on_frame

        self.reset_button = QPushButton("Reset", self)

        # Row 1

        def on_reset():
            self.logger.info("Reset")
            self.frame_renderer.reset()
            self.update_fps_labels()
        self.reset_button.clicked.connect(on_reset)

        # Row 2

        self.backwards_button = QPushButton("Backwards", self)

        def on_backward():
            """Runs renderer backwards"""
            self.logger.info("Backwards")
            self.frame_renderer.backwards()
            self.frame_renderer.unpause()
            self.set_player_toggle_states()

        self.backwards_button.clicked.connect(on_backward)
        self.backwards_button.setCheckable(True)

        self.pause_button = QPushButton("Pause", self)

        def on_pause():
            """Pauses the renderer"""
            self.logger.info("Pause")
            self.frame_renderer.pause()
            self.pause_button.setChecked(self.frame_renderer.is_paused)
            self.set_player_toggle_states()
        self.pause_button.clicked.connect(on_pause)
        self.pause_button.setCheckable(True)
        self.pause_button.setChecked(self.frame_renderer.is_paused)

        self.forwards_button = QPushButton("Forwards", self)

        def on_forward():
            """Runs the renderer forwards"""
            self.logger.info("Forwards")
            self.frame_renderer.forwards()
            self.frame_renderer.unpause()
            self.set_player_toggle_states()
        self.forwards_button.clicked.connect(on_forward)
        self.forwards_button.setCheckable(True)

        # Row 3

        self.render_button = QPushButton("Render", self)

        def on_render():
            self.logger.info("Render")
            self.frame_renderer.save_not_save()
            self.render_button.setChecked(self.frame_renderer.save)
        self.render_button.clicked.connect(on_render)
        self.render_button.setCheckable(True)
        self.render_button.setChecked(self.frame_renderer.save)

        self.repeat_button = QPushButton("Don't Repeat", self)

        def on_repeat():
            self.logger.info("Repeat")
            self.frame_renderer.repeat_unrepeat()
        self.repeat_button.setCheckable(True)
        self.repeat_button.clicked.connect(on_repeat)

        # Row 4

        self.startframe_button = QPushButton("Set Start Frame", self)

        def on_set_startframe():
            self.logger.info("Set Start Frame")
            text = self.line_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_startframe(int(float(text)))
                self.update_fps_labels()
        self.startframe_button.clicked.connect(on_set_startframe)

        self.set_frame_button = QPushButton("Set Current Frame", self)

        def on_set_frame():
            self.logger.info("Set Current Frame")
            text = self.set_frame_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_frame(int(float(text)))
                self.update_fps_labels()
        self.set_frame_button.clicked.connect(on_set_frame)

        self.stopframe_button = QPushButton("Set Stop Frame", self)

        def on_set_stop_frame():
            self.logger.info("Set Stop Frame")
            text = self.stopframe_edit.text()
            if text.isnumeric():
                self.frame_renderer.set_stopframe(int(float(text)))
                self.update_fps_labels()
        self.stopframe_button.clicked.connect(on_set_stop_frame)

        # Row 5

        self.startframe_edit = QLineEdit("", parent=self)
        self.set_frame_edit = QLineEdit("", parent=self)
        self.stopframe_edit = QLineEdit("", parent=self)

        # Row 6

        self.img_format_button = QPushButton("Set Img Format", self)

        def on_img_format():
            self.logger.info(f"Setting image format {self.img_format_widget.text()}")
            self.frame_renderer.set_img_format(self.img_format_widget.text())
        self.img_format_button.clicked.connect(on_img_format)

        # Row 7

        self.img_format_widget = QLineEdit("png")

        # Row 8

        self.path_button = QPushButton("Set Out Path", self)

        def on_set_path():
            save_path = QFileDialog.getExistingDirectory(self)
            self.logger.info(f"Setting path {save_path}")
            self.frame_renderer.set_save_path(save_path)
        self.path_button.clicked.connect(on_set_path)

        # Row 9

        self.text_widget = QLabel()

        # Layout

        player_layout = QHBoxLayout()
        player_layout.addWidget(self.backwards_button)
        player_layout.addWidget(self.pause_button)
        player_layout.addWidget(self.forwards_button)

        frame_set_layout = QHBoxLayout()
        frame_set_layout.addWidget(self.startframe_button)
        frame_set_layout.addWidget(self.set_frame_button)
        frame_set_layout.addWidget(self.stopframe_button)

        frame_set_edit_layout = QHBoxLayout()
        frame_set_edit_layout.addWidget(self.startframe_edit)
        frame_set_edit_layout.addWidget(self.set_frame_edit)
        frame_set_edit_layout.addWidget(self.stopframe_edit)

        render_settings_layout = QHBoxLayout()
        render_settings_layout.addWidget(self.render_button)
        render_settings_layout.addWidget(self.repeat_button)

        layout = QVBoxLayout()
        layout.addWidget(self.reset_button)
        layout.addLayout(player_layout)
        layout.addLayout(render_settings_layout)
        layout.addLayout(frame_set_layout)
        layout.addLayout(frame_set_edit_layout)
        layout.addWidget(self.img_format_button)
        layout.addWidget(self.img_format_widget)
        layout.addWidget(self.path_button)
        layout.addWidget(self.text_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setFixedSize(QSize(500, 300))
        self.update_fps_labels()

        self.editor = NodeEditor(self.node_factories, self.patch)

    def run(self):
        """
        Run the GUI
        :return:
        """
        self.frame_renderer.run(self.patch)
        self.show()
        self.editor.show()
        self.app.exec()

    def _live_fps(self):
        """
        Estimates current FPS
        :return:
        """
        if len(self.frame_times) == 0:
            return 0
        frame_time_diff = np.diff(self.frame_times)
        return 1/np.mean(frame_time_diff)

    def set_player_toggle_states(self):
        """
        Sets togglable buttons in Player based on frame renderer.
        :return:
        """
        if not self.frame_renderer.is_paused:
            self.forwards_button.setChecked(self.frame_renderer.is_forward)
            self.backwards_button.setChecked(not self.frame_renderer.is_forward)
        else:
            self.forwards_button.setChecked(False)
            self.backwards_button.setChecked(False)
        self.pause_button.setChecked(self.frame_renderer.is_paused)

    def update_fps_labels(self):
        """
        Updates the FPS label at the bottom
        :return:
        """
        self.text_widget.setText(f"frame: {self.frame_renderer.start_frame} - {self.current_frame} / {self.frame_renderer.stop_frame}, "
                                 f"Render Time: {self.current_frame/self.frame_renderer.fps:.2f}, Real Time: {self.render_time:.2f}, FPS: {self._live_fps():.2f}")
