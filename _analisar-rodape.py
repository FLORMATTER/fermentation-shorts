# -*- coding: utf-8 -*-
"""
_analisar-rodape.py — acha tudo que cai na zona coberta pela barra de legenda.

A barra `.ncap` do player-video-longo-7-legumes.html e `position:absolute; bottom:0`
com ~73 px de altura e fundo 86% opaco. Como o stage tem 720 px, ela cobre de
y = 647 ate y = 720. Qualquer coisa desenhada nessa faixa fica escondida.

Este script lista, cena por cena, todo elemento com y >= LIMITE.
Nao altera nada.
"""
import io
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(RAIZ, 'video-longo', 'player-video-longo-7-legumes.html')
LIMITE = 640  # a partir daqui comeca a ficar perigoso

txt = io.open(ARQ, encoding='utf-8').read()

# cada cena e um objeto com body:`...`  — pega o corpo de cada um
cenas = re.findall(r'body:`(.*?)`', txt, re.S)

EL = re.compile(r'<(text|rect|circle|ellipse|line|path)\b[^>]*>')
ATR = re.compile(r'\b(y|y1|y2|cy)\s*=\s*"(-?\d+(?:\.\d+)?)"')

total = 0
for i, corpo in enumerate(cenas):
    achados = []
    for m in EL.finditer(corpo):
        tag = m.group(1)
        if tag == 'path':
            continue  # path e geometria livre, nao da para julgar por atributo
        for a in ATR.finditer(m.group(0)):
            val = float(a.group(2))
            if val >= LIMITE:
                # conteudo textual ajuda a identificar
                t = re.search(r'>([^<>]{2,60})<', m.group(0))
                rotulo = t.group(1) if t else ''
                achados.append((tag, a.group(1), val, rotulo))
    if achados:
        print('--- cena %d  (%d elemento(s) na zona)' % (i, len(achados)))
        for tag, attr, val, rotulo in sorted(achados, key=lambda x: -x[2]):
            print('    <%s %s="%g">  %s' % (tag, attr, val, rotulo[:52]))
        total += len(achados)

print()
print('TOTAL: %d elemento(s) em %d cena(s)' % (total, len(cenas)))
print('Zona coberta pela barra: y = 647 a 720')
