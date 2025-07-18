import torch
import math


def rotation_2D(phi, device):
    return torch.tensor([[math.cos(phi), -math.sin(phi)], [math.sin(phi), math.cos(phi)]], device=device)

