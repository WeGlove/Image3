import os.path
from alpha_comp.compositors.Leaves.polar_divsion import PolarDivision
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
import torch
from strips.constraints import identity, mat_split, rotation

if __name__ == "__main__":
    path = os.path.join("../playground", "stars")
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
                                PolarDivision(torch.tensor([[960, 540], [640, 540], [480, 540], [384, 540]], device=cuda),
                                                    scale=5, ratio=0))
        points = strip.get_animated_properties()["_PolarDivision:Points"]
        shift = strip.get_animated_properties()["_PolarDivision:Shift"]
        weights = strip.get_animated_properties()["_PolarDivision:Weights_rad"]
        scale = strip.get_animated_properties()["_PolarDivision:Scale"]

        rotation_constraint_a = rotation.Rotation(torch.tensor([1920/2, 1080/2], device=cuda), cuda)
        rotation_constraint_b = rotation.Rotation(torch.tensor([1920/2, 1080/2], device=cuda), cuda)
        rotation_constraint_c = rotation.Rotation(torch.tensor([1920/2, 1080/2], device=cuda), cuda)
        points.set_constraint(mat_split.MatSplit([identity.Identity(), rotation_constraint_a, rotation_constraint_b,
                                                  rotation_constraint_c]))
        rotation_constraint_a.angle.set_anim_style("Sine")
        rotation_constraint_b.angle.set_anim_style("Sine")
        rotation_constraint_c.angle.set_anim_style("Sine")

        points.set_key_frame(0, torch.tensor([[960, 540], [960, 540], [480, 540], [384, 540]], device=cuda))

        points.set_key_frame(30, torch.tensor([[960, 540], [960, 540], [480, 540], [384, 540]], device=cuda))

        points.set_key_frame(280, torch.tensor([[960, 540], [640, 540], [480, 540], [384, 540]], device=cuda))
        rotation_constraint_a.angle.set_key_frame(280, 0)

        rotation_constraint_a.angle.set_key_frame(530, 360)
        weights.set_key_frame(530, torch.tensor([1, 1, 0, 0], device=cuda))

        rotation_constraint_a.angle.set_key_frame(780, 0)
        weights.set_key_frame(780, torch.tensor([0, 1, 1, 0], device=cuda))
        rotation_constraint_b.angle.set_key_frame(780, 0)

        rotation_constraint_a.angle.set_key_frame(1030, 360)
        rotation_constraint_b.angle.set_key_frame(1030, -360)
        weights.set_key_frame(1030, torch.tensor([1, 1, 1, 0], device=cuda))
        rotation_constraint_c.angle.set_key_frame(1030, 0)

        rotation_constraint_c.angle.set_key_frame(1280, 360)
        weights.set_key_frame(1280, torch.tensor([0, 0, 0, 1], device=cuda))
        rotation_constraint_a.angle.set_key_frame(1280, 360)
        rotation_constraint_b.angle.set_key_frame(1280, -360)

        weights.set_key_frame(1530, torch.tensor([1.1, -1, 1.1, -1], device=cuda))
        rotation_constraint_a.angle.set_key_frame(1560, 360)
        rotation_constraint_b.angle.set_key_frame(1560, -360)
        rotation_constraint_c.angle.set_key_frame(1560, 360)

        rotation_constraint_a.angle.set_key_frame(1810, 360*2)
        rotation_constraint_b.angle.set_key_frame(1810, -360/2)
        rotation_constraint_c.angle.set_key_frame(1810, 360*3)
        weights.set_key_frame(1810, torch.tensor([1.1, -1, 1.1, -1], device=cuda))

        weights.set_key_frame(2060, torch.tensor([0, 1.1, -1, 0], device=cuda))
        rotation_constraint_a.angle.set_key_frame(2060, 360)
        rotation_constraint_b.angle.set_key_frame(2060, -360)
        rotation_constraint_c.angle.set_key_frame(2060, 360 * 5)

        weights.set_key_frame(2310, torch.tensor([0, 1, 0, 0], device=cuda))
        rotation_constraint_a.angle.set_key_frame(2310, torch.tensor(360, device=cuda))

        rotation_constraint_a.angle.set_key_frame(2560, torch.tensor(0, device=cuda))
        rotation_constraint_a.origin.set_key_frame(2560, torch.tensor([1920/2, 1080/2], device=cuda))

        rotation_constraint_a.angle.set_key_frame(2810, torch.tensor(-360, device=cuda))
        rotation_constraint_a.origin.set_key_frame(2810, torch.tensor([0., 0.], device=cuda))
        weights.set_key_frame(2810, torch.tensor([0, 1, 0, 0], device=cuda))

        rotation_constraint_a.angle.set_key_frame(3060, torch.tensor(360, device=cuda))
        rotation_constraint_a.origin.set_key_frame(3060, torch.tensor([1920., 1080.], device=cuda))
        weights.set_key_frame(3060, torch.tensor([0, 1, 1, 0], device=cuda))
        rotation_constraint_b.angle.set_key_frame(3060, torch.tensor(-360, device=cuda))

        rotation_constraint_a.angle.set_key_frame(3310, torch.tensor(0, device=cuda))
        rotation_constraint_b.angle.set_key_frame(3310, torch.tensor(90, device=cuda))
        rotation_constraint_a.origin.set_key_frame(3310, torch.tensor([-200., 0], device=cuda))
        rotation_constraint_b.origin.set_key_frame(3310, torch.tensor([0, -200.], device=cuda))

        weights.set_key_frame(3750, torch.tensor([0, 1, 1, 1], device=cuda))
        rotation_constraint_a.angle.set_key_frame(3750, torch.tensor(1000, device=cuda))
        rotation_constraint_b.angle.set_key_frame(3750, torch.tensor(100, device=cuda))
        rotation_constraint_c.angle.set_key_frame(3750, torch.tensor(260, device=cuda))
        rotation_constraint_a.origin.set_key_frame(3750, torch.tensor([1920., 1080.], device=cuda))
        rotation_constraint_b.origin.set_key_frame(3750, torch.tensor([-100., 540.], device=cuda))
        rotation_constraint_c.origin.set_key_frame(3750, torch.tensor([1920., -1000.], device=cuda))
        scale.set_key_frame(3750, 5)

        scale.set_key_frame(4000, 0)
        weights.set_key_frame(4000, torch.tensor([1, 0, 0, 0], device=cuda))

        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=False)
