import os.path
import numpy as np
from PIL import Image
from Nodes.alpha_comp import Renderer
from strips.mass_composition import MassComposition
import torch
from Nodes.alpha_comp.compositors.Leaves.point_mapping import PointMapping
from Nodes.alpha_comp.compositors import Lines


if __name__ == "__main__":
    path = os.path.join("../playground", "wood")
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

        comp = PointMapping([Lines(), Lines(rotation=90)], duty_cycle=torch.tensor([1, 1, 1, 1], device=cuda))

        strip = MassComposition(2900, images, comp)
        print(strip.get_animated_properties())
        properties = strip.get_animated_properties()

        duty_cycle = properties['MassComposition_PointMapping:DutyCycle']
        weights = properties['MassComposition_PointMapping:Weights']
        lines0_freq = properties['MassComposition_PointMapping:PointMap-0_Lines:Frequency']
        lines0_shift = properties['MassComposition_PointMapping:PointMap-0_Lines:Shift']
        lines0_rotation = properties['MassComposition_PointMapping:PointMap-0_Lines:Rotation']
        lines0_center = properties['MassComposition_PointMapping:PointMap-0_Lines:Center']
        lines1_freq = properties['MassComposition_PointMapping:PointMap-1_Lines:Frequency']
        lines1_shift = properties['MassComposition_PointMapping:PointMap-1_Lines:Shift']
        lines1_rotation = properties['MassComposition_PointMapping:PointMap-1_Lines:Rotation']
        lines1_center = properties['MassComposition_PointMapping:PointMap-1_Lines:Center']

        lines0_shift.set_key_frame(0, 0)

        lines0_shift.set_key_frame(250, 200)
        weights.set_key_frame(250, torch.tensor([1, 0], device=cuda))

        weights.set_key_frame(500, torch.tensor([1, 1], device=cuda))
        lines0_shift.set_key_frame(500, 200)

        lines0_shift.set_key_frame(750, 400)
        lines1_shift.set_key_frame(750, 0)
        weights.set_key_frame(750, torch.tensor([1, 1], device=cuda))


        lines0_shift.set_key_frame(1000, 600)
        lines1_shift.set_key_frame(1000, -200)
        weights.set_key_frame(1000, torch.tensor([0, 1], device=cuda))

        lines0_shift.set_key_frame(1250, 800)
        lines1_shift.set_key_frame(1250, -400)
        weights.set_key_frame(1250, torch.tensor([1, 0], device=cuda))

        lines0_shift.set_key_frame(1500, 1000)
        lines1_shift.set_key_frame(1500, -600)
        weights.set_key_frame(1500, torch.tensor([1, 1], device=cuda))
        lines0_freq.set_key_frame(1500, 1)

        lines0_shift.set_key_frame(1750, 1200)
        lines1_shift.set_key_frame(1750, -800)
        lines0_freq.set_key_frame(1750, 16)
        lines1_freq.set_key_frame(1750, 1)

        lines0_shift.set_key_frame(2000, 1400)
        lines1_shift.set_key_frame(2000, -1000)
        lines1_freq.set_key_frame(2000, 16)
        lines1_rotation.set_key_frame(2000, 90)

        lines0_shift.set_key_frame(2250, 1800)
        lines1_shift.set_key_frame(2250, -1200)
        lines1_freq.set_key_frame(2250, 1)
        lines0_freq.set_key_frame(2250, 1)
        lines1_rotation.set_key_frame(2250, 225)

        lines0_shift.set_key_frame(2500, 2000)
        lines1_shift.set_key_frame(2500, -1400)
        duty_cycle.set_key_frame(2500, torch.tensor([1, 1, 1, 1], device=cuda))

        duty_cycle.set_key_frame(2600, torch.tensor([0, 1, 1, 1], device=cuda))

        duty_cycle.set_key_frame(2700, torch.tensor([0, 0, 1, 1], device=cuda))

        duty_cycle.set_key_frame(2800, torch.tensor([0, 0, 0, 1], device=cuda))


        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
