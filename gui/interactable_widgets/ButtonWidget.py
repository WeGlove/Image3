from PyQt6.QtWidgets import QPushButton, QWidget


class ButtonWidget(QWidget):

    def __init__(self, parent, node, k):
        super().__init__(parent=parent)
        self.button = QPushButton(parent=self)
        self.k = k

        def get_on_button_press():
            def on_press(_):
                self.node.get_interactable(self.k).toggle()

            return on_press

        self.node = node
        self.button.clicked.connect(get_on_button_press())
        self.button.show()

        #pos = self.pos()
        #edit_field.move(pos.x(), pos.y() + self.SOCKET_OFFSET + j * self.LINE_SIZE + len(self.socket_labels) * self.LINE_SIZE)
