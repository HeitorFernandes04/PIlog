import sys

import numpy as np
from PIL import Image

from logaritmica import transformacao_log


def main():
    if len(sys.argv) != 2:
        print("uso: python3 main.py foto.jpg")
        return

    caminho = sys.argv[1]
    original = np.array(Image.open(caminho))
    resultado = transformacao_log(original)

    Image.fromarray(original).show(title="original")
    Image.fromarray(resultado).show(title="log")
    Image.fromarray(resultado).save("resultado.png")
    print("resultado salvo em resultado.png")


if __name__ == "__main__":
    main()