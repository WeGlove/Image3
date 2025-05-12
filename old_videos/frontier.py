import os.path
import numpy as np
from PIL import Image
from src.Nodes import Renderer
from src.Nodes.imaging.mass_composition import MassComposition
import torch
from src.Nodes import PointMapping
from src.Nodes import Circles
from src.Nodes import Spirals
from src.Nodes import Lines
from src.Nodes import Closeness


if __name__ == "__main__":
    path = os.path.join("../playground", "stars")
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

        sun = np.array(Image.open(os.path.join("../playground", "sun.png")))
        sun = torch.tensor(sun, device=cuda)

        comp = PointMapping([Lines(), Lines(rotation=90), Circles(torch.tensor([[1920/2, 1080/2]], device=cuda)),
                             Spirals(torch.tensor([[1920/2, 1080/2]], device=cuda), frequency=4)])

        strip = MassComposition(5400, images, comp)
        print(strip.get_animated_properties())
        properties = strip.get_animated_properties()
        duty_cycle = properties['MassComposition_PointMapping:DutyCycle']
        weights = properties['MassComposition_PointMapping:Weights']

        frequency_0 = properties['MassComposition_PointMapping:PointMap-0_Lines:Frequency']
        shift_0 = properties['MassComposition_PointMapping:PointMap-0_Lines:Shift']
        rotation_0 = properties['MassComposition_PointMapping:PointMap-0_Lines:Rotation']
        center_0 = properties['MassComposition_PointMapping:PointMap-0_Lines:Center']
        frequency_1 = properties['MassComposition_PointMapping:PointMap-1_Lines:Frequency']
        shift_1 = properties['MassComposition_PointMapping:PointMap-1_Lines:Shift']
        rotation_1 = properties['MassComposition_PointMapping:PointMap-1_Lines:Rotation']
        center_1 = properties['MassComposition_PointMapping:PointMap-1_Lines:Center']
        points_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Points']
        scale_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Scale']
        shift_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Shift']
        ratio_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Ratio']
        rotation_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Rotation']
        frequency_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Frequency']
        weights_rad_2 = properties['MassComposition_PointMapping:PointMap-2_PolarDivision:Weights_rad']
        points_3 = properties['MassComposition_PointMapping:PointMap-3_PolarDivision:Points']
        shift_3 = properties['MassComposition_PointMapping:PointMap-3_PolarDivision:Rotation']
        rotation_3 = properties['MassComposition_PointMapping:PointMap-3_PolarDivision:Rotation']
        frequency_3 = properties['MassComposition_PointMapping:PointMap-3_PolarDivision:Frequency']
        weights_angle_3 = properties['MassComposition_PointMapping:PointMap-3_PolarDivision:Weights_angle']

        weights.set_key_frame(0, torch.tensor([1,0,0,0], device=cuda))
        shift_0.set_key_frame(0, 0)

        shift_0.set_key_frame(250, 200)
        weights.set_key_frame(250, torch.tensor([1, 0, 0, 0], device=cuda))

        shift_0.set_key_frame(500, 400)
        weights.set_key_frame(500, torch.tensor([1, 0, 0.1, 0], device=cuda))

        shift_0.set_key_frame(750, 400)
        weights.set_key_frame(750, torch.tensor([1, 0, 1, 0], device=cuda))
        shift_2.set_key_frame(750, 0)

        shift_0.set_key_frame(1000, 600)
        shift_2.set_key_frame(1000, -200)
        weights.set_key_frame(1000, torch.tensor([1, 0, 1, 0], device=cuda))

        shift_0.set_key_frame(1250, 800)
        shift_2.set_key_frame(1250, -400)
        weights.set_key_frame(1250, torch.tensor([1, 0.1, 1, 0], device=cuda))

        shift_0.set_key_frame(1350, 880)
        shift_2.set_key_frame(1350, -480)
        weights.set_key_frame(1350, torch.tensor([1, 0.1, 1, 0], device=cuda))

        shift_0.set_key_frame(1600, 1080)
        shift_2.set_key_frame(1600, -680)
        weights.set_key_frame(1600, torch.tensor([1, 1, 1, 0], device=cuda))

        shift_0.set_key_frame(1850, 1280)
        shift_2.set_key_frame(1850, -880)
        weights.set_key_frame(1850, torch.tensor([1, 1, 1, 0], device=cuda))

        shift_0.set_key_frame(2100, 1480)
        shift_2.set_key_frame(2100, -1080)
        shift_3.set_key_frame(2100, 0)
        weights.set_key_frame(2100, torch.tensor([0, 0, 1, 0], device=cuda))

        shift_2.set_key_frame(2350, -1280)
        shift_3.set_key_frame(2350, 10)
        weights.set_key_frame(2350, torch.tensor([0, 0, 1, 1], device=cuda))

        shift_2.set_key_frame(2600, -1480)
        shift_3.set_key_frame(2600, 20)
        weights.set_key_frame(2600, torch.tensor([0, 0, 0, 1], device=cuda))

        shift_3.set_key_frame(2850, 30)
        weights.set_key_frame(2850, torch.tensor([0, 0, 0, 1], device=cuda))

        shift_3.set_key_frame(3100, 40)
        weights.set_key_frame(3100, torch.tensor([1, 1, 0, 1], device=cuda))
        shift_0.set_key_frame(3100, 1480)
        shift_1.set_key_frame(3100, 0)

        shift_0.set_key_frame(3350, 1680)
        shift_1.set_key_frame(3350, -200)
        shift_3.set_key_frame(3350, 50)
        weights.set_key_frame(3100, torch.tensor([1, 1, 0, 1], device=cuda))

        shift_0.set_key_frame(3350, 1880)
        shift_1.set_key_frame(3350, -400)
        shift_3.set_key_frame(3350, 60)
        weights.set_key_frame(3350, torch.tensor([1, 1, 1, 1], device=cuda))
        rotation_0.set_key_frame(3350, 0)
        rotation_1.set_key_frame(3350, 90)

        shift_0.set_key_frame(3600, 2080)
        shift_1.set_key_frame(3600, -600)
        shift_3.set_key_frame(3600, 70)
        rotation_0.set_key_frame(3600, 45)
        rotation_1.set_key_frame(3600, 135)
        center_0.set_key_frame(3600, torch.tensor([1920/2, 1080/2], device=cuda))
        center_1.set_key_frame(3600, torch.tensor([1920/2, 1080/2], device=cuda))

        shift_0.set_key_frame(3850, 2280)
        shift_1.set_key_frame(3850, -800)
        shift_3.set_key_frame(3850, 80)
        center_0.set_key_frame(3850, torch.tensor([0, 0], device=cuda))
        center_1.set_key_frame(3850, torch.tensor([1920, 1080], device=cuda))
        points_2.set_key_frame(3850, torch.tensor([[1920/3, 1080/3], [1920/2, 1080/2], [2*1920/3, 2*1080/3]], device=cuda))
        weights_rad_2.set_key_frame(3850, torch.tensor([0, 1, 0]))

        shift_0.set_key_frame(4100, 2480)
        shift_1.set_key_frame(4100, -1000)
        shift_3.set_key_frame(4100, 90)
        weights_rad_2.set_key_frame(4100, torch.tensor([1, 0, 1]))

        shift_0.set_key_frame(4350, 2680)
        shift_1.set_key_frame(4350, -1200)
        shift_3.set_key_frame(4350, 100)
        weights_rad_2.set_key_frame(4350, torch.tensor([1, -1, 1]))
        weights.set_key_frame(4350, torch.tensor([1, 1, 1, 1], device=cuda))

        shift_0.set_key_frame(4600, 2880)
        shift_1.set_key_frame(4600, -1400)
        shift_3.set_key_frame(4600, 110)
        weights.set_key_frame(4600, torch.tensor([1, 1, 1, 0], device=cuda))

        shift_0.set_key_frame(4850, 3080)
        shift_1.set_key_frame(4850, -1600)
        shift_3.set_key_frame(4850, 120)
        weights.set_key_frame(4850, torch.tensor([1, 0, 1, 0], device=cuda))

        shift_0.set_key_frame(5100, 3280)
        shift_3.set_key_frame(5100, 130)
        weights.set_key_frame(5100, torch.tensor([0, 0, 1, 0], device=cuda))
        duty_cycle.set_key_frame(5100, torch.tensor([1,1,1,1,1], device=cuda))

        duty_cycle.set_key_frame(5150, torch.tensor([0,1,1,1,1], device=cuda))

        duty_cycle.set_key_frame(5200, torch.tensor([0,0,1,1,1], device=cuda))

        duty_cycle.set_key_frame(5250, torch.tensor([0,0,0,1,1], device=cuda))

        duty_cycle.set_key_frame(5300, torch.tensor([0,0,0,0,1], device=cuda))

        strips.append(strip)

        #############################

        comp = Closeness(sun)
        strip = MassComposition(6000, images + [sun], comp)

        properties = strip.get_animated_properties()
        weights = properties['MassComposition_Closeness:Weights']
        image = properties['MassComposition_Closeness:Image']

        weights.set_key_frame(5400, torch.tensor([0,0,0,0,1,0], device=cuda))
        weights.set_key_frame(5500, torch.tensor([0,0,0,1,1,0], device=cuda))
        weights.set_key_frame(5600, torch.tensor([0,0,1,1,1,0], device=cuda))
        weights.set_key_frame(5700, torch.tensor([0,1,1,1,1,0], device=cuda))
        weights.set_key_frame(5800, torch.tensor([1,1,1,1,1,0], device=cuda))
        weights.set_key_frame(5900, torch.tensor([1,1,1,1,1,0], device=cuda))
        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=5300, stop_frame=6000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
