import os.path
import numpy as np
from PIL import Image
from src.Nodes import Renderer
from src.Nodes.imaging.mass_composition import MassComposition
import torch
from src.Nodes import PointMapping
from src.Nodes import Lines


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

        comp = PointMapping([Lines(frequency=1)], duty_cycle=torch.tensor([1, 1, 1, 1], device=cuda))

        strip = MassComposition(3600, images, comp)
        print(strip.get_animated_properties())
        properties = strip.get_animated_properties()

        duty_cycle = properties['MassComposition_PointMapping:DutyCycle']
        lines_freq = properties['MassComposition_PointMapping:PointMap-0_Lines:Frequency']
        lines_shift = properties['MassComposition_PointMapping:PointMap-0_Lines:Shift']
        lines_rotation = properties['MassComposition_PointMapping:PointMap-0_Lines:Rotation']
        lines_center = properties['MassComposition_PointMapping:PointMap-0_Lines:Center']

        lines_shift.set_key_frame(0, 0)
        lines_shift.set_key_frame(100, 0)

        lines_shift.set_key_frame(350, 200)
        lines_freq.set_key_frame(350, 1)

        lines_freq.set_key_frame(600, 2)
        lines_shift.set_key_frame(600, 200)
        lines_rotation.set_key_frame(600, 0)

        lines_shift.set_key_frame(850, 0)
        lines_rotation.set_key_frame(850, 90)
        lines_center.set_key_frame(850, torch.tensor([1920/2, 1080/2], device=cuda))

        lines_rotation.set_key_frame(1100, 135)
        lines_shift.set_key_frame(1100, -200)
        lines_center.set_key_frame(1100, torch.tensor([0, 0], device=cuda))
        duty_cycle.set_key_frame(1100, torch.tensor([1, 1, 1, 1], device=cuda))

        lines_shift.set_key_frame(1350, -400)
        duty_cycle.set_key_frame(1350, torch.tensor([0, 1, 1, 1], device=cuda))

        lines_shift.set_key_frame(1600, -600)
        duty_cycle.set_key_frame(1600, torch.tensor([1, 0, 1, 1], device=cuda))

        lines_shift.set_key_frame(1850, -800)
        duty_cycle.set_key_frame(1850, torch.tensor([1, 1, 0, 1], device=cuda))

        lines_shift.set_key_frame(2100, -1200)
        duty_cycle.set_key_frame(2100, torch.tensor([1, 1, 1, 0], device=cuda))

        lines_shift.set_key_frame(2200, -1400)
        duty_cycle.set_key_frame(2200, torch.tensor([0, 0, 1, 1], device=cuda))

        lines_shift.set_key_frame(2300, -1600)
        duty_cycle.set_key_frame(2300, torch.tensor([0, 1, 0, 1], device=cuda))

        lines_shift.set_key_frame(2400, -1800)
        duty_cycle.set_key_frame(2400, torch.tensor([0, 1, 1, 0], device=cuda))

        lines_shift.set_key_frame(2500, -2000)
        duty_cycle.set_key_frame(2500, torch.tensor([1, 0, 0, 1], device=cuda))

        lines_shift.set_key_frame(2600, -2200)
        duty_cycle.set_key_frame(2600, torch.tensor([1, 0, 1, 0], device=cuda))

        lines_shift.set_key_frame(2700, -2400)
        duty_cycle.set_key_frame(2700, torch.tensor([1, 1, 0, 0], device=cuda))
        lines_freq.set_key_frame(2700, 2)
        lines_rotation.set_key_frame(2700, 135)
        lines_center.set_key_frame(2700, torch.tensor([0, 0], device=cuda))

        lines_shift.set_key_frame(3300, -3000)
        duty_cycle.set_key_frame(3300, torch.tensor([1, 2, 3, 4], device=cuda))
        lines_freq.set_key_frame(3300, 1)
        lines_rotation.set_key_frame(3300, 360)
        lines_center.set_key_frame(3300, torch.tensor([1920, 0], device=cuda))

        lines_shift.set_key_frame(3550, -3300)
        lines_freq.set_key_frame(3550, 0.1)
        duty_cycle.set_key_frame(3550, torch.tensor([1, 0, 0, 0], device=cuda))

        duty_cycle.set_key_frame(3650, torch.tensor([1, 0, 0, 0], device=cuda))

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=1000, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
