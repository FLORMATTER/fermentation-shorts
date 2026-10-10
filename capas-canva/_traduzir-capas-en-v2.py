#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CAPAS EM INGLES - LAYOUT IDENTICO AO PORTUGUES (v14)

O QUE MUDOU DA v13
------------------
Na v13 o nome ia para um RODAPE solido escuro no pe da capa (tudo centralizado
em baixo). Isso NAO e o layout do portugues.

No portugues (medido em _medir2.py / _medir3.py) o layout e:

    [selo verde redondo]              <- canto superior esquerdo
    NOME DO LEGUME      (branco, Arial Black, bloco centralizado)
    2% DE SAL           (amarelo, menor)
    7 DIAS              (amarelo, maior)

...tudo posicionado NA PROPRIA ARTE, e nao num rodape. O nome fica onde
estava o titulo portugues (topo ou meio da imagem, conforme a capa), e as
linhas de sal/tempo logo abaixo, tambem sobre a arte.

Excecao: CHUCRUTE tinha o titulo no topo (2 linhas) + pill amarela.

COMO
----
1. _limpar-texto.py ja apagou TODO o texto portugues (inpaint) -> _limpas2
2. aqui a gente abre a arte limpa e REDesenha o texto em ingles nas
   coordenadas medidas do original (por capa, na tabela T abaixo).

Uso:  python _limpar-texto.py && python _traduzir-capas-en-v2.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
LIMPO = os.path.join(BASE, "_limpas4")
SAIDA = os.path.join(BASE, "_english")
os.makedirs(SAIDA, exist_ok=True)

W, H = 1080, 1920

BRANCO = (255, 255, 255)
AMARELO = (250, 208, 74)
VERDE = (46, 110, 46)

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


def _sombra(d, x, y, txt, f, cor=(0, 0, 0, 170)):
    for dx, dy in ((-3, 3), (3, 3), (3, -3), (-3, -3)):
        d.text((x + dx, y + dy), txt, font=f, fill=cor)


def desenha_nome(d, nome, y, tam, larg_max, alvo_cx=None, cor=BRANCO):
    """
    Nome do legume (Arial Black, branco). Suporta '\n' para 2 linhas.
    Cada linha e centralizada no bloco (alvo_cx = W/2 por padrao).
    Devolve a altura total usada.
    """
    linhas = nome.split("\n")
    f = ft(F_BLACK, tam)
    while max(d.textlength(l, font=f) for l in linhas) > larg_max and f.size > 40:
        f = ft(F_BLACK, f.size - 3)
    entrelinha = f.size * 1.04
    cx = alvo_cx if alvo_cx is not None else W / 2
    for i, l in enumerate(linhas):
        tw = d.textlength(l, font=f)
        x = cx - tw / 2
        yy = y + i * entrelinha
        _sombra(d, x, yy, l, f)
        d.text((x, yy), l, font=f, fill=cor)
    return int(entrelinha * len(linhas))


def desenha_amarelo(d, txt, y, tam, larg_max, cor=AMARELO):
    """Linha amarela (Arial Black) centralizada. Devolve altura usada."""
    f = ft(F_BLACK, tam)
    while d.textlength(txt, font=f) > larg_max and f.size > 26:
        f = ft(F_BLACK, f.size - 2)
    tw = d.textlength(txt, font=f)
    x = (W - tw) / 2
    _sombra(d, x, y, txt, f, cor=(0, 0, 0, 165))
    d.text((x, y), txt, font=f, fill=cor)
    return f.size


def selo(img, texto="CHAPTER 1 OF 7"):
    """Selo verde REDONDO no canto superior esquerdo (igual ao portugues)."""
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy, r = 148, 148, 94
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=VERDE + (255,))
    f = ft(F_BOLD, 26)
    p = texto.split()
    linhas = [(" ".join(p[:2])), (" ".join(p[2:]))]
    linhas = [l for l in linhas if l]
    alt = f.size * 1.3 * len(linhas)
    y = cy - alt / 2
    for l in linhas:
        tw = d.textlength(l, font=f)
        d.text((cx - tw / 2, y), l, font=f, fill=(255, 255, 255))
        y += f.size * 1.3


