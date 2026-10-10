#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CAPAS EM INGLES - montagem FINAL (v13)

FLUXO COMPLETO
--------------
  _limpar-texto.py   ->  _limpas/capa-<legume>-9x16.png
        (OpenCV inpaint remove o portugues queimado e o selo verde antigo)

  _traduzir-capas.py ->  _english/capa-<legume>-en-9x16.png
        (esta versao: pega a arte LIMPA, sem texto nenhum, e poe o rodape
         solido com o texto em ingles)

POR QUE AGORA DA CERTO
----------------------
Nas versoes anteriores a gente tentava RECORTAR uma parte limpa da arte.
Medido, nao existe janela alta o suficiente (_janelas.py). Com o inpaint a
arte INTEIRA fica limpa, entao nao precisa mais recortar nem dar zoom: a
capa usa o enquadramento original do Canva, so com o texto traduzido.

Uso:  python _limpar-texto.py  &&  python _traduzir-capas.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

BASE = os.path.dirname(os.path.abspath(__file__))
LIMPO = os.path.join(BASE, "_limpas2")
SAIDA = os.path.join(BASE, "_english")
os.makedirs(SAIDA, exist_ok=True)

W, H = 1080, 1920
RODAPE = 560
ARTE_H = H - RODAPE          # 1360

R = (255, 255, 255)
Y = (250, 208, 74)
VERDE = (46, 110, 46)
FUNDO = (11, 11, 13)

F_BLACK = "C:/Windows/Fonts/ariblk.ttf"
F_BOLD = "C:/Windows/Fonts/arialbd.ttf"
F_IMPACT = "C:/Windows/Fonts/impact.ttf"


def ft(caminho, tam):
    for c in (caminho, "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, tam)
            except Exception:
                pass
    return ImageFont.load_default()


def montar(entrada, saida, nome, sal, tempo, num=0, com_badge=True,
           topo_extra=0):
    """
    entrada : arquivo dentro de _limpas (ja sem texto portugues)
    topo_extra : quantos px cortar do topo (para tirar sobras de selo)
    """
    src = Image.open(os.path.join(LIMPO, entrada)).convert("RGB")
    if topo_extra:
        src = src.crop((0, topo_extra, src.size[0], src.size[1]))

    # arte cover em 1080xARTE_H, a partir do topo (o enquadramento original
    # do Canva tem o assunto centralizado; ancoramos no topo e cortamos o
    # excesso em baixo, que e mesa vazia)
    fw, fh = src.size
    esc = max(W / fw, ARTE_H / fh)
    nw, nh = max(W, int(fw * esc)), max(ARTE_H, int(fh * esc))
    arte = src.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - W) // 2
    arte = arte.crop((x0, 0, x0 + W, ARTE_H))

    canvas = Image.new("RGB", (W, H), FUNDO)
    canvas.paste(arte, (0, 0))

    d = ImageDraw.Draw(canvas, "RGBA")

    # ---------- rodape solido ----------
    d.rectangle([0, ARTE_H, W, H], fill=FUNDO)
    tr = 170
    for i in range(tr):
        a = int(255 * (i / tr) ** 0.85)
        d.line([(0, ARTE_H - tr + i), (W, ARTE_H - tr + i)], fill=FUNDO + (a,))

    if com_badge:
        bx, by, bw, bh = 54, 54, 262, 60
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6, fill=VERDE)
        f = ft(F_BOLD, 31)
        txt = f"CHAPTER {num} OF 7"
        tw = d.textlength(txt, font=f)
        while tw > bw - 16 and f.size > 15:
            f = ft(F_BOLD, f.size - 2)
            tw = d.textlength(txt, font=f)
        d.text((bx + (bw - tw) / 2, by + (bh - f.size) / 2 - 3), txt,
               font=f, fill=(255, 255, 255))

    # nome
    y = ARTE_H + 66
    f_nome = ft(F_BLACK, 92)
    while d.textlength(nome, font=f_nome) > W - 80 and f_nome.size > 50:
        f_nome = ft(F_BLACK, f_nome.size - 4)
    tw = d.textlength(nome, font=f_nome)
    x = (W - tw) / 2
    for dx, dy in ((-3, 3), (3, 3), (3, -3), (-3, -3)):
        d.text((x + dx, y + dy), nome, font=f_nome, fill=(0, 0, 0, 175))
    d.text((x, y), nome, font=f_nome, fill=R)

    y += f_nome.size + 38
    d.line([(W * 0.31, y + 6), (W * 0.69, y + 6)], fill=(240, 200, 70, 235), width=4)
    y += 46
    f_sal = ft(F_BOLD, 50)
    while d.textlength(sal, font=f_sal) > W - 90 and f_sal.size > 28:
        f_sal = ft(F_BOLD, f_sal.size - 2)
    tw = d.textlength(sal, font=f_sal)
    d.text(((W - tw) / 2, y), sal, font=f_sal, fill=R)
    y += 74
    f_t = ft(F_IMPACT, 104)
    while d.textlength(tempo, font=f_t) > W - 70 and f_t.size > 56:
        f_t = ft(F_IMPACT, f_t.size - 2)
    tw = d.textlength(tempo, font=f_t)
    d.text(((W - tw) / 2, y), tempo, font=f_t, fill=Y)

    destino = os.path.join(SAIDA, saida)
    canvas.save(destino, "PNG", optimize=True)
    return destino


