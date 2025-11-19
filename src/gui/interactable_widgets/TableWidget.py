import logging
import traceback

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from src.gui.interactable_widgets.interactableWidget import InteractableWidget


class TableWidget(InteractableWidget):

    BUTTON_SPACE = 70

    def __init__(self, parent, node, k, line_offset):
        super().__init__(parent, node, k, line_offset)
        self.logger = logging.getLogger(__name__)
        self.add_button = QPushButton("Add", parent=parent)
        self.remove_button = QPushButton("Remove", parent=parent)
        self.cycle_button = QPushButton("Cycle", parent=parent)
        self.edit_fields = []
        self.line_strs = []

        def to_json():
            return str([str(l_str) for l_str in self.line_strs])

        def get_on_edit(k):
            def on_edit(_):
                edit_field = self.edit_fields[k]
                self.line_strs[k] = edit_field.text()
                self.node.get_interactable(self.k).set(to_json())

            return on_edit

        def on_add_button_press(_):
            self.node.get_interactable(self.k).set("")
            edit_field = QLineEdit(parent=parent)
            edit_field.move(0, self.SOCKET_OFFSET + (self.line_offset + 1 + len(self.edit_fields)) * self.LINE_SIZE)
            edit_field.textEdited.connect(get_on_edit(len(self.edit_fields)))
            edit_field.show()
            self.edit_fields.append(edit_field)
            self.line_strs.append("")

        self.add_button.move(0, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)
        self.add_button.clicked.connect(on_add_button_press)
        self.add_button.show()

        def on_remove_button_press(_):
            if len(self.edit_fields) == 0:
                return
            edit_field = self.edit_fields[-1]
            edit_field.setParent(None)
            self.edit_fields = self.edit_fields[:-1]
            self.line_strs = self.line_strs[:-1]

        self.remove_button.move(self.BUTTON_SPACE, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)
        self.remove_button.clicked.connect(on_remove_button_press)
        self.remove_button.show()

        def on_cycle_button_press(_):
            if len(self.edit_fields) < 2:
                return

            text_0 = self.edit_fields[0].text()
            for k, edit_field in enumerate(self.edit_fields[:-1]):
                edit_field.setText(self.edit_fields[k+1].text())
                self.line_strs[k] = edit_field.text()

            self.edit_fields[-1].setText(text_0)
            self.line_strs[-1] = text_0

        self.cycle_button.move(self.BUTTON_SPACE*2, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)
        self.cycle_button.clicked.connect(on_cycle_button_press)
        self.cycle_button.show()

        def update():
            for edit_field in self.edit_fields:
                edit_field.setParent(None)
            self.edit_fields = []
            self.line_strs = []

            x = self.node.interactables[self.k].get()

            try:
                out_list = eval(x)
                for k, y in enumerate(out_list):
                    on_add_button_press(...)
                    self.edit_fields[k].setText(y)
                    self.line_strs[k] = y
                self.node.interactables[self.k].set(to_json())
            except Exception:
                self.logger.error(traceback.format_exc())
                self.logger.error(f"Node Name: {self.node.get_node_name()} Error String: {x}")

        self._update = update

    def update(self):
        self._update()

    def move(self, x, y):
        self.add_button.move(x, y)
        self.remove_button.move(x + self.BUTTON_SPACE, y)
        self.cycle_button.move(x + self.BUTTON_SPACE*2, y)
        for k, edit_field in enumerate(self.edit_fields):
           edit_field.move(x, y + (k+1) * self.LINE_SIZE)

    def cut(self):
        for edit_field in self.edit_fields:
            edit_field.setParent(None)
        self.add_button.setParent(None)
        self.remove_button.setParent(None)
        self.cycle_button.setParent(None)
