import os.path
from Nodes.alpha_comp.compositors.Leaves import PolarDivision
import numpy as np
from PIL import Image
from Nodes.alpha_comp import Renderer
from Nodes.mass_composition import MassComposition
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

        strip = MassComposition(4500, images,
                                PolarDivision(torch.tensor([[960, 540], [960, 540], [960, 540], [960, 540], [960, 540]], device=cuda),
                                                    frequency=20, ratio=1))
        points = strip.get_animated_properties()["_PolarDivision:Points"]
        scale = strip.get_animated_properties()["_PolarDivision:Scale"]
        shift = strip.get_animated_properties()["_PolarDivision:Shift"]
        ratio = strip.get_animated_properties()["_PolarDivision:Ratio"]
        rotation = strip.get_animated_properties()["_PolarDivision:Rotation"]
        frequency = strip.get_animated_properties()["_PolarDivision:Frequency"]
        weights_rad = strip.get_animated_properties()["_PolarDivision:Weights_rad"]
        weights_angle = strip.get_animated_properties()["_PolarDivision:Weights_angle"]

        rotation.set_key_frame(0, 0)

        points.set_key_frame(250, torch.tensor([[960, 540], [960, 540], [960, 540], [960, 540], [960, 540]], device=cuda))

        points.set_key_frame(500, torch.tensor([[640, 540], [960, 540], [960, 540], [960, 540], [1280, 540]], device=cuda))

        points.set_key_frame(750, torch.tensor([[384, 540], [640, 540], [960, 540], [1280, 540], [1536, 540]], device=cuda))
        weights_angle.set_key_frame(750, torch.tensor([1, 1, 1, 1, 1], device=cuda))

        weights_angle.set_key_frame(1000, torch.tensor([1, -1, 1, -1, 1], device=cuda))

        points.set_key_frame(1250, torch.tensor([[384, 540], [640, 540], [960, 540], [1280, 540], [1536, 540]], device=cuda))

        points.set_key_frame(1500,
                             torch.tensor([[640, 360], [640, 720], [960, 540], [1280, 360], [1280, 720]], device=cuda))

        weights_angle.set_key_frame(1500, torch.tensor([1, -1, 1, -1, 1], device=cuda))

        weights_angle.set_key_frame(1750, torch.tensor([-1, 1, 1, 1, -1], device=cuda))

        weights_angle.set_key_frame(2000, torch.tensor([-1, 1, 1, 1, -1], device=cuda))

        weights_angle.set_key_frame(2250, torch.tensor([1, 1, -1, 1, 1], device=cuda))

        rotation.set_key_frame(2500, 90 * 10)
        ratio.set_key_frame(2500, 1)

        ratio.set_key_frame(2750, 0.3)
        rotation.set_key_frame(2750, 90*10)

        shift.set_key_frame(3000, 0)

        scale.set_key_frame(3250, 1)

        shift.set_key_frame(3500, 10000)
        rotation.set_key_frame(3500, 90 * 12)
        scale.set_key_frame(3500, 100)

        scale.set_key_frame(4000, 10)
        ratio.set_key_frame(4000, 0.3)

        ratio.set_key_frame(4250, 0)

        ratio.set_key_frame(4500, 1)

        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
