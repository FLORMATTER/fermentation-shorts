# -*- coding: utf-8 -*-
"""
_inventario.py — o que ja esta em ingles e o que ainda falta traduzir.

Varre a arvore do projeto, ignora as pastas que nao sao video (aulas, guias,
_arquivo morto) e, para cada .html, estima o idioma e conta as strings visiveis
que parecem portugues.

Uso:
    python _inventario.py            # so a tabela
    python _inventario.py --tudo     # inclui aulas/, guias/ e _arquivo/
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = ('.workbuddy-ai', '_revisao', 'node_modules')

# palavras que so aparecem em portugues (nao existem em ingles)
PT = re.compile(r'\b(que|para|com|nao|não|você|voce|água|agua|sal|dias|semanas|'
                r'pote|dentes?|mão|mao|fermenta|prensa|massageia|repolho|cenoura|'
                r'rabanete|beterraba|couve|alho|cebola|pepino|pronta|pronto|'
                r'crocante|bancada|esperar|volta|cor|sua|seu|isso|mais)\b', re.I)
EN = re.compile(r'\b(the|and|with|you|water|salt|days|weeks|jar|cloves?|hand|'
                r'ferment|cabbage|carrot|radish|beet|cauliflower|garlic|onion|'
                r'cucumber|ready|crunchy|counter|wait|back|colour|color|your|'
                r'more|that|this)\b', re.I)


def strings_visiveis(d):
    """Strings que o espectador ve: cap/sub/hint do JS, <text> e texto do HTML."""
    out = []
    for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo'):
        out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
    out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
    corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
    out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
    return [s for s in out if s.strip()]


def main():
    tudo = '--tudo' in sys.argv
    linhas = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [x for x in dirs if x not in IGNORAR]
        rel = os.path.relpath(base, RAIZ).replace('\\', '/')
        pasta = rel.split('/')[0]
        if not tudo and pasta in ('aulas', 'guias', '_arquivo'):
            continue
        for a in sorted(arqs):
            if not a.endswith('.html'):
                continue
            p = os.path.join(base, a)
            d = io.open(p, encoding='utf-8', errors='replace').read()
            st = strings_visiveis(d)
            txt = ' '.join(st)
            npt = len(PT.findall(txt))
            nen = len(EN.findall(txt))
            idioma = 'EN' if nen > npt else 'PT'
            linhas.append((pasta + '/' + a, idioma, npt, nen, len(st)))

    pt = [l for l in linhas if l[1] == 'PT']
    en = [l for l in linhas if l[1] == 'EN']
    print('%-58s %-4s %5s %5s %5s' % ('arquivo', 'idl', 'PT', 'EN', 'str'))
    print('-' * 82)
    for l in sorted(linhas):
        print('%-58s %-4s %5d %5d %5d' % l)
    print('-' * 82)
    print('TOTAL: %d arquivo(s)  |  %d em PT  |  %d em EN' % (len(linhas), len(pt), len(en)))
    print()
    print('FALTAM TRADUZIR (%d):' % len(pt))
    for l in sorted(pt):
        print('  ' + l[0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
