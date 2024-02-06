import torch


def get_polar(width, height, device):
    center_vector = torch.tensor([width / 2, height / 2], device=device)
    x, y = torch.meshgrid(torch.linspace(0, width, steps=width, device=device),
                          torch.linspace(0, height, steps=height, device=device))
    pixel_vectors = torch.stack([x, y]).transpose(0, 1).transpose(1, 2)

    pixel_vectors_center = pixel_vectors - center_vector
    pixel_polar = torch.linalg.norm(pixel_vectors_center, axis=-1)
    return pixel_polar


def radial(width, height, pixels_polar, radius_low, radius_high, device):
    arr = torch.ones(width, height, device=device)

    arr[pixels_polar > radius_high] = 0
    arr[pixels_polar < radius_low] = 0

    arr = arr.repeat(3, 1, 1).transpose(0, 1).transpose(1, 2)

    return arr
