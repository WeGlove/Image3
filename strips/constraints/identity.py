from Nodes.constraint import Constraint


class Identity(Constraint):

    def get_animated_properties(self, visitors):
        return []

    def constrain(self, interp):
        return interp

