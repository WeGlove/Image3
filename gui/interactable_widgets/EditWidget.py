from PyQt6.QtWidgets import QLineEdit
from gui.interactable_widgets.interactableWidget import InteractableWidget


class EditWidget(InteractableWidget):

    def __init__(self, parent, node, k, line_offset):
        super().__init__(line_offset)
        self.edit_field = QLineEdit(parent=parent)
        self.k = k

        def get_on_edit():
            def on_edit(_):
                self.node.get_interactable(self.k).set(self.edit_field.text())

            return on_edit

        self.node = node
        self.edit_field.textEdited.connect(get_on_edit())
        self.edit_field.show()
        self.edit_field.move(0, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)

    def move(self, x, y):
        self.edit_field.move(x, y)
