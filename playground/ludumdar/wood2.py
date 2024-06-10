import os.path
import numpy as np
from PIL import Image
from Nodes.alpha_comp import Renderer
from strips.mass_composition import MassComposition
import torch
from Nodes.alpha_comp.compositors.Leaves.point_mapping import PointMapping
from Nodes.alpha_comp.compositors.Leaves.point_maps.circles import Circles
from Nodes.alpha_comp.compositors.Leaves.point_maps.spirals import Spirals
from Nodes.alpha_comp.compositors import Lines
from Nodes.alpha_comp.compositors.Leaves.Closeness import Closeness


if __name__ == "__main__":
    path = os.path.join("..", "ludumdar", "nightmare")
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

        sun = np.array(Image.open(os.path.join("..", "sun.png")))
        sun = torch.tensor(sun, device=cuda)

        comp = PointMapping([Lines(), Lines(rotation=90), Circles(torch.tensor([[1920/2, 1080/2]], device=cuda)),
                             Spirals(torch.tensor([[1920/2, 1080/2]], device=cuda), frequency=4)])

        strip = MassComposition(5400, images, comp)
        print(strip.get_animated_properties())
        properties = strip.get_animated_properties()
        duty_cycle = properties['MassComposition_PointMapping:DutyCycle']
        weights = properties['MassComposition_PointMapping:Weights']


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

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=6000, repeat=True, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