def capa(entrada, saida, nome, sal, dias, sel="CHAPTER 1 OF 7",
         y_nome=300, tam_nome=150, tam_sal=58, tam_dias=100,
         pill=False, sub_txt=None, gap_sal=26, gap_dias=14,
         y_sal=None, y_dias=None):
    """
    y_nome   : topo do titulo em px (medido do original portugues).
    y_sal    : topo ABSOLUTO da linha de sal (se None, calcula relativo).
    y_dias   : topo ABSOLUTO dos dias (se None, calcula relativo).
    sal      : linha amarela menor (ou texto da pill).
    dias     : linha amarela maior ("" = nao desenhar).
    pill     : sal dentro de pill amarela (estilo chucrute).
    sub_txt  : linha branca pequena no pe (watermark).
    """
    img = Image.open(os.path.join(LIMPO, entrada)).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    if sel:
        selo(img, sel)
        d = ImageDraw.Draw(img, "RGBA")

    # ---------- nome (branco) ----------
    alt_nome = desenha_nome(d, nome, y_nome, tam_nome, W - 140)

    y = y_nome + alt_nome + gap_sal
    if y_sal is not None:
        y = y_sal

    # ---------- sal ----------
    if pill:
        f = ft(F_BOLD, tam_sal)
        tw = d.textlength(sal, font=f)
        pw, ph = tw + 56, f.size + 34
        px, py = (W - pw) / 2, y
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=6, fill=AMARELO)
        d.text((px + 28, py + (ph - f.size) / 2 - 5), sal, font=f,
               fill=(22, 22, 22))
        y = py + ph + gap_dias + 22
    else:
        alt_sal = desenha_amarelo(d, sal, y, tam_sal, W - 190)
        y = y + alt_sal + gap_dias

    # ---------- dias ----------
    if dias:
        if y_dias is not None:
            y = y_dias
        desenha_amarelo(d, dias, y, tam_dias, W - 150)

    if sub_txt:
        f = ft(F_BOLD, 30)
        tw = d.textlength(sub_txt, font=f)
        d.text(((W - tw) / 2, H - 130), sub_txt, font=f, fill=(255, 255, 255))

    destino = os.path.join(SAIDA, saida)
    img.save(destino, "PNG", optimize=True)
    return destino


def main():
    # Layout medido do portugues (_medir2/_medir3). Cada tupla:
    # (arquivo, saida, nome, sal, dias, selo, y_nome, tam_nome, tam_sal,
    #  tam_dias, y_sal, y_dias)
    T = [
        ("capa-repolho-9x16.png",    "capa-repolho-en-9x16.png",
         "RED CABBAGE", "2% SALT", "7 DAYS",      "CHAPTER 1 OF 7",
         285, 150, 56, 96, 1524, 1600),
        ("capa-cenoura-9x16.png",    "capa-cenoura-en-9x16.png",
         "CARROTS",     "2% SALT", "6 DAYS",      "CHAPTER 2 OF 7",
         972, 150, 56, 96, 1434, 1586),
        ("capa-rabanete-9x16.png",   "capa-rabanete-en-9x16.png",
         "RADISHES",    "2% SALT", "5-7 DAYS",    "CHAPTER 3 OF 7",
         462, 150, 56, 96, 1560, 1612),
        ("capa-couve-flor-9x16.png", "capa-couve-flor-en-9x16.png",
         "CAULIFLOWER", "2.5% SALT", "7-10 DAYS", "CHAPTER 4 OF 7",
         546, 112, 56, 96, 1318, 1404),
        ("capa-beterraba-9x16.png",  "capa-beterraba-en-9x16.png",
         "BEETROOT",    "2% SALT", "7-10 DAYS",   "CHAPTER 5 OF 7",
         962, 150, 56, 96, 1108, 1266),
        ("capa-cebola-9x16.png",     "capa-cebola-en-9x16.png",
         "ONION +\nBEET", "2% SALT", "10-14 DAYS", "CHAPTER 6 OF 7",
         912, 132, 56, 96, 1528, 1622),
        ("capa-alho-9x16.png",       "capa-alho-en-9x16.png",
         "GARLIC IN\nHONEY", "NO SALT", "3-4 WEEKS", "CHAPTER 7 OF 7",
         960, 132, 56, 96, 1422, 1566),
    ]

    gerados = []
    for (arq, saida, nome, sal, dias, sel, yn, tn, ts, td, ys, yd) in T:
        gerados.append(capa(arq, saida, nome, sal, dias, sel, yn,
                            tam_nome=tn, tam_sal=ts, tam_dias=td,
                            y_sal=ys, y_dias=yd))

    gerados.append(capa("capa-chucrute-9x16.png", "capa-chucrute-en-9x16.png",
                        "SAUERKRAUT\nIN 7 DAYS", "2% SALT - NO WATER", "",
                        "CHAPTER 8", 246, 146, 40, 0, pill=True,
                        sub_txt="JUST HANDS - NO FACE"))

    print()
    for g in gerados:
        im = Image.open(g)
        print("[OK] %-34s %dx%d  %4d KB"
              % (os.path.basename(g), im.size[0], im.size[1],
                 os.path.getsize(g) // 1024))


if __name__ == "__main__":
    main()
