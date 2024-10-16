import traceback

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from gui.interactable_widgets.interactableWidget import InteractableWidget


class TableWidget(InteractableWidget):

    BUTTON_SPACE = 70

    def __init__(self, parent, node, k, line_offset):
        super().__init__(parent, node, k, line_offset)
        self.add_button = QPushButton("Add", parent=parent)
        self.remove_button = QPushButton("Remove", parent=parent)
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
            print(self.edit_fields, self.line_strs)
            edit_field = self.edit_fields[-1]
            edit_field.setParent(None)
            self.edit_fields = self.edit_fields[:-1]
            self.line_strs = self.line_strs[:-1]
            print(self.edit_fields, self.line_strs)
            print("++++++++++++++++++++++++")

        self.remove_button.move(self.BUTTON_SPACE, self.SOCKET_OFFSET + self.line_offset * self.LINE_SIZE)
        self.remove_button.clicked.connect(on_remove_button_press)
        self.remove_button.show()

        def update():
            for edit_field in self.edit_fields:
                edit_field.setParent(None)
            self.edit_fields = []
            self.line_strs = []

            x = self.node.interactables[self.k].get()

            try:
                out_list = eval(x)
                for k, y in enumerate(out_list):
                    print(k, y)
                    on_add_button_press(...)
                    self.edit_fields[k].setText(y)
                    self.line_strs[k] = y
            except Exception:
                print(traceback.format_exc())

        self._update = update

    def update(self):
        self._update()
        print(self.line_strs, self.edit_fields)

    def move(self, x, y):
        self.add_button.move(x, y)
        self.remove_button.move(x + self.BUTTON_SPACE, y)
        for k, edit_field in enumerate(self.edit_fields):
           edit_field.move(x, y + (k+1) * self.LINE_SIZE)

    def cut(self):
        for edit_field in self.edit_fields:
            edit_field.setParent(None)
        self.add_button.setParent(None)
