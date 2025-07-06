import numpy as np
import torch


def color_range(R, G, B):
    img = torch.stack([R, G, B])
    max_RGB = torch.max(img, dim=-1)
    min_RGB = torch.min(img, dim=-1)

    return min_RGB, max_RGB, max_RGB - min_RGB


def sat_hsv(C, V):
    S = np.zeros(V.shape)
    S[V != 0] = C[V != 0] / V[V != 0]
    return S


def sat_hsl(C, V):
    L = V - C/2
    S = torch.zeros(C.shape)
    S[0 < L < 1] = C[0 < L < 1] / (1 - torch.abs(2*V[0 < L < 1] - C[0 < L < 1] - 1))
    return S


def hue(R, G, B, V, S):
    max_r = V == R
    max_g = V == G
    max_b = V == B

    H = torch.zeros(S.shape)
    H[max_r] = 60 * (((G[max_r] - B[max_r]) / C[max_r]) % 6)
    H[max_g] = 60 * (((B[max_g] - R[max_g]) / C[max_g]) + 2)
    H[max_b] = 60 * (((R[max_b] - G[max_b]) / C[max_b]) + 4)
    H = H / 360
    return H


def rgb_to_hsv(R, G, B):
    min_RGB, V, C = color_range(R, G, B)
    S = sat_hsv(C, V)
    H = hue(R, G, B, V, S)

    return np.array([H, S, V]).transpose((1, 2, 0))


def rgb_to_hsl(R, G, B):
    min_RGB, V, C = color_range(R, G, B)
    L = V - C/2
    S = sat_hsl(C, V)
    H = hue(R, G, B, V, S)

    return np.array([H, S, L]).transpose((1, 2, 0))


def grey_scale(R, G, B):
    return torch.mean(torch.stack([R, G, B]))


def hsv_to_rgb(H, S, V):
    C = V * S
    H_rgb = H * 360 / 60
    X = C * (1 - torch.abs((H_rgb % 2) - 1))

    R, G, B = torch.zeros(H.shape), torch.zeros(H.shape), torch.zeros(H.shape)

    R[H<6] = C[H<6]
    G[H<6] = 0
    B[H<6] = X[H<6]

    R[H<5] = X[H<5]
    G[H<5] = 0
    B[H<5] = C[H<5]

    R[H<4] = 0
    G[H<4] = X[H<4]
    B[H<4] = C[H<4]

    R[H<3] = 0
    G[H<3] = C[H<3]
    B[H<3] = X[H<3]

    R[H<2] = X[H<2]
    G[H<2] = C[H<2]
    B[H<2] = 0

    R[H<1] = C[H<1]
    G[H<1] = X[H<1]
    B[H<1] = 0

    return R, G, B


def hsl_to_rgb(H, S, L):
    C = (1-torch.abs(2*L-1) * S)
    H_rgb = H * 360 / 60
    X = C * (1 - torch.abs((H_rgb % 2) - 1))

    R, G, B = torch.zeros(H.shape), torch.zeros(H.shape), torch.zeros(H.shape)

    R[H<6] = C[H<6]
    G[H<6] = 0
    B[H<6] = X[H<6]

    R[H<5] = X[H<5]
    G[H<5] = 0
    B[H<5] = C[H<5]

    R[H<4] = 0
    G[H<4] = X[H<4]
    B[H<4] = C[H<4]

    R[H<3] = 0
    G[H<3] = C[H<3]
    B[H<3] = X[H<3]

    R[H<2] = X[H<2]
    G[H<2] = C[H<2]
    B[H<2] = 0

    R[H<1] = C[H<1]
    G[H<1] = X[H<1]
    B[H<1] = 0

    return R, G, B
