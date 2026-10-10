#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Monta as 7 capas 9:16 (1080x1920) dos Shorts a partir dos candidatos
aprovados do Canva (400x600 cada).

Por que existe: a API de export do Canva recusou todos os designs 9:16
("Not allowed to access design"), enquanto o design 16:9 exporta normal.
Como os candidatos ja estavam baixados em 400x600, montamos a capa final
localmente.

DECISAO DE DESIGN
-----------------
Os candidatos do Canva JA vem com o texto pronto (nome + sal + tempo),
porem em 400x600 (2:3) e nao em 9:16. Entao NAO escrevemos texto por
cima -- isso gerava duplicacao. Em vez disso:

  * fundo = a arte esticada para 1080x1920, desfocada e escurecida
  * a arte nitida entra em full-bleed (cobre a largura toda)
  * o pequeno excesso vertical e resolvido com corte no centro

Resultado: capa 1080x1920 com a arte e o texto originais do Canva,
sem nenhuma camada de texto adicionada por nos.

Uso:  python _gerar-capas.py
"""
import os
from PIL import Image, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(BASE, "_rascunho")

W, H = 1080, 1920

CAPAS = [
    ("r2.png",   "capa-repolho-9x16.png"),
    ("cen4.png", "capa-cenoura-9x16.png"),
    ("rab1.png", "capa-rabanete-9x16.png"),
    ("cf1.png",  "capa-couve-flor-9x16.png"),
    ("bet1.png", "capa-beterraba-9x16.png"),
    ("ceb1.png", "capa-cebola-9x16.png"),
    ("alh3.png", "capa-alho-9x16.png"),
]


def montar(origem, destino):
    arte = Image.open(origem).convert("RGB")
    ow, oh = arte.size

    # 1) fundo desfocado cobrindo 9:16 (evita qualquer borda vazia)
    escala = max(W / ow, H / oh)
    bg = arte.resize((int(ow * escala) + 1, int(oh * escala) + 1), Image.LANCZOS)
    bx = (bg.width - W) // 2
    by = (bg.height - H) // 2
    bg = bg.crop((bx, by, bx + W, by + H))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=48))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)

    # 2) arte nitida em full-bleed (cobre a largura; sobra altura -> corta)
    escala_arte = W / ow
    largura_arte = W
    alt_arte = int(oh * escala_arte)
    arte_g = arte.resize((largura_arte, alt_arte), Image.LANCZOS)

    if alt_arte > H:
        # corte centrado -- como o texto dos candidatos fica no rodape,
        # cortamos um pouco mais do topo para preservar o rodape inteiro
        excesso = alt_arte - H
        corte = int(excesso * 0.35)
        arte_g = arte_g.crop((0, corte, largura_arte, corte + H))
    else:
        # raro: arte mais baixa que o canvas -> centraliza sobre o fundo
        arte_g = arte_g.crop((0, 0, largura_arte, alt_arte))

    x = 0
    y = (H - arte_g.size[1]) // 2
    bg.paste(arte_g, (x, y))

    bg.save(destino, "PNG", optimize=True)
    return bg.size


def main():
    feitas = []
    for origem, saida in CAPAS:
        caminho = os.path.join(DRAFT, origem)
        if not os.path.exists(caminho):
            print(f"[FALTA] {origem}")
            continue
        destino = os.path.join(BASE, saida)
        w, h = montar(caminho, destino)
        kb = os.path.getsize(destino) // 1024
        print(f"[OK] {saida:30s} {w}x{h}  {kb} KB")
        feitas.append(saida)

    print(f"\nTotal: {len(feitas)}/7 capas geradas.")


if __name__ == "__main__":
    main()
