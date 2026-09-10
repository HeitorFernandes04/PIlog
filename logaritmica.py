import numpy as np


def transformacao_log(imagem):
    r = imagem.astype(np.float64) / 255.0
    c = 1.0 / np.log(2)
    s = c * np.log(1 + r)
    return (s * 255).astype(np.uint8)