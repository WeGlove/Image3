from PyQt6.QtWidgets import QPushButton, QWidget
from gui.interactable_widgets.interactableWidget import InteractableWidget


class ButtonWidget(InteractableWidget):

    def __init__(self, parent, node, k, line_offset):
        super().__init__(parent, node, k, line_offset)
        self.button = QPushButton(parent=parent)

        def get_on_button_press():
            def on_press(_):
                self.node.get_interactable(self.k).toggle()

            return on_press

        self.button.clicked.connect(get_on_button_press())
        self.button.show()

        self.button.move(0, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)

    def move(self, x, y):
        self.button.move(x, y)

    def cut(self):
        self.button.setParent(None)
