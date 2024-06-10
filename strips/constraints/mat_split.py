import torch
from Nodes.constraint import Constraint


class MatSplit(Constraint):

    def __init__(self, constraints):
        super().__init__()
        self.constraints = constraints

    def constrain(self, interp):
        interps = []
        for k, constrain in enumerate(self.constraints):
            out_interp = constrain.constrain(interp[k])
            interps.append(out_interp)

        mat = torch.stack(interps)
        return mat

    def get_animated_properties(self, visitor):
        animated_properties = [constraint.get_animated_properties(visitor + "_" + f"MatSplit:Constraint-{k}") for k, constraint in enumerate(self.constraints)]
        out_dict = {}
        for animated_property in animated_properties:
            out_dict.update(animated_property)
        return out_dict


