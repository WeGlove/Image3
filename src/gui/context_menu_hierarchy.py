from PyQt6.QtWidgets import QMenu
import traceback
import logging


class ContextMenuHierarchy:

    def __init__(self, hierarchy, parent):
        self.parent = parent
        self.hierarchy = hierarchy
        self.menu, self.sub_hierarchies = self.load_submenus(self.hierarchy)
        self.logger = logging.getLogger(__name__)

    def load_submenus(self, hierarchy):
        current_menu = QMenu(self.parent)
        sub_hierarchies = dict()

        for value in hierarchy:
            if type(value) == tuple:
                sub_hierarchy_name = value[0]
                sub_hierarchy = value[1]
                sub_hierarchies[sub_hierarchy_name] = ContextMenuHierarchy(sub_hierarchy, self.parent)
                current_menu.addAction(value[0])
            else:
                current_menu.addAction(value)

        return current_menu, sub_hierarchies

    def exec(self, event):
        self.menu.move(self.parent.mapToGlobal(event.pos()))
        action = self.menu.exec()
        if action is None:
            raise ValueError("Aborted selection")

        action_text = action.text()

        if action_text in self.hierarchy:
            return [action_text]

        if action_text not in self.sub_hierarchies:
            raise ValueError("Unknown sub hierarchy")

        sub_hierarchy = self.sub_hierarchies[action_text]

        sub_hierarchy.menu.move(self.parent.mapToGlobal(event.pos()))
        action_trace = sub_hierarchy.exec(event)
        return [action_text] + action_trace
