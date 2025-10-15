import torch


def bin_round(map, k, shift):
    if torch.is_complex(map):
        map.imag = torch.floor(map.imag / k + shift) * k
        map.real = torch.floor(map.real / k + shift) * k
    else:
        map = torch.floor(map / k + shift) * k

    return map