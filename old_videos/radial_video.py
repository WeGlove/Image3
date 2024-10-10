import os.path
from Nodes.maps.alpha_comp import RadialsWrap
import numpy as np
from PIL import Image
from Nodes.maps.alpha_comp import Renderer
from Nodes.imaging.mass_composition import MassComposition
import torch



if __name__ == "__main__":
    path = os.path.join("../playground", "clouds")
    out_path = os.path.join(os.path.join("C:", "Users", "tobia", "Desktop", "out_out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    print("loading images")
    imgs = [torch.tensor(np.array(Image.open(os.path.join(path, file))), device=cuda) for file in os.listdir(path)]
    print("loaded images")

    with (torch.cuda.device(0)):
        strips = []

        images = []
        for i, file in enumerate(os.listdir(path)):
            print(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=cuda)
            images.append(img)

        strip = MassComposition(4100, images, RadialsWrap())
        shift = strip.get_animated_properties()["_RadialsWarp:Shift"]
        shift.set_key_frame(0, 100)
        shift.set_key_frame(1000, 100)

        size = strip.get_animated_properties()["_RadialsWarp:Size"]
        shift = strip.get_animated_properties()["_RadialsWarp:Shift"]
        size.set_key_frame(0, 0)
        size.set_key_frame(1000, 0.01)
        size.set_key_frame(1100, 0.01)
        shift.set_key_frame(1100, 0)
        shift.set_key_frame(1500, 300)
        size.set_key_frame(1500, 0.01)
        shift.set_key_frame(3000, -500)
        size.set_key_frame(3000, 0.5)
        size.set_key_frame(3300, 0)
        shift.set_key_frame(3300, 0)
        size.set_key_frame(4000, 2)
        shift.set_key_frame(4000, 500)
        size.set_key_frame(4100, 0)

        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=False)
