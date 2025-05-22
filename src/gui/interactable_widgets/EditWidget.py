from PyQt6.QtWidgets import QLineEdit
from src.gui.interactable_widgets.interactableWidget import InteractableWidget


class EditWidget(InteractableWidget):

    def __init__(self, parent, node, k, line_offset):
        super().__init__(parent, node, k, line_offset)
        self.edit_field = QLineEdit(parent=parent)

        def get_on_edit():
            def on_edit(_):
                self.node.get_interactable(self.k).set(self.edit_field.text())

            return on_edit

        self.edit_field.textEdited.connect(get_on_edit())
        self.edit_field.show()
        self.edit_field.move(0, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)

    def move(self, x, y):
        self.edit_field.move(x, y)

    def cut(self):
        self.edit_field.setParent(None)

    def update(self):
        x = self.node.interactables[self.k].get()
        self.edit_field.setText(str(x))
