import os.path
import numpy as np
from PIL import Image
from Nodes.alpha_comp import Renderer
from Nodes.mass_composition import MassComposition
import torch
from Nodes.alpha_comp.compositors.Leaves.point_mapping import PointMapping
from Nodes.alpha_comp.compositors import Lines

if __name__ == "__main__":
    path = os.path.join("..", "ludumdar", "quill")
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

        comp = PointMapping([Lines(frequency=20)])

        strip = MassComposition(6000, images, comp)

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=6000, repeat=True, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
