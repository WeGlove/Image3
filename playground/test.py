import os.path
import numpy as np
from PIL import Image
from alpha_comp.renderer import Renderer
from strips.mass_composition import MassComposition
import torch
from alpha_comp.compositors.Leaves.point_mapping import PointMapping
from alpha_comp.compositors.Leaves.point_maps.line import Line
from alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs


if __name__ == "__main__":
    path = os.path.join(".", "wood")
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

        #comp = PointMapping(LineConfigs.get_NGons(3, torch.tensor([0., 0.], device=cuda), 1., cuda))
        comp = PointMapping(LineConfigs.get_star(3, torch.tensor([0., 0.], device=cuda), 1., cuda))

        strip = MassComposition(16271, images, comp)
        properties = strip.get_animated_properties()
        print(properties)
        shift = properties["MassComposition_PointMapping:Shift"]
        frequency = properties["MassComposition_PointMapping:Frequency"]

        shift.set_key_frame(0, 0)
        shift.set_key_frame(1000, 9)

        frequency.set_key_frame(0, 1)
        frequency.set_key_frame(1000, 10)

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        renderer.run(strips, fps_wait=True)
