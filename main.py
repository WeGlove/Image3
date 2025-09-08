from src.gui.render_gui import RenderGui
from src.renderer import Renderer
import torch
import logging
from src.factories import get_io_factory, get_math_factory, get_imaging_factory, get_tensor_conv_factory


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    logger.info(f"Is Cuda available {torch.cuda.is_available()}")
    device = torch.device('cuda')

    with torch.cuda.device(0):
        renderer = Renderer(device)

        factories = [get_io_factory(), get_math_factory(), get_imaging_factory(), get_tensor_conv_factory()]
        logger.info(f"Created {len(factories)} factories")

        logger.info("Running GUI")
        window = RenderGui(renderer, factories)
        window.run()
