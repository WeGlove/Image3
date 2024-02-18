import torch


def get_polar(width, height, device):
    pixel_vectors_center = get_centered_vector_map(width, height, device)
    pixel_polar = torch.linalg.norm(pixel_vectors_center, axis=-1)
    return pixel_polar


def get_centered_vector_map(width, height, device):
    center_vector = torch.tensor([width / 2, height / 2], device=device)
    x, y = torch.meshgrid(torch.linspace(0, width, steps=width, device=device),
                          torch.linspace(0, height, steps=height, device=device))
    pixel_vectors = torch.stack([x, y]).transpose(0, 1).transpose(1, 2)

    pixel_vectors_center = pixel_vectors - center_vector
    return pixel_vectors_center


def get_vector_map(width, height, device):
    x, y = torch.meshgrid(torch.linspace(0, width, steps=width, device=device),
                          torch.linspace(0, height, steps=height, device=device))
    pixel_vectors = torch.stack([x, y]).transpose(0, 1).transpose(1, 2)

    return pixel_vectors


def get_centered_homo_vector_map(width, height, device):
    vector_map = get_centered_vector_map(width, height, device)
    homo_part = torch.ones((width, height), device=device)
    a = vector_map[:, :, 0]
    b = vector_map[:, :, 1]
    homo_vector_map = torch.stack([a, b, homo_part])
    homo_vector_map = homo_vector_map.transpose(0, 1).transpose(1, 2)
    return homo_vector_map


def get_homo_vector_map(width, height, device):
    vector_map = get_vector_map(width, height, device)
    homo_part = torch.ones((width, height), device=device)
    a = vector_map[:, :, 0]
    b = vector_map[:, :, 1]
    homo_vector_map = torch.stack([a, b, homo_part])
    homo_vector_map = homo_vector_map.transpose(0, 1).transpose(1, 2)
    return homo_vector_map


def radial(width, height, pixels_polar, radius_low, radius_high, device):
    arr = torch.ones(width, height, device=device)

    arr[pixels_polar > radius_high] = 0
    arr[pixels_polar < radius_low] = 0

    arr = arr.repeat(3, 1, 1).transpose(0, 1).transpose(1, 2)

    return arr


def radial_map(pixels_polar, amount, size):
    arr = (pixels_polar * size) % amount
    arr = torch.floor(arr)

    return arr.repeat(3, 1, 1).transpose(0, 1).transpose(1, 2)
