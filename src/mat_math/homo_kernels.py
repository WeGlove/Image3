import torch
import math


def scale(x, y):
    return torch.tensor([[x, 0, 0], [0, y, 0], [0, 0, 1]])

def squeeze(k):
    return scale(k, 1 / k)

def shear_x(x):
    return torch.tensor([[1, torch.tan(x), 0], [0, 1, 0], [0, 0, 1]])


def shear_y(y):
    return torch.tensor([[1, 0, 0], [torch.tan(y), 1, 0], [0, 0, 1]])


def rotation_2D(phi, device):
    return torch.tensor([[math.cos(phi), -math.sin(phi), 0], [math.sin(phi), math.cos(phi), 0], [0, 0, 1]], device=device)


def perspective_projection_y(y=1):
    return torch.tensor([[1, 0, 0], [0, 1, 0], [0, y, 0]])


def perspective_projection_x(x=1):
    return torch.tensor([[1, 0, 0], [0, 1, 0], [x, 0, 0]])


def translate(x, y):
    return torch.tensor([[1, 0, x], [0, 1, y], [0, 0, 1]])


def reflect():
    return torch.tensor([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])


def reflect_x():
    return torch.tensor([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])


def reflect_y():
    return torch.tensor([[1, 0, 0], [0, -1, 0], [0, 0, 1]])


def orthogonal_projection(x, y):
    factor = torch.linalg.norm(torch.tensor([x, y])) ** 2
    return torch.tensor([[x ** 2 / factor, x * y / factor, 0], [x * y / factor, y ** 2 / factor, 0], [0, 0, 1]])


def reflection(x, y):
    factor = torch.linalg.norm(torch.tensor([x, y])) ** 2
    return torch.tensor(
        [[(x ** 2 - y ** 2) / factor, 2 * x * y / factor, 0], [2 * x * y / factor, (y ** 2 - x ** 2) / factor, 0],
         [0, 0, 1]])