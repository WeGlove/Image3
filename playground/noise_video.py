import math
import os.path
from alpha_comp.compositors.Leaves.noise import Noise
from alpha_comp.compositors.Leaves.two_point_weights import TwoPointWeights
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
import torch


if __name__ == "__main__":
    path = os.path.join("../playground", "mountains")
    out_path = os.path.join(os.path.join("C:", "Users", "tobia", "Desktop", "out_out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    print("loading images")
    imgs = [torch.tensor(np.array(Image.open(os.path.join(path, file))), device=cuda) for file in os.listdir(path)]
    print("loaded images")

    with ((torch.cuda.device(0))):
        strips = []

        images = []
        for i, file in enumerate(os.listdir(path)):
            print(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=cuda)
            images.append(img)

        strip = MassComposition(1000, images, TwoPointWeights(torch.tensor([0, 0], device=cuda), torch.tensor([1920, 1080], device=cuda), weight_a=0.5))
        a = strip.get_animated_properties()["_RadialsWarp:PointA"]
        a.set_key_frame(0, torch.tensor([0, 0], device=cuda))
        a.set_key_frame(1000, torch.tensor([0, 1080], device=cuda))

        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        renderer.run(strips, fps_wait=True)
