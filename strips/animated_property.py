import torch


class AnimatedProperty:

    def __init__(self, initial_value):
        self.keyframes = []
        self.initial_value = initial_value
        self.frame = -1
        self.animation_style = "Linear"
        self.function = lambda x: x

    def set_anim_function(self, function):
        self.function = function

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
                    point_on_line = (torch.cos(point_on_line * torch.pi + torch.pi) + 1) / 2

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
            return self.function(interp)
        elif self.animation_style == "Sine":
            interp = self.sin_interp()
            return self.function(interp)
        elif self.animation_style == "NearestNeighbor":
            interp = self.nearest_neighbor()
            return self.function(interp)
        else:
            raise ValueError(f"Unknown animation style {self.animation_style}")

    def set_frame(self, frame):
        self.frame = frame

    def is_animated(self):
        return len(self.keyframes) != 0

