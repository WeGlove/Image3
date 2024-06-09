import torch
import math


def scale(x, y):
    return torch.tensor([[x, 0], [0, y]])

def squeeze(k):
    return scale(k, 1 / k)

def shear_x(x):
    return torch.tensor([[1, torch.tan(x)], [0, 1]])


def shear_y(y):
    return torch.tensor([[1, 0], [torch.tan(y), 1]])


def rotation_2D(phi, device):
    return torch.tensor([[math.cos(phi), -math.sin(phi)], [math.sin(phi), math.cos(phi)]], device=device)


def reflect():
    return torch.tensor([[-1, 0], [0, -1]])


def reflect_x():
    return torch.tensor([[-1, 0], [0, 1]])


def reflect_y():
    return torch.tensor([[1, 0], [0, -1]])


def orthogonal_projection(x, y):
    factor = torch.linalg.norm(torch.tensor([x, y])) ** 2
    return torch.tensor([[x ** 2 / factor, x * y / factor], [x * y / factor, y ** 2 / factor]])


def reflection(x, y):
    factor = torch.linalg.norm(torch.tensor([x, y])) ** 2
    return torch.tensor(
        [[(x ** 2 - y ** 2) / factor, 2 * x * y / factor], [2 * x * y / factor, (y ** 2 - x ** 2) / factor]])