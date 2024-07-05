import os.path
import numpy as np
from PIL import Image
from gui.render_gui import RenderGui
from renderer import Renderer
from strips.mass_composition import MassComposition
import torch
from node_factory import NodeFactory
from PyQt6.QtWidgets import QApplication
from strips.frame_counter import FrameCounter


if __name__ == "__main__":
    path = os.path.join(".", "inversions")
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

        frame_counter = FrameCounter()
        factory = NodeFactory(cuda, frame_counter)

        out = factory.out()

        strip = MassComposition(16271, images, out)
        strips.append(strip)

        app = QApplication([])
        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True,
                            save_path="C:\\Users\\tobia\\Desktop\\out_out", save=False, frame_counter=frame_counter)
        window = RenderGui(renderer, factory, strip)

        window.run(app, strips, fps_wait=True)
