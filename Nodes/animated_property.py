import torch
import math


class AnimatedProperty:

    def __init__(self, initial_value):
        self.keyframes = []
        self.initial_value = initial_value
        self.frame = -1
        self.animation_style = "Linear"
        self.constraint = None

    def set_anim_style(self, style):
        self.animation_style = style

    def set_key_frame(self, frame, value):
        self.keyframes.append((frame, value))
        self.keyframes = sorted(self.keyframes, key=lambda k: k[0])

    def linear_interp(self):
        if len(self.keyframes) == 0:
            return self.initial_value

        for k, (frame, value) in enumerate(self.keyframes):
            position = frame - self.frame
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
            return self.initial_value

        for k, (frame, value) in enumerate(self.keyframes):
            position = frame - self.frame
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
            return self.initial_value

        for k, (frame, value) in enumerate(self.keyframes):
            position = frame - self.frame
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

    def get(self):
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

    def set_next(self):
        self.frame += 1
        if self.constraint is not None:
            self.constraint.set_next()

    def set_previous(self):
        self.frame -= 1
        if self.constraint is not None:
            self.constraint.set_previous()

    def set_frame(self, frame):
        self.frame = frame
        if self.constraint is not None:
            self.constraint.set_frame(frame)

    def is_animated(self):
        return len(self.keyframes) != 0 or self.is_constrained()

    def set_constraint(self, constraint):
        self.constraint = constraint

    def is_constrained(self):
        return self.constraint is not None

    def get_animated_properties(self, visitor):
        if self.constraint is None:
            return {}
        else:
            return self.constraint.get_animated_properties(visitor + "_" + "AnimatedProperty:Constraint")

    def to_dict(self):
        return {"AnimatedProperty": self.constraint if self.constraint is None else self.constraint.to_dict(),
                "Keyframe": self.keyframes}
