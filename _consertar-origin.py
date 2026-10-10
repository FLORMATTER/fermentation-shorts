# -*- coding: utf-8 -*-
"""
Conserta o bug (g): `transform-origin` com PALAVRA-CHAVE em SVG.

Em SVG, palavra-chave e `%` resolvem contra o viewBox (405x720), nao contra o
elemento -> o pivo cai longe do desenho e a peca (faca, mao, ponteiro) varre a tela.
Em 49 dos 50 padroes do projeto o elemento JA esta dentro de um
<g transform="translate(...)">, ou seja o pivo certo e o PADRAO (0 0) = a ancora do
grupo. Entao o conserto e simplesmente REMOVER a declaracao.

Mantem: `0 0`, valores em px e `transform-box:fill-box`.

Uso:
    python _consertar-origin.py            # dry-run: mostra o que faria
    python _consertar-origin.py --apply    # grava
"""
import io
import os
import re
import sys
import glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
APLICAR = '--apply' in sys.argv

STYLE = re.compile(r'style="([^"]*)"')
PERIGO = re.compile(r'^(?:center|left|right|top|bottom|[\d.]+%)(?:\s+(?:center|left|right|'
                    r'top|bottom|[\d.]+%))*$', re.I)
SEGURO = re.compile(r'^(?:0(?:px)?\s+0(?:px)?|\d+(?:\.\d+)?px\s+\d+(?:\.\d+)?px)$')


def limpa(st):
    """Remove as declaracoes transform-origin perigosas de um style."""
    if 'transform-origin' not in st:
        return st, 0
    if 'fill-box' in st:
        return st, 0
    mantidas, removidas = [], 0
    for parte in st.split(';'):
        if parte.strip().lower().startswith('transform-origin'):
            val = parte.split(':', 1)[1].strip() if ':' in parte else ''
            if SEGURO.match(val):
                mantidas.append(parte)
                continue
            if PERIGO.match(val):
                removidas += 1
                continue
        mantidas.append(parte)
    if not removidas:
        return st, 0
    return ';'.join(mantidas), removidas


total_arq = 0
total_oc = 0
for f in sorted(glob.glob(os.path.join(RAIZ, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    if rel.startswith('.workbuddy-ai/'):
        continue
    d = io.open(f, encoding='utf-8', newline='').read()
    n = [0]

    def sub(m):
        novo, q = limpa(m.group(1))
        n[0] += q
        return 'style="%s"' % novo

    d2 = STYLE.sub(sub, d)
    if not n[0]:
        continue
    total_arq += 1
    total_oc += n[0]
    print('%-52s %2d declaracao(oes) removida(s)' % (rel, n[0]))
    if APLICAR:
        io.open(f, 'w', encoding='utf-8', newline='').write(d2)

print('-' * 70)
print('TOTAL: %d declaracao(oes) em %d arquivo(s)  [%s]'
      % (total_oc, total_arq, 'GRAVADO' if APLICAR else 'DRY-RUN'))
if not APLICAR:
    print('rodar de novo com --apply para gravar')
