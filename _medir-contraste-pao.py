# -*- coding: utf-8 -*-
"""_medir-contraste-pao.py — mede o contraste dos elementos do short de pao.

    python _medir-contraste-pao.py

Nao olha PNG: calcula a cor EFETIVA de cada elemento (com o `opacity` composto
sobre o fundo) a partir do proprio SVG, e imprime a distancia RGB de cada par que
precisa se distinguir.

Por que existe: o render mostrou o pote do levain como um BLOCO PALIDO e os
circulos 'levain'/'farinha' como o MESMO circulo. "Dá pra ver" nao e' medida —
abaixo de ~130 de distancia nao se le'. Aqui o numero aparece antes do conserto.
"""
import re
import sys

LIMITE = 130


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def sobre(cor, fundo, op):
    """Cor com `opacity` composta sobre o fundo."""
    c, f = rgb(cor), rgb(fundo)
    return tuple(round(op * c[i] + (1 - op) * f[i]) for i in range(3))


def dist(a, b):
    return round(sum((a[i] - b[i]) ** 2 for i in range(3)) ** .5)


def ver(rotulo, a, b):
    d = dist(a, b)
    if d < 30:
        v = 'INVISIVEL'
    elif d < LIMITE:
        v = 'FRACO'
    else:
        v = 'visivel'
    print('  %-42s %-9s %3d  %s' % (rotulo, '#%02x%02x%02x' % a, d, v))
    return d


BG = '#faf3e3'
HALO = sobre('#e8d9b5', BG, .55)
HALO35 = sobre('#e8d9b5', BG, .35)

print('=== CENA 0 (o pote do levain) ===')
print('  fundo %s | halo %s' % (BG, '#%02x%02x%02x' % HALO))
ver('pote de vidro sobre o halo', rgb('#fffdf6'), HALO)
ver('levain DENTRO do pote', rgb('#efe0bd'), rgb('#fffdf6'))
ver('levain (novo) DENTRO do pote', rgb('#d9b872'), rgb('#fffdf6'))
ver('bolha branca sobre o levain (novo)', rgb('#ffffff'), rgb('#d9b872'))
ver('mound de farinha sobre o fundo', rgb('#f2e6c9'), rgb(BG))

print('\n=== CENA 2 (os tres circulos) ===')
for rot, c in (('levain', '#efe0bd'), ('levain (novo)', '#d9b872'),
               ('farinha', '#f2e6c9'), ('farinha (nova)', '#fbf7ec'),
               ('agua', '#e6f1fb'), ('agua (nova)', '#6fb0dd')):
    print('  %-20s %s' % (rot, c))
ver('levain x farinha  (COMO ESTA)', rgb('#efe0bd'), rgb('#f2e6c9'))
ver('levain x agua     (COMO ESTA)', rgb('#efe0bd'), rgb('#e6f1fb'))
ver('farinha x agua    (COMO ESTA)', rgb('#f2e6c9'), rgb('#e6f1fb'))
ver('levain x farinha  (novo)', rgb('#d9b872'), rgb('#fbf7ec'))
ver('levain x agua     (novo)', rgb('#d9b872'), rgb('#6fb0dd'))
ver('farinha x agua    (novo)', rgb('#fbf7ec'), rgb('#6fb0dd'))
ver('texto "agua" sobre a agua (nova)', rgb('#1f4e79'), rgb('#6fb0dd'))
ver('contorno da agua sobre a agua (novo)', rgb('#1f5c8a'), rgb('#6fb0dd'))

print('\n=== CENA 4 (a massa e o gluten) ===')
ver('massa sobre o halo (.5)', rgb('#f2e6c9'), HALO)
ver('massa (nova) sobre o halo (.35)', rgb('#d4ad64'), HALO35)
ver('massa (nova) sobre o fundo', rgb('#d4ad64'), rgb(BG))
ver('linha do gluten sobre a massa (nova)', rgb('#7a4d1c'), rgb('#d4ad64'))
ver('bolha branca sobre a massa (nova)', rgb('#ffffff'), rgb('#d4ad64'))
