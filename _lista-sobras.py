# -*- coding: utf-8 -*-
"""_lista-sobras.py — lista unica e deduplicada do que falta traduzir.

Mesma comparacao do _sobras-vs-original.py, mas agrupando as frases iguais que
aparecem em varios arquivos, para virar UMA tabela de traducao (o dicionario).
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
from importlib.machinery import SourceFileLoader

mod = SourceFileLoader('sob', os.path.join(RAIZ, '_sobras-vs-original.py')).load_module()

# strings que sao iguais nos dois idiomas de proposito -> nao sao sobra
NEUTRO = re.compile(r'^(pH|kg|g|ml|L|Pizza|Tacos|Sushi|OBS|Canva|CapCut|YouTube|'
                    r'\d+\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
                    r'\$\{[^}]*\}|[^A-Za-zÀ-ÿ]*)$')


def main():
    sobras = {}
    for en, pt in mod.pares():
        if not pt:
            continue
        rel = os.path.relpath(en, RAIZ).replace('\\', '/')
        s_en = mod.visiveis(io.open(en, encoding='utf-8', errors='replace').read())
        s_pt = mod.visiveis(io.open(pt, encoding='utf-8', errors='replace').read())
        for x in s_en & s_pt:
            if mod.tem_letras(x) and not NEUTRO.match(x):
                sobras.setdefault(x, set()).add(rel)

    print('FRASES A TRADUZIR: %d\n' % len(sobras))
    for s, arqs in sorted(sobras.items(), key=lambda x: (-len(x[1]), x[0])):
        print('[%dx] %s' % (len(arqs), s))

    print('\n' + '=' * 74)
    print('neutras (iguais nos dois idiomas, ignoradas):')
    for en, pt in mod.pares():
        if not pt:
            continue
        s_en = mod.visiveis(io.open(en, encoding='utf-8', errors='replace').read())
        s_pt = mod.visiveis(io.open(pt, encoding='utf-8', errors='replace').read())
        for x in sorted(s_en & s_pt):
            if mod.tem_letras(x) and NEUTRO.match(x):
                print('   %s' % x)


if __name__ == '__main__':
    main()
