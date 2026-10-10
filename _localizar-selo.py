# -*- coding: utf-8 -*-
"""_localizar-selo.py — em QUE cena esta cada selo suspeito.

Ler 30 PNGs na mao e caro. Este script diz a cena (e portanto qual folha do
_revisar-cenas.py olhar) de cada texto suspeito, em ordem.

Uso:
    python _localizar-selo.py arquivo-en.html
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
from importlib.machinery import SourceFileLoader

lt = SourceFileLoader('lt', os.path.join(RAIZ, '_largura-texto.py')).load_module()


def cenas(d):
    """(indice, corpo) de cada <svg class="scene">."""
    out = []
    for m in re.finditer(r'<svg class="scene"[^>]*>(.*?)</svg>', d, re.S):
        out.append(m.group(1))
    return out


def main():
    p = sys.argv[1]
    d = io.open(p, encoding='utf-8', errors='replace').read()
    corpo_cenas = cenas(d)
    print('%s — %d cena(s)\n' % (os.path.relpath(p).replace('\\', '/'), len(corpo_cenas)))
    for i, c in enumerate(corpo_cenas):
        achados = []
        for g in lt.GBLOCO.finditer(c):
            b = g.group(1)
            if '<rect' not in b or '<text' not in b:
                continue
            ws = [float(lt.attrs(r.group(1)).get('width', 0))
                  for r in lt.RECT.finditer(b)]
            ws = [x for x in ws if x > 0]
            if not ws:
                continue
            caixa = max(ws)
            for m in lt.TEXT.finditer(b):
                a = lt.attrs(m.group(1))
                f = float(a.get('font-size', 14))
                w = int(float(a.get('font-weight', 400)))
                n, larg = lt.largura(m.group(2), f, w)
                if larg > caixa:
                    achados.append((larg / caixa, n, f, larg, caixa,
                                    lt.TAGS.sub('', m.group(2)).strip()))
        if achados:
            folha = i // 3 + 1
            print('cena %d  -> folha %d' % (i, folha))
            for r, n, f, larg, caixa, txt in achados:
                print('    x%.2f  %2d car · %.0fpx → %.0fpx (caixa %.0f) | %s'
                      % (r, n, f, larg, caixa, txt))


if __name__ == '__main__':
    main()
