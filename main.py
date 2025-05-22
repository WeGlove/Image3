import os.path
from src.gui.render_gui import RenderGui
from src.renderer import Renderer
import torch
import logging
from src.factories import (get_map_factory, get_io_factory, get_math_factory, get_imaging_factory,
                           get_tensor_conv_factory, get_maps_2vec_factory, get_maps_nvec_factory)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    save_path = os.path.join(os.path.join(".", "out"))

    logger.info(f"Is Cuda available {torch.cuda.is_available()}")
    device = torch.device('cuda')

    with torch.cuda.device(0):
        renderer = Renderer(30, device, width=1920, height=1080, start_frame=0, stop_frame=16271, repeat=True,
                            save_path=save_path, save=False)

        factories = [get_map_factory(),
                     get_io_factory(), get_math_factory(),
                     get_imaging_factory(), get_tensor_conv_factory(),
                     get_maps_2vec_factory(), get_maps_nvec_factory()]
        logger.info(f"Created {len(factories)} factories")

        logger.info("Running GUI")
        window = RenderGui(renderer, factories)
        window.run(fps_wait=True)
