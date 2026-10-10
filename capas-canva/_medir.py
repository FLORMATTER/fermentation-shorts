#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mede as coordenadas exatas dos blocos de texto queimados nas capas.

Estrategia: o texto do Canva e BRANCO ou AMARELO/LARANJA, sempre muito mais
claro que o fundo escuro. Entao varremos linha por linha contando pixels
"claros". Onde a contagem sobe, tem texto. Onde volta a zero, acabou.

Isso nos da as faixas (y0, y1) com precisao, sem chutar.

Uso:  python _medir.py
"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))


def e_texto(r, g, b):
    """
    Pixel que provavelmente e TEXTO do Canva.
    Critério apertado para nao confundir com a arte clara (vidro, sal, alho):
      - branco quase puro
      - amarelo/laranja SATURADO (o texto amarelo e bem mais vivo que a madeira)
    """
    mx, mn = max(r, g, b), min(r, g, b)
    sat = (mx - mn) / mx if mx else 0
    # branco: claro e dessaturado
    if mn > 205 and sat < 0.12:
        return True
    # amarelo do Canva: R e G altos, B baixo, saturacao alta
    if r > 200 and g > 150 and b < 110 and sat > 0.45:
        return True
    return False


def mapear(nome):
    img = Image.open(os.path.join(BASE, nome)).convert("RGB")
    W, H = img.size
    px = img.load()

    linhas = []
    for y in range(0, H, 4):
        n = 0
        for x in range(0, W, 4):
            if e_texto(*px[x, y]):
                n += 1
        linhas.append((y, n))

    # agrupar linhas consecutivas com contagem >= 3 em "blocos"
    blocos = []
    ini = None
    vazio = 0
    for y, n in linhas:
        if n >= 3:
            if ini is None:
                ini = y
            vazio = 0
        else:
            if ini is not None:
                vazio += 4
                if vazio >= 40:          # 40px sem texto = fim do bloco
                    blocos.append((ini, y - vazio + 4))
                    ini = None
    if ini is not None:
        blocos.append((ini, H))

    print(f"\n{'='*66}")
    print(f"{nome}   ({W}x{H})")
    print(f"{'='*66}")
    for (a, b) in blocos:
        if b - a < 14:
            continue
        # amostrar: em que x comeca e termina o texto do bloco?
        xs = []
        for y in range(a, b, 3):
            for x in range(0, W, 4):
                if e_texto(*px[x, y]):
                    xs.append(x)
        if not xs:
            continue
        print(f"  y {a:5d} -> {b:5d}   (alt {b-a:4d})   x {min(xs):5d} -> {max(xs):5d}   centrado={'SIM' if abs((min(xs)+max(xs))/2 - W/2) < 60 else 'NAO'}")
    return blocos


if __name__ == "__main__":
    for f in ["capa-repolho-9x16.png", "capa-cenoura-9x16.png", "capa-rabanete-9x16.png",
              "capa-couve-flor-9x16.png", "capa-beterraba-9x16.png", "capa-cebola-9x16.png",
              "capa-alho-9x16.png", "capa-chucrute-9x16.png"]:
        mapear(f)
