import math
import os.path
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
import torch
from alpha_comp.compositors.Leaves.point_maps.lines import Lines
from strips.constraints.jitter import Jitter
from alpha_comp.compositors.Leaves.point_mapping import PointMapping
from alpha_comp.compositors.Leaves.point_maps.circles import Circles
from alpha_comp.compositors.Leaves.point_maps.spirals import Spirals
from alpha_comp.compositors.Leaves.point_maps.lines import Lines


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

        b = Lines(rotation=70/360*math.pi*2, frequency=0.01)
        comp = PointMapping([Lines(frequency=0.001), b], duty_cycle=torch.tensor([1,2,4,8], device=cuda))

        strip = MassComposition(3600, images, comp)
        shift = strip.get_animated_properties()['MassComposition_PointMapping:PointMap-1_Lines:Shift']
        shift.set_key_frame(0, 0)
        shift.set_key_frame(10000, 10000)

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=1000000, repeat=True, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        renderer.run(strips, fps_wait=False)
