import os.path
from Nodes.maps.alpha_comp import PointWeights
import numpy as np
from PIL import Image
from Nodes.maps.alpha_comp import Renderer
from Nodes.misc.mass_composition import MassComposition
import torch


if __name__ == "__main__":
    path = os.path.join("../playground", "clouds")
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
                                PointWeights(torch.tensor([[960, 540], [960, 540], [960, 540]], device=cuda),
                                             weights=torch.tensor([1/3, 1/3, 1/3], device=cuda)))
        points = strip.get_animated_properties()["_PointWeights:Points"]
        shift = strip.get_animated_properties()["_PointWeights:Shift"]
        weights = strip.get_animated_properties()["_PointWeights:Weights"]
        size = strip.get_animated_properties()["_PointWeights:Size"]

        shift.set_key_frame(0, 0)

        shift.set_key_frame(250, 100)
        points.set_key_frame(250, torch.tensor([[960, 540], [960, 540], [960, 540]], device=cuda))

        points.set_key_frame(500, torch.tensor([[640, 540], [960, 540], [1280, 540]], device=cuda))
        points.set_key_frame(750, torch.tensor([[640, 720], [960, 360], [1280, 720]], device=cuda))
        weights.set_key_frame(750, torch.tensor([1, 1, 1], device=cuda))

        weights.set_key_frame(1000, torch.tensor([1, 10, 1], device=cuda))

        weights.set_key_frame(1250, torch.tensor([10, 1, 10], device=cuda))
        points.set_key_frame(1250, torch.tensor([[640, 720], [960, 360], [1280, 720]], device=cuda))

        weights.set_key_frame(1750, torch.tensor([1, 1, 1], device=cuda))
        points.set_key_frame(1750, torch.tensor([[0, 1080], [960, 0], [1920, 1080]], device=cuda))

        weights.set_key_frame(2250, torch.tensor([1, -1.5, 1], device=cuda))
        points.set_key_frame(2250, torch.tensor([[640, 720], [960, 360], [1280, 720]], device=cuda))

        points.set_key_frame(2500, torch.tensor([[640, 540], [960, 540], [1280, 540]], device=cuda))
        shift.set_key_frame(2500, 100)

        shift.set_key_frame(2750, 200)
        weights.set_key_frame(2750, torch.tensor([1, -1.5, 1], device=cuda))

        weights.set_key_frame(3250, torch.tensor([-1.25, 2, -1.25], device=cuda))
        shift.set_key_frame(3250, 200)

        shift.set_key_frame(3500, 300)
        size.set_key_frame(3500, 0.1)

        size.set_key_frame(4000, 0.001)

        size.set_key_frame(4500, 1)

        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
