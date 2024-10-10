import os.path
import numpy as np
from PIL import Image
from Nodes.maps.alpha_comp import Renderer
from Nodes.misc.mass_composition import MassComposition
from Nodes.maps.alpha_comp import Closeness
import torch

if __name__ == "__main__":
    path = os.path.join("../playground", "news2")
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
        template_images = images[4:] + [torch.zeros(1920, 1080, device=cuda)]
        images = images[:4]


        strip = MassComposition(3600, images,
                                Closeness(template_images[4], weights=torch.tensor([1, 1, 1, 1, 1, 1, 1], device=cuda)))

        weights = strip.get_animated_properties()["_Closeness:Weights"]
        anim_image = strip.get_animated_properties()["_Closeness:Image"]

        anim_image.set_key_frame(100, template_images[4] / 255)

        anim_image.set_key_frame(450, template_images[0] / 255)

        anim_image.set_key_frame(800, template_images[1] / 255)

        anim_image.set_key_frame(1150, template_images[2] / 255)

        anim_image.set_key_frame(1500, template_images[3] / 255)

        weights.set_key_frame(1500, torch.tensor([1, 1, 1, 1, 1, 1, 1], device=cuda))

        anim_image.set_key_frame(1850, template_images[0] / 255)
        weights.set_key_frame(1850, torch.tensor([0, 0, 1, 1, 1, 1, 1], device=cuda))

        anim_image.set_key_frame(2200, template_images[2] / 255)
        weights.set_key_frame(2200, torch.tensor([1, 1, 0, 0, 1, 1, 1], device=cuda))

        anim_image.set_key_frame(2550, template_images[1] / 255)
        weights.set_key_frame(2550, torch.tensor([1, 1, 1, 1, 0, 0, 0], device=cuda))

        anim_image.set_key_frame(2900, template_images[3] / 255)
        weights.set_key_frame(2900, torch.tensor([0, 1, 0, 0, 1, 0, 1], device=cuda))

        anim_image.set_key_frame(3250, template_images[1] / 255)
        weights.set_key_frame(3250, torch.tensor([0, 0, 1, 1, 0, 0, 0], device=cuda))

        anim_image.set_key_frame(3600, template_images[0] / 255)
        weights.set_key_frame(3600, torch.tensor([1, 0, 0, 0, 0, 1, 0], device=cuda))

        strips.append(strip)

        renderer = Renderer(30, cuda, width=1920, height=1080, start_frame=0, stop_frame=1000000, repeat=False, save_path="C:\\Users\\tobia\\Desktop\\out_out", save=True)
        renderer.run(strips, fps_wait=False)
