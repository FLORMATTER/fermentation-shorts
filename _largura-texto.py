# -*- coding: utf-8 -*-
"""
_largura-texto.py — triagem de texto que NAO CABE (o erro (h)).

O `_validar-short.py` mede coordenadas; nao mede LARGURA. Em SVG o texto nao
quebra linha nem encolhe: ele vaza para os dois lados quando esta centralizado.
Este script ESTIMA a largura de cada <text> e compara com:
  1. a largura do cartao (viewBox)  -> texto que sai do quadro;
  2. a largura do <rect> irmao dentro do mesmo <g> -> selo estourado.

E so uma TRIAGEM: a estimativa erra para mais ou para menos conforme a fonte.
O que ele aponta precisa ser confirmado no render.

Uso:
    python _largura-texto.py arquivo.html
    python _largura-texto.py pasta/*-en.html
    python _largura-texto.py arquivo.html --todos   # lista tudo, nao so o suspeito
"""
import glob
import io
import os
import re
import sys

# avanco medio por caractere, em "em", medido nos cartoes reais da serie
K_BOLD = 0.62     # font-weight >= 700
K_NORMAL = 0.53

TEXT = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.S)
ATTR = re.compile(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"')
RECT = re.compile(r'<rect\b([^>]*)/?>')
GBLOCO = re.compile(r'<g\b[^>]*>(.*?)</g>', re.S)
TAGS = re.compile(r'<[^>]+>')


def attrs(s):
    return {k: v for k, v in ATTR.findall(s)}


def largura(txt, font, weight):
    limpo = TAGS.sub('', txt).strip()
    k = K_BOLD if weight >= 700 else K_NORMAL
    return len(limpo), len(limpo) * k * font


def analisa(path):
    d = io.open(path, encoding='utf-8', errors='replace').read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', d)
    largura_cartao = float(vb.group(1)) if vb else 405.0

    achados = []
    # ── 1. texto que estoura o cartao ──────────────────────────────────────
    for m in TEXT.finditer(d):
        a = attrs(m.group(1))
        font = float(a.get('font-size', 14))
        weight = int(float(a.get('font-weight', 400)))
        n, w = largura(m.group(2), font, weight)
        if w > largura_cartao * 0.94:
            achados.append(('cartao', n, font, weight, w, largura_cartao,
                            TAGS.sub('', m.group(2)).strip()[:52]))

    # ── 2. texto que estoura o <rect> do mesmo <g> (selo) ─────────────────
    for g in GBLOCO.finditer(d):
        corpo = g.group(1)
        if '<rect' not in corpo or '<text' not in corpo:
            continue
        larguras = [float(attrs(r.group(1)).get('width', 0))
                    for r in RECT.finditer(corpo)]
        larguras = [x for x in larguras if x > 0]
        if not larguras:
            continue
        caixa = max(larguras)
        for m in TEXT.finditer(corpo):
            a = attrs(m.group(1))
            font = float(a.get('font-size', 14))
            weight = int(float(a.get('font-weight', 400)))
            n, w = largura(m.group(2), font, weight)
            if w > caixa * 1.02:
                achados.append(('selo', n, font, weight, w, caixa,
                                TAGS.sub('', m.group(2)).strip()[:52]))
    return largura_cartao, achados


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    alvos = []
    for a in args:
        alvos += glob.glob(a) if any(c in a for c in '*?[') else [a]
    if not alvos:
        print(__doc__)
        return 1

    total = 0
    for p in alvos:
        if not os.path.exists(p):
            print('nao encontrado:', p)
            continue
        cartao, achados = analisa(p)
        nome = os.path.relpath(p).replace('\\', '/')
        if not achados:
            print('%-52s ok (cartao %g)' % (nome, cartao))
            continue
        print('%-52s %d suspeito(s)' % (nome, len(achados)))
        for tipo, n, font, weight, w, caixa, txt in achados:
            total += 1
            print('   [%s] %3d car · %.0fpx → %.0fpx (caixa %.0f) | %s'
                  % (tipo, n, font, w, caixa, txt))
    print('-' * 70)
    print('TOTAL: %d suspeito(s). CONFIRMAR NO RENDER — isto e so estimativa.' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
