import torch
import math
from Nodes.node import Node
from Nodes.value_property import ValueProperty
from Nodes.node import NodeSocket


class AnimatedProperty(Node):

    def __init__(self, node_id, device, frame_counter, initial_value=None, keyframes=None):
        self.keyframes = []
        if keyframes is not None:
            for keyframe in keyframes:
                self.set_key_frame(keyframe[0], keyframe[1])
        self.initial_value = NodeSocket(False, "Initial Value",
                                        ValueProperty(initial_value, node_id, device, frame_counter))
        self.animation_style = "Linear"
        self.constraint = None
        super().__init__(node_id, "", frame_counter, [self.initial_value], device, [])

    def set_anim_style(self, style):
        self.animation_style = style

    def set_key_frame(self, frame, value):
        self.keyframes.append((frame, value))
        self.keyframes = sorted(self.keyframes, key=lambda k: k[0])

    def clear_key_frames(self):
        self.keyframes = []

    def linear_interp(self):
        if len(self.keyframes) == 0:
            return self.initial_value.get().produce()

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

                    return val_b * point_on_line + val_a * (1-point_on_line)
        else:
            return self.keyframes[-1][1]

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

        if self.constraint is not None:
            interp = self.constraint.constrain(interp)

        return interp

    def to_dict(self):
        property_dict = super().to_dict()
        key_frame_list = []
        for (frame, value) in self.keyframes:
            if type(value) == torch.Tensor:
                value = value.tolist()
            key_frame_list.append([frame, value])
        property_dict["properties"]["keyframes"] = key_frame_list
        return property_dict

    @staticmethod
    def get_node_name():
        return "Animated Property"
