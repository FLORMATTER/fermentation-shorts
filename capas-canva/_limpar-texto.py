#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Removedor de texto queimado (OpenCV inpaint).

O PROBLEMA
----------
As capas do Canva tem o texto portugues QUEIMADO no PNG. Nas capas onde o
titulo cai NO MEIO DA ARTE (cebola, beterraba, alho, chucrute) nao existe
janela limpa: medido em _janelas.py, a densidade de texto na area do assunto
chega a 16000 pixels.

TENTATIVAS QUE FALHARAM (registro para nao repetir)
---------------------------------------------------
  * borrar no lugar                  -> portugues continua legivel
  * esticar textura de cima          -> listras horizontais
  * so recortar a "janela limpa"     -> nao existe janela alta o suficiente
  * recortar janela pequena + zoom   -> vira borrao ilegivel (6x de aumento)

A SOLUCAO (esta)
----------------
  1. acha os pixels de texto por cor (branco puro / amarelo vivo)
  2. engorda a mascara o suficiente para pegar o antialias das bordas
  3. cv2.inpaint(..., INPAINT_TELEA) reconstroi o fundo por tras do texto
  4. o resultado e uma arte limpa, sem buracos, sem listras

Assim a capa inteira pode ser usada, sem precisar de rodape nem zoom.

Uso:  python _limpar-texto.py
"""

import os
import numpy as np
import cv2
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(BASE, "_limpas")
os.makedirs(SAIDA, exist_ok=True)


def mascara_texto(bgr, folga=3, limiar_branco=178, limiar_amar=0.36):
    """
    Devolve mascara binaria (0/255) dos pixels que sao texto do Canva.
    Criterios (em RGB):
      branco:  min(r,g,b) > limiar_branco  e  saturacao < 0.15
      amarelo: r > 175, g > 130, b < 135, saturacao > limiar_amar

    Os limiares sao GENEROSOS de proposito: e melhor apagar um pouco do fundo
    (o inpaint reconstroi) do que deixar sobra de texto. Alguns textos do Canva
    sao menores/apagados (ex.: "5 A 7 DIAS" do rabanete) e escapavam do
    criterio antigo, tao apertado quanto o usado para MEDIR densidade.

    Depois dilata `folga` px para cobrir o antialias/sombra do texto.
    """
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

    branco = (mn > limiar_branco) & (sat < 0.15)
    amarelo = (r > 175) & (g > 130) & (b < 135) & (sat > limiar_amar)
    m = (branco | amarelo).astype(np.uint8) * 255

    if folga > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (folga * 2 + 1,) * 2)
        m = cv2.dilate(m, k, iterations=1)
    return m


def limpar(caminho, saida, folga=3, raio=7, metodo="telea", suavizar=True,
           limpar_selo=True):
    """
    Remove o texto queimado (+ o selo verde antigo) e salva a arte limpa.

    limpar_selo=True: o selo "CAPITULO N DE 7" fica no canto superior esquerdo.
    Depois do inpaint o texto dele sai, mas sobra um borrao verde. Entao a
    gente inclui o VERDE daquela caixa na mascara tambem -> o canto fica
    reconstruido com o fundo da foto.
    """
    bgr = cv2.imread(caminho)
    if bgr is None:
        raise IOError("nao abriu " + caminho)

    m = mascara_texto(bgr, folga)

    if limpar_selo:
        # verde apenas nas regioes onde o selo pode estar (cantos superiores).
        # repolho tem o selo na DIREITA; os outros na esquerda.
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.int16)
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        verde = ((g > 60) & (g > r * 1.25) & (g > b * 1.25)).astype(np.uint8) * 255
        caixa = np.zeros_like(verde)
        caixa[80:560, 20:430] = 255       # canto superior esquerdo
        caixa[120:300, 700:1050] = 255    # canto superior direito (repolho)
        verde = cv2.bitwise_and(verde, caixa)
        if folga > 0:
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (folga * 2 + 1,) * 2)
            verde = cv2.dilate(verde, k, iterations=1)
        m = cv2.bitwise_or(m, verde)

    bandeira = cv2.INPAINT_TELEA if metodo == "telea" else cv2.INPAINT_NS
    out = cv2.inpaint(bgr, m, raio, bandeira)

    # uma passada leve de suavizacao so onde foi reconstruido,
    # para disfarcar a transicao do inpaint
    if suavizar:
        borr = cv2.GaussianBlur(out, (0, 0), 2.2)
        a = (m.astype(np.float32) / 255.0)[:, :, None]
        out = (out * (1 - a) + borr * a).astype(np.uint8)

    cv2.imwrite(saida, out)

    pct = 100.0 * (m > 0).sum() / m.size
    return pct


if __name__ == "__main__":
    alvos = [
        "capa-repolho-9x16.png", "capa-cenoura-9x16.png",
        "capa-rabanete-9x16.png", "capa-couve-flor-9x16.png",
        "capa-beterraba-9x16.png", "capa-cebola-9x16.png",
        "capa-alho-9x16.png", "capa-chucrute-9x16.png",
    ]
    print()
    for nome in alvos:
        src = os.path.join(BASE, nome)
        dst = os.path.join(SAIDA, nome)
        try:
            pct = limpar(src, dst)
            kb = os.path.getsize(dst) // 1024
            print("[OK] %-30s  area apagada %.2f%%  %d KB" % (nome, pct, kb))
        except Exception as e:
            print("[ERRO] %-30s  %s" % (nome, e))
