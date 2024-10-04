class FrameCounter:

    def __init__(self, initial_frame=0):
        self.frame = initial_frame
        self.was_set = False
        self.was_reversed = False

    def next(self):
        self.frame += 1
        self.was_set = False
        self.was_reversed = False

    def previous(self):
        self.frame -= 1
        self.was_set = False
        self.was_reversed = True

    def set_frame(self, frame):
        self.frame = frame
        self.was_set = True

    def get(self):
        return self.frame
        self.was_reversed = False
