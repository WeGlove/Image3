import os.path
from src.Nodes import Spirals
import numpy as np
from PIL import Image
from src.Nodes import Renderer
from src.Nodes.imaging.mass_composition import MassComposition
import torch


if __name__ == "__main__":
    path = os.path.join("../../playground", "mountains")
    out_path = os.path.join(os.path.join("C:", "Users", "tobia", "Desktop", "out_out"))

    print("cuda", torch.cuda.is_available())

    cuda = torch.device('cuda')

    print("loading images")
    imgs = [torch.tensor(np.array(Image.open(os.path.join(path, file))), device=cuda) for file in os.listdir(path)]
    print("loaded images")

    with ((torch.cuda.device(0))):
        strips = []

        images = []
        for i, file in enumerate(os.listdir(path)):
            print(f"Loading Image: {i}")
            img = np.array(Image.open(os.path.join(path, file)))
            img = torch.tensor(img, device=cuda)
            images.append(img)

        strip = MassComposition(3900, images, Spirals())
        shift = strip.get_animated_properties()["_Spirals:Scale"]
        rotation = strip.get_animated_properties()["_Spirals:Rotation"]
        frequency = strip.get_animated_properties()["_Spirals:Frequency"]
        shift.set_key_frame(0, 0)
        rotation.set_key_frame(0, 0)

        rotation.set_key_frame(100, 0)

        rotation.set_key_frame(350, 1)
        frequency.set_key_frame(350, 1)

        rotation.set_key_frame(900, 10)
        frequency.set_key_frame(900, 2)

        rotation.set_key_frame(1050, 15)

        rotation.set_key_frame(1100, 17)

        rotation.set_key_frame(1150, 19)
        frequency.set_key_frame(1200, 2)

        frequency.set_key_frame(1800, 30)
        rotation.set_key_frame(1800, 19)

        rotation.set_key_frame(2200, 50)
        frequency.set_key_frame(2200, 30)

        frequency.set_key_frame(2300, 0.001)

        frequency.set_key_frame(2900, 400)

        frequency.set_key_frame(3000, 1)
        rotation.set_key_frame(3000, 50)

        rotation.set_key_frame(3100, 52)
        shift.set_key_frame(3100, 0)

        shift.set_key_frame(3300, 0.001)
        rotation.set_key_frame(3300, 52)

        shift.set_key_frame(3600, 0.01)

        shift.set_key_frame(3800, 10)
        rotation.set_key_frame(3800, 60)
        frequency.set_key_frame(3800, 1)

        frequency.set_key_frame(3900, 0.001)


        strips.append(strip)

        renderer = Renderer(30, cuda, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=True)
