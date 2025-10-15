import torch
import math
from src.Nodes.node import Node
from src.Nodes.node import NodeSocket
from src.interactables.node_table import NodeTable
from src.Nodes.internal.internal_value import InternalValue


class AnimatedProperty(Node):

    def __init__(self):
        self.keyframes_interactable = NodeTable()
        self.keyframes = []
        self.initial_value = NodeSocket("Initial Value", default=InternalValue(0))
        self.animation_style = "Linear"
        super().__init__([self.initial_value], [self.keyframes_interactable], "Used to animate a value")

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.keyframes = [eval(x) for x in self.keyframes_interactable.get_values()]

    def linear_interp(self):
        if len(self.keyframes) == 0:
            return self.initial_value.get().produce()

        for k, (frame, value) in enumerate(self.keyframes):
            position = frame - self.frame_counter.get()
            if position > 0:
                if k == 0:
                    if type(self.keyframes[0][1]) is list:
                        return torch.tensor(self.keyframes[0][1], device=self.defaults.device)
                    return self.keyframes[0][1]
                else:
                    frame_b, val_b = self.keyframes[k - 1]
                    frame_a, val_a = self.keyframes[k]

                    if type(val_a) is list:
                        val_a = torch.tensor(val_a, device=self.defaults.device)

                    if type(val_b) is list:
                        val_b = torch.tensor(val_b, device=self.defaults.device)

                    length = frame_a - frame_b
                    point_on_line = position / length

                    return val_b * point_on_line + val_a * (1-point_on_line)
        else:
            out = self.keyframes[-1][1]
            if type(out) is list:
                out = torch.tensor(out, device=self.defaults.device)
            return out

    def sin_interp(self):
        if len(self.keyframes) == 0:
            return self.initial_value.get().get()

        for k, (frame, value) in enumerate(self.keyframes):
            position = frame - self.frame_counter.get()
            if position > 0:
                if k == 0:
                    return self.keyframes[0][1]
                else:
                    frame_b, val_b = self.keyframes[k - 1]
                    frame_a, val_a = self.keyframes[k]

                    length = frame_a - frame_b
                    point_on_line = position / length
                    point_on_line = (math.cos(point_on_line * torch.pi + torch.pi) + 1) / 2

                    return val_b * point_on_line + val_a * (1-point_on_line)
        else:
            return self.keyframes[-1][1]

    def nearest_neighbor(self):
        if len(self.keyframes) == 0:
            return self.initial_value.get().get()

        for k, (frame, value) in enumerate(self.keyframes):
            position = frame - self.frame_counter.get()
            if position > 0:
                if k == 0:
                    return self.keyframes[0][1]
                else:
                    frame_b, val_b = self.keyframes[k - 1]
                    frame_a, val_a = self.keyframes[k]

                    length = frame_a - frame_b
                    point_on_line = position / length

                    if point_on_line < 0.5:
                        return val_b
                    else:
                        return val_a

        else:
            return self.keyframes[-1][1]

    def produce(self):
        if self.animation_style == "Linear":
            interp = self.linear_interp()
        elif self.animation_style == "Sine":
            interp = self.sin_interp()
        elif self.animation_style == "NearestNeighbor":
            interp = self.nearest_neighbor()
        else:
            raise ValueError(f"Unknown animation style {self.animation_style}")

        return interp
