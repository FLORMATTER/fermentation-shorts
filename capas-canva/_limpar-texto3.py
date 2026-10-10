#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LIMPEZA REFORCADA v3 - _limpas4

Diferenca da v2: a mascara de BANDA nao apaga "tudo que e claro" na faixa
inteira. Isso pegava reflexos do VIDRO/tampa do pote (a cenoura ficou com a
tampa borrada). Agora, dentro da banda, a gente so apaga pixels que formam
TEXTO: componentes conexos com geometria de letra -- caixas pequenas/medias,
alinhadas, e que NAO sao enormes manchas de brilho.

Estrategia:
1. mascara por cor (limiar moderado) global -> pega texto puro
2. dentro das bandas, conecta os componentes e mantem apenas os que se
   parecem com letras (altura 20..220 px, largura <= 900)
3. remove componentes muito "gordos" (brilho do vidro): razao
   area/(w*h) alta E largura grande -> descarta
4. inpaint telea raio 11

Uso: python _limpar-texto3.py
"""
import os
import numpy as np
import cv2

BASE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(BASE, "_limpas4")
os.makedirs(SAIDA, exist_ok=True)

BANDAS = {
    "capa-repolho-9x16.png":    [(250, 485), (1495, 1705)],
    "capa-cenoura-9x16.png":    [(950, 1095), (1415, 1675)],
    "capa-rabanete-9x16.png":   [(440, 636), (1585, 1695)],
    "capa-couve-flor-9x16.png": [(515, 745), (1295, 1505)],
    "capa-beterraba-9x16.png":  [(940, 1085), (1090, 1345)],
    "capa-cebola-9x16.png":     [(895, 1175), (1505, 1705)],
    "capa-alho-9x16.png":       [(940, 1070), (1405, 1650)],
    "capa-chucrute-9x16.png":   [(222, 605), (1615, 1695)],
}


def mascara_cor(bgr, mn_min=140, sat_max=0.20):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    branco = ((mn > mn_min) & (sat < sat_max))
    amarelo = ((r > 165) & (g > 125) & (b < 150) & ((r - b) > 55))
    return (branco | amarelo).astype(np.uint8) * 255


def dentro_das_bandas(bgr, bandas):
    """Mantem so o texto dentro das bandas conhecidas, filtrando blobs."""
    h, w = bgr.shape[:2]
    base = mascara_cor(bgr, mn_min=120, sat_max=0.26)

    m = np.zeros((h, w), np.uint8)
    for (y0, y1) in bandas:
        y0 = max(0, y0); y1 = min(h, y1)
        sub = base[y0:y1].copy()

        # fecha pequenos buracos entre letras -> blobs por linha
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 5))
        sub = cv2.morphologyEx(sub, cv2.MORPH_CLOSE, k)

        n, lab, stats, _ = cv2.connectedComponentsWithStats(sub, 8)
        keep = np.zeros_like(sub)
        for i in range(1, n):
            x, yy, ww, hh, area = stats[i]
            if hh < 14 or ww < 8:
                continue
            if hh > 260:                       # bloco gigante = brilho/objeto
                continue
            dens = area / float(max(ww * hh, 1))
            # blob muito "cheio" e grande -> provavel brilho do vidro
            if ww > 700 and dens > 0.55 and hh > 60:
                continue
            # letras tem densidade tipica 0.15..0.65
            if dens < 0.08:
                continue
            keep[yy:yy + hh, x:x + ww] = np.maximum(
                keep[yy:yy + hh, x:x + ww], sub[yy:yy + hh, x:x + ww])
        m[y0:y1] = keep

    k2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    m = cv2.dilate(m, k2, iterations=1)
    return m


def verde_selo(bgr, folga=7):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    verde = ((g > 55) & (g > r * 1.20) & (g > b * 1.20)).astype(np.uint8) * 255
    caixa = np.zeros_like(verde)
    caixa[60:580, 10:440] = 255
    caixa[100:320, 690:1060] = 255
    verde = cv2.bitwise_and(verde, caixa)
    if folga > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (folga * 2 + 1,) * 2)
        verde = cv2.dilate(verde, k, iterations=1)
    return verde


def limpar(caminho, saida):
    bgr = cv2.imread(caminho)
    nome = os.path.basename(caminho)

    m_bandas = dentro_das_bandas(bgr, BANDAS.get(nome, []))
    m_cor = mascara_cor(bgr, mn_min=175, sat_max=0.14)   # texto puro global
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    m_cor = cv2.dilate(m_cor, k, iterations=1)
    m_selo = verde_selo(bgr)

    m = np.maximum(np.maximum(m_bandas, m_cor), m_selo)
    out = cv2.inpaint(bgr, m, 11, cv2.INPAINT_TELEA)

    borr = cv2.GaussianBlur(out, (0, 0), 2.4)
    a = (m.astype(np.float32) / 255.0)[:, :, None]
    out = (out * (1 - a) + borr * a).astype(np.uint8)

    cv2.imwrite(saida, out)
    return 100.0 * (m > 0).sum() / m.size


if __name__ == "__main__":
    alvos = [
        "capa-repolho-9x16.png", "capa-cenoura-9x16.png",
        "capa-rabanete-9x16.png", "capa-couve-flor-9x16.png",
        "capa-beterraba-9x16.png", "capa-cebola-9x16.png",
        "capa-alho-9x16.png", "capa-chucrute-9x16.png",
    ]
    print()
    for n in alvos:
        try:
            pct = limpar(os.path.join(BASE, n), os.path.join(SAIDA, n))
            kb = os.path.getsize(os.path.join(SAIDA, n)) // 1024
            print("[OK] %-30s apagado %.2f%%  %d KB" % (n, pct, kb))
        except Exception as e:
            print("[ERRO] %-30s %s" % (n, e))
