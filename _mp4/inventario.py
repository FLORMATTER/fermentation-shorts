"""_mp4/inventario.py — o que ja tem .mp4, o que falta e quanto custa renderizar.

    python _mp4/inventario.py

Usa exatamente o MESMO filtro do `--todos` do _gerar-mp4.js (arquivo .html que
contem `<svg class="scene`), para a lista bater com o que o piloto pegaria.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PULAR = {'.git', 'node_modules', '_revisao', '__pycache__'}

# custo medido em 18/09 nesta maquina (segundos de render por segundo de video)
CUSTO = {'1080': 4.9, '720': 1.6}


def duracao(html):
    return sum(int(m) for m in re.findall(r'\bms\s*:\s*(\d+)', html)) / 1000.0


def main():
    linhas = []
    for pasta, subs, arqs in os.walk(RAIZ):
        subs[:] = [s for s in subs if s not in PULAR and not s.startswith('.')]
        for f in arqs:
            if not f.lower().endswith('.html'):
                continue
            p = os.path.join(pasta, f)
            try:
                html = open(p, encoding='utf-8', errors='replace').read()
            except Exception:
                continue
            if '<svg class="scene' not in html:
                continue
            rel = os.path.relpath(p, RAIZ).replace('\\', '/')
            linhas.append((rel, duracao(html), os.path.exists(re.sub(r'\.html?$', '.mp4', p))))

    linhas.sort()
    tem = [x for x in linhas if x[2]]
    falta = [x for x in linhas if not x[2]]

    print('%-58s %8s  %s' % ('arquivo', 'duracao', 'mp4'))
    for rel, d, ok in linhas:
        print('%-58s %7.1fs  %s' % (rel, d, 'sim' if ok else '--'))
    print()
    print('total: %d arquivo(s) | com mp4: %d | sem mp4: %d' % (len(linhas), len(tem), len(falta)))
    soma = sum(d for _, d, _ in falta)
    print('duracao dos que faltam: %.0f s (%.1f min de video)' % (soma, soma / 60))
    for w, c in CUSTO.items():
        print('  renderizar todos em %sp: ~%.0f min' % (w, soma * c / 60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
