import os.path
import numpy as np
from PIL import Image
from Nodes.alpha_comp import Renderer
from Nodes.mass_composition import MassComposition
import torch
from Nodes.alpha_comp.compositors.Leaves.Closeness import Closeness


if __name__ == "__main__":
    path = os.path.join("")
    out_path = os.path.join(os.path.join("C:", "Users", "tobia", "Desktop", "out_out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    with ((torch.cuda.device(0))):
        strips = []

        images = []
        for i, file in enumerate(os.listdir(path)):
            print(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=cuda)
            print(img)
            images.append(img)

        comp = Closeness(images[0])

        strip = MassComposition(16271, images, comp)

        animated_properties = strip.get_animated_properties()
        print(animated_properties)
        weights = animated_properties["MassComposition_Closeness:Weights"]

        weights.set_key_frame(0, torch.tensor([0, 0, 1]))
        weights.set_key_frame(2711, torch.tensor([0, 1, 0]))
        weights.set_key_frame(5422, torch.tensor([0, 1, 1]))
        weights.set_key_frame(8133, torch.tensor([1, 0, 1]))
        weights.set_key_frame(10844, torch.tensor([1, 1, 0]))
        weights.set_key_frame(13555, torch.tensor([1, 1, 1]))
        weights.set_key_frame(16271, torch.tensor([1, 0, 0]))

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
