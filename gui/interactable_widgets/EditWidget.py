from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLineEdit


class EditWidget(QWidget):

    def __init__(self, parent, node, k):
        super().__init__(parent=parent)
        self.edit_field = QLineEdit(parent=parent)
        self.k = k

        def get_on_edit():
            def on_edit(_):
                self.node.get_interactable(self.k).set(self.edit_field.text())

            return on_edit

        self.node = node
        self.edit_field.clicked.connect(get_on_edit())