def main():
    # (arquivo em _limpas2, saida, nome, sal, tempo, num, topo_extra, badge)
    # topo_extra: corta N px do topo para eliminar sobras de texto/selo que o
    #             inpaint deixou no fundo escuro (onde qualquer reconstrucao
    #             aparece contra o preto). Couve-flor tem o topo todo preto,
    #             entao cortar 600px nao perde nada.
    T = [
        ("capa-repolho-9x16.png",    "capa-repolho-en-9x16.png",    "RED CABBAGE",  "2% SALT",   "7 DAYS",      1,  360, True),
        ("capa-cenoura-9x16.png",    "capa-cenoura-en-9x16.png",    "CARROTS",      "2% SALT",   "6 DAYS",      2,  420, True),
        ("capa-rabanete-9x16.png",   "capa-rabanete-en-9x16.png",   "RADISHES",     "2% SALT",   "5-7 DAYS",    3,  260, True),
        ("capa-couve-flor-9x16.png", "capa-couve-flor-en-9x16.png", "CAULIFLOWER",  "2.5% SALT", "7-10 DAYS",   4,  600, True),
        ("capa-beterraba-9x16.png",  "capa-beterraba-en-9x16.png",  "BEETROOT",     "2% SALT",   "7-10 DAYS",   5,  300, True),
        ("capa-cebola-9x16.png",     "capa-cebola-en-9x16.png",     "ONION + BEET", "2% SALT",   "10-14 DAYS",  6,  400, True),
        ("capa-alho-9x16.png",       "capa-alho-en-9x16.png",       "GARLIC HONEY", "NO SALT",   "3-4 WEEKS",   7,  300, True),
    ]

    gerados = []
    for (arq, saida, nome, sal, tempo, num, topo, badge) in T:
        gerados.append(montar(arq, saida, nome, sal, tempo, num, badge, topo))

    gerados.append(montar("capa-chucrute-9x16.png", "capa-chucrute-en-9x16.png",
                          "SAUERKRAUT", "2% SALT · NO WATER", "READY IN 7 DAYS",
                          0, False, 110))

    print()
    for g in gerados:
        im = Image.open(g)
        print("[OK] %-34s %dx%d  %4d KB"
              % (os.path.basename(g), im.size[0], im.size[1],
                 os.path.getsize(g) // 1024))


if __name__ == "__main__":
    main()
