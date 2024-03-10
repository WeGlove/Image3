import os.path
from alpha_comp.compositors.Leaves.polar_divsion import PolarDivision
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
import torch
from strips.constraints import identity, mat_split, rotation

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

        strip = MassComposition(4500, images,
                                PolarDivision(torch.tensor([[960, 540], [1500, 540]], device=cuda),
                                                    frequency=20, ratio=0))
        points = strip.get_animated_properties()["_PolarDivision:Points"]
        shift = strip.get_animated_properties()["_PolarDivision:Shift"]

        rotation_constraint = rotation.Rotation(torch.tensor([1920/2, 1080/2], device=cuda), cuda)
        x = mat_split.MatSplit([identity.Identity(), rotation_constraint])
        points.set_constraint(mat_split.MatSplit([identity.Identity(), rotation_constraint]))

        shift.set_key_frame(0, 0)
        rotation_constraint.angle.set_key_frame(0, 0)

        shift.set_key_frame(1000, 1000)
        rotation_constraint.angle.set_key_frame(1000, 1000)

        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        renderer.run(strips, fps_wait=True)
