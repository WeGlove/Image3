import os.path
from src.gui.render_gui import RenderGui
from src.renderer import Renderer
import torch
from src.factories import (get_map_factory, get_system_factory, get_io_factory, get_math_factory, get_imaging_factory,
                           get_tensor_conv_factory, get_maps_2vec_factory, get_maps_nvec_factory)
from PyQt6.QtWidgets import QApplication
from src.frame_counter import FrameCounter
from src.patch import Patch


if __name__ == "__main__":
    save_path = os.path.join(os.path.join(".", "out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    with ((torch.cuda.device(0))):

        frame_counter = FrameCounter()
        factories = [get_map_factory(cuda, frame_counter), get_system_factory(cuda, frame_counter),
                     get_io_factory(cuda, frame_counter), get_math_factory(cuda, frame_counter),
                     get_imaging_factory(cuda, frame_counter), get_tensor_conv_factory(cuda, frame_counter),
                     get_maps_2vec_factory(cuda, frame_counter), get_maps_nvec_factory(cuda, frame_counter)]

        out = factories[1].instantiate("Output")
        patch = Patch(out)

        app = QApplication([])
        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True,
                            save_path=save_path, save=False, frame_counter=frame_counter)
        window = RenderGui(renderer, factories, patch)

        window.run(app, patch, fps_wait=True)
