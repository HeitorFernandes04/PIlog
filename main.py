import argparse
import os
import sys

import numpy as np
from PIL import Image

from logaritmica import transformacao_log


def carregar(caminho, cinza):
    imagem = Image.open(caminho)
    if cinza:
        imagem = imagem.convert("L")
    elif imagem.mode not in ("L", "RGB"):
        imagem = imagem.convert("RGB")
    return np.array(imagem)


def processar_imagem(caminho, pasta_saida, cinza, mostrar):
    original = carregar(caminho, cinza)
    resultado = transformacao_log(original)

    os.makedirs(pasta_saida, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0]
    destino = os.path.join(pasta_saida, f"{nome}_log.png")
    Image.fromarray(resultado).save(destino)
    print(f"imagem: {caminho}  ->  {destino}")

    if mostrar:
        Image.fromarray(original).show(title="original")
        Image.fromarray(resultado).show(title="log")


def rodar_testes():
    entrada = np.array([0, 16, 64, 127, 191, 255], dtype=np.uint8)
    saida = transformacao_log(entrada)
    print("entrada:", entrada.tolist())
    print("saida:  ", saida.tolist())

    erros = []
    if saida[0] != 0:
        erros.append("r=0 deveria virar s=0 (preto continua preto)")
    if saida[-1] != 255:
        erros.append("r=255 deveria virar s=255 (branco continua branco)")
    if not np.all(np.diff(saida.astype(int)) >= 0):
        erros.append("a saida deveria ser crescente (funcao monotona)")
    if not np.all(saida[1:-1] > entrada[1:-1]):
        erros.append("valores intermediarios deveriam clarear (s > r)")

    if erros:
        print("FALHOU:")
        for erro in erros:
            print(f"  - {erro}")
        return 1

    print("OK: extremos batem, funcao crescente, clareia os tons intermediarios")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Transformacao logaritmica de intensidade (s = c*log(1+r))."
    )
    parser.add_argument("imagem", nargs="?", help="imagem de entrada")
    parser.add_argument("--saida", default="saida", help="pasta dos resultados")
    parser.add_argument("--cinza", action="store_true",
                        help="converte para tons de cinza antes de processar")
    parser.add_argument("--mostrar", action="store_true",
                        help="abre a imagem original e o resultado")
    parser.add_argument("--testes", action="store_true",
                        help="confere a formula em valores conhecidos")
    args = parser.parse_args()

    if args.testes:
        return rodar_testes()

    if not args.imagem:
        parser.print_help()
        return 1

    processar_imagem(args.imagem, args.saida, args.cinza, args.mostrar)
    return 0


if __name__ == "__main__":
    sys.exit(main())