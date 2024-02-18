class AnimatedProperty:

    def __init__(self, initial_value):
        self.keyframes = []
        self.initial_value = initial_value
        self.frame = -1
        self.animation_style = "Linear"

    def set_key_frame(self, frame, value):
        self.keyframes.append((frame, value))
        self.keyframes = sorted(self.keyframes, key=lambda k: k[0])

    def linear_interp(self):
        if len(self.keyframes) == 0:
            return self.initial_value

        for k, (frame, value) in enumerate(self.keyframes):
            if self.frame < frame:
                if k == 0:
                    return self.initial_value
                else:
                    frame_b, val_b = self.keyframes[k - 1]
                    frame_a, val_a = self.keyframes[k]

                    length = frame_a - frame_b
                    point_on_line = self.frame / length

                    return val_b * (1-point_on_line) + val_a * point_on_line
        else:
            return self.keyframes[-1][1]

    def get(self):
        if self.animation_style == "Linear":
            return self.linear_interp()
        else:
            raise ValueError(f"Unknown animation style {self.animation_style}")

    def set_frame(self, frame):
        self.frame = frame

    def is_animated(self):
        return len(self.keyframes) != 0

