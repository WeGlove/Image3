from strips.strip import Strip
import torch
import cv2


class MassComposition(Strip):

    def __init__(self, length, images, compositor):
        super().__init__(length)
        self.images = images
        self.compositor = compositor
        self.animated_properties = dict()

    def initialize(self, width, height, fps, initial_frame, initial_image, device):
        self.fps = fps
        self.initial_frame = initial_frame
        self.initial_image = initial_image
        self.device = device
        self.width = width
        self.height = height
        self.animated_properties = self.get_animated_properties()
        self.compositor.initialize(self.width, self.height, len(self.images), self.device)
        new_dict = dict()
        for key, value in self.animated_properties.items():
            if value.is_animated():
                new_dict[key] = self.animated_properties[key]
        self.animated_properties = new_dict
        print(self.animated_properties)

    def produce(self, last_image, frame):
        for animated_property in self.animated_properties.values():
            animated_property.set_frame(frame)

        stack_img = None

        for i, img in enumerate(self.images):
            if stack_img is None:
                stack_img = torch.zeros(img.shape, device=self.device)

            mask = self.compositor.composite(i, img)

            stack_img = stack_img + torch.multiply(img, mask.transpose(0, 1))

        return stack_img

    def free(self):
        for img in self.images:
            del img

        self.compositor.free()

    def get_animated_properties(self):
        return self.compositor.get_animated_properties("")
