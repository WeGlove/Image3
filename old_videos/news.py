import os.path
from alpha_comp.compositors.Leaves.polar_divsion import PolarDivision
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
from alpha_comp.compositors.Leaves.Closeness import Closeness
import torch
from strips.constraints import identity, mat_split, rotation

if __name__ == "__main__":
    path = os.path.join("../playground", "news")
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

        strip = MassComposition(6800, images,
                                Closeness(imgs[3], weights=torch.tensor([0, 1, 1, 1, 1])))

        weights = strip.get_animated_properties()["_Closeness:Weights"]

        weights.set_key_frame(0, torch.tensor([0, 0, 0, 1, 0], device=cuda))
        weights.set_key_frame(100, torch.tensor([0, 0, 0, 1, 0], device=cuda))
        weights.set_key_frame(600, torch.tensor([0, 0, 0, 0, 1], device=cuda))
        weights.set_key_frame(800, torch.tensor([0, 0, 0, 0, 1], device=cuda))
        weights.set_key_frame(1300, torch.tensor([0, 0, 1, 0, 0], device=cuda))
        weights.set_key_frame(1500, torch.tensor([0, 0, 1, 0, 0], device=cuda))
        weights.set_key_frame(2000, torch.tensor([0, 1, 0, 0, 0], device=cuda))
        weights.set_key_frame(2200, torch.tensor([0, 1, 0, 0, 0], device=cuda))
        weights.set_key_frame(2700, torch.tensor([1, 0, 0, 0, 0], device=cuda))
        weights.set_key_frame(2900, torch.tensor([1, 0, 0, 0, 0], device=cuda))
        weights.set_key_frame(3200, torch.tensor([1, 1, 0, 0, 0], device=cuda))
        weights.set_key_frame(3500, torch.tensor([1, 0, 1, 0, 0], device=cuda))
        weights.set_key_frame(3800, torch.tensor([1, 0, 0, 0, 1], device=cuda))
        weights.set_key_frame(4100, torch.tensor([0, 1, 1, 0, 0], device=cuda))
        weights.set_key_frame(4400, torch.tensor([0, 1, 0, 0, 1], device=cuda))
        weights.set_key_frame(4700, torch.tensor([0, 0, 1, 0, 1], device=cuda))
        weights.set_key_frame(5000, torch.tensor([1, 1, 1, 0, 0], device=cuda))
        weights.set_key_frame(5200, torch.tensor([1, 1, 0, 0, 1], device=cuda))
        weights.set_key_frame(5400, torch.tensor([1, 0, 0, 1, 1], device=cuda))
        weights.set_key_frame(5600, torch.tensor([0, 1, 1, 0, 1], device=cuda))
        weights.set_key_frame(6100, torch.tensor([1, 1, 1, 0, 1], device=cuda))
        weights.set_key_frame(6600, torch.tensor([0, 0, 0, 1, 0], device=cuda))
        weights.set_key_frame(6800, torch.tensor([0, 0, 0, 1, 0], device=cuda))

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1080, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=False)
