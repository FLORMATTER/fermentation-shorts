#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Acha a MELHOR janela livre de texto para cada capa.

A ideia: para cada altura possivel de janela (da maior para a menor), varrer
todas as posicoes verticais e calcular quantos pixels de TEXTO existem dentro.
A primeira janela (mais alta) com ZERO texto vence.

Assim a gente para de chutar coordenadas na mao.
"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))


def e_texto(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    sat = (mx - mn) / mx if mx else 0
    if mn > 205 and sat < 0.12:          # branco
        return True
    if r > 200 and g > 150 and b < 110 and sat > 0.45:   # amarelo vivo
        return True
    return False


def mapa_texto(img):
    """Retorna lista por linha: quantos pixels de texto naquela linha (x/4)."""
    W, H = img.size
    px = img.convert("RGB").load()
    linhas = []
    for y in range(H):
        n = 0
        for x in range(0, W, 4):
            if e_texto(*px[x, y]):
                n += 1
        linhas.append(n)
    return linhas


def janelas_bos(linhas, H, min_alt, max_alt, tol_max=0):
    """
    Retorna as janelas candidatas ordenadas por altura desc.
    tol_max = quantos pixels de texto ainda toleramos (0 = nenhum).
    """
    # suavizar um pouco para nao quebrar por 1 linha solta
    cands = []
    for alt in range(max_alt, min_alt - 1, -8):
        for y0 in range(0, H - alt + 1, 8):
            total = sum(linhas[y0:y0 + alt])
            if total <= tol_max:
                cands.append((alt, y0, total))
    return cands


if __name__ == "__main__":
    alvos = [
        ("capa-beterraba-9x16.png", 620),
        ("capa-cebola-9x16.png", 620),
        ("capa-alho-9x16.png", 620),
        ("capa-chucrute-9x16.png", 620),
    ]
    for nome, min_alt in alvos:
        img = Image.open(os.path.join(BASE, nome))
        W, H = img.size
        linhas = mapa_texto(img)
        print(f"\n{'='*70}")
        print(f"{nome}")
        print(f"{'='*70}")
        # imprime o mapa resumido em blocos de 32px
        print("  ocupacao de texto por faixa de 32px:")
        for y0 in range(0, H, 32):
            tot = sum(linhas[y0:y0 + 32])
            if tot > 0:
                barra = "#" * min(60, tot // 12)
                print(f"    y{y0:5d}  {tot:6d}  {barra}")
        c = janelas_bos(linhas, H, min_alt, 1100, tol_max=0)
        print(f"\n  janelas 100%% limpas (alt >= {min_alt}), top 6:")
        for alt, y0, t in c[:6]:
            print(f"    alt {alt:4d}  y {y0:5d} -> {y0+alt:5d}")
        if not c:
            print("  >>> NENHUMA janela 100% limpa nesse tamanho")
            c = janelas_bos(linhas, H, min_alt, 1100, tol_max=40)
            print("  melhor com tolerancia 40 px de texto:")
            for alt, y0, t in c[:6]:
                print(f"    alt {alt:4d}  y {y0:5d} -> {y0+alt:5d}  (ruido {t})")
