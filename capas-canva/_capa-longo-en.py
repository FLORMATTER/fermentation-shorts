#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Capa do VIDEO LONGO em ingles (1280x720) - thumb do YouTube.

DIFICULDADE ESPECIFICA DESTA CAPA
---------------------------------
O texto "30 DIAS" (amarelo, gigante) esta EM CIMA DOS POTES DE VIDRO.
Inpaint ali NAO funciona: o vidro e transparente, entao o algoritmo nao tem
o que reconstruir e vira uma mancha (testado: ficou um borrao verde/esbranquicado).

TRES ESTRATEGIAS TESTADAS (ver _teste-apagar30.py)
--------------------------------------------------
  A) inpaint TELEA .................. borrao verde -> RUIM
  B) clone das bordas (degrade vertical entre a linha 10px acima e a 10px
     abaixo da caixa) ............... FICOU OTIMO: o vidro reconstroi natural
  C) mediana por coluna ............. limpo, mas mais chapado que B

SOLUCAO ADOTADA = A (inpaint) nas linhas de cima/baixo + B (clone) na linha
do meio. Assim o "30 DIAS" ANTIGO DESAPARECE DE VERDADE, e o "30 DAYS" novo
e escrito depois sobre um fundo limpo (sem fantasma atras).
"""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(BASE, "_english")
os.makedirs(SAIDA, exist_ok=True)

W, H = 1280, 720

BRANCO = (255, 255, 255)
AMARELO = (255, 214, 0)
PRETO = (0, 0, 0)

# caixa do "30 DIAS" original (medida: x312..993 y284..444) + folga
CX0, CX1 = 300, 1005
CY0, CY1 = 272, 458

F_BLACK = "C:/Windows/Fonts/ariblk.ttf"
F_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def ft(caminho, tam):
    for c in (caminho, "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, tam)
            except Exception:
                pass
    return ImageFont.load_default()


def limpar_topo_e_base(bgr):
    """
    Apaga "7 LEGUMES" (parede escura) e "FACIL -> DIFICIL" (mesa de madeira)
    com inpaint -- la o fundo e solido e a reconstrucao funciona.
    """
    h, w = bgr.shape[:2]

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

    branco = ((mn > 175) & (sat < 0.16)).astype(np.uint8) * 255
    amarelo = ((r > 180) & (g > 135) & (b < 140) & (sat > 0.38)).astype(np.uint8) * 255

    cx = np.zeros((h, w), np.uint8)
    cx[70:255, 140:1150] = 255      # 7 LEGUMES   -> parede escura
    cx[580:685, 355:925] = 255      # FACIL->DIFICIL -> madeira

    m = np.zeros((h, w), np.uint8)
    for camada in (branco, amarelo):
        m = np.maximum(m, cv2.bitwise_and(camada, cx))

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    m = cv2.dilate(m, k, iterations=1)

    return cv2.inpaint(bgr, m, 9, cv2.INPAINT_TELEA)


def apagar_30dias(bgr):
    """
    Apaga o "30 DIAS" que esta SOBRE O VIDRO.

    Tecnica vencedora = "rente 1px" (testada em _teste-apagar30c.py):
      para cada pixel da caixa, interpola LINEARMENTE entre a cor da
      coluna NA LINHA IMEDIATAMENTE ACIMA (y0-1) e NA IMEDIATAMENTE
      ABAIXO (y1). Usar referencia RENTE (1 px) e o detalhe que importa:
      a reconstrucao ENCOSTA na referencia sem degrau -> nao aparece a
      "linha de emenda" que surgia com faixas de 10/25 px.

    Testado e descartado:
      - faixa de 10-25 px acima/abaixo -> cria tarja clara na emenda
      - usar o minimo das referencias    -> fica bom mas com leve faixa
      - blur forte do entorno            -> NAO apaga (so borra o texto)

    Resultado: o "30 DIAS" some por completo e o vidro/mesa ficam naturais.
    """
    out = bgr.copy()
    y0, y1, x0, x1 = CY0, CY1, CX0, CX1

    topo = bgr[y0 - 1, x0:x1].astype(np.float32)      # (larg, 3)
    base = bgr[y1, x0:x1].astype(np.float32)

    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    mix = topo[None, :, :] * (1 - t) + base[None, :, :] * t

    out[y0:y1, x0:x1] = np.clip(mix, 0, 255).astype(np.uint8)
    return out


def main():
    bgr = cv2.imread(os.path.join(BASE, "capa-video-longo-7-legumes.png"))
    bgr = limpar_topo_e_base(bgr)       # apaga topo e base (inpaint)
    bgr = apagar_30dias(bgr)            # apaga o "30 DIAS" sobre o vidro (clone)
    img = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(img)

    # ---------- 1. "7 VEGETABLES" (topo, branco) ----------
    f = ft(F_BLACK, 132)
    while d.textlength("7 VEGETABLES", font=f) > W - 120 and f.size > 60:
        f = ft(F_BLACK, f.size - 4)
    tw = d.textlength("7 VEGETABLES", font=f)
    x = (W - tw) / 2
    y = 84
    d.text((x, y), "7 VEGETABLES", font=f, fill=BRANCO,
           stroke_width=6, stroke_fill=(0, 0, 0))

    # ---------- 2. "30 DAYS" (meio, amarelo) ----------
    # O "30 DIAS" antigo ja foi apagado -> aqui e um fundo limpo.
    # Mantemos o MESMO tamanho/peso do original para a capa nao perder forca.
    f2 = ft(F_BLACK, 150)
    while d.textlength("30 DAYS", font=f2) > W - 260 and f2.size > 80:
        f2 = ft(F_BLACK, f2.size - 4)
    tw2 = d.textlength("30 DAYS", font=f2)
    x2 = (W - tw2) / 2
    y2 = 300
    d.text((x2, y2), "30 DAYS", font=f2, fill=AMARELO,
           stroke_width=9, stroke_fill=PRETO)

    # ---------- 3. "EASY -> HARD" (base, amarelo) ----------
    f3 = ft(F_BLACK, 60)
    txt3 = "EASY  \u2192  HARD"
    while d.textlength(txt3, font=f3) > W - 260 and f3.size > 34:
        f3 = ft(F_BLACK, f3.size - 2)
    tw3 = d.textlength(txt3, font=f3)
    x3 = (W - tw3) / 2
    y3 = 596
    d.text((x3, y3), txt3, font=f3, fill=AMARELO,
           stroke_width=5, stroke_fill=PRETO)

    destino = os.path.join(SAIDA, "capa-video-longo-en-1280x720.png")
    img.save(destino, "PNG", optimize=True)
    print("[OK] %s  %dx%d  %d KB" % (
        os.path.basename(destino), img.size[0], img.size[1],
        os.path.getsize(destino) // 1024))


if __name__ == "__main__":
    main()
