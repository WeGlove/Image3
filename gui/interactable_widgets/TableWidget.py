from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from gui.interactable_widgets.interactableWidget import InteractableWidget


class TableWidget(InteractableWidget):

    def __init__(self, parent, node, k, line_offset):
        super().__init__(line_offset)
        self.add_button = QPushButton(parent=parent)
        self.edit_fields = []
        self.k = k
        self.line_strs = []

        def to_json():
            return str([f"\"{l_str}\"," for l_str in self.line_strs])

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

        self.node = node
        self.add_button.move(0, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)
        self.add_button.clicked.connect(on_add_button_press)
        self.add_button.show()

    def move(self, x, y):
        self.add_button.move(x, y)
        for k, edit_field in enumerate(self.edit_fields):
           edit_field.move(x, y + (k+1) * self.LINE_SIZE)
