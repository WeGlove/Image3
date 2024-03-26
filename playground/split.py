import math
import os.path
from alpha_comp.compositors.Leaves.polar_divsion import PolarDivision
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
from alpha_comp.compositors.Leaves.Closeness import Closeness
from alpha_comp.compositors.Nodes.SizeSplit import SizeSplit
import torch
from strips.constraints import identity, mat_split, rotation
from alpha_comp.compositors.Leaves.lines import Lines
from mat_math.homo_kernels import rotation_2D
from strips.constraints.jitter import Jitter


if __name__ == "__main__":
    path = os.path.join("../playground", "news2")
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
            images.append(img)
        template_images = images[4:] + [torch.zeros(1920, 1080, device=cuda)]
        images = images[:4]

        comp = Lines(rotation=0)

        strip = MassComposition(3600, images, comp)

        freq_prop = strip.get_animated_properties()['_Lines:Frequency']
        rotation = strip.get_animated_properties()['_Lines:Rotation']
        rotation.set_constraint(Jitter(frequency=0.1, amplitude=0.000001, device=cuda))
        #freq_prop.set_key_frame(0, 0.01)
        rotation.set_key_frame(0, 0)

        #freq_prop.set_key_frame(1000, 0.001)
        #rotation.set_key_frame(10000, 2*math.pi)

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=1000000, repeat=True, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        renderer.run(strips, fps_wait=False)
