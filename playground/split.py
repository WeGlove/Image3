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

        comp = SizeSplit(
            PolarDivision(points=torch.tensor([[1920/2, 1080/2]], device=cuda)),
            PolarDivision(points=torch.tensor([[1920/2, 1080/2]], device=cuda)))

        comp = PolarDivision(points=torch.tensor([[1920 / 2, 1080 / 2]], device=cuda))

        strip = MassComposition(3600, images, comp)
        #a_shift = strip.get_animated_properties()["_SizeSplit:CompositorA_PolarDivision:Shift"]
        #b_shift = strip.get_animated_properties()["_SizeSplit:CompositorB_PolarDivision:Shift"]

        #a_shift.set_key_frame(0, 0)
        #b_shift.set_key_frame(0, 0)

        #a_shift.set_key_frame(1000, 10000)
        #b_shift.set_key_frame(1000, -10000)

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=1000000, repeat=True, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        renderer.run(strips, fps_wait=False)
