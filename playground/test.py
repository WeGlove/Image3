import os.path
import numpy as np
from PIL import Image
from render_gui import RenderGui
from renderer import Renderer
from strips.mass_composition import MassComposition
import torch
from Nodes.alpha_comp.compositors.Leaves.point_mapping_min import PointMappingMin
from Nodes.alpha_comp.compositors.Leaves.point_maps.LineConfigs import LineConfigs
from strips.constraints.buffer import MeanBuffer
from strips.constraints.fromfile import FromFile
from PyQt6.QtWidgets import QApplication


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

        #comp = PointMappingMin(LineConfigs.get_NGons(3, torch.tensor([0., 0.], device=cuda), 1., cuda))
        comp = PointMappingMin(LineConfigs.get_random(5, torch.tensor([0., 0.], device=cuda), 1., cuda))

        strip = MassComposition(16271, images, comp)

        constraint = FromFile(os.path.join(".", "2.png"))
        constraint_buffer = MeanBuffer(constraint, 100)

        shift = comp.get_subnode(1)
        shift.set_key_frame(0, 0)
        shift.set_constraint(constraint_buffer)

        print(comp.to_dict())

        app = QApplication([])
        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True,
                            save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False)
        window = RenderGui(renderer)

        window.run(app, strips, fps_wait=True)
